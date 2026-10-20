# -*- coding: utf-8 -*-
"""NON-REGRESSION DES PIECES 1 A 4 (faux cerveau, faux Google, dossier jetable).

Ca ne prouve PAS que le sens de ses choix est bon (seul le vrai cerveau le dit, chez le proprietaire).
Ca prouve que les REGLES DU PROGRAMME tiennent toujours apres le nettoyage des prenoms :
  1. le plan : tiroirs, rangement, vital, et la PROTECTION (rien n'ecrase un plan plein, rien n'est perdu) ;
  2. l'archiviste : un sous-tiroir qui n'existe pas ne se cree pas, la division au seuil, remplace/reprend ;
  3. le journal du vital : l'heure du GESTE, jamais celle du message quand ce n'est pas le meme jour ;
  4. comprendre : les dates calculees par le PROGRAMME, le vital, la panne qui se dit.
"""
import os, sys, io, json, shutil

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import faux


# ======================================================================= PIECE 1 : LE PLAN
def piece1(c):
    co, d = faux.monter("piece1", "Thomas")
    P = co.plan
    t_vie = P.nouveau_tiroir("Vie privee", sens="tout ce qui touche a sa famille")
    t_fille = P.nouveau_tiroir("Ma fille", parent=t_vie)
    c.oui("1. un tiroir et son sous-tiroir sont crees", t_vie != t_fille and t_vie and t_fille)
    c.oui("1. le meme nom au meme endroit ne cree pas deux tiroirs",
          P.nouveau_tiroir("vie privee") == t_vie, P.nouveau_tiroir("vie privee"))
    t_ecole = P.tiroir_par_chemin(["Vie privee", "Ma fille", "Ecole"])
    c.oui("1. un chemin complet rend le dernier tiroir", P.chemin(t_ecole) == ["Vie privee", "Ma fille", "Ecole"],
          P.chemin(t_ecole))

    f1 = co.ecrire_fiche("souvenir", "La rentree", "Elle est entree en 6e.", source="essai")
    P.ranger([f1["n"]], t_ecole)
    c.oui("1. la fiche est rangee dans le bon tiroir", P.tiroir_de(f1["n"]) == t_ecole, P.tiroir_de(f1["n"]))
    c.oui("1. et on retrouve son chemin en clair",
          P.chemin_de_la_fiche(f1["n"]) == ["Vie privee", "Ma fille", "Ecole"], P.chemin_de_la_fiche(f1["n"]))

    P.poser_le_vital(f1["n"], "n'importe quoi")
    c.oui("1. dans le doute, c'est VITAL", P.vital_de(f1["n"]) == "vital", P.vital_de(f1["n"]))
    P.poser_le_vital(f1["n"], "loisir")
    c.oui("1. un niveau connu est garde tel quel", P.vital_de(f1["n"]) == "loisir", P.vital_de(f1["n"]))

    c.oui("1. le texte de la fiche n'a jamais ete reecrit",
          co.fiches(toutes=True)[0]["texte"] == "Elle est entree en 6e.")

    # --- la protection du plan
    plein = P.charger()
    c.oui("1. le plan a bien du contenu", P._a_du_contenu(plein))
    try:
        P.sauver({"version": 1, "tiroirs": {}, "rangement": {}})
        c.oui("1. PROTECTION : un plan VIDE n'ecrase jamais un plan plein", False, "aucun refus")
    except P.PlanProtege:
        c.oui("1. PROTECTION : un plan VIDE n'ecrase jamais un plan plein", True)
    c.oui("1. ... et le plan sur le disque est toujours la",
          P._a_du_contenu(P._lire_un_plan(P.F_PLAN)))
    c.oui("1. ... et la copie de secours existe", os.path.exists(P.F_PLAN + ".copie"))

    with io.open(P.F_PLAN, "w", encoding="utf-8") as f:
        f.write("{ ceci n'est pas du json")
    P._CACHE.update(plan=None, mtime=None, illisible="")
    charge = P.charger()
    c.oui("1. PROTECTION : un plan ABIME n'est PAS pris pour un plan vide",
          bool(P._CACHE.get("illisible")), P._CACHE.get("illisible"))
    try:
        P.nouveau_tiroir("Un tiroir de plus")
        c.oui("1. PROTECTION : on n'ecrit plus rien dans un plan abime", False, "ecriture acceptee")
    except P.PlanProtege:
        c.oui("1. PROTECTION : on n'ecrit plus rien dans un plan abime", True)
    abime = io.open(P.F_PLAN, encoding="utf-8").read()
    c.oui("1. ... et le fichier abime n'a pas ete touche", abime.startswith("{ ceci"))

    ok, phrase = P.reparer_depuis_la_copie()
    c.oui("1. REPARATION : le plan est remis depuis la copie", ok, phrase)
    c.oui("1. ... et les tiroirs sont revenus",
          P.chemin(t_ecole) == ["Vie privee", "Ma fille", "Ecole"], P.chemin(t_ecole))
    c.oui("1. ... et le fichier abime est garde a cote (rien n'est perdu)",
          any(x.startswith("plan.json.abime") for x in os.listdir(d)), os.listdir(d))

    co.plan.ecrire_le_plan_lisible(co.fiches(toutes=True), 4)
    cat = io.open(os.path.join(d, "MON PLAN (catalogue).txt"), encoding="utf-8").read()
    c.oui("1. le catalogue lisible est ecrit, sans jeton", "Vie privee" in cat and "{proprietaire}" not in cat)


# ======================================================================= PIECE 2 : L'ARCHIVISTE
def piece2(c):
    co, d = faux.monter("piece2", "Thomas")
    P, K = co.plan, co.classement
    for i in range(1, 6):
        co.ecrire_fiche("souvenir", "Souvenir %d" % i, "Un moment numero %d avec sa fille." % i, source="essai")

    # l'archiviste repond : une grande categorie neuve + un sous-tiroir qui n'existe PAS encore
    faux.REPONSES["archiviste_rangement"] = {"fiches": [
        {"n": 1, "chemin": ["Vie privee"], "sens_si_nouveau": "sa famille", "vital": "courant"},
        {"n": 2, "chemin": ["Vie privee", "Ma fille", "Ecole"], "vital": "courant"},
        {"n": 3, "chemin": ["Vie privee"], "vital": "n'importe quoi"},
        {"n": 4, "chemin": ["Vie privee"], "vital": "courant", "remplace": 1},
        {"n": 5, "chemin": ["Vie privee"], "vital": "courant", "reprend": 1},
    ]}
    faits = K.ranger_le_neuf(tout=True)
    c.oui("2. l'archiviste a range les fiches neuves", bool(faits), faits)
    c.oui("2. une grande categorie neuve est bien creee",
          P.chemin_de_la_fiche(1) == ["Vie privee"], P.chemin_de_la_fiche(1))
    c.oui("2. REGLE : un sous-tiroir qui n'existe pas n'est PAS cree ; la fiche va au tiroir du dessus",
          P.chemin_de_la_fiche(2) == ["Vie privee"], P.chemin_de_la_fiche(2))
    c.oui("2. un niveau de vital inconnu devient VITAL", P.vital_de(3) == "vital", P.vital_de(3))
    c.oui("2. « remplace » est note comme un lien vers l'ancienne fiche",
          P.liens_de(4).get("remplace") == 1, P.liens_de(4))
    c.oui("2. ... et l'ancienne est MARQUEE, jamais effacee (son texte est intact)",
          co.fiches(toutes=True)[0].get("etat") == "remplacee"
          and co.fiches(toutes=True)[0]["texte"] == "Un moment numero 1 avec sa fille.",
          (co.fiches(toutes=True)[0].get("etat"), co.fiches(toutes=True)[0]["texte"]))
    c.oui("2. « reprend » est note aussi", P.liens_de(5).get("reprend") == 1, P.liens_de(5))
    c.oui("2. les textes des 5 fiches sont intacts",
          all(("Un moment numero %d" % i) in f["texte"] for i, f in enumerate(co.fiches(toutes=True), 1)))

    # la division : le seuil du dossier d'essai est 4
    t_vie = P.tiroir_de(1)
    dedans = len(P.fiches_du_tiroir(t_vie, profond=False))
    c.oui("2. le tiroir est au-dela du seuil de division (4)", dedans >= 4, dedans)
    c.oui("2. le programme le signale comme a diviser",
          t_vie in P.a_diviser(co.fiches(toutes=True), 4), P.a_diviser(co.fiches(toutes=True), 4))
    faux.REPONSES["archiviste_division"] = {"sous_tiroirs": [
        {"nom": "Les bons moments", "sens": "ce qui s'est bien passe", "fiches": [1, 3]},
        {"nom": "Les mauvais moments", "sens": "ce qui s'est mal passe", "fiches": [4, 5]}]}
    avant = len(co.fiches(toutes=True))
    K.diviser(t_vie)
    c.oui("2. la division cree les sous-tiroirs et y descend les fiches",
          P.chemin_de_la_fiche(1) == ["Vie privee", "Les bons moments"], P.chemin_de_la_fiche(1))
    c.oui("2. ... et l'autre groupe aussi",
          P.chemin_de_la_fiche(4) == ["Vie privee", "Les mauvais moments"], P.chemin_de_la_fiche(4))
    c.oui("2. la division n'a ni efface ni ajoute une seule fiche", len(co.fiches(toutes=True)) == avant)

    parti = faux.tout_ce_qui_est_parti()
    c.oui("2. aucun prenom en dur dans les consignes de l'archiviste",
          "{proprietaire}" not in parti and "Fred" not in parti)


# ======================================================================= PIECE 3 : LE VITAL
def piece3(c):
    co, d = faux.monter("piece3", "Thomas")
    Q = co.quotidien

    faux.REPONSES["journal_du_quotidien"] = {"gestes": [
        {"quoi": "pris son cachet", "fait": True, "jour": "aujourd'hui", "heure": "08:12"}]}
    e = Q.noter_le_vital("J'ai pris mon cachet a 8h12.", "2026-10-20 10:00")
    c.oui("3. l'heure DITE est notee, pas celle du message",
          e and e[0]["heure"] == "08:12" and e[0]["heure_de"] == Q.HEURE_DITE, e)
    c.oui("3. ... et on garde l'heure a laquelle il l'a dit", e[0]["dit_le"] == "2026-10-20 10:00", e[0]["dit_le"])

    faux.REPONSES["journal_du_quotidien"] = {"gestes": [
        {"quoi": "ferme le gaz", "fait": True, "jour": "hier", "heure": ""}]}
    e = Q.noter_le_vital("Hier soir j'ai ferme le gaz.", "2026-10-20 16:10")
    c.oui("3. un geste d'un AUTRE jour sans heure : « heure pas dite », JAMAIS l'heure du message",
          e and e[0]["heure"] == "" and e[0]["heure_de"] == "heure pas dite", e)
    c.oui("3. ... et c'est bien le bon jour (hier)", e[0]["jour"] == "2026-10-19", e[0]["jour"])

    faux.REPONSES["journal_du_quotidien"] = {"gestes": [
        {"quoi": "pris son cachet", "fait": False, "jour": "hier", "heure": ""}]}
    e = Q.noter_le_vital("Hier j'ai oublie mon cachet.", "2026-10-20 21:30")
    c.oui("3. un OUBLI affirme est note PAS FAIT, sans heure inventee",
          e and e[0].get("etat") == "pas fait" and e[0]["heure"] == "", e)

    faux.REPONSES["journal_du_quotidien"] = {"gestes": [
        {"quoi": "pris sa tension", "fait": True, "jour": "aujourd'hui", "heure": "8 pm"}]}
    e = Q.noter_le_vital("J'ai pris ma tension a 8 pm.", "2026-10-20 21:00")
    c.oui("3. « 8 pm » devient 20:00", e and e[0]["heure"] == "20:00", e)

    faux.REPONSES["journal_du_quotidien"] = {"gestes": [
        {"quoi": "a uitat pastila", "fait": True, "jour": "ieri", "heure": ""}]}
    e = Q.noter_le_vital("Ieri am uitat pastila.", "2026-10-20 09:00")
    c.oui("3. un jour qu'il ne comprend pas n'est JAMAIS devine en silence : il le dit",
          e and e[0].get("jour_incertain") == "ieri", e)

    faux.REPONSES["journal_du_quotidien"] = {"gestes": []}
    e = Q.noter_le_vital("Je vais prendre mon cachet tout a l'heure.", "2026-10-20 09:00")
    c.oui("3. un geste seulement PREVU n'est pas note", e == [], e)

    t = Q.lire("2026-10-18")
    c.oui("3. aucune trace ce jour-la -> « je n'ai pas de trace », jamais « oui »",
          "AUCUNE trace" in t and "pas de trace" in t, t[:120])

    t = Q.lire("2026-10-20")
    c.oui("3. le journal du jour est rendu avec les gestes", "pris son cachet" in t, t[:160])
    c.oui("3. ... et il dit toujours d'ou elle le sait", "TU DIS TOUJOURS D'OU TU LE SAIS" in t)

    # l'ANCIEN marqueur, deja ecrit dans les vieux journaux, se lit encore
    vieux = {"jour": "2026-10-17", "heure": "08:00", "heure_de": "dite par Fred", "quoi": "vieux cachet",
             "dit_le": "2026-10-17 11:00", "message": "je l'ai pris a 8h", "note_le": "2026-10-17 11:00"}
    co.ajouter_ligne(Q._f_journal(), vieux)
    ligne = Q._ligne(vieux)
    c.oui("3. un journal DEJA ECRIT (« dite par Fred ») se relit exactement comme avant",
          "heure dite par" in ligne and "17/10/2026" in ligne, ligne)
    c.oui("3. ... et le nom affiche vient du reglage", "Thomas" in co.avec_le_nom(ligne), co.avec_le_nom(ligne))

    co.journal("envoyer_mail", {"a": "x"}, "Mail envoye a Monsieur Henri")
    t = Q.lire("2026-10-20", avec_mes_gestes=True)
    c.oui("3. avec_mes_gestes=True : ce qu'ELLE a fait est montre", "CE QUE J'AI FAIT MOI-MEME" in t)
    t = Q.lire("2026-10-20", avec_mes_gestes=False)
    c.oui("3. SEPARATION : pour une question sur la personne, ses mails a elle sont retires",
          "CE QUE J'AI FAIT MOI-MEME" not in t)


# ======================================================================= PIECE 4 : COMPRENDRE
def piece4(c):
    co, d = faux.monter("piece4", "Thomas")
    K = co.comprendre

    faux.REPONSES["comprendre"] = {"qui_parle": {"comment": "inconnu"}, "de_qui": [],
                                   "de_quoi": "les cheveux de sa fille a 8 ans", "quand": "moment",
                                   "du": "hier", "au": "", "vital": False, "flou": ""}
    r = K.comprendre("et ses cheveux ?", "", "2026-10-20 10:00")
    c.oui("4. la phrase de sens remplace le collage des messages",
          r["de_quoi"] == "les cheveux de sa fille a 8 ans", r["de_quoi"])
    c.oui("4. « hier » est CALCULE par le programme", r["du"] == "2026-10-19", r["du"])
    c.oui("4. un seul jour donne remplit du ET au", r["au"] == "2026-10-19", r["au"])
    c.oui("4. le quand est garde", r["quand"] == "moment", r["quand"])

    faux.REPONSES["comprendre"] = {"qui_parle": {"comment": "inconnu"}, "de_qui": [], "de_quoi": "le mois dernier",
                                   "quand": "histoire", "du": "2026-09-30", "au": "2026-09-01",
                                   "vital": False, "flou": ""}
    r = K.comprendre("et en septembre ?", "", "2026-10-20 10:00")
    c.oui("4. des dates a l'envers sont remises dans l'ordre",
          (r["du"], r["au"]) == ("2026-09-01", "2026-09-30"), (r["du"], r["au"]))

    faux.REPONSES["comprendre"] = {"qui_parle": {"comment": "inconnu"}, "de_qui": [], "de_quoi": "x",
                                   "quand": "n'importe quoi", "du": "la semaine du poisson", "au": "",
                                   "vital": "oui", "flou": "anciens ou recents ?"}
    r = K.comprendre("et ca ?", "", "2026-10-20 10:00")
    c.oui("4. un « quand » hors liste retombe sur maintenant", r["quand"] == "maintenant", r["quand"])
    c.oui("4. une date pas comprise n'est JAMAIS devinee : elle est dite",
          r["dates_incertaines"] and not r["du"], (r["dates_incertaines"], r["du"]))
    c.oui("4. « oui » vaut vital", r["vital"] is True)
    c.oui("4. une question possible est gardee", r["flou"] == "anciens ou recents ?", r["flou"])
    c.oui("4. ... et elle est dite au bibliothecaire", "anciens ou recents ?" in K.en_clair(r), K.en_clair(r))

    faux.REPONSES["comprendre"] = "ceci n'est pas du json"
    r = K.comprendre("ou en est le dossier ?", "", "2026-10-20 10:00")
    c.oui("4. EN PANNE : on cherche avec le message tel quel, et la panne est dite",
          r["de_quoi"] == "ou en est le dossier ?" and bool(r["panne"]), (r["de_quoi"], r["panne"]))
    c.oui("4. en panne, elle ne decide JAMAIS « pas besoin de chercher »",
          r["quand"] == "maintenant" and r["vital"] is False)

    jours = K.jours_du_journal({"du": "2026-10-18", "au": "2026-10-20"}, "2026-10-20 10:00")
    c.oui("4. le vital lit tous les jours de la periode",
          jours == ["2026-10-18", "2026-10-19", "2026-10-20"], jours)
    jours = K.jours_du_journal({}, "2026-10-20 10:00")
    c.oui("4. sans periode, c'est le jour du message", jours == ["2026-10-20"], jours)

    parti = faux.tout_ce_qui_est_parti()
    c.oui("4. la consigne de « comprendre » ne suppose personne et ne porte aucun prenom",
          "ne suppose personne" in parti and "Fred" not in parti)


def essai():
    c = faux.Compte("LES PIECES 1 A 4")
    piece1(c)
    piece2(c)
    piece3(c)
    piece4(c)
    return c.fin()


if __name__ == "__main__":
    justes, total = essai()
    sys.exit(0 if justes == total else 1)
