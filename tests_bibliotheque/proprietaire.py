# -*- coding: utf-8 -*-
"""ESSAI : LE NOM DU PROPRIETAIRE NE VIT QU'A UN SEUL ENDROIT (le reglage), et aucun prenom n'est en dur.

Faux cerveau, faux Google, dossier jetable. Ca ne prouve PAS que le sens de ses reponses est bon ;
ca prouve que le PROGRAMME ne laisse echapper aucun prenom et ne perd jamais le nom ecrit.
"""
import os, sys, io, re, time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import faux

# Les SEULES occurrences de « fred » admises dans nouvelle/ : des noms qui appartiennent a l'ANCIEN
# programme (luciana.py, qu'on ne touche pas) et le marqueur deja ecrit dans les vieux journaux.
TOLERES = ("ArretDemandeParFred", "_arret_si_fred_a_dit_stop", "fredAParle", "dite par Fred")


def sans_les_toleres(ligne):
    for t in TOLERES:
        ligne = ligne.replace(t, "")
    return ligne


def essai():
    c = faux.Compte("LE NOM DU PROPRIETAIRE")

    # ---------------------------------------------------------------- A. aucun prenom en dur
    c.oui("le reglages.json LIVRE part vierge (aucun nom dedans)",
          faux.reglage_proprietaire_livre() == "", repr(faux.reglage_proprietaire_livre()))

    restes = []
    for nom in sorted(os.listdir(faux.NOUVELLE)):
        if not nom.endswith((".py", ".txt", ".json")):
            continue
        for i, ligne in enumerate(io.open(os.path.join(faux.NOUVELLE, nom), encoding="utf-8",
                                          errors="replace").read().splitlines(), 1):
            if "fred" in sans_les_toleres(ligne).lower():
                restes.append("%s:%d" % (nom, i))
    c.oui("aucun prenom en dur dans nouvelle/ (hors noms de l'ancien programme)",
          not restes, " ".join(restes))

    co, _d = faux.monter("prop_jeton", "Thomas")
    c.oui("personnalite.txt porte le JETON, pas un prenom",
          "{proprietaire}" in co.personnalite() and "Fred" not in co.personnalite())
    c.oui("proprietaire() rend le nom du reglage", co.proprietaire() == "Thomas", co.proprietaire())
    c.oui("le jeton est remplace dans un texte",
          co.avec_le_nom("bonjour {proprietaire}") == "bonjour Thomas")
    c.oui("l'etiquette d'une regle porte le nom", co.nature_en_clair("regle") == "Regle de Thomas",
          co.nature_en_clair("regle"))

    co, _d = faux.monter("prop_vide", None)
    c.oui("reglage vide -> un mot neutre, JAMAIS un prenom",
          co.proprietaire() == "le proprietaire", co.proprietaire())
    c.oui("reglage vide -> le jeton devient le mot neutre",
          co.avec_le_nom("bonjour {proprietaire}") == "bonjour le proprietaire")

    # ---------------------------------------------------------------- B. une mise a jour n'ecrase jamais
    co, d = faux.monter("prop_ecrire", None)
    ecrit, nom = co.poser_le_proprietaire("Anne")
    c.oui("sur un reglage vide : le nom est ecrit une fois", ecrit and nom == "Anne", (ecrit, nom))
    c.oui("et il est relu tout de suite", co.proprietaire() == "Anne", co.proprietaire())
    ecrit2, nom2 = co.poser_le_proprietaire("Bernard")
    c.oui("une mise a jour qui repasse par la : REFUSE d'ecraser",
          (not ecrit2) and nom2 == "Anne", (ecrit2, nom2))
    c.oui("le nom en place n'a pas bouge", co.proprietaire() == "Anne", co.proprietaire())
    ecrit3, _n = co.poser_le_proprietaire("")
    c.oui("un nom vide n'efface rien", (not ecrit3) and co.proprietaire() == "Anne", co.proprietaire())

    # une ligne « proprietaire »: "" dans le fichier ne remplace pas le nom connu du programme
    co.DEFAUT["proprietaire"] = "Anne"
    with io.open(co.F_REGLAGES, "w", encoding="utf-8") as f:
        f.write('{"proprietaire": ""}')
    c.oui("une ligne VIDE dans le fichier ne remplace jamais le nom connu",
          co.proprietaire() == "Anne", co.proprietaire())
    co.DEFAUT["proprietaire"] = ""

    # ---------------------------------------------------------------- C. rien ne fuit au cerveau
    co, d = faux.monter("prop_tour", "Thomas")
    faux.REPONSES.update({
        "comprendre": {"qui_parle": {"comment": "dit", "nouveau": "Thomas", "raison": "il signe"},
                       "de_qui": [], "de_quoi": "ou en est le dossier", "quand": "maintenant", "vital": False},
        "bibliothecaire": {"fiches": [{"n": 1, "pourquoi": "ca repond"}]},
        "relecture": {"regles": []},
        "conversation": "Voila.",
        "apprentissage": {"lecons": []},
        "journal_du_quotidien": {"gestes": []},
        "archiviste_rangement": {"fiches": []},
    })
    co.ecrire_fiche("regle", "Reponds court", "Reponds toujours en deux phrases.", source="essai")
    co.ecrire_fiche("souvenir", "Le dossier", "On a parle du dossier le 2 octobre.", source="essai")
    texte = co.repondre("C'est Thomas. Ou en est le dossier ?")
    time.sleep(2)
    parti = faux.tout_ce_qui_est_parti()
    c.oui("elle a repondu", texte.strip() == "Voila.", texte)
    c.oui("AUCUN jeton {proprietaire} n'est parti au cerveau", "{proprietaire}" not in parti,
          parti[max(0, parti.find("{proprietaire}") - 60):parti.find("{proprietaire}") + 60])
    c.oui("le nom du reglage, lui, est bien parti", "Thomas" in parti)
    etapes = sorted({e for e, _s, _c in faux.APPELS})
    c.oui("les quatre etapes ont bien tourne (comprendre, bibliothecaire, relecture, conversation)",
          {"comprendre", "bibliothecaire", "relecture", "conversation"} <= set(etapes), etapes)
    for etape in ("bibliothecaire", "relecture", "comprendre", "apprentissage"):
        textes = faux.appels_de(etape)
        c.oui("la consigne de « %s » ne contient aucun prenom en dur" % etape,
              textes and not re.search(r"\bfred\b", (textes[0][0] + textes[0][1]).lower()),
              etape)

    outils = co.outils_du_tour("deepseek-flash")
    desc = " ".join(str(o.get("description") or "") for o in outils)
    c.oui("les descriptions des outils portent le nom, pas le jeton",
          ("Thomas" in desc) and ("{proprietaire}" not in desc))

    co.ecrire_lisible()
    lisible = io.open(co.F_LISIBLE, encoding="utf-8").read()
    c.oui("« MA BIBLIOTHEQUE (lisible).txt » ne montre pas le jeton", "{proprietaire}" not in lisible)
    c.oui("... et montre bien le nom", "Thomas" in lisible)

    # le journal du quotidien lisible
    co.quotidien.noter_le_vital("J'ai pris mon cachet a 8h.", "2026-10-20 10:00")
    faux.REPONSES["journal_du_quotidien"] = {"gestes": [{"quoi": "pris son cachet", "fait": True,
                                                         "jour": "aujourd'hui", "heure": "08:00"}]}
    co.quotidien.noter_le_vital("J'ai pris mon cachet a 8h.", "2026-10-20 10:00")
    j = io.open(co.quotidien._f_lisible(), encoding="utf-8").read()
    c.oui("« MON JOURNAL DU QUOTIDIEN.txt » ne montre pas le jeton", "{proprietaire}" not in j, j[:200])

    return c.fin()


if __name__ == "__main__":
    justes, total = essai()
    sys.exit(0 if justes == total else 1)
