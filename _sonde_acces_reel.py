# -*- coding: utf-8 -*-
"""SONDE JETABLE DU CHANTIER DU 06/10/2026 -- A SUPPRIMER SANS REGRET.

Elle n'a servi qu'a une chose : savoir si Python, depuis la session de travail, pouvait LIRE
les vrais fichiers de C:\\Users\\Fred\\Luciana. La reponse n'a pas pu etre obtenue : le
lancement de python a ete refuse dans cette session. Elle est laissee ici parce que le bac a
sable a aussi refuse de la supprimer. Elle ne lit rien, n'ecrit rien, n'efface rien, et
aucun autre fichier du depot ne l'appelle.

    del _sonde_acces_reel.py
"""
import os

CHEMINS = (r"C:\Users\Fred\Luciana\rangement_journee.jsonl",
           r"C:\Users\Fred\Luciana\journee_rangee.json",
           r"C:\Users\Fred\Luciana\plan_bibliotheque.json")

for chemin in CHEMINS:
    try:
        with open(chemin, "r", encoding="utf-8", errors="replace") as f:
            n = sum(1 for _ in f)
        print("LISIBLE   %-32s %d ligne(s), %d octets"
              % (os.path.basename(chemin), n, os.path.getsize(chemin)))
    except Exception as ex:
        print("REFUSE    %-32s %s" % (os.path.basename(chemin), str(ex)[:160]))
