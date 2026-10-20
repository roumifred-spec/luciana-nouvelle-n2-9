# -*- coding: utf-8 -*-
# LECTURE SEULE : on ne modifie RIEN. On cherche le nom exact du reglage de la memoire par le sens.
import io

P = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\luciana.py"
S = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\res_reglage_sens.txt"

L = io.open(P, encoding="utf-8", errors="replace").read().splitlines()

motifs = ["reglage_memoire_sens", "REGLAGE_SENS", "def rappel_automatique",
          "def _rappel_par_le_sens", "def _rappel_mots"]

out = []
for n, ligne in enumerate(L, 1):
    for m in motifs:
        if m in ligne:
            out.append("%d| %s" % (n, ligne))
            break

io.open(S, "w", encoding="utf-8").write("\n".join(out))
print("ok, %d lignes" % len(out))
