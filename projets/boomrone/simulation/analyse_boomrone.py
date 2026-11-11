"""Lecture des résultats ngspice / LTspice, mesures et courbes (appelé par sim_boomrone.py plot)."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from spicelib import RawRead

import sim_boomrone as S

RES, FIG = S.RES, S.FIG
FPWM = S.P["f_pwm"]
PER = 1.0 / FPWM
C_NG, C_LT, C_AN = "#1f77b4", "#d62728", "#2ca02c"
plt.rcParams.update({
    "font.size": 10, "axes.grid": True, "grid.alpha": 0.25, "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 130, "axes.titlesize": 11, "axes.titleweight": "bold", "legend.frameon": False,
})

TRAN_VECS = ["v(vbm)", "i(vbat)", "i(lm1)", "i(lm2)", "i(lm3)", "i(lm4)", "v(d1)", "v(vbl)", "v(v3)", "v(v2)"]


# ------------------------------------------------------------------ lecture
def read_tran(case, load, tool, suffix=""):
    out = f"{case}_{load}{suffix}_{tool}"
    names = ["v(vbm)", "i(vbat)", "i(lm1)", "i(lm2)", "i(lm3)", "i(lm4)", "v(d1)"]
    if case in ("cas2", "cas3"):
        names += ["v(vbl)", "v(v3)"]
    if case == "cas3":
        names += ["v(v2)"]
    d = {}
    if tool == "ngspice":
        a = np.loadtxt(RES / f"{out}.txt")
        d["t"] = a[:, 0]
        for k, n in enumerate(names):
            d[n] = a[:, 1 + 2 * k]
    else:
        r = RawRead(str(RES / f"{out}.raw"))
        d["t"] = np.abs(r.get_trace("time").get_wave(0))
        for n in names:
            nm = n.upper().replace("V(", "V(").replace("I(", "I(")
            nm = {"v(vbm)": "V(vbm)", "i(vbat)": "I(Vbat)", "v(d1)": "V(d1)", "v(vbl)": "V(vbl)", "v(v3)": "V(v3)", "v(v2)": "V(v2)"}.get(n, None) or ("I(Lm%s)" % n[-2])
            d[n] = r.get_trace(nm).get_wave(0)
    d["i(vbat)"] = -d["i(vbat)"]
    d["i_mot"] = -(d["i(lm1)"] + d["i(lm2)"] + d["i(lm3)"] + d["i(lm4)"]) * (-1) if False else (d["i(lm1)"] + d["i(lm2)"] + d["i(lm3)"] + d["i(lm4)"])
    return d


def uniform(d, name, t0, t1, dt=20e-9):
    tt = np.arange(t0, t1, dt)
    return tt, np.interp(tt, d["t"], d[name])


def pp(d, name, t0, t1):
    m = (d["t"] >= t0) & (d["t"] <= t1)
    return d[name][m].max() - d[name][m].min()


def smooth_min(d, name, t0, t1, w=0.5e-6):
    """min / max après une moyenne glissante de 0,5 µs : ignore les pointes de commutation de quelques ns
    (sans inductance de câblage dans le modèle, leur hauteur n'est pas crédible)."""
    tt, y = uniform(d, name, t0, t1, dt=10e-9)
    n = int(w / 10e-9)
    ys = np.convolve(y, np.ones(n) / n, mode="valid")
    return ys.min(), ys.max()


def fund(d, name, t0, n_per=20):
    """Amplitude (crête) de la composante a f_pwm sur n_per périodes entières."""
    tt, y = uniform(d, name, t0, t0 + n_per * PER)
    y = y - y.mean()
    w = np.exp(-2j * np.pi * FPWM * tt)
    return 2 * abs((y * w).mean())


def read_ac(kind_out, tool, loop=False):
    out = f"{kind_out}_{tool}"
    if tool == "ngspice":
        a = np.loadtxt(RES / f"{out}.txt")
        f = a[:, 0]
        x1 = a[:, 1] + 1j * a[:, 2]
        x2 = a[:, 4] + 1j * a[:, 5]
    else:
        r = RawRead(str(RES / f"{out}.raw"))
        f = np.real(r.get_trace("frequency").get_wave(0))
        if loop:
            x1 = r.get_trace("V(fbd)").get_wave(0)
            x2 = r.get_trace("V(fbn)").get_wave(0)
        else:
            x1 = r.get_trace("V(vo)").get_wave(0)
            x2 = r.get_trace("V(vin)").get_wave(0)
    return f, x1, x2


def ac_name(kind, esr, cout, loop):
    return f"ac_{kind}_{'loop_' if loop else ''}{esr:g}_{cout:.3g}".replace("e-", "m").replace("+", "")


def psrr(kind, esr, cout, tool):
    f, vo, vi = read_ac(ac_name(kind, esr, cout, False), tool)
    return f, vo / vi


def loopgain(kind, esr, cout, tool):
    f, fbd, fbn = read_ac(ac_name(kind, esr, cout, True), tool, loop=True)
    return f, -fbd / fbn


def margins(f, T):
    mag = np.abs(T)
    ph = np.degrees(np.unwrap(np.angle(T)))
    idx = np.where((mag[:-1] >= 1) & (mag[1:] < 1))[0]
    if len(idx) == 0:
        return None, None, None
    i = idx[0]
    # interpolation log
    a = (0 - 20 * np.log10(mag[i])) / (20 * np.log10(mag[i + 1]) - 20 * np.log10(mag[i]))
    fu = f[i] * (f[i + 1] / f[i]) ** a
    phu = ph[i] + a * (ph[i + 1] - ph[i])
    pm = 180 + phu
    pm = (pm + 180) % 360 - 180
    # marge de gain : phase = -180 -> |T|
    gm = None
    j = np.where((ph[:-1] > -180) & (ph[1:] <= -180))[0]
    if len(j):
        gm = -20 * np.log10(mag[j[0]])
    return fu, pm, gm


def psrr_analytic(kind, f, esr, cout):
    """Même petit signal, calculé a la main (numpy) : contrôle indépendant des deux simulateurs."""
    p = S.P
    if kind.startswith("mcp"):
        h = 10 ** (-p["mcp_psrr_db"] / 20)
        rl = 3.0 / p["i_logic"] if kind == "mcp" else 24.0
        rl_ref = p["mcp_psrr_vr"] / p["mcp_psrr_il"]
    else:
        h = p["xc_line"]
        rl = 2.0 / p["i_flow"]
        rl_ref = 2.0 / p["i_flow"]
    gm = p["k_fb"] * p["a0"] * p["gmp"]
    inv_ro = h * (gm + 1 / rl_ref) / (1 - h)
    s = 2j * np.pi * f
    Ap = 1 / ((1 + s / (2 * np.pi * p["fp"])) * (1 + s / (2 * np.pi * p["fg"])))
    Yc = s * cout / (1 + s * esr * cout)
    return inv_ro / (inv_ro + 1 / rl + Yc + gm * Ap)


def db(x):
    return 20 * np.log10(np.abs(x))


# ------------------------------------------------------------------ figures
def fig_cas1(m):
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.2))
    t0 = 1.0e-3 + 6 * PER
    win = (t0, t0 + 3 * PER)
    cols = {"vol": "#1b7837", "crete": "#c51b7d", "pess": "#e08214"}
    lab = {"vol": "5,5 A, 55 mΩ", "crete": "9,5 A, 55 mΩ", "pess": "7,5 A, 110 mΩ"}
    for load in ("vol", "crete", "pess"):
        for tool, ls in (("ngspice", "-"), ("LTspice", "--")):
            d = read_tran("cas1", load, tool)
            msk = (d["t"] >= win[0]) & (d["t"] <= win[1])
            ax[0, 0].plot((d["t"][msk] - win[0]) * 1e6, d["v(vbm)"][msk], ls, color=cols[load], lw=1.3,
                          label=f"{lab[load]} — {tool}" if tool == "ngspice" else None)
            ax[0, 1].plot((d["t"][msk] - win[0]) * 1e6, d["i(vbat)"][msk], ls, color=cols[load], lw=1.3)
    ax[0, 0].plot([], [], "k-", label="trait plein : ngspice"); ax[0, 0].plot([], [], "k--", label="tirets : LTspice")
    ax[0, 0].axhline(3.3, color="gray", ls=":", lw=1); ax[0, 0].text(0.5, 3.31, "seuil de coupure actuel 3,3 V", color="gray", fontsize=8)
    ax[0, 0].set(title="Tension de la ligne moteurs VBATM (3 périodes PWM)", xlabel="temps (µs)", ylabel="V")
    ax[0, 0].legend(loc="lower right", fontsize=8)
    ax[0, 1].set(title="Courant tiré de la batterie", xlabel="temps (µs)", ylabel="A")
    # démarrage
    for tool, ls, c in (("ngspice", "-", C_NG), ("LTspice", "--", C_LT)):
        d = read_tran("cas1", "demarrage", tool)
        tt, v = uniform(d, "v(vbm)", 0, S.T_END["demarrage"], dt=PER / 4)
        n = int(len(tt) // 4)
        vmin = v[: n * 4].reshape(n, 4).min(axis=1)
        vmax = v[: n * 4].reshape(n, 4).max(axis=1)
        tc = tt[: n * 4].reshape(n, 4).mean(axis=1) * 1e3
        ax[1, 0].plot(tc, vmin, ls, color=c, lw=1.4, label=f"min par période — {tool}")
        ax[1, 0].plot(tc, vmax, ls, color=c, lw=0.8, alpha=0.6)
        tt, ib = uniform(d, "i(vbat)", 0, S.T_END["demarrage"], dt=PER / 4)
        ibm = ib[: n * 4].reshape(n, 4).mean(axis=1)
        ax[1, 1].plot(tc, ibm, ls, color=c, lw=1.4, label=tool)
    ax[1, 0].axhline(3.3, color="gray", ls=":", lw=1)
    ax[1, 0].set(title="Démarrage des moteurs : enveloppe de VBATM", xlabel="temps (ms)", ylabel="V")
    ax[1, 0].legend(fontsize=8)
    ax[1, 1].set(title="Démarrage : courant batterie moyenné par période", xlabel="temps (ms)", ylabel="A")
    ax[1, 1].legend(fontsize=8)
    fig.suptitle("Cas 1 — batterie, résistance interne et 4 moteurs en PWM à 24 kHz (HYP : moteur 1 Ω / 25 µH, voir rapport)", fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG / "fig1_batterie_moteurs.png")
    plt.close(fig)


def fig_phase(m):
    fig, ax = plt.subplots(1, 2, figsize=(13, 4))
    t0 = 1.0e-3 + 6 * PER
    for load, c, name in (("vol", "#1b7837", "PWM en phase"), ("vol_dec", "#762a83", "PWM décalées de 90°")):
        d = read_tran("cas1", load, "ngspice")
        msk = (d["t"] >= t0) & (d["t"] <= t0 + 3 * PER)
        ax[0].plot((d["t"][msk] - t0) * 1e6, d["v(vbm)"][msk], color=c, label=name)
        ax[1].plot((d["t"][msk] - t0) * 1e6, d["i(vbat)"][msk], color=c, label=name)
    ax[0].set(title="VBATM en stationnaire : PWM en phase ou décalées (ngspice)", xlabel="temps (µs)", ylabel="V"); ax[0].legend()
    ax[1].set(title="Courant batterie", xlabel="temps (µs)", ylabel="A")
    fig.tight_layout(); fig.savefig(FIG / "fig1b_phase_pwm.png"); plt.close(fig)


def fig_psrr(m):
    p = S.P
    f = np.logspace(1, 7, 400)
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
    # MCP1700
    cfg = [("mcp_test", 0.02, 1e-6, "fiche : 1 µF, 24 Ω", "#7f7f7f"), ("mcp", 0.02, p["c_out_3v0"], "carte : 4,7 µF, 23 Ω (130 mA)", C_NG),
           ("mcp", 0.02, 1e-6, "carte, COUT = 1 µF", "#ff7f0e")]
    for kind, esr, c, lab, col in cfg:
        fa, ha = psrr(kind, esr, c, "ngspice")
        fb, hb = psrr(kind, esr, c, "LTspice")
        ax[0].semilogx(fa, db(ha), color=col, lw=2, label=f"{lab} — ngspice")
        ax[0].semilogx(fb, db(hb), "--", color="k", lw=0.9)
        ax[0].semilogx(f, db(psrr_analytic(kind, f, esr, c)), ":", color=C_AN, lw=1.2)
    ax[0].plot([], [], "k--", lw=0.9, label="LTspice (superposé)"); ax[0].plot([], [], ":", color=C_AN, label="calcul numpy")
    ax[0].plot([100], [-44], "k*", ms=11, label="fiche : −44 dB à 100 Hz"); ax[0].axvline(FPWM, color="gray", ls=":", lw=1)
    ax[0].text(FPWM * 1.1, -15, "24 kHz\n(PWM)", color="gray", fontsize=8)
    ax[0].set(title="MCP1700 (3,0 V) — rejet d'ondulation VBATL → +3V0", xlabel="fréquence (Hz)", ylabel="dB", ylim=(-70, -10), xlim=(10, 1e7))
    ax[0].legend(fontsize=7.5, loc="lower left")
    # XC6206
    fa, ha = psrr("xc", 0.02, p["c_out_2v0"], "ngspice"); fb, hb = psrr("xc", 0.02, p["c_out_2v0"], "LTspice")
    ax[1].semilogx(fa, db(ha), color=C_NG, lw=2, label="carte : 2,2 µF, 222 Ω — ngspice")
    ax[1].semilogx(fb, db(hb), "--", color="k", lw=0.9, label="LTspice (superposé)")
    ax[1].semilogx(f, db(psrr_analytic("xc", f, 0.02, p["c_out_2v0"])), ":", color=C_AN, label="calcul numpy")
    ax[1].plot([10], [db(p["xc_line"])], "k*", ms=11, label="fiche : 0,05 %/V (continu)")
    ax[1].axvline(FPWM, color="gray", ls=":", lw=1)
    ax[1].set(title="XC6206 (2,0 V) — rejet d'ondulation +3V0 → +2V0", xlabel="fréquence (Hz)", ylabel="dB", ylim=(-90, -10), xlim=(10, 1e7))
    ax[1].legend(fontsize=7.5, loc="lower left")
    fig.tight_layout(); fig.savefig(FIG / "fig2_psrr.png"); plt.close(fig)


def fig_stab(m):
    fig, ax = plt.subplots(2, 2, figsize=(13, 8))
    cols = {0.005: "#08519c", 0.1: "#3182bd", 0.5: "#6baed6", 1.0: "#fd8d3c", 2.0: "#d94801"}
    rows = {}
    for kind, col, ctitle, cout, esrs in (("mcp", 0, "MCP1700 (4,7 µF)", S.P["c_out_3v0"], (0.005, 0.1, 0.5, 1.0, 2.0)),
                                          ("xc", 1, "XC6206 (2,2 µF)", S.P["c_out_2v0"], (0.005, 2.0))):
        for esr in esrs:
            for tool, ls in (("ngspice", "-"), ("LTspice", "--")):
                f, T = loopgain(kind, esr, cout, tool)
                ax[0, col].semilogx(f, db(T), ls, color=cols[esr], lw=1.6 if tool == "ngspice" else 0.9,
                                    label=f"ESR {esr*1e3:g} mΩ" if tool == "ngspice" else None)
                ax[1, col].semilogx(f, np.degrees(np.unwrap(np.angle(T))), ls, color=cols[esr], lw=1.6 if tool == "ngspice" else 0.9)
                if tool == "ngspice":
                    fu, pm, gm = margins(f, T)
                    rows[f"{kind}_{esr:g}"] = dict(fu=fu, pm=pm, gm=gm)
        ax[0, col].axhline(0, color="k", lw=0.8)
        ax[0, col].set(title=f"Gain de boucle — {ctitle}", ylabel="dB", xlim=(10, 1e7))
        ax[1, col].axhline(-180, color="k", lw=0.8)
        ax[1, col].set(xlabel="fréquence (Hz)", ylabel="phase (°)", xlim=(10, 1e7))
        ax[0, col].legend(fontsize=8)
    fig.suptitle("Stabilité des LDO (modèle de boucle HYP) — trait plein : ngspice, tirets : LTspice", fontweight="bold")
    fig.tight_layout(); fig.savefig(FIG / "fig3_stabilite.png"); plt.close(fig)
    m["stab"] = rows


def fig_chain(m):
    t0 = 1.0e-3 + 6 * PER
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.2))
    for tool, ls, c in (("ngspice", "-", C_NG), ("LTspice", "--", C_LT)):
        d = read_tran("cas2", "vol", tool)
        d3 = read_tran("cas3", "vol", tool)
        tt, vbm = uniform(d, "v(vbm)", t0, t0 + 3 * PER)
        _, vbl = uniform(d, "v(vbl)", t0, t0 + 3 * PER)
        _, v3 = uniform(d, "v(v3)", t0, t0 + 3 * PER)
        _, v2 = uniform(d3, "v(v2)", t0, t0 + 3 * PER)
        x = (tt - t0) * 1e6
        ax[0, 0].plot(x, vbm, ls, color=c, label=f"VBATM — {tool}")
        ax[0, 0].plot(x, vbl, ls, color=c, lw=0.9, alpha=0.7)
        ax[0, 1].plot(x, (v3 - v3.mean()) * 1e3, ls, color=c, label=f"+3V0 — {tool}")
        ax[0, 1].plot(x, (v2 - v2.mean()) * 1e3 * 10, ls, color=c, lw=0.9, alpha=0.6)
        # démarrage
        dd = read_tran("cas2", "demarrage", tool)
        tt, vb = uniform(dd, "v(vbm)", 0, S.T_END["demarrage"], dt=PER / 40)
        nb = len(tt) // 40
        vbr = vb[: nb * 40].reshape(nb, 40)
        if tool == "ngspice":
            ax[1, 0].fill_between(tt[: nb * 40].reshape(nb, 40).mean(axis=1) * 1e3, vbr.min(axis=1), vbr.max(axis=1), color="#bbbbbb", alpha=0.6, label="VBATM (min–max par période)")
        tt, v = uniform(dd, "v(vbl)", 0, S.T_END["demarrage"], dt=PER / 4)
        n = len(tt) // 4
        ax[1, 0].plot(tt[: n * 4].reshape(n, 4).mean(axis=1) * 1e3, v[: n * 4].reshape(n, 4).min(axis=1), ls, color="k", lw=1.2, alpha=0.8, label="VBATL (min par période)" if tool == "ngspice" else None)
        tt, v3 = uniform(dd, "v(v3)", 0, S.T_END["demarrage"], dt=PER / 4)
        ax[1, 0].plot(tt * 1e3, v3, ls, color="#1b7837", lw=1.6, label="+3V0" if tool == "ngspice" else None)
        # impulsion du capteur
        msk = (d3["t"] >= 0.55e-3) & (d3["t"] <= 0.9e-3)
        ax[1, 1].plot((d3["t"][msk] - 0.6e-3) * 1e6, d3["v(v2)"][msk], ls, color=c, label=f"+2V0 — {tool}")
    ax[0, 0].axhline(3.3, color="gray", ls=":", lw=1)
    ax[0, 0].set(title="Stationnaire : VBATM (fort) et VBATL après ferrite (faible)", xlabel="temps (µs)", ylabel="V")
    ax[0, 0].legend(fontsize=8, loc="center right")
    ax[0, 1].set(title="Ondulation de +3V0 (mV, fort) et de +2V0 (mV × 10, faible)", xlabel="temps (µs)", ylabel="mV")
    ax[0, 1].legend(fontsize=8)
    ax[1, 0].axhline(3.0, color="gray", ls=":", lw=1); ax[1, 0].axhline(2.91, color="#d94801", ls=":", lw=1)
    ax[1, 0].text(0.05, 2.86, "limite 2,91 V pour +3V0 (DES-009)", color="#d94801", fontsize=8)
    ax[1, 0].set(title="Démarrage des moteurs : VBATM, VBATL et +3V0", xlabel="temps (ms)", ylabel="V", ylim=(2.5, 3.8))
    ax[1, 0].legend(fontsize=8, loc="center right")
    ax[1, 1].set(title="Impulsion de 70 mA du capteur de flux (100 µs) : +2V0", xlabel="temps (µs)", ylabel="V")
    ax[1, 1].legend(fontsize=8)
    fig.suptitle("Cas 2 et 3 — la chaîne complète : batterie → moteurs → ferrite → LDO 3,0 V → LDO 2,0 V", fontweight="bold")
    fig.tight_layout(); fig.savefig(FIG / "fig4_chaine_alimentation.png"); plt.close(fig)


def fig_tools(m):
    timing = json.loads((RES / "timing.json").read_text())
    names = [k for k in timing if k.endswith("_ngspice") and (k.startswith("cas"))]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    x = np.arange(len(names))
    ng = [timing[n]["s"] for n in names]
    lt = [timing[n.replace("_ngspice", "_LTspice")]["s"] for n in names]
    ax[0].bar(x - 0.2, ng, 0.4, color=C_NG, label="ngspice 47"); ax[0].bar(x + 0.2, lt, 0.4, color=C_LT, label="LTspice 26.1")
    ax[0].set_xticks(x); ax[0].set_xticklabels([n.replace("_ngspice", "") for n in names], rotation=40, ha="right", fontsize=8)
    ax[0].set(title="Temps de calcul (s) — simulation temporelle", ylabel="s"); ax[0].legend()
    # écart entre les deux outils sur l'ondulation de VBATM : brut (pointes comprises) et lissé 0,5 µs
    keys = [("cas1", l) for l in ("vol", "vol_dec", "crete", "pess")]
    t0 = 1.0e-3 + 5 * PER
    raw = {"ngspice": [], "LTspice": []}; lis = {"ngspice": [], "LTspice": []}
    for tool in ("ngspice", "LTspice"):
        for c, l in keys:
            d = read_tran(c, l, tool)
            raw[tool].append(pp(d, "v(vbm)", t0, 1.5e-3))
            lo, hi = smooth_min(d, "v(vbm)", t0, 1.5e-3)
            lis[tool].append(hi - lo)
    xx = np.arange(len(keys))
    ax[1].bar(xx - 0.2, raw["ngspice"], 0.4, color=C_NG, label="ngspice"); ax[1].bar(xx + 0.2, raw["LTspice"], 0.4, color=C_LT, label="LTspice")
    ax[1].set_xticks(xx); ax[1].set_xticklabels([l for _, l in keys])
    ax[1].set(title="Ondulation de VBATM, brute (pointes de commutation comprises)", ylabel="V crête-à-crête"); ax[1].legend()
    ax[2].bar(xx - 0.2, lis["ngspice"], 0.4, color=C_NG, label="ngspice"); ax[2].bar(xx + 0.2, lis["LTspice"], 0.4, color=C_LT, label="LTspice")
    ax[2].set_xticks(xx); ax[2].set_xticklabels([l for _, l in keys])
    ax[2].set(title="Ondulation de VBATM, lissée sur 0,5 µs", ylabel="V crête-à-crête"); ax[2].legend()
    fig.tight_layout(); fig.savefig(FIG / "fig5_comparaison_outils.png"); plt.close(fig)


# ------------------------------------------------------------------ mesures
def metrics():
    m = {}
    t0 = 1.0e-3 + 5 * PER
    t1 = 1.5e-3
    for tool in ("ngspice", "LTspice"):
        for load in ("vol", "vol_dec", "crete", "pess"):
            d = read_tran("cas1", load, tool)
            msk = (d["t"] >= t0) & (d["t"] <= t1)
            m[f"cas1/{load}/{tool}"] = dict(
                vbm_moy=float(d["v(vbm)"][msk].mean()), vbm_min=float(d["v(vbm)"][msk].min()), vbm_max=float(d["v(vbm)"][msk].max()),
                vbm_pp=float(pp(d, "v(vbm)", t0, t1)), ibat_moy=float(d["i(vbat)"][msk].mean()), ibat_pp=float(pp(d, "i(vbat)", t0, t1)),
                imot_pp=float(pp(d, "i(lm1)", t0, t1)), vbm_h1=float(fund(d, "v(vbm)", 1.0e-3 + 5 * PER)),
            )
            lo, hi = smooth_min(d, "v(vbm)", t0, t1)
            m[f"cas1/{load}/{tool}"].update(vbm_min_lisse=float(lo), vbm_max_lisse=float(hi), vbm_pp_lisse=float(hi - lo))
        d = read_tran("cas1", "demarrage", tool)
        lo, _ = smooth_min(d, "v(vbm)", 0.2e-3, S.T_END["demarrage"])
        m[f"cas1/demarrage/{tool}"] = dict(vbm_min_lisse=float(lo), vbm_min=float(d["v(vbm)"][d["t"] > 0.2e-3].min()), ibat_max=float(d["i(vbat)"][d["t"] > 0.2e-3].max()),
                                           ibat_fin=float(d["i(vbat)"][d["t"] > 3.0e-3].mean()))
        for load in ("vol", "crete", "pess"):
            d = read_tran("cas2", load, tool)
            msk = (d["t"] >= t0) & (d["t"] <= t1)
            m[f"cas2/{load}/{tool}"] = dict(
                vbl_pp=float(pp(d, "v(vbl)", t0, t1)), v3_moy=float(d["v(v3)"][msk].mean()), v3_pp=float(pp(d, "v(v3)", t0, t1)),
                v3_h1=float(fund(d, "v(v3)", 1.0e-3 + 5 * PER)), vbm_h1=float(fund(d, "v(vbm)", 1.0e-3 + 5 * PER)),
                vbl_h1=float(fund(d, "v(vbl)", 1.0e-3 + 5 * PER)), v3_min=float(d["v(v3)"][msk].min()), vbl_min=float(d["v(vbl)"][msk].min()))
        d = read_tran("cas2", "demarrage", tool)
        msk = d["t"] > 0.2e-3
        m[f"cas2/demarrage/{tool}"] = dict(vbm_min=float(d["v(vbm)"][msk].min()), vbl_min=float(d["v(vbl)"][msk].min()), v3_min=float(d["v(v3)"][msk].min()),
                                           v3_moy_fin=float(d["v(v3)"][d["t"] > 3.0e-3].mean()))
        d = read_tran("cas3", "vol", tool)
        msk = (d["t"] >= t0) & (d["t"] <= 0.58e-3 + 1e-3)
        mm = (d["t"] >= 1.0e-3) & (d["t"] <= 1.5e-3)
        pk = (d["t"] >= 0.55e-3) & (d["t"] <= 0.9e-3)
        m[f"cas3/vol/{tool}"] = dict(v2_moy=float(d["v(v2)"][mm].mean()), v2_pp=float(pp(d, "v(v2)", 1.0e-3 + 5 * PER, 1.5e-3)),
                                     v2_h1=float(fund(d, "v(v2)", 1.0e-3 + 5 * PER)), v3_h1=float(fund(d, "v(v3)", 1.0e-3 + 5 * PER)),
                                     v2_min_pk=float(d["v(v2)"][pk].min()), v2_pre_pk=float(d["v(v2)"][(d["t"] > 0.5e-3) & (d["t"] < 0.6e-3)].mean()))
    # vérifications : pas fin et dropout maximal
    for tool in ("ngspice", "LTspice"):
        for load in ("vol", "crete"):
            d = read_tran("cas1", load, tool, "_fin")
            lo, hi = smooth_min(d, "v(vbm)", t0, t1)
            m[f"fin/{load}/{tool}"] = dict(vbm_min=float(d["v(vbm)"][(d["t"] >= t0) & (d["t"] <= t1)].min()), vbm_pp=float(pp(d, "v(vbm)", t0, t1)),
                                           vbm_min_lisse=float(lo), vbm_pp_lisse=float(hi - lo))
        for load in ("crete", "demarrage"):
            d = read_tran("cas2", load, tool, "_dromax")
            msk = d["t"] > 0.2e-3
            m[f"dromax/{load}/{tool}"] = dict(vbl_min=float(d["v(vbl)"][msk].min()), v3_min=float(d["v(v3)"][msk].min()),
                                              v3_moy_fin=float(d["v(v3)"][d["t"] > 1.0e-3].mean()))
    # PSRR et marges
    ps = {}
    for tool in ("ngspice", "LTspice"):
        for kind, esr, c in (("mcp_test", 0.02, 1e-6), ("mcp", 0.02, S.P["c_out_3v0"]), ("xc", 0.02, S.P["c_out_2v0"])):
            f, h = psrr(kind, esr, c, tool)
            ps[f"{kind}/{tool}"] = dict(dc=float(db(h[0])), at100=float(np.interp(np.log10(100), np.log10(f), db(h))),
                                        at1k=float(np.interp(np.log10(1e3), np.log10(f), db(h))), at24k=float(np.interp(np.log10(FPWM), np.log10(f), db(h))),
                                        at100k=float(np.interp(np.log10(1e5), np.log10(f), db(h))))
    m["psrr"] = ps
    return m


def main():
    FIG.mkdir(exist_ok=True)
    m = metrics()
    fig_cas1(m); fig_phase(m); fig_psrr(m); fig_stab(m); fig_chain(m); fig_tools(m)
    (RES / "metriques.json").write_text(json.dumps(m, indent=1, default=float))
    print(json.dumps(m, indent=1, default=float))


if __name__ == "__main__":
    main()
