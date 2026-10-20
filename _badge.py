# -*- coding: utf-8 -*-
# LECTURE SEULE : quel numero de version portera le badge a l'ecran ?
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

s = open("luciana.py", encoding="utf-8").read()

print("=== AUTOUR DE 'TON AMIE' (l'en-tete de l'appli) ===")
i = s.find("TON AMIE")
print(s[max(0, i - 400):i + 250] if i >= 0 else "pas trouve")

print("")
print("=== LES 12 PREMIERES LIGNES QUI PORTENT 'v125' ===")
n = 0
for ligne in s.split("\n"):
    if "v125" in ligne:
        n += 1
        print("   %d: %s" % (n, ligne.strip()[:220]))
        if n >= 12:
            break
print("")
print("=== LE FICHIER EN SERVICE PORTE-T-IL v126 ? ===")
print("   'v126' present : %d fois" % s.count("v126"))
