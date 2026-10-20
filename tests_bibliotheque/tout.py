# -*- coding: utf-8 -*-
"""TOUS LES ESSAIS DU BANC, D'UN COUP.

    python tests_bibliotheque/tout.py

Faux cerveau, faux Google, dossiers jetables (tests_bibliotheque/home_*). Ces essais ne touchent
NI ~/Luciana, NI ~/Luciana_neuve, NI le port 8002, NI le reglages.json livre dans nouvelle/.
Ils ne disent PAS si le SENS de ses reponses est bon : ca, seul le vrai cerveau le dira chez le
proprietaire (les .bat 5 a 8). Ils disent si le PROGRAMME tient ses regles.
"""
import os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import proprietaire, registre, pieces

if __name__ == "__main__":
    total_j, total_t, detail = 0, 0, []
    for nom, module in (("le nom du proprietaire", proprietaire), ("le registre des personnes", registre),
                        ("les pieces 1 a 4", pieces)):
        j, t = module.essai()
        total_j += j
        total_t += t
        detail.append((nom, j, t))
    print("\n" + "=" * 70)
    for nom, j, t in detail:
        print("  %-30s %d juste(s) sur %d%s" % (nom, j, t, "" if j == t else "   <-- DES RATES"))
    print("  %-30s %d juste(s) sur %d, %d rate(s)." % ("TOTAL", total_j, total_t, total_t - total_j))
    print("=" * 70)
    sys.exit(0 if total_j == total_t else 1)
