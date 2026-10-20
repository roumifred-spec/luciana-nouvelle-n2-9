# -*- coding: utf-8 -*-
"""REPARER LE PLAN DE LA BIBLIOTHEQUE (sortie de secours, decidee le 20/10/2026).
Regarde chaque dossier ~/Luciana_neuve* qui a un plan.json. S'il est abime, propose de remettre la derniere bonne
copie (plan.json.copie). Rien n'est efface : le fichier abime est garde a cote. Rien n'est fait sans « OUI »."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan as P

HOME = os.path.expanduser("~")
dossiers = sorted(d for d in glob.glob(os.path.join(HOME, "Luciana_neuve*"))
                  if os.path.isdir(d) and (os.path.exists(os.path.join(d, "plan.json"))
                                           or os.path.exists(os.path.join(d, "plan.json.copie"))))
if not dossiers:
    print("Aucun plan trouve dans %s\\Luciana_neuve*. Rien a faire." % HOME)
abimes = 0
for d in dossiers:
    P.poser_le_dossier(d)
    try:
        P._lire_un_plan(P.F_PLAN)
        print("OK      %s : plan.json est sain." % d)
        continue
    except Exception as ex:
        abimes += 1
        print("\nABIME   %s : plan.json est illisible (%s)." % (d, str(ex)[:200]))
    rep = input("Remettre la derniere bonne copie a sa place ? Tape OUI puis Entree (autre chose = ne rien faire) : ")
    if rep.strip().upper() != "OUI":
        print("Rien n'a ete touche.")
        continue
    ok, phrase = P.reparer_depuis_la_copie()
    print(("REPARE  " if ok else "PAS REPARE  ") + phrase)
if dossiers and not abimes:
    print("\nAucun plan abime : rien n'a ete touche.")
