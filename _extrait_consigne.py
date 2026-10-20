# -*- coding: utf-8 -*-
# Extraction, LECTURE SEULE : on ne modifie rien. Sert a savoir quel mot manque dans la consigne.
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

s = open("luciana.py", encoding="utf-8").read()

print("=== LES MOTS CHERCHES PAR LE BANC, DANS TOUT LE FICHIER ===")
for mot in ("Divers", "doute", "SUJET", "hierarchique", "sujet", "hierarchie"):
    print("  %-14s : %d fois" % (mot, s.count(mot)))

print("")
print("=== LA VRAIE CONSIGNE DE RANGEMENT (telle qu'ecrite dans le code) ===")
for m in re.finditer(r"CONSIGNE_DE_RANGEMENT_PLAN\s*=", s):
    i = m.start()
    print(s[i:i + 3000])
    print("=== fin de l'extrait (position %d) ===" % i)
