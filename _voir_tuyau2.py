# -*- coding: utf-8 -*-
# LECTURE SEULE : on ne modifie RIEN. On cherche OU le rappel automatique est branche.
import io

P = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\luciana.py"
S = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\res_tuyau3.txt"

L = io.open(P, encoding="utf-8", errors="replace").read().splitlines()

motifs = ["_rappel_par_le_sens", "_biblio2_memoire(", "sens_chercher(", "grand tiroir",
          "GRAND_TIROIR", "rappel = ", "rappel =", "+ rappel", "rappel,", "rappel)",
          "rappel\n", "RAPPEL_ACTIF", "rappeler_la_memoire", "_rappel("]

out = []
for n, ligne in enumerate(L, 1):
    bas = ligne.lower()
    for m in motifs:
        if m.lower() in bas:
            out.append("%d| %s" % (n, ligne))
            break

io.open(S, "w", encoding="utf-8").write("\n".join(out))
print("ok, %d lignes" % len(out))
