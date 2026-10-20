# -*- coding: utf-8 -*-
"""Verifie POUR DE VRAI, dans le fichier livre, les 3 points que le script de controle
a signales en echec. On lit la source, on n'invente rien."""
import io, re, sys

FICHIER = "luciana.py"
lignes = io.open(FICHIER, "r", encoding="utf-8").read().split("\n")

def montrer(motif, contexte=4, maxi=12):
    print("=" * 90)
    print("MOTIF RECHERCHE : %s  (lignes contenant ce texte)" % motif)
    print("=" * 90)
    n = 0
    for i, l in enumerate(lignes, 1):
        if motif in l:
            n += 1
            if n > maxi:
                break
            print("--- ligne %d ---" % i)
            for j in range(max(0, i - 1 - contexte), min(len(lignes), i + contexte)):
                print("   %d: %s" % (j + 1, lignes[j][:200]))
    if n == 0:
        print("   AUCUNE OCCURRENCE.")
    print("")

montrer("RELANCE_REPONDS_SUR_LE_FOND", contexte=10, maxi=3)
montrer("LE PROGRAMME T", contexte=8, maxi=2)
montrer("proposerEnvoi", contexte=6, maxi=4)
