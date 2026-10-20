# -*- coding: utf-8 -*-
# LECTURE SEULE : on ne modifie RIEN. On regarde le tuyau de l'ancienne memoire.
import io

P = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\luciana.py"
S = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\res_zones.txt"

L = io.open(P, encoding="utf-8", errors="replace").read().splitlines()
plages = [(29090, 29200), (29760, 29900), (30040, 30200), (3895, 3940), (5040, 5095)]

out = []
for a, b in plages:
    out.append("=" * 70)
    out.append("LIGNES %d a %d" % (a, b))
    out.append("=" * 70)
    for n in range(a, min(b, len(L)) + 1):
        out.append("%d| %s" % (n, L[n - 1]))

io.open(S, "w", encoding="utf-8").write("\n".join(out))
print("ok, %d lignes ecrites" % len(out))
