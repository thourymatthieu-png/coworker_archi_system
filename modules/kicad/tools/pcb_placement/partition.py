"""Partitionnement par graphe (min-cut) : regroupe les composants d'un bloc trop gros en
sous-groupes fortement connectes, par bissection spectrale (vecteur de Fiedler) puis
raffinement local Kernighan-Lin. Sans dependance externe (pas de networkx) : la matrice du
graphe est petite (quelques dizaines de composants par bloc), numpy suffit.

Sur Boomrone, les "blocs fonctionnels" de haut niveau sont deja connus (une feuille de
schema = un DES-xxx, cf. kicad_tetris_extract.REF_TO_BLOCK) : ce module sert au niveau
INFERIEUR (decouper un bloc en petits groupes, etape 2 du placement hierarchique), et au
niveau GENERIQUE (si le champ "block" d'un composant est absent/inconnu, pour une carte sans
hierarchie de schema exploitable)."""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from .model import Board, Net


def build_weight_matrix(refs: List[str], nets: Dict[str, Net], extra=None) -> np.ndarray:
    """Expansion en clique ponderee : un reseau de k pastilles ajoute un poids 1/(k-1) entre
    chaque paire de composants qu'il relie (evite qu'un gros bus domine le cout de coupe)."""
    idx = {r: i for i, r in enumerate(refs)}
    n = len(refs)
    w = np.zeros((n, n), dtype=float)
    for net in nets.values():
        members = sorted({ref for ref, _pad in net.pins if ref in idx})
        k = len(members)
        if k < 2:
            continue
        weight = 1.0 / (k - 1)
        for a in range(k):
            ia = idx[members[a]]
            for b in range(a + 1, k):
                ib = idx[members[b]]
                w[ia, ib] += weight
                w[ib, ia] += weight
    for ra, rb, wt in (extra or ()):   # liens supplementaires (ex. condensateur de decouplage - circuit)
        if ra in idx and rb in idx and ra != rb:
            w[idx[ra], idx[rb]] += wt
            w[idx[rb], idx[ra]] += wt
    return w


def spectral_bisect(refs: List[str], w: np.ndarray) -> Tuple[List[str], List[str]]:
    """Coupe le graphe en deux par le signe du vecteur de Fiedler (2e plus petite valeur
    propre du Laplacien) : minimise approximativement la somme des poids coupes pour une
    partition equilibree."""
    n = len(refs)
    if n <= 2:
        mid = n // 2
        return refs[:mid] or refs[:1], refs[mid:] or refs[1:]
    degrees = w.sum(axis=1)
    laplacian = np.diag(degrees) - w
    # Petites matrices (<< 200) : eigh dense est largement assez rapide ici.
    eigvals, eigvecs = np.linalg.eigh(laplacian)
    fiedler = eigvecs[:, 1]  # la plus petite valeur propre (0) correspond au vecteur constant
    order = np.argsort(fiedler)
    mid = n // 2
    group_a = [refs[i] for i in order[:mid]]
    group_b = [refs[i] for i in order[mid:]]
    return group_a, group_b


def _cut_weight(idx_a: List[int], idx_b: List[int], w: np.ndarray) -> float:
    return float(w[np.ix_(idx_a, idx_b)].sum())


def kl_refine(refs: List[str], group_a: List[str], group_b: List[str], w: np.ndarray, max_passes: int = 8) -> Tuple[List[str], List[str]]:
    """Raffinement Kernighan-Lin : echange par paires tant que ca reduit le poids de coupe,
    en gardant les deux groupes de taille egale (+-1)."""
    idx = {r: i for i, r in enumerate(refs)}
    a = list(group_a)
    b = list(group_b)

    for _ in range(max_passes):
        improved = False
        best_gain = 0.0
        best_pair = None
        for ia, ra in enumerate(a):
            for ib, rb in enumerate(b):
                # Gain d'un echange ra <-> rb sur le poids de coupe total (externe aux deux
                # groupes inchange ; seul le poids interne/croise des deux change).
                before = _pair_cut_contrib(ra, rb, a, b, idx, w)
                after = _pair_cut_contrib(rb, ra, a, b, idx, w)
                gain = before - after
                if gain > best_gain + 1e-9:
                    best_gain = gain
                    best_pair = (ia, ib)
        if best_pair is None:
            break
        ia, ib = best_pair
        a[ia], b[ib] = b[ib], a[ia]
        improved = True
        if not improved:
            break
    return a, b


def _pair_cut_contrib(ref_in_a_slot: str, ref_in_b_slot: str, a: List[str], b: List[str], idx: Dict[str, int], w: np.ndarray) -> float:
    """Poids de coupe induit si `ref_in_a_slot` occupe une place du groupe A et
    `ref_in_b_slot` une place du groupe B (sert a comparer avant/apres un echange)."""
    ia = idx[ref_in_a_slot]
    total = 0.0
    for rb in b:
        if rb == ref_in_b_slot:
            continue
        total += w[ia, idx[rb]]
    return total


def partition_refs(refs: List[str], nets: Dict[str, Net], max_group_size: int, extra=None) -> List[List[str]]:
    """Decoupe recursivement `refs` en groupes de taille <= max_group_size par bissection
    spectrale + raffinement KL. Retourne une liste de groupes (couverture complete, sans
    recouvrement)."""
    if len(refs) <= max_group_size:
        return [refs]
    w_full = build_weight_matrix(refs, nets, extra)
    group_a, group_b = spectral_bisect(refs, w_full)
    group_a, group_b = kl_refine(refs, group_a, group_b, w_full)
    result = []
    for g in (group_a, group_b):
        if g:
            result.extend(partition_refs(g, nets, max_group_size, extra))
    return result


def partition_board(board: Board, max_group_size: int) -> Dict[str, List[List[str]]]:
    """Pour chaque bloc fonctionnel du schema (board.blocks()), sous-partitionne ses
    composants en petits groupes si besoin. Retourne {bloc: [groupe1, groupe2, ...]}."""
    out: Dict[str, List[List[str]]] = {}
    for block in board.blocks():
        refs = board.refs_in_block(block)
        out[block] = partition_refs(refs, board.nets, max_group_size)
    return out
