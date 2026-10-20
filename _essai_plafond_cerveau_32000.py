# -*- coding: utf-8 -*-
"""_essai_plafond_cerveau_32000.py — LA MESURE QUI MANQUE, POUR UN SEUL CHIFFRE.

LA QUESTION, ET RIEN D'AUTRE : est-ce qu'on peut demander max_tokens=32000 au cerveau SANS flux
(sans "streaming"), comme Luciana appelle le cerveau aujourd'hui ?

POURQUOI CETTE QUESTION : Fred a demande de monter les max_tokens de 16 000 a 32 000. Mais
luciana.py dit ceci, noir sur blanc, a sa ligne ~17653 (c'est un releve DATE du 06/10/2026, pas
une supposition) :
    "On ne le monte pas plus haut : un plafond de 32 000 sans flux a ete REFUSE par la
     bibliotheque a l'essai du 06/10"
Or la CONVERSATION de Fred passe par le meme chemin, sans flux (cli.messages.create). Monter le
chiffre a l'aveugle, c'est donc risquer de casser TOUTE la conversation au lieu de la reparer.
On ne devine pas : on mesure.

CE QUE CA COUTE : quasiment rien. Si la bibliotheque refuse, elle refuse AVANT d'appeler le
service : zero centime. Si elle accepte, l'appel demande juste le mot "ok" : quelques jetons de
sortie sur le modele le moins cher. max_tokens est un PLAFOND, pas une commande : demander
32 000 ne fait pas ecrire 32 000 jetons.

CE QUE CA NE FAIT PAS : ca ne modifie AUCUN fichier. Ca lit la cle, ca passe un appel minuscule,
ca affiche le resultat.

A lancer depuis le dossier du programme :
    python _essai_plafond_cerveau_32000.py

PUIS : recopier les lignes affichees a Claude. C'est la reponse, sur du reel.
"""
import os
import sys

A_ESSAYER = [16000, 24000, 32000, 64000]
DOSSIER_PRIVE = os.path.join(os.path.expanduser("~"), "Luciana")


def lire_la_cle():
    """La cle est dans le dossier PRIVE ~/Luciana, jamais dans le dossier du programme."""
    for nom in ("cle.txt", "cle_api.txt", "cle_claude.txt", "reglages.json"):
        chemin = os.path.join(DOSSIER_PRIVE, nom)
        if not os.path.isfile(chemin):
            continue
        try:
            with open(chemin, "r", encoding="utf-8", errors="replace") as f:
                brut = f.read()
        except Exception:
            continue
        if nom.endswith(".json"):
            import json
            try:
                d = json.loads(brut)
            except Exception:
                continue
            for k in ("cle", "cle_api", "api_key", "anthropic_api_key"):
                if str(d.get(k) or "").startswith("sk-"):
                    return str(d[k]).strip(), chemin
        else:
            for ligne in brut.splitlines():
                if ligne.strip().startswith("sk-"):
                    return ligne.strip(), chemin
    if str(os.environ.get("ANTHROPIC_API_KEY") or "").startswith("sk-"):
        return os.environ["ANTHROPIC_API_KEY"].strip(), "variable ANTHROPIC_API_KEY"
    return "", ""


def main():
    try:
        import anthropic
    except ImportError:
        print("La bibliotheque 'anthropic' n'est pas installee ici. Rien n'a ete essaye.")
        return 1
    print("Version de la bibliotheque anthropic : %s"
          % getattr(anthropic, "__version__", "inconnue"))

    cle, ou = lire_la_cle()
    if not cle:
        print("")
        print("JE N'AI PAS TROUVE LA CLE dans %s." % DOSSIER_PRIVE)
        print("Rien n'a ete essaye, et aucun fichier n'a ete touche.")
        print("Si tu veux lancer l'essai : colle la cle dans la variable ANTHROPIC_API_KEY,")
        print("ou dis-moi le nom exact du fichier qui la contient.")
        return 1
    print("Cle lue depuis : %s  (elle n'est PAS affichee ici)" % ou)

    cli = anthropic.Anthropic(api_key=cle)
    modele = "claude-haiku-4-5-20251001"   # le moins cher : l'essai porte sur le CHIFFRE, pas le modele
    print("Modele de l'essai : %s" % modele)
    print("")
    print("%-10s %-12s %s" % ("max_tokens", "RESULTAT", "CE QUE LA BIBLIOTHEQUE OU LE SERVICE A DIT"))
    print("-" * 100)
    resultats = []
    for plafond in A_ESSAYER:
        try:
            r = cli.messages.create(model=modele, max_tokens=plafond,
                                    messages=[{"role": "user", "content": "Reponds juste : ok"}])
            sortis = getattr(getattr(r, "usage", None), "output_tokens", "?")
            print("%-10d %-12s %s" % (plafond, "ACCEPTE", "reponse recue, %s jetons ecrits" % sortis))
            resultats.append((plafond, True, ""))
        except Exception as ex:
            msg = str(ex).replace("\n", " ")[:200]
            print("%-10d %-12s %s" % (plafond, "REFUSE", msg))
            resultats.append((plafond, False, msg))
    print("-" * 100)
    print("")
    acceptes = [p for p, ok, _ in resultats if ok]
    refuses = [p for p, ok, _ in resultats if not ok]
    if acceptes:
        print("LE PLUS HAUT PLAFOND ACCEPTE SANS FLUX : %d" % max(acceptes))
    if refuses:
        print("LE PLUS BAS PLAFOND REFUSE SANS FLUX   : %d" % min(refuses))
        print("")
        print("=> On ne peut donc PAS monter les max_tokens de Luciana au-dessus de %d"
              % max(acceptes or [0]))
        print("   sans changer la facon d'appeler le cerveau (passer en flux). Ce serait un NOUVEAU")
        print("   MECANISME : Fred l'a interdit dans ce chantier. C'est a lui de trancher.")
    else:
        print("=> 32 000 passe. Claude peut alors monter les deux max_tokens de 16 000 a 32 000")
        print("   en toute securite : il suffit de lui redonner CES lignes-ci.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
