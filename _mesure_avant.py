# -*- coding: utf-8 -*-
"""Mesure, sans rien executer du programme (lecture par AST), le poids du texte FIXE."""
import ast, io, json, sys, os

CHEMIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "luciana.py")
src = io.open(CHEMIN, encoding="utf-8").read()
arbre = ast.parse(src)

valeurs = {}
for n in arbre.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        nom = n.targets[0].id
        if nom in ("PERSONNALITE", "TOOLS", "MEMOIRE_CARACTERES_MAX", "CARNETS_DETAIL_MINIMUM",
                   "CARNETS_DETAIL_MAX", "OUTILS_WEB_LOCAUX"):
            try:
                valeurs[nom] = ast.literal_eval(n.value)
            except Exception as e:
                valeurs[nom] = "NON LISIBLE : %s" % e

print("PERSONNALITE :", len(valeurs.get("PERSONNALITE") or ""), "caracteres")
tools = valeurs.get("TOOLS")
if isinstance(tools, list):
    envoye = json.dumps(tools, ensure_ascii=False)
    print("TOOLS : %d outils, %d caracteres (JSON envoye a l'API)" % (len(tools), len(envoye)))
    desc = sum(len(o.get("description", "")) for o in tools)
    sch = sum(len(json.dumps(o.get("input_schema", {}), ensure_ascii=False)) for o in tools)
    print("   dont descriptions : %d car. | schemas : %d car." % (desc, sch))
    print("   les 12 plus grosses descriptions :")
    for o in sorted(tools, key=lambda o: -len(o.get("description", "")))[:12]:
        print("     %-28s %6d" % (o.get("name"), len(o.get("description", ""))))
else:
    print("TOOLS :", tools)
print("MEMOIRE_CARACTERES_MAX :", valeurs.get("MEMOIRE_CARACTERES_MAX"))
print("CARNETS_DETAIL_MINIMUM :", valeurs.get("CARNETS_DETAIL_MINIMUM"))
