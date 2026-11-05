"""Parametres de l'optimisation, charges depuis (ou sauves vers) un fichier JSON. Valeurs par
defaut raisonnables pour une carte type Boomrone (~100 composants, carte de quelques cm2) ;
a ajuster selon la densite de la carte et le temps de calcul accepte."""
from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from typing import Optional

from .annealing import AnnealingConfig
from .cost import CostWeights
from .hierarchy import HierarchyConfig


@dataclass
class StoppingCriteria:
    max_cycles: int = 6          # nombre de cycles complets (place -> evalue -> ameliore) par strategie
    no_improve_cycles: int = 2   # arret anticipe si aucune amelioration de cout depuis N cycles
    time_budget_s: Optional[float] = None  # arret anticipe si depasse (None = pas de limite de temps)


@dataclass
class EngineConfig:
    # --- Poids de la fonction de cout (section 4 de la mission) ---
    weight_area: float = 1.0              # poids de la surface totale occupee (objectif prioritaire)
    weight_wirelength: float = 0.5        # poids de la longueur de cablage estimee (HPWL)
    weight_congestion: float = 0.3        # poids de la congestion des zones de routage
    weight_crossings: float = 0.4         # poids des croisements de pistes probables
    weight_accessibility: float = 0.2     # poids de l'inaccessibilite des pastilles
    weight_vias: float = 0.6              # poids du nombre de vias estime
    min_clearance_mm: float = 0.3         # distance minimale entre boitiers (contrainte dure)
    overlap_penalty_weight: float = 1000.0  # poids ecrasant de la contrainte "pas de recouvrement"
    weight_decoupling: float = 10.0       # poids par mm de depassement de la distance de decouplage
    decoupling_file: Optional[str] = None  # decouplage.json (condensateur -> broche d'alimentation) ; None = sans regle
    live_dir: Optional[str] = None        # dossier de suivi en direct (page web), None = desactive
    decoupling_max_mm: float = 5.0        # distance max par defaut quand une regle n'en donne pas (valeur de projet, pas de fiche)

    # --- Hierarchie (section 3) ---
    max_group_size: int = 10              # taille max d'un "petit groupe" avant repartitionnement
    fd_iterations_group: int = 300        # iterations de placement par forces dirigees (niveau groupe)
    fd_iterations_assembly: int = 250     # iterations de placement par forces dirigees (assemblage macro)

    # --- Recuit simule (section 2.C) ---
    # Valeurs validees sur Boomrone (107 composants, 2026-11-05) : 0 recouvrement et une
    # surface ~1,8x la surface d'origine sur chacune des 2 strategies x 3 cycles de l'essai
    # (cf. tools/pcb_placement/README.md) en ~20 minutes totales (2 strategies paralleles).
    sa_group_iterations: int = 1500
    sa_group_t0: float = 8.0
    sa_block_iterations: int = 2000
    sa_block_t0: float = 10.0
    sa_global_iterations: int = 3500
    sa_global_t0: float = 1.5
    sa_t_end: float = 0.03
    block_move_prob: float = 0.4          # probabilite de deplacer un bloc entier plutot qu'un composant (niveau global)
    penalty_ramp: bool = False             # penalite progressive du recuit global (cf. HierarchyConfig)
    penalty_start: float = 0.03
    penalty_ramp_frac: float = 0.7
    use_compaction: bool = True           # passe de compactage deterministe en fin de pipeline (0 recouvrement garanti, cf. hierarchy.optimize_board)

    # --- Boucle d'optimisation et strategies paralleles (sections 6 et 10) ---
    stopping: StoppingCriteria = field(default_factory=lambda: StoppingCriteria(max_cycles=3, no_improve_cycles=2))
    n_parallel_strategies: int = 2        # nombre de strategies (graines/poids differents) executees en parallele
    n_candidates_per_cycle: int = 1       # candidats generes par cycle au sein d'une strategie (1 = pas de restart interne)
    random_seed: int = 0

    def to_cost_weights(self) -> CostWeights:
        return CostWeights(
            area=self.weight_area,
            wirelength=self.weight_wirelength,
            congestion=self.weight_congestion,
            crossings=self.weight_crossings,
            accessibility=self.weight_accessibility,
            vias=self.weight_vias,
            min_clearance_mm=self.min_clearance_mm,
            overlap_penalty_weight=self.overlap_penalty_weight,
            decoupling=self.weight_decoupling,
        )

    def to_hierarchy_config(self, seed: Optional[int] = None) -> HierarchyConfig:
        s = self.random_seed if seed is None else seed
        return HierarchyConfig(
            max_group_size=self.max_group_size,
            fd_iterations_group=self.fd_iterations_group,
            fd_iterations_assembly=self.fd_iterations_assembly,
            sa_group=AnnealingConfig(iterations=self.sa_group_iterations, t0=self.sa_group_t0, t_end=self.sa_t_end, seed=s),
            sa_block=AnnealingConfig(iterations=self.sa_block_iterations, t0=self.sa_block_t0, t_end=self.sa_t_end, seed=s),
            sa_global=AnnealingConfig(iterations=self.sa_global_iterations, t0=self.sa_global_t0, t_end=self.sa_t_end, seed=s),
            block_move_prob=self.block_move_prob,
            use_compaction=self.use_compaction,
            penalty_ramp=self.penalty_ramp,
            penalty_start=self.penalty_start,
            penalty_ramp_frac=self.penalty_ramp_frac,
            seed=s,
        )

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dataclasses.asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "EngineConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        stopping_data = data.pop("stopping", None)
        cfg = cls(**data)
        if stopping_data:
            cfg.stopping = StoppingCriteria(**stopping_data)
        return cfg
