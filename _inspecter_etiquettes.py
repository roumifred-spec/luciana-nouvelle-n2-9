# -*- coding: utf-8 -*-
"""_inspecter_etiquettes.py — REGARDER LES ETIQUETTES DE L'ARCHIVISTE, SANS RIEN TOUCHER.

A QUOI CA SERT : voir, sur du reel, ce que l'archiviste a ecrit dans
C:\\Users\\Fred\\Luciana\\etiquettes_essai.jsonl : combien d'etiquettes, de quelle source, quels
statuts, et a quoi ressemble une etiquette. C'est l'outil qui a servi a constater, avant de coder
le bibliothecaire de la v134, que les lignes de source 'carnet' sont les seules dont l'identifiant
designe un TIROIR (les lignes 'bibliotheque' designent un fichier .md).

CE SCRIPT EST EN LECTURE SEULE. Il ouvre le fichier, il compte, il affiche, il referme. Il n'ecrit
rien, ne cree rien, ne modifie rien -- ni dans C:\\Users\\Fred\\Luciana, ni ailleurs.

    python _inspecter_etiquettes.py
"""
import collections
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

F = os.path.join(os.path.expanduser("~"), "Luciana", "etiquettes_essai.jsonl")

if not os.path.isfile(F):
    print("PAS D'ETIQUETTES : %s n'existe pas." % F)
    print("Ce n'est pas une panne : le bibliothecaire de la v134 retombe alors sur le")
    print("fonctionnement de la v133. C'est le filet, et il est voulu.")
    sys.exit(0)

L = []
abimees = 0
with io.open(F, encoding="utf-8") as f:
    for ligne in f:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            L.append(json.loads(ligne))
        except Exception:
            abimees += 1

print("fichier    : %s" % F)
print("etiquettes : %d  (lignes abimees, ignorees : %d)" % (len(L), abimees))
print("sources    : %s" % dict(collections.Counter(x.get("source") for x in L)))
print("statuts    : %s" % dict(collections.Counter(x.get("statut") for x in L)))
print("")
print("LES TIROIRS (source 'carnet') : ce sont les SEULS que le bibliothecaire utilise,")
print("parce que leur champ 'tiroir' est le nom d'un carnet de Fred.")
carnets = [x for x in L if x.get("source") == "carnet"]
print("  %d tiroir(s) etiquete(s)." % len(carnets))
for x in carnets:
    print("   - %-50s statut=%-12s resume=%s"
          % (str(x.get("tiroir"))[:50], x.get("statut"), str(x.get("resume"))[:60]))
print("")
a_trancher = [x for x in carnets if x.get("statut") == "a trancher"]
print("DEFAUT CONNU DE L'ARCHIVISTE : %d tiroir(s) sur %d ont un statut 'a trancher'."
      % (len(a_trancher), len(carnets)))
print("Le bibliothecaire ne les fait PAS reculer : 'a trancher' n'est pas 'remplace'.")
print("C'est a Fred de trancher, pas au programme.")
