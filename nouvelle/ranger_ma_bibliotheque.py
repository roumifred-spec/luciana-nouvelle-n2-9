# -*- coding: utf-8 -*-
"""LE PREMIER RANGEMENT DE SA BIBLIOTHEQUE DANS LE PLAN (piece 2 de la bibliotheque rangee, 20/10/2026).

Apres chaque echange, l'archiviste range tout seul ce qui est NEUF. Mais une grosse reserve ancienne (par exemple
les fiches de l'import) ne part pas en douce : elle se range ICI, une seule fois, quand Fred le decide.

1) D'abord un ESSAI : combien de fiches pas encore rangees, combien de texte, et une estimation du prix.
2) Seulement si on tape OUI : l'archiviste les range par lots, cree les categories lui-meme, et divise les tiroirs
   trop pleins au fur et a mesure. S'il s'arrete (panne, internet), on relance : il reprend ou il en etait.
Rien n'est efface, aucun texte n'est reecrit : seules les etiquettes (le plan) sont posees.
"""
import os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import luciana_neuve as N     # charge l'ancien programme (cles, cerveaux) et le coeur
C = N.coeur
K = C.classement
P = C.plan

# Prix notes dans le code de l'import (DeepSeek, dollars par million de jetons) : A REVERIFIER sur le site.
PRIX_LU, PRIX_ECRIT = 0.30, 1.20


def main():
    print("\n  LE PREMIER RANGEMENT DE SA BIBLIOTHEQUE DANS LE PLAN.\n")
    reste = K.a_ranger(tout=True)
    if not reste:
        print("  Toutes les fiches sont deja rangees. Rien a faire.")
        print("  Le plan est ici : %s" % P.F_PLAN_LISIBLE)
        return
    car = sum(len(f.get("texte", "")) for f in reste)
    lots = len(K._lots(reste))
    lu = (car + lots * 15000) / 3.5 / 1e6          # le texte des fiches + le plan et les consignes a chaque lot
    ecrit = lots * 1500 / 1e6
    print("  Fiches pas encore rangees : %d (%d caracteres), en %d lot(s)." % (len(reste), car, lots))
    print("  Prix estime (DeepSeek, prix du code a reverifier) : environ %.2f $, plus les divisions des tiroirs"
          " et le calcul du sens chez Google (presque rien)." % (lu * PRIX_LU + ecrit * PRIX_ECRIT))
    if input("\n  Tape OUI (en majuscules) pour ranger : ").strip() != "OUI":
        print("  Rien n'a ete fait.")
        return
    total = {"rangees": 0, "divisions": 0}
    while True:
        st = K.ranger_le_neuf(tout=True, lots_max=5, dire=lambda t: print("   ", t))
        total["rangees"] += st["rangees"]
        total["divisions"] += st["divisions"]
        for p in st["pannes"]:
            print("  PANNE : %s" % p)
        if not st["rangees"] and not st["divisions"]:
            break
        print("  ... %d fiche(s) rangee(s) jusqu'ici, %d encore a ranger." % (total["rangees"], st["reste"]))
        if not st["reste"]:
            break
    reste = K.a_ranger(tout=True)
    print("\n  FINI : %d fiche(s) rangee(s), %d tiroir(s) divise(s). %d fiche(s) pas rangee(s)%s."
          % (total["rangees"], total["divisions"], len(reste),
             (" (relance plus tard : il reprendra)" if reste else "")))
    print("  Le plan, lisible au Bloc-notes : %s" % P.F_PLAN_LISIBLE)


if __name__ == "__main__":
    main()
