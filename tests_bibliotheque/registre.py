# -*- coding: utf-8 -*-
"""ESSAI DU REGISTRE DES PERSONNES (faux cerveau) : les REGLES DU PROGRAMME, pas le sens.

On donne au programme ce que « comprendre » aurait deduit, et on verifie ce que le programme TRANCHE :
  - qui parle : suite refusee en nouvelle session, nom deja au registre -> pas de double, « prouve » n'existe pas ;
  - DE QUI ON PARLE : le meme comptage des homonymes que pour qui parle. Deux personnes du meme nom restent
    DEUX personnes : on ne fusionne jamais, on ne fabrique pas de double, et on POSE UNE QUESTION ;
  - l'import : la personne a qui est la memoire entre au registre (p1), role « proprietaire », « dit (import) ».
"""
import os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import faux


def deduit(numero="", nouveau="", comment="deduit", distingue="", raison=""):
    return {"numero": numero, "nouveau": nouveau, "comment": comment, "distingue": distingue, "raison": raison}


def essai():
    c = faux.Compte("LE REGISTRE DES PERSONNES")
    co, _d = faux.monter("registre", "Thomas")
    PE = co.personnes

    # ------------------------------------------------------------------ QUI PARLE (non-regression)
    PE.poser_demarrage("2000-01-01 00:00")
    r = PE.attribuer(1, "2026-10-20 09:00", {"qui_parle": deduit(comment="inconnu")})
    c.oui("machine vierge, rien ne montre qui parle -> inconnu, aucune personne inventee",
          r["parle"] == "inconnu" and len(PE.personnes()) == 0, (r["parle"], len(PE.personnes())))

    r = PE.attribuer(2, "2026-10-20 09:30", {"qui_parle": deduit(nouveau="Marie", comment="dit")})
    marie = r["parle"]
    c.oui("elle se nomme -> une personne de plus au registre",
          marie.startswith("p") and len(PE.personnes()) == 1, (marie, len(PE.personnes())))

    r = PE.attribuer(3, "2026-10-20 09:35", {"qui_parle": deduit(comment="suite")})
    c.oui("5 minutes apres, rien n'a change -> suite acceptee",
          r["parle"] == marie and r["comment"] == "deduit (suite)", (r["parle"], r["comment"]))

    r = PE.attribuer(4, "2026-10-20 14:00", {"qui_parle": deduit(comment="suite")})
    c.oui("plus de 3 heures de silence -> suite REFUSEE, on repart de inconnu",
          r["parle"] == "inconnu" and "refusee" in r["raison"], (r["parle"], r["raison"]))

    r = PE.attribuer(5, "2026-10-20 14:05", {"qui_parle": deduit(nouveau="Marie", comment="dit")})
    c.oui("« c'est Marie » et une seule Marie au registre -> c'est elle, PAS de double",
          r["parle"] == marie and len(PE.personnes()) == 1, (r["parle"], len(PE.personnes())))
    c.oui("le mot « prouve » n'apparait jamais",
          "prouv" not in (r["comment"] + r["raison"]).lower(), r["raison"])

    r = PE.attribuer(6, "2026-10-20 14:10", {"qui_parle": deduit(comment="inconnu")}, vital=True)
    c.oui("un geste vital d'un inconnu -> une question",
          r["parle"] == "inconnu" and bool(r["question_qui"]), (r["parle"], r["question_qui"]))

    # deux homonymes pour QUI PARLE
    autre_marie = PE.ajouter_personne("Marie", "dit", date="2026-10-20 15:00")
    PE.ajouter_lien(autre_marie, "la voisine")
    r = PE.attribuer(7, "2026-10-20 15:10", {"qui_parle": deduit(numero=marie, comment="dit")})
    c.oui("deux Marie et rien ne les distingue -> on ne choisit pas, on demande",
          r["parle"] == "inconnu" and bool(r["question_qui"]), (r["parle"], r["question_qui"]))
    r = PE.attribuer(8, "2026-10-20 15:20",
                     {"qui_parle": deduit(numero=autre_marie, comment="dit", distingue="elle dit : la voisine")})
    c.oui("deux Marie mais le message les distingue -> c'est bien celle-la, sans question",
          r["parle"] == autre_marie and not r["question_qui"], (r["parle"], r["question_qui"]))

    # ------------------------------------------------------------------ DE QUI ON PARLE (le manque corrige)
    co, _d = faux.monter("registre_dequi", "Thomas")
    PE = co.personnes
    PE.poser_demarrage("2000-01-01 00:00")
    p_qui_parle = PE.ajouter_personne("Paul", "dit", date="2026-10-19 09:00")
    m1 = PE.ajouter_personne("Marie", "dit", date="2026-10-19 09:00")
    PE.ajouter_lien(m1, "la fille de Madame Dupont")
    avant = len(PE.personnes())

    r = PE.attribuer(10, "2026-10-20 10:00",
                     {"qui_parle": deduit(numero=p_qui_parle, comment="dit"),
                      "de_qui": [{"numero": "", "nouveau": "Marie", "appellation": "Marie"}]})
    c.oui("de qui : une SEULE Marie au registre -> c'est elle, aucun double cree",
          r["de_qui"] == [m1] and len(PE.personnes()) == avant, (r["de_qui"], len(PE.personnes())))

    m2 = PE.ajouter_personne("Marie", "dit", date="2026-10-20 11:00")      # une deuxieme Marie, une autre personne
    PE.ajouter_lien(m2, "la voisine de Madame Dupont")
    avant = len(PE.personnes())
    r = PE.attribuer(11, "2026-10-20 11:10",
                     {"qui_parle": deduit(numero=p_qui_parle, comment="dit"),
                      "de_qui": [{"numero": "", "nouveau": "Marie", "appellation": "Marie"}]})
    c.oui("de qui : DEUX Marie et rien ne distingue -> aucune n'est choisie",
          r["de_qui"] == [], r["de_qui"])
    c.oui("... et une QUESTION est posee", bool(r["question_qui"]), r["question_qui"])
    c.oui("... et AUCUNE personne de plus n'est fabriquee",
          len(PE.personnes()) == avant, len(PE.personnes()))
    c.oui("... et le programme dit pourquoi (les deux sont nommees)",
          any(m1 in a and m2 in a for a in r.get("de_qui_ambigus") or []), r.get("de_qui_ambigus"))
    c.oui("... et les deux Marie restent DEUX personnes distinctes (jamais fusionnees)",
          m1 in PE.personnes() and m2 in PE.personnes() and m1 != m2)

    r = PE.attribuer(12, "2026-10-20 11:20",
                     {"qui_parle": deduit(numero=p_qui_parle, comment="dit"),
                      "de_qui": [{"numero": m2, "appellation": "la voisine",
                                  "distingue": "il dit : la voisine de Madame Dupont"}]})
    c.oui("de qui : deux Marie MAIS le message les distingue -> la bonne est prise, sans question",
          r["de_qui"] == [m2] and not r["question_qui"], (r["de_qui"], r["question_qui"]))

    r = PE.attribuer(13, "2026-10-20 11:30",
                     {"qui_parle": deduit(numero=p_qui_parle, comment="dit"),
                      "de_qui": [{"numero": m1, "appellation": "Marie"}]})
    c.oui("de qui : un numero donne mais un homonyme et rien ne distingue -> on demande",
          r["de_qui"] == [] and bool(r["question_qui"]), (r["de_qui"], r["question_qui"]))

    avant = len(PE.personnes())
    r = PE.attribuer(14, "2026-10-20 12:00",
                     {"qui_parle": deduit(numero=p_qui_parle, comment="dit"),
                      "de_qui": [{"numero": "", "nouveau": "Monsieur Henri", "lien": "un client"}]})
    c.oui("de qui : un nom que personne ne porte -> une personne de plus, avec son lien",
          len(r["de_qui"]) == 1 and len(PE.personnes()) == avant + 1, (r["de_qui"], len(PE.personnes())))
    henri = r["de_qui"][0]
    c.oui("... et son lien dit de qui elle est le client",
          any("Paul" in l["texte"] or p_qui_parle in l["texte"] for l in PE.personnes()[henri]["liens"]),
          PE.personnes()[henri]["liens"])

    # ------------------------------------------------------------------ L'IMPORT : p1 = le proprietaire
    co, _d = faux.monter("registre_import", "Anne")
    PE = co.personnes
    pid, ce_qui = PE.poser_le_proprietaire("Anne", "dit (import)", date="2026-10-20 08:00")
    c.oui("machine vierge : l'import fait entrer le proprietaire en p1", pid == "p1", (pid, ce_qui))
    c.oui("... avec le role « proprietaire »", PE.qui_est_le_proprietaire() == "p1",
          PE.qui_est_le_proprietaire())
    c.oui("... et on dit d'ou ca vient : « dit (import) »",
          PE.personnes()["p1"]["entree"] == "dit (import)", PE.personnes()["p1"]["entree"])
    c.oui("... et sous son vrai nom", PE.nom_de("p1") == "Anne", PE.nom_de("p1"))

    pid2, ce_qui2 = PE.poser_le_proprietaire("Anne", "dit (import)")
    c.oui("un deuxieme import ne cree JAMAIS un double",
          pid2 == "p1" and len(PE.personnes()) == 1, (pid2, len(PE.personnes()), ce_qui2))

    co, _d = faux.monter("registre_import2", "Anne")
    PE = co.personnes
    deja = PE.ajouter_personne("Anne", "deduit", date="2026-10-19 09:00")
    pid3, ce_qui3 = PE.poser_le_proprietaire("Anne", "dit (import)")
    c.oui("si une personne de ce nom est deja la : on lui pose le role, pas de double",
          pid3 == deja and len(PE.personnes()) == 1, (pid3, len(PE.personnes()), ce_qui3))

    co, _d = faux.monter("registre_import3", "Anne")
    PE = co.personnes
    PE.ajouter_personne("Anne", "deduit", date="2026-10-19 09:00")
    PE.ajouter_personne("Anne", "deduit", date="2026-10-19 10:00")
    pid4, ce_qui4 = PE.poser_le_proprietaire("Anne", "dit (import)")
    c.oui("si DEUX personnes portent ce nom : le programme ne choisit pas a sa place",
          pid4 == "" and len(PE.personnes()) == 2, (pid4, ce_qui4, len(PE.personnes())))

    # ------------------------------------------------------------------ rien n'est jamais efface
    co, _d = faux.monter("registre_jamais", "Anne")
    PE = co.personnes
    a = PE.ajouter_personne("Anne", "dit", date="2026-10-19 09:00")
    PE.poser_role(a, "proprietaire")
    PE.ajouter_appellation(a, "Annie")
    b = PE.ajouter_personne("Anne", "dit", date="2026-10-19 10:00")
    c.oui("deux personnes du meme nom = deux fiches, et les deux restent",
          len(PE.personnes()) == 2 and a != b)
    c.oui("les anciennes appellations restent toutes",
          len(PE.personnes()[a]["appellations"]) == 2, PE.personnes()[a]["appellations"])
    c.oui("le programme COMPTE bien deux personnes de ce nom",
          len(PE.combien_de_ce_nom("Anne")) == 2, PE.combien_de_ce_nom("Anne"))

    return c.fin()


if __name__ == "__main__":
    justes, total = essai()
    sys.exit(0 if justes == total else 1)
