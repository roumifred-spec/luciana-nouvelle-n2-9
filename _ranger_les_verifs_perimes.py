# -*- coding: utf-8 -*-
"""RANGER LES VIEUX SCRIPTS DE CONTROLE PERIMES (chantier du 06/10/2026, v121).

LE PROBLEME, CONSTATE DANS LES FICHIERS ET PAS RACONTE : trois scripts de controle de la
racine du depot cherchent un programme qui n'existe plus,
    C:\\Users\\Fred\\Desktop\\luciana_v91\\luciana_v91\\luciana.py
donc ils sortent un FAUX ROUGE a chaque recuperation de code :
    _verif_v95.py (ligne 29), _verif_v94.py (ligne 23), _verif_v93.py (ligne 15).

CE QUE FAIT CE SCRIPT, ET RIEN DE PLUS :
  - il deplace ces trois fichiers de la racine vers le sous-dossier archives_verif/ ;
  - avec "git mv" si git est disponible (l'historique suit le fichier), sinon avec un
    deplacement de fichier normal (os.replace) ;
  - IL N'EFFACE RIEN, JAMAIS. Il refuse d'ecraser un fichier deja present dans
    archives_verif/, et il ne touche a aucun autre fichier du depot.
  - il ne touche a AUCUN dossier en dehors du depot : ni C:\\Users\\Fred\\Luciana, ni
    C:\\Users\\Fred\\Lumi, ni C:\\Users\\Fred\\Desktop\\Lumi_appli, ni
    C:\\Users\\Daniela\\Luminita, ni le programme en service luciana_v96.

POURQUOI UN SCRIPT ET PAS UN DEPLACEMENT DIRECT : dans la session qui a prepare ce
chantier, le bac a sable a REFUSE tout deplacement, toute copie et toute suppression de
fichier (Copy-Item, Move-Item, cp, rm, New-Item ont tous ete bloques), et le lancement de
python n'a pas ete autorise. Le rangement n'a donc PAS pu etre fait dans cette session :
c'est dit franchement, et voici le script qui le fait en une commande.

A LANCER, dans le dossier du depot :
    python _ranger_les_verifs_perimes.py

L'EQUIVALENT A LA MAIN (Windows, dans le dossier du depot) :
    git mv _verif_v93.py archives_verif\\_verif_v93.py
    git mv _verif_v94.py archives_verif\\_verif_v94.py
    git mv _verif_v95.py archives_verif\\_verif_v95.py
"""
import os
import shutil
import subprocess
import sys

# LA LISTE, ET SEULEMENT CELLE-LA. Chaque entree : (nom du fichier, pourquoi il est perime).
A_RANGER = [
    ("_verif_v93.py", "chemin en dur vers luciana_v91 (ligne 15) : dossier disparu"),
    ("_verif_v94.py", "chemin en dur vers luciana_v91 (ligne 23) : dossier disparu"),
    ("_verif_v95.py", "chemin en dur vers luciana_v91 (ligne 29) : dossier disparu"),
]
DOSSIER_ARCHIVES = "archives_verif"


def git_marche(ici):
    """Vrai si git repond ici. On ne fait aucune hypothese : on essaie, pour de vrai."""
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"],
                                cwd=ici, stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False


def main():
    ici = os.path.dirname(os.path.abspath(__file__))
    archives = os.path.join(ici, DOSSIER_ARCHIVES)
    if not os.path.isdir(archives):
        os.makedirs(archives)
        print("Dossier cree : %s" % DOSSIER_ARCHIVES)

    avec_git = git_marche(ici)
    print("git utilisable ici : %s" % ("OUI (git mv)" if avec_git else "NON (deplacement simple)"))
    print("")

    deplaces, deja, absents, rates = [], [], [], []
    for nom, pourquoi in A_RANGER:
        source = os.path.join(ici, nom)
        cible = os.path.join(archives, nom)
        if os.path.exists(cible):
            # ON N'ECRASE JAMAIS. S'il y a deja une archive, on la laisse tranquille.
            deja.append(nom)
            print("DEJA RANGE : %s (archives_verif/%s existe) -- je n'y touche pas." % (nom, nom))
            continue
        if not os.path.isfile(source):
            absents.append(nom)
            print("PAS A LA RACINE : %s -- rien a faire." % nom)
            continue
        fait = False
        if avec_git:
            try:
                subprocess.check_output(["git", "mv", nom, "%s/%s" % (DOSSIER_ARCHIVES, nom)],
                                        cwd=ici, stderr=subprocess.STDOUT)
                fait = True
            except Exception as ex:
                print("   (git mv a refuse pour %s : %s -- j'essaie le deplacement simple)"
                      % (nom, str(ex)[:150]))
        if not fait:
            try:
                shutil.move(source, cible)
                fait = True
            except Exception as ex:
                rates.append((nom, str(ex)[:200]))
                print("ECHEC : %s n'a PAS pu etre deplace (%s)" % (nom, str(ex)[:200]))
        if fait:
            deplaces.append(nom)
            print("RANGE : %s -> %s/%s   (%s)" % (nom, DOSSIER_ARCHIVES, nom, pourquoi))

    print("")
    print("=" * 72)
    print("RESULTAT : %d range(s), %d deja range(s), %d absent(s), %d echec(s)"
          % (len(deplaces), len(deja), len(absents), len(rates)))
    # LA PREUVE, PAS LA PROMESSE : on verifie que chaque fichier est bien la ou on le dit.
    for nom, _p in A_RANGER:
        a_la_racine = os.path.isfile(os.path.join(ici, nom))
        dans_archives = os.path.isfile(os.path.join(archives, nom))
        print("   %-18s racine: %-3s   archives_verif: %-3s"
              % (nom, "OUI" if a_la_racine else "non", "OUI" if dans_archives else "non"))
    print("RIEN N'A ETE SUPPRIME : les fichiers sont deplaces, pas effaces.")
    print("=" * 72)
    return 1 if rates else 0


if __name__ == "__main__":
    sys.exit(main())
