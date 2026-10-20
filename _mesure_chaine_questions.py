# -*- coding: utf-8 -*-
"""Mesure : la chaine des questions existe-t-elle chez Luciana ? Lecture seule."""
import io, os, re

ICI = os.path.dirname(os.path.abspath(__file__))
LUMI = r"C:\Users\Fred\Lumi_appli"

MOTS = ["en_suspens", "le_lot_attend", "bloc_pour_l_assistante",
        "bloc_pour_le_proprietaire", "ranger_les_reponses", "amorcer",
        "garder_les_questions", "memoire_et_questions", "biblio2_pont",
        "biblio2_questions"]


def lire(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


print("=== FICHIERS CHEZ LUCIANA ===")
for n in sorted(os.listdir(ICI)):
    if n.startswith("biblio2_") and n.endswith(".py"):
        print("  %-32s %8d o" % (n, os.path.getsize(os.path.join(ICI, n))))

print("\n=== FICHIERS CHEZ LUMINITA ===")
for n in sorted(os.listdir(LUMI)):
    if n.startswith("biblio2_") and n.endswith(".py"):
        print("  %-32s %8d o" % (n, os.path.getsize(os.path.join(LUMI, n))))

print("\n=== OCCURRENCES DANS luciana.py ===")
t = lire(os.path.join(ICI, "luciana.py"))
print("  lignes = %d" % len(t.splitlines()))
for m in MOTS:
    print("  %-30s %d" % (m, t.count(m)))

print("\n=== OCCURRENCES DANS LES MODULES biblio2 DE LUCIANA ===")
for n in sorted(os.listdir(ICI)):
    if n.startswith("biblio2_") and n.endswith(".py"):
        tt = lire(os.path.join(ICI, n))
        trouve = ["%s=%d" % (m, tt.count(m)) for m in MOTS if tt.count(m)]
        print("  %-32s %s" % (n, ", ".join(trouve) or "(rien)"))
