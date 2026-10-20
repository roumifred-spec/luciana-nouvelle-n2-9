# -*- coding: utf-8 -*-
"""LE CHIFFRE AVANT / APRES DES CONSIGNES, ET RIEN D'AUTRE.

Ce petit script ne contrôle rien et ne pose rien : il MESURE, sur le VRAI carnet de Fred
(C:\\Users\\Fred\\Luciana\\consignes.jsonl, lu en LECTURE SEULE), combien de caracteres de
consignes partent au cerveau a chaque message :
  - AVANT  = le comportement de la v99 (_construire_consignes_v99) ;
  - APRES  = le carnet range par sujet de la v107 (_construire_consignes_par_sujet).
Les deux sont mesures sur le MEME carnet, a la MEME seconde : c'est donc comparable.

Le controle complet du chantier, lui, c'est _verif_v107.py (c'est celui-la qu'il faut lire
avant de valider). Celui-ci sert juste a donner le chiffre, vite, sans tout derouler.

POUR LE LANCER :
    python _mesure_consignes_avant.py
"""
import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
CIBLE = os.path.join(ICI, "luciana.py")

try:
    spec = importlib.util.spec_from_file_location("luciana_mesure", CIBLE)
    L = importlib.util.module_from_spec(spec)
    sys.modules["luciana_mesure"] = L
    spec.loader.exec_module(L)          # le fichier a un garde __main__ : rien ne demarre
except Exception as ex:
    print("Je n'ai pas pu charger %s : %s" % (CIBLE, str(ex)[:300]))
    sys.exit(1)

try:
    actives = L.consignes_actives()
except Exception as ex:
    print("Je n'ai pas pu lire le carnet de consignes : %s" % str(ex)[:300])
    sys.exit(1)

print("=" * 92)
print("LE CHIFFRE AVANT / APRES  (mesure sur le vrai carnet de Fred, rien n'est ecrit)")
print("=" * 92)
print("carnet lu           : %s" % L.FICHIER_CONSIGNES)
print("consignes actives   : %d" % len(actives))
print("dont capitales      : %d" % sum(1 for c in actives if L._est_capitale(c)))
print("plafond             : %d car. par message" % L.CONSIGNES_CARACTERES_MAX)


def numeros_presents(texte):
    """Les numeros de consigne dont il reste AU MOINS une trace dans ce qui part au cerveau."""
    import re
    vus = set()
    for ligne in (texte or "").splitlines():
        m = re.match(r"- n(\d+)", ligne.strip())
        if m:
            vus.add(int(m.group(1)))
    return vus


tous = set(c["numero"] for c in actives)

print("-" * 92)
try:
    t99, m99 = L._construire_consignes_v99()
    perdues = sorted(tous - numeros_presents(t99))
    print("AVANT (v99) :")
    print("   caracteres de consignes envoyes : %d" % m99.get("contenu", 0))
    print("   capitales donnees EN ENTIER     : %d" % m99.get("capitales", 0))
    print("   capitales SACRIFIEES            : %d  -> n%s"
          % (m99.get("capitales_refusees", 0),
             ", n".join(str(n) for n in m99.get("refusees") or []) or "(aucune)"))
    print("   consignes dont il ne reste AUCUNE trace : %d  -> n%s"
          % (len(perdues), ", n".join(str(n) for n in perdues) or "(aucune)"))
except Exception as ex:
    print("AVANT (v99) : je n'ai pas pu mesurer -- %s" % str(ex)[:300])

print("-" * 92)
try:
    phrase = " ".join(sys.argv[1:]) or ("Remets la croix sur les pastilles et repare la "
                                       "validation en double.")
    print("APRES (v107, range par sujet) -- phrase d'essai : %r" % phrase)
    t107, m107 = L._construire_consignes_par_sujet(phrase)
    perdues = sorted(tous - numeros_presents(t107))
    print("   caracteres de consignes envoyes : %d" % m107.get("contenu", 0))
    print("   NOYAU donne en entier           : n%s"
          % (", n".join(str(n) for n in m107.get("noyau") or []) or "(aucun)"))
    print("   DETAIL par sujet                : n%s"
          % (", n".join(str(n) for n in m107.get("par_sujet") or []) or "(aucun)"))
    print("   INDEX (toutes les consignes)    : %d car." % m107.get("index", 0))
    print("   consignes dont il ne reste AUCUNE trace : %d  -> n%s"
          % (len(perdues), ", n".join(str(n) for n in perdues) or "(aucune)"))
except Exception as ex:
    print("APRES (v107) : je n'ai pas pu mesurer -- %s" % str(ex)[:300])
print("=" * 92)
