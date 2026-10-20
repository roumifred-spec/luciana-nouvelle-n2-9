# -*- coding: utf-8 -*-
"""OUTIL JETABLE DU CHANTIER - CE FICHIER PEUT ETRE SUPPRIME SANS RIEN CASSER.
Il sort, sur le disque, le luciana.py du commit 5f8bd4e (la v89), pour pouvoir relire le code
d'ecriture de la bibliotheque (biblio_ranger, _slug, _trouver). Ce code a ete repris tel quel
dans le chantier du rangement de la journee : il n'y a plus rien a extraire, c'est fait.
Il n'ecrit RIEN dans la memoire de Fred et ne touche pas a luciana.py.
"""
import os
import subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
sortie = subprocess.run(["git", "show", "5f8bd4e:luciana.py"], cwd=ICI,
                        capture_output=True).stdout.decode("utf-8", "replace")
dest = os.path.join(ICI, "_v89_extrait.py")
with open(dest, "w", encoding="utf-8") as f:
    f.write(sortie)
print("ecrit : %s (%d lignes)" % (dest, len(sortie.splitlines())))
