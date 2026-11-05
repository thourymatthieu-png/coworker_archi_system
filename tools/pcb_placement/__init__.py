"""Moteur d'optimisation du placement PCB, independant de KiCad pendant les calculs.

Entree : le JSON produit par tools/kicad_tetris_extract.py (lecture seule du .kicad_pcb via
pcbnew, Python embarque de KiCad). Sortie : un JSON de solution (positions/rotations),
applique sur une COPIE du PCB par tools/kicad_apply_placement.py (jamais le fichier original).

Aucun module de ce paquet n'importe pcbnew : il tourne avec le Python systeme (numpy et
matplotlib suffisent), voir tools/pcb_optimize_placement.py pour la ligne de commande.
"""
