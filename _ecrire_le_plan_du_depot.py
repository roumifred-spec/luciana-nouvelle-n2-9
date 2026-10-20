# -*- coding: utf-8 -*-
# =====================================================================
#  REECRIRE LA COPIE DE TRAVAIL DU PLAN (plan_bibliotheque.json, dans le depot)
#
#  A QUOI CA SERT : plan_bibliotheque.json, dans le depot, est une COPIE DE TRAVAIL -- celle que
#  Fred relit. Le VRAI plan, celui dont Luciana se sert, est C:\Users\Fred\Luciana\plan_bibliotheque.json,
#  et il se refait tout seul au demarrage a partir de la semence qui est dans luciana.py.
#  Ce petit programme regenere la copie du depot a partir de la MEME semence, pour que les deux ne
#  partent jamais chacune de leur cote. Il est a relancer apres chaque chantier qui touche au plan.
#
#  CE QU'IL NE FAIT PAS, ET C'EST VOLONTAIRE :
#    - il ne touche a AUCUN fichier de C:\Users\Fred\Luciana (ni carnet, ni souvenirs, ni le vrai
#      plan) : il n'ecrit QUE plan_bibliotheque.json, ici, dans le depot ;
#    - il n'appelle aucun cerveau : zero jeton, zero centime.
#
#  COMMENT ON LE LANCE :  python _ecrire_le_plan_du_depot.py
# =====================================================================
import io
import json
import os
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import luciana as L                                                          # noqa: E402

CIBLE = os.path.join(ICI, "plan_bibliotheque.json")

# On fabrique un carnet qui porte EXACTEMENT les noms de la semence (les noms reels des carnets de
# Fred, releves le 06/10/2026). Le vrai carnet.json de Fred n'est ni lu ni ecrit ici.
CARNET = dict((nom, {"etat": "", "maj": ""}) for nom in L.PLAN_BIBLIO_SEMENCE)

# On detourne le plan vers la copie du depot AVANT de regenerer : rien n'est ecrit ailleurs.
L.FICHIER_PLAN_BIBLIO = CIBLE
# Le journal part dans un dossier jetable : ce petit programme ne laisse aucun dechet dans le depot.
L.FICHIER_JOURNAL_TIROIRS = os.path.join(tempfile.mkdtemp(prefix="plan_depot_"), "journal.jsonl")

if os.path.exists(CIBLE):
    os.remove(CIBLE)                      # on repart de la semence, pas d'un vieux plan a trous

plan, ajoutes, disparus, sans_mots = L.regenerer_plan_biblio(carnet=CARNET, ecrire=False)

plan["a_lire_avant_de_toucher"] = [
    "CE FICHIER EST LE PLAN DE LA BIBLIOTHEQUE DE LUCIANA. C'est lui, et lui seul, qui decide "
    "quels carnets sont mis sous ses yeux a chaque message de Fred -- ET dans quel tiroir le "
    "rangement du soir a le droit d'ecrire. Depuis le 06/10/2026 il commande les DEUX SENS.",
    "LES NOMS SONT LES NOMS EXACTS des carnets de Fred. Le programme n'en invente JAMAIS un. "
    "Le 'titre' et la 'categorie' sont des CHAMPS EN PLUS : ils n'ont RIEN renomme.",
    "CATEGORIE -> SOUS-TIROIRS : la bibliotheque est hierarchique. La categorie, c'est le rayon ; "
    "le tiroir, c'est le sous-tiroir. (La metaphore de Fred : on tape 'voiture' sur une "
    "marketplace et on recoit 50 000 annonces, donc on ajoute marque, cylindree, couleur.)",
    "TRI A DEUX CLES : 'mots' = par MOT (un mot entier vaut 3 points, une ressemblance de debut "
    "de mot en vaut 1) ; 'sujet' = par SUJET (2 points). Le sujet n'ouvre JAMAIS un tiroir tout "
    "seul : il ne fait que departager ceux qu'un vrai mot a deja designes.",
    "'principal': true = le tiroir GENERAL de sa categorie. C'est lui qui repond quand Fred nomme "
    "la categorie toute seule ('Luminita') -- et Luciana dit quand meme qu'il y avait plusieurs "
    "candidats.",
    "ETAT : 'actif' = il peut sortir des qu'un mot-cle est reconnu. 'dort' = il ne sort QUE si "
    "Fred nomme un de ses mots-cles exactement. 'clos' = il ne sort JAMAIS tout seul.",
    "CE FICHIER EST UNE COPIE DE TRAVAIL, dans le depot. Le vrai plan, celui que Luciana utilise, "
    "est C:\\Users\\Fred\\Luciana\\plan_bibliotheque.json : il se cree tout seul au premier "
    "demarrage a partir de la semence qui est dans luciana.py.",
    "POUR REFAIRE CETTE COPIE :  python _ecrire_le_plan_du_depot.py",
]

with open(CIBLE, "w", encoding="utf-8") as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("=" * 78)
print("COPIE DE TRAVAIL DU PLAN REECRITE : %s" % CIBLE)
print("Tiroirs : %d" % len(plan["tiroirs"]))
sans_categorie = [t["nom"] for t in plan["tiroirs"] if not (t.get("categorie") or "").strip()]
print("Tiroirs SANS categorie : %d%s" % (len(sans_categorie),
                                         ("  -> " + ", ".join(sans_categorie[:5])) if sans_categorie else ""))
print("Tiroirs SANS mot-cle   : %d" % len(sans_mots))
print("Noms de PLAN_CATEGORIES inconnus de la semence : %d%s"
      % (len(L.PLAN_CATEGORIES_INCONNUES),
         ("  -> " + ", ".join(L.PLAN_CATEGORIES_INCONNUES)) if L.PLAN_CATEGORIES_INCONNUES else ""))
print("=" * 78)
sys.exit(0 if not sans_categorie and not L.PLAN_CATEGORIES_INCONNUES else 1)
