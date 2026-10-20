# -*- coding: utf-8 -*-
"""_mesure_v135_honnetete_avant.py -- LA MESURE AVANT DE TOUCHER A QUOI QUE CE SOIT.

A QUOI CA SERT : dire, en caracteres REELS lus sur le disque, ce que pesent
  - PERSONNALITE_V107 (la longue, celle qui n'est plus envoyee par defaut),
  - PERSONNALITE_COURTE (celle qui part VRAIMENT a chaque message),
  - la CLAUSE D'HONNETETE telle qu'elle est ecrite dans PERSONNALITE_V107.
Et dire si la clause est deja presente, ou non, dans PERSONNALITE_COURTE.

CE SCRIPT NE MODIFIE RIEN. Il lit luciana.py comme du texte, il ne l'importe pas
(l'importer lancerait le serveur). Il compte, il affiche, c'est tout.

    python _mesure_v135_honnetete_avant.py
"""
import ast
import io
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER_PY = os.path.join(ICI, "luciana.py")

DEBUT_CLAUSE = "REGLE D'HONNETETE (elle vaut pour TOI"
FIN_CLAUSE = "\n\nTU ES LE CHEF D'ORCHESTRE"


def litteraux(chemin):
    """Rend {nom: texte} pour les affectations du genre  NOM = \"\"\"...\"\"\"  au premier niveau."""
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as f:
        source = f.read()
    arbre = ast.parse(source, chemin)
    trouves = {}
    for noeud in arbre.body:
        if isinstance(noeud, ast.Assign) and isinstance(noeud.value, ast.Constant) \
                and isinstance(noeud.value.value, str):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name):
                    trouves[cible.id] = noeud.value.value
    return trouves


def main():
    if not os.path.isfile(FICHIER_PY):
        print("INTROUVABLE : %s" % FICHIER_PY)
        return 1
    textes = litteraux(FICHIER_PY)
    longue = textes.get("PERSONNALITE_V107")
    courte = textes.get("PERSONNALITE_COURTE")
    if longue is None or courte is None:
        print("PAS TROUVE les deux personnalites dans %s." % FICHIER_PY)
        print("  PERSONNALITE_V107 : %s" % ("trouvee" if longue else "PAS TROUVEE"))
        print("  PERSONNALITE_COURTE : %s" % ("trouvee" if courte else "PAS TROUVEE"))
        return 1

    debut = longue.find(DEBUT_CLAUSE)
    fin = longue.find(FIN_CLAUSE, debut) if debut >= 0 else -1
    clause = longue[debut:fin].rstrip() if (debut >= 0 and fin > debut) else ""

    print("")
    print("MESURE AVANT -- v135, la regle d'honnetete (lu sur le disque)")
    print("  %s" % FICHIER_PY)
    print("")
    print("  PERSONNALITE_V107   (la longue)        : %7d caracteres" % len(longue))
    print("  PERSONNALITE_COURTE (celle qui part)   : %7d caracteres" % len(courte))
    print("  LA CLAUSE D'HONNETETE                  : %7d caracteres" % len(clause))
    print("")
    print("  La clause est-elle deja dans la courte ? %s"
          % ("OUI" if clause and clause in courte else "NON"))
    print("  La clause est-elle bien dans la longue ? %s"
          % ("OUI" if clause and clause in longue else "NON"))
    print("")
    if clause:
        print("LA CLAUSE, MOT POUR MOT, TELLE QU'ELLE EST DANS PERSONNALITE_V107 :")
        print("-" * 100)
        print(clause)
        print("-" * 100)
    else:
        print("ATTENTION : la clause n'a PAS ete retrouvee dans PERSONNALITE_V107.")
        return 1
    print("")
    print("  Si on ajoute la clause a la courte : %d + 2 + %d = %d caracteres"
          % (len(courte), len(clause), len(courte) + 2 + len(clause)))
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
