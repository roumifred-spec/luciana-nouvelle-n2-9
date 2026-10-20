# -*- coding: utf-8 -*-
# LECTURE SEULE : le badge de la version AVANT (la sauvegarde) et celui de la version posee.
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FICHIERS = [
    ("AVANT (la sauvegarde)", r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96"
                              r"\SAUVEGARDE_luciana_v126_avant_regles_de_tri_2026-10-06_2015.py"),
    ("APRES (la version posee)", r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96\luciana.py"),
]

for titre, p in FICHIERS:
    print("=== %s ===" % titre)
    if not os.path.exists(p):
        print("   ABSENT : %s" % p)
        continue
    print("   %s" % p)
    print("   %d octets" % os.path.getsize(p))
    s = open(p, encoding="utf-8").read()
    i = s.find('class="nom">')
    trouve = s[i:i + 220].replace("\n", " ") if i >= 0 else "ligne du badge NON TROUVEE"
    print("   BADGE : %s" % trouve)
    print("")
