# -*- coding: utf-8 -*-
# LECTURE SEULE : on ne modifie RIEN. La zone ou le tour est assemble.
import io

P = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\luciana.py"
S = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\res_zones2.txt"

L = io.open(P, encoding="utf-8", errors="replace").read().splitlines()
plages = [(30195, 30400)]

out = []
for a, b in plages:
    out.append("=" * 70)
    out.append("LIGNES %d a %d" % (a, b))
    out.append("=" * 70)
    for n in range(a, min(b, len(L)) + 1):
        out.append("%d| %s" % (n, L[n - 1]))

io.open(S, "w", encoding="utf-8").write("\n".join(out))
print("ok, %d lignes ecrites" % len(out))
