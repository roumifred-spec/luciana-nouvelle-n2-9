# -*- coding: utf-8 -*-
# LECTURE SEULE : on ouvre le programme EN SERVICE et on montre ses lignes qui parlent
# du chien de garde. Rien n'est modifie.
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CHEMIN = r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96\luciana.py"

print("=" * 78)
print("1) LE FICHIER EN SERVICE")
print("=" * 78)
import os
taille = os.path.getsize(CHEMIN)
quand = os.path.getmtime(CHEMIN)
import datetime
print("chemin :", CHEMIN)
print("taille :", taille, "octets")
print("ecrit le :", datetime.datetime.fromtimestamp(quand))

src = open(CHEMIN, encoding="utf-8", errors="replace").read()
lignes = src.split("\n")
print("lignes :", len(lignes))

print()
print("=" * 78)
print("2) COMBIEN DE FOIS LE CHIEN DE GARDE EST NOMME DANS LE PROGRAMME")
print("=" * 78)
for motif in ("_verif_rangement_auto", "chien_de_garde", "CHIEN_DE_GARDE", "rangement_auto"):
    print("%-28s : %d fois" % (motif, src.count(motif)))

print()
print("=" * 78)
print("3) LES LIGNES EXACTES (numero + texte)")
print("=" * 78)
n = 0
for i, ligne in enumerate(lignes, 1):
    if "chien_de_garde" in ligne.lower() or "verif_rangement_auto" in ligne.lower() or "rangement_auto" in ligne.lower():
        n += 1
        print("%6d | %s" % (i, ligne[:200]))
print()
print("TOTAL de lignes qui nomment le chien de garde :", n)
