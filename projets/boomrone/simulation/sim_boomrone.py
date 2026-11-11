#!/usr/bin/env python3
"""Simulation SPICE de l'alimentation de la carte Boomrone : génère les netlists,
les lance dans ngspice ET dans LTspice, relit les résultats et trace les courbes.

Trois cas :
  1. batterie + résistance interne + 4 moteurs en PWM  -> ondulation et creux de tension
  2. LDO 3,0 V (MCP1700) alimenté par cette ligne        -> PSRR, stabilité, ondulation de +3V0
  3. LDO 2,0 V (XC6206) du capteur de flux, sur +3V0     -> idem

Usage : python sim_boomrone.py [run|plot|all]   (depuis ce dossier)
Toutes les valeurs d'entrée sont dans PARAMS, avec leur source ou la mention « HYP » (hypothèse,
à vérifier). Voir rapport-simulation-spice.md.
"""
import math, os, shutil, subprocess, sys, time, json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NET = HERE / "netlists"
RES = HERE / "resultats"
FIG = HERE / "figures"
NGSPICE = Path(os.environ.get("NGSPICE_EXE", r"C:\Users\33766\tools\ngspice_pkg\mingw64\bin\ngspice_con.exe"))
LTSPICE = Path(os.environ.get("LTSPICE_EXE", r"C:\Users\33766\AppData\Local\Programs\ADI\LTspice\LTspice.exe"))

# --------------------------------------------------------------------------------------------
# Paramètres (source entre crochets ; HYP = hypothèse non sourcée, à vérifier)
# --------------------------------------------------------------------------------------------
P = dict(
    vocv=3.70,        # V  batterie à vide, bilan de « Architecture » — 03-architecture.md
    rint=0.040,       # ohm résistance interne batterie 40 mohm ±20 [03-architecture.md, bilan] (à mesurer)
    rcon=0.015,       # ohm connecteur, fils et pistes 15 mohm [03-architecture.md, bilan ; DES-008]
    f_pwm=24e3,       # Hz  période 41,7 us [04-conception-detaillee.md, DES-007]
    ron=0.036,        # ohm AO3400A : 24 typ / 48 max a VGS=2,5 V [AO3400A.pdf rev 3, p.1-2] ; milieu retenu
    vgs=3.0,          # V  grille pilotée en 3,0 V [DES-007]
    t_edge=65e-9,     # s  HYP front de grille : 2,2 x (47 ohm x 630 pF) [DES-007 : 47 ohm, Ciss 630 pF typ.]
    # moteurs 8520 : aucune donnée de fiche (DOU-190)
    rm=1.0,           # ohm HYP résistance de l'induit
    lm=25e-6,         # H   HYP inductance de l'induit
    # découplage de la ligne moteurs [DES-007] ; ESR : HYP
    c_bulk=22e-6, n_bulk=2, esr_bulk=5e-3, c_hf=100e-9,
    c_mot=100e-9,     # 100 nF aux bornes de chaque moteur [DES-007]
    # diode SS34 : fiche absente du dossier (DOU-187 levé, fiche non relevée ici) -> HYP
    d_is=3e-6, d_n=1.05, d_rs=0.04, d_cjo=200e-12,
    # entrée des régulateurs [DES-008, DES-009]
    r_fer=0.10,       # ohm ferrite BLM18PG121SN1D, ordre de grandeur [DES-008] (fiche absente, DOU-186)
    c_in_l=22e-6, esr_in=5e-3, c_in_ldo=1e-6,
    # logique et capteur
    i_logic=0.130,    # A  dimensionnement du régulateur 3,0 V [DES-009]
    c_out_3v0=4.7e-6, # F  [DES-009]
    c_out_2v0=2.2e-6, # F  [DES-005]
    i_flow=0.009,     # A  charge du capteur de flux [DES-005]
    i_flow_pk=0.070,  # A  pointe a la montée [DES-005]
    # courants moyens totaux et cas du bilan [03-architecture.md]
    i_hover=5.5, i_crest=9.5, i_pess=7.5, r_pess=0.110,
    # LDO MCP1700 3,0 V [MCP1700.pdf DS20001826C]
    mcp_psrr_db=44.0, mcp_psrr_vr=1.2, mcp_psrr_il=0.050,   # p.4 : 44 dB a 100 Hz, COUT 1 uF, IL 50 mA, VR 1,2 V
    mcp_vdo=0.178, mcp_idrop=0.250,                          # p.3 : 178 mV typ a 250 mA
    mcp_iq=1.6e-6,                                           # p.3 : 1,6 uA typ
    # LDO XC6206 2,0 V [XC6206.pdf ETR0305_004b]
    xc_line=0.0005,   # 0,05 %/V typ (regulation en ligne, p.4)
    xc_vdo=0.350, xc_idrop=0.100,                            # 350 mV typ a 100 mA [DES-005, fiche p.5]
    xc_iq=1.0e-6,                                            # 1,0 uA typ (p.4)
    # modèle de boucle des LDO : HYP (aucune fiche ne donne la bande passante de la boucle)
    k_fb=0.4, gmp=0.5, a0=6.3, fp=1.0e6, fg=3.0e6,
)

COLORS = {"ngspice": "#1f77b4", "LTspice": "#d62728"}


# --------------------------------------------------------------------------------------------
# Génération des netlists
# --------------------------------------------------------------------------------------------
def fmt(x):
    return f"{x:.6g}"


def ldo_subckt(name, vset, vdo, idrop, iq, h_dc, rl_ref, loopbreak=False, vin_nom=3.7, i_nom=0.13, p=P):
    """Modèle comportemental d'un LDO.
    - décrochage : courant limité par (vin-vout)/rdo avec rdo = vdo/idrop (fiche)
    - PSRR en continu calé sur la fiche : H = (1/ro)/(1/ro + 1/RL + gm_boucle)
    - boucle (HYP) : gm_boucle = k*a0*gmp = 1,26 S, pôles de l'ampli à fp et fg
    """
    k, gmp, a0 = p["k_fb"], p["gmp"], p["a0"]
    gm_loop = k * a0 * gmp
    inv_ro = h_dc * (gm_loop + 1.0 / rl_ref) / (1.0 - h_dc)
    ro = 1.0 / inv_ro
    rdo = vdo / idrop
    # tension de référence pour obtenir vset au courant nominal
    ipass = max(i_nom - (vin_nom - vset) / ro, 1e-4)
    vref = k * vset + ipass / (gmp * a0)
    cp = 1.0 / (2 * math.pi * p["fp"] * 1e3)
    cg = 1.0 / (2 * math.pi * p["fg"] * 1e3)
    link = "Lbrk fbd fbn 1G" if loopbreak else "Vz fbd fbn 0"
    pins = "vin vout gnd fbd fbn" if loopbreak else "vin vout gnd"
    if loopbreak:
        link = "Lbrk fbd fbn 1G"
    efb = "Efb fbd gnd vout gnd " + fmt(k)
    txt = f"""* LDO comportemental {name} (voir sim_boomrone.py) : ro={fmt(ro)} ohm, rdo={fmt(rdo)} ohm, vref={fmt(vref)} V
.subckt {name} {pins}
Iq vin gnd {fmt(iq)}
Rro vin vout {fmt(ro)}
Vref ref gnd {fmt(vref)}
{efb}
{link}
Eea ea1 gnd ref fbn {fmt(a0)}
Rp ea1 ea 1k
Cp ea gnd {fmt(cp)}
Rg ea ea2 1k
Cg ea2 gnd {fmt(cg)}
Bp vin vout I=max(0,min({fmt(gmp)}*v(ea2),(v(vin)-v(vout))/{fmt(rdo)}))
.ends {name}
"""
    return txt, dict(ro=ro, rdo=rdo, vref=vref, gm_loop=gm_loop)


def mcp_subckt(**kw):
    p = P
    h = 10 ** (-p["mcp_psrr_db"] / 20)
    rl = p["mcp_psrr_vr"] / p["mcp_psrr_il"]
    return ldo_subckt("MCP1700", 3.0, p["mcp_vdo"], p["mcp_idrop"], p["mcp_iq"], h, rl, i_nom=p["i_logic"], **kw)


def xc_subckt(**kw):
    p = P
    return ldo_subckt("XC6206", 2.0, p["xc_vdo"], p["xc_idrop"], p["xc_iq"], p["xc_line"], 2.0 / p["i_flow"],
                      vin_nom=3.0, i_nom=p["i_flow"], **kw)


def power_block(rint, per_stagger, emf_expr, d, tdelay, emf_pwl=None):
    """Batterie + découplage + 4 moteurs en PWM. Retourne le texte et la liste des vecteurs."""
    p = P
    per = 1.0 / p["f_pwm"]
    ton = d * per
    L = []
    L.append(f"Vbat vb0 0 {fmt(p['vocv'])}")
    L.append(f"Rint vb0 vb1 {fmt(rint)}")
    L.append(f"Rcon vb1 vbm {fmt(p['rcon'])}")
    for i in range(p["n_bulk"]):
        L.append(f"Cb{i+1} vbm cb{i+1} {fmt(p['c_bulk'])}")
        L.append(f"Rb{i+1} cb{i+1} 0 {fmt(p['esr_bulk'])}")
    L.append(f"Chf vbm 0 {fmt(p['c_hf'])}")
    L.append(f".model SWN SW(Vt=1.5 Vh=0.2 Ron={fmt(p['ron'])} Roff=10Meg)")
    L.append(f".model DSS34 D(Is={fmt(p['d_is'])} N={fmt(p['d_n'])} Rs={fmt(p['d_rs'])} Cjo={fmt(p['d_cjo'])})")
    for k in range(1, 5):
        td = tdelay + (k - 1) * per * per_stagger
        L.append(f"Vg{k} g{k} 0 PULSE(0 {fmt(p['vgs'])} {fmt(td)} {fmt(p['t_edge'])} {fmt(p['t_edge'])} {fmt(ton)} {fmt(per)})")
        L.append(f"S{k} d{k} 0 g{k} 0 SWN")
        L.append(f"Rm{k} vbm ma{k} {fmt(p['rm'])}")
        L.append(f"Lm{k} ma{k} mb{k} {fmt(p['lm'])}")
        L.append(f"Ve{k} mb{k} d{k} {emf_expr}")
        L.append(f"Cm{k} vbm d{k} {fmt(p['c_mot'])}")
        L.append(f"Ds{k} d{k} vbm DSS34")
    return "\n".join(L)


def emf_for(i_avg_total, rint, d):
    """Force contre-électromotrice qui donne ~ le courant moyen visé (calcul approché)."""
    p = P
    vbm = p["vocv"] - i_avg_total * (rint + p["rcon"])
    i_m = i_avg_total / 4
    return max(0.0, d * vbm - i_m * (p["rm"] + d * p["ron"]) - (1 - d) * 0.5)


# Cas de charge : (clé, titre, courant total, rint total de la batterie, duty, décalage de phase, démarrage)
LOADS = {
    "vol":      dict(titre="Stationnaire nominal (5,5 A, 40 mΩ)",            itot=P["i_hover"], rint=P["rint"], d=0.70, stag=0.0, start=False),
    "vol_dec":  dict(titre="Stationnaire, PWM décalées de 90°",              itot=P["i_hover"], rint=P["rint"], d=0.70, stag=0.25, start=False),
    "crete":    dict(titre="Crête après lancer (9,5 A, 40 mΩ)",              itot=P["i_crest"], rint=P["rint"], d=0.95, stag=0.0, start=False),
    "pess":     dict(titre="Stationnaire pessimiste (7,5 A, 95 mΩ batterie)", itot=P["i_pess"], rint=P["r_pess"] - P["rcon"], d=0.85, stag=0.0, start=False),
    "demarrage": dict(titre="Démarrage : force contre-électromotrice de 0 à sa valeur en 2 ms (appel de courant)", itot=P["i_hover"], rint=P["rint"], d=0.70, stag=0.0, start=True),
}

T_END = {"vol": 1.5e-3, "vol_dec": 1.5e-3, "crete": 1.5e-3, "pess": 1.5e-3, "demarrage": 3.5e-3}


EMF_CACHE = HERE / "emf_calibree.json"


def load_emf(load):
    """F.c.e.m. calibrée (par calibrate()) ou, a défaut, estimation approchée."""
    c = LOADS[load]
    key = "vol" if c["start"] else load
    if key == "vol_dec":
        key = "vol"
    if EMF_CACHE.exists():
        d = json.loads(EMF_CACHE.read_text())
        if key in d:
            return d[key]
    return emf_for(c["itot"], c["rint"], c["d"])


def calibrate():
    """Ajuste la f.c.e.m. de chaque cas pour que le courant moyen de la batterie atteigne le courant visé
    (5,5 A / 9,5 A / 7,5 A du bilan de « Architecture »), avec ngspice, 3 itérations."""
    import numpy as np
    NET.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)
    cache = {}
    for load in ("vol", "crete", "pess"):
        c = LOADS[load]
        e = emf_for(c["itot"], c["rint"], c["d"])
        for it in range(4):
            cache[load] = e
            EMF_CACHE.write_text(json.dumps(cache))
            txt, vecs, out = tran_netlist("cas1", load, "ngspice")
            run_ngspice(txt, f"calib_{load}")
            out_txt = RES / f"cas1_{load}_ngspice.txt"
            a = np.loadtxt(out_txt)
            m = a[:, 0] > 1.0e-3
            i_meas = -a[m, 3].mean()
            err = i_meas - c["itot"]
            print(f"calibration {load}: iter {it} emf={e:.4f} V -> I = {i_meas:.3f} A (cible {c['itot']})", flush=True)
            if abs(err) < 0.02 * c["itot"]:
                break
            e = max(0.0, e + (err / 4) * (P["rm"] + 0.4))
        cache[load] = e
    EMF_CACHE.write_text(json.dumps(cache))
    return cache


def build_power(load):
    c = LOADS[load]
    e = load_emf(load)
    if c["start"]:
        emf = f"PWL(0 0 0.3m 0 2.3m {fmt(e)})"
        e_final = e
    else:
        emf = fmt(e)
        e_final = e
    return power_block(c["rint"], c["stag"], emf, c["d"], 5e-6), e_final


def tran_netlist(case, load, tool, tmax=20e-9, suffix=""):
    """case : 'cas1' (puissance seule), 'cas2' (chaîne jusqu'à +3V0), 'cas3' (jusqu'à +2V0)."""
    p = P
    body, e_final = build_power(load)
    vecs = ["v(vbm)", "i(vbat)", "i(lm1)", "i(lm2)", "i(lm3)", "i(lm4)", "v(d1)"]
    sub = ""
    extra = []
    if case in ("cas2", "cas3"):
        extra.append(f"Rfer vbm vbl {fmt(p['r_fer'])}")
        extra.append(f"Cil vbl cil {fmt(p['c_in_l'])}")
        extra.append(f"Ril cil 0 {fmt(p['esr_in'])}")
        extra.append(f"Cild vbl 0 {fmt(p['c_in_ldo'])}")
        extra.append("XU3 vbl v3 0 MCP1700")
        extra.append(f"Cout3 v3 c3x {fmt(p['c_out_3v0'])}")
        extra.append("Rc3 c3x 0 20m")
        extra.append(f"Rl3 v3 0 {fmt(3.0 / p['i_logic'])}")
        sub += mcp_subckt()[0]
        vecs += ["v(vbl)", "v(v3)"]
    if case == "cas3":
        extra.append("XU2 v3 v2 0 XC6206")
        extra.append(f"Cout2 v2 c2x {fmt(p['c_out_2v0'])}")
        extra.append("Rc2 c2x 0 20m")
        extra.append(f"Rl2 v2 0 {fmt(2.0 / p['i_flow'])}")
        # pointe de 70 mA pendant 100 us a la montée, appliquée à t = 0,6 ms
        extra.append(f"Ipk v2 0 PULSE(0 {fmt(p['i_flow_pk'] - p['i_flow'])} 0.6m 1u 1u 100u 10)")
        sub += xc_subckt()[0]
        vecs += ["v(v2)"]
    tend = T_END[load]
    head = f"* Boomrone {case} {load} — {LOADS[load]['titre']} (force contre-électromotrice par moteur : {e_final:.3f} V, HYP)"
    lines = [head, body, *extra, sub, f".tran {fmt(tmax)} {fmt(tend)} 0 {fmt(tmax)}"]
    out = f"{case}_{load}{suffix}_{tool}"
    if tool == "ngspice":
        lines += [".control", "set filetype=ascii", "run", f"wrdata {out}.txt " + " ".join(vecs), "quit", ".endc"]
    lines.append(".end")
    return "\n".join(lines) + "\n", vecs, out


def ac_netlist(kind, tool, esr=None, cout=None, fu_scale=1.0, loop=False):
    """kind : 'mcp_test' (conditions de la fiche), 'mcp' (point de fonctionnement), 'xc'. Retourne netlist, sortie."""
    p = P
    if kind.startswith("mcp"):
        sub = mcp_subckt(loopbreak=loop)[0]
        name, vin_dc = "MCP1700", p["vocv"] - 0.5
        if kind == "mcp_test":
            # conditions de la fiche : VR = 1,2 V -> on simule le modèle a 3,0 V avec la même charge en ohm (24 ohm)
            rl, c = 24.0, 1e-6
        else:
            rl, c = 3.0 / p["i_logic"], p["c_out_3v0"]
    else:
        sub = xc_subckt(loopbreak=loop)[0]
        name, vin_dc = "XC6206", 3.0
        rl, c = 2.0 / p["i_flow"], p["c_out_2v0"]
    if cout is not None:
        c = cout
    esr = 0.02 if esr is None else esr
    lines = [f"* AC {kind} esr={esr} cout={c}"]
    lines.append(f"Vin vin 0 {fmt(vin_dc)} AC 1")
    lines.append(f"XU vin vo 0 fbd fbn {name}" if loop else f"XU vin vo 0 {name}")
    lines.append(f"Co vo cx {fmt(c)}")
    lines.append(f"Resr cx 0 {fmt(esr)}")
    lines.append(f"Rl vo 0 {fmt(rl)}")
    if loop:
        # Vin sans ondulation : source continue ; injection dans la boucle
        lines[1] = f"Vin vin 0 {fmt(vin_dc)}"
        lines.append("Vinj inj 0 0 AC 1")
        lines.append("Cinj inj fbn 1G")
    lines.append(sub)
    lines.append(".ac dec 60 10 10Meg")
    out = f"ac_{kind}_{'loop_' if loop else ''}{esr:g}_{c:.3g}_{tool}".replace("e-", "m").replace("+", "")
    if tool == "ngspice":
        if loop:
            probe = "v(fbd) v(fbn)"
        else:
            probe = "v(vo) v(vin)"
        lines += [".control", "run", f"wrdata {out}.txt {probe}", "quit", ".endc"]
    lines.append(".end")
    return "\n".join(lines) + "\n", out


# --------------------------------------------------------------------------------------------
# Lancement
# --------------------------------------------------------------------------------------------
def run_ngspice(netlist_text, out):
    path = NET / f"{out}.cir"
    path.write_text(netlist_text.encode("ascii", "replace").decode(), encoding="ascii")
    t0 = time.time()
    r = subprocess.run([str(NGSPICE), "-b", "-o", str(NET / f"{out}.log"), str(path)], cwd=str(RES), capture_output=True, text=True, timeout=1800)
    dt = time.time() - t0
    return dt, r.returncode


def run_ltspice(netlist_text, out):
    path = NET / f"{out}.cir"
    path.write_text(netlist_text.encode("ascii", "replace").decode(), encoding="ascii")
    t0 = time.time()
    r = subprocess.run([str(LTSPICE), "-b", str(path)], cwd=str(NET), capture_output=True, text=True, timeout=1800)
    dt = time.time() - t0
    # LTspice écrit le .raw à côté du netlist : on le range dans resultats/
    raw = NET / f"{out}.raw"
    if raw.exists():
        shutil.move(str(raw), str(RES / f"{out}.raw"))
    op = NET / f"{out}.op.raw"
    if op.exists():
        op.unlink()
    return dt, r.returncode


def all_jobs():
    jobs = []
    for load in ("vol", "vol_dec", "crete", "pess", "demarrage"):
        jobs.append(("tran", "cas1", load))
    for load in ("vol", "crete", "pess", "demarrage"):
        jobs.append(("tran", "cas2", load))
    jobs.append(("tran", "cas3", "vol"))
    return jobs


def run_extras():
    """Vérifications : pas de calcul plus fin (convergence) et dropout maximal de la fiche pour le MCP1700."""
    NET.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)
    timing = json.loads((RES / "timing.json").read_text()) if (RES / "timing.json").exists() else {}
    for tool in ("ngspice", "LTspice"):
        fn = run_ngspice if tool == "ngspice" else run_ltspice
        for load in ("vol", "crete"):
            txt, vecs, out = tran_netlist("cas1", load, tool, tmax=5e-9, suffix="_fin")
            dt, rc = fn(txt, out); timing[out] = dict(s=round(dt, 1), rc=rc); print(out, round(dt, 1), rc, flush=True)
        old = P["mcp_vdo"]
        P["mcp_vdo"] = 0.350   # dropout maximal garanti (MCP1700.pdf p.3 : 350 mV a 250 mA)
        for load in ("crete", "demarrage"):
            txt, vecs, out = tran_netlist("cas2", load, tool, suffix="_dromax")
            dt, rc = fn(txt, out); timing[out] = dict(s=round(dt, 1), rc=rc); print(out, round(dt, 1), rc, flush=True)
        P["mcp_vdo"] = old
    (RES / "timing.json").write_text(json.dumps(timing, indent=1))


def run_all():
    NET.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)
    calibrate()
    timing = {}
    for kind, case, load in all_jobs():
        for tool in ("ngspice", "LTspice"):
            txt, vecs, out = tran_netlist(case, load, tool)
            fn = run_ngspice if tool == "ngspice" else run_ltspice
            dt, rc = fn(txt, out)
            timing[out] = dict(s=round(dt, 1), rc=rc)
            print(f"{out:32s} {dt:7.1f} s rc={rc}", flush=True)
    # AC : PSRR et boucle
    ac_jobs = [("mcp_test", None, None, False), ("mcp", None, None, False), ("xc", None, None, False)]
    for esr in (0.005, 0.1, 0.5, 1.0, 2.0):
        ac_jobs.append(("mcp", esr, None, True))
    for esr in (0.005, 2.0):
        ac_jobs.append(("xc", esr, None, True))
    ac_jobs.append(("mcp", 0.02, 1e-6, False))
    for kind, esr, c, loop in ac_jobs:
        for tool in ("ngspice", "LTspice"):
            txt, out = ac_netlist(kind, tool, esr=esr, cout=c, loop=loop)
            fn = run_ngspice if tool == "ngspice" else run_ltspice
            dt, rc = fn(txt, out)
            timing[out] = dict(s=round(dt, 1), rc=rc)
            print(f"{out:32s} {dt:7.1f} s rc={rc}", flush=True)
    (RES / "timing.json").write_text(json.dumps(timing, indent=1))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("run", "all"):
        run_all()
    if what in ("extras", "all"):
        run_extras()
    if what in ("plot", "all"):
        import analyse_boomrone  # noqa: F401  (même dossier)
        analyse_boomrone.main()
