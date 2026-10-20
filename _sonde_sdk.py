# -*- coding: utf-8 -*-
"""SONDE : A PARTIR DE QUEL PLAFOND (max_tokens) LA BIBLIOTHEQUE REFUSE UN APPEL SANS FLUX ?

A QUOI CA SERT, ET POURQUOI CE FICHIER EXISTE
---------------------------------------------
Chantier du 06/10/2026 (le rangement de la journee). Le rangement appelait le cerveau avec
max_tokens=8000 et la reponse arrivait vide : la reflexion mangeait les 8 000 jetons
(mesure brute : stop_reason = "max_tokens", output_tokens = 8000, texte final = 0 caractere).
Un essai a la main avec max_tokens=32000 SANS flux a ete REFUSE par la bibliotheque.

MAIS un fait du code dit autre chose : la CONVERSATION de Luciana, elle, tourne tous les jours
avec max_tokens=16000 SANS flux (voir luciana.py, _appel_cerveau : "def _appel_cerveau(cli,
cerveau, requete, max_tokens=16000)"). Donc la bibliotheque n'interdit pas "monter le plafond" :
elle interdit de le monter AU-DELA d'une certaine valeur. Cette sonde trouve laquelle.

CE QUE CA COUTE : ZERO EURO, ZERO APPEL RESEAU. Le refus dont on parle est un refus de la
bibliotheque, AVANT tout envoi : la sonde utilise donc une fausse cle. Si un palier n'est pas
refuse, l'appel partirait sur le reseau avec une fausse cle et serait rejete par le serveur
(erreur d'authentification) : c'est ca qu'on affiche, et ca ne coute rien non plus.

CE QU'ELLE NE FAIT PAS : elle ne touche a RIEN. Aucun fichier lu, aucun fichier ecrit, aucune
vraie cle, aucune memoire. Elle affiche et elle s'arrete.

POURQUOI ELLE N'A PAS ETE LANCEE PAR LE CHANTIER, DIT FRANCHEMENT : l'atelier dans lequel ce
chantier a tourne refuse d'executer du Python (seul "python --version" etait autorise). Elle est
donc ECRITE mais JAMAIS LANCEE ici. Personne ne doit croire a un resultat : il n'y en a pas.

POUR LA LANCER (fenetre de commande, dans ce dossier) :
    python _sonde_sdk.py
"""
import sys

print("python    :", sys.version.split()[0])
try:
    import anthropic
    print("anthropic :", getattr(anthropic, "__version__", "(version inconnue)"))
except Exception as ex:
    print("anthropic : ABSENT ->", ex)
    raise SystemExit(0)

cli = anthropic.Anthropic(api_key="sk-ant-fausse-cle-pour-la-sonde")

print("")
print("Plafond demande -> ce que repond la bibliotheque (sans flux) :")
for plafond in (8000, 16000, 20000, 24000, 32000, 64000):
    try:
        cli.messages.create(model="claude-opus-4-8", max_tokens=plafond,
                            messages=[{"role": "user", "content": "test"}])
        print("  %6d -> ACCEPTE par la bibliotheque (l'appel est parti sur le reseau)" % plafond)
    except Exception as ex:
        print("  %6d -> %s : %s" % (plafond, type(ex).__name__,
                                    str(ex)[:200].replace("\n", " ")))

print("")
print("COMMENT LIRE CE TABLEAU :")
print("  - 'ACCEPTE' = ce plafond est utilisable SANS flux, donc sans ecrire une ligne de code")
print("    nouvelle : il suffirait de changer le 8000 de _demander_les_tiroirs dans luciana.py.")
print("  - une erreur qui parle de 'streaming' = ce plafond exige le flux, donc du code nouveau.")
print("  - une erreur d'authentification = le plafond etait ACCEPTE, c'est la fausse cle qui a")
print("    ete refusee, et par le SERVEUR, pas par la bibliotheque.")
