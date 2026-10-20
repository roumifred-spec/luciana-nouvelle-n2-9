# -*- coding: utf-8 -*-
"""
LE SCRIPT DE CONTROLE DE LA MEMOIRE 2 — chantier du 11/10/2026.

CE QU'IL FAIT : il joue les six points du chantier, du debut a la fin, et il DIT CE QUI
RATE. Il ne dit jamais « tout est vert » si ce n'est pas vrai : chaque test qui echoue est
nomme, et le script se termine en annoncant le nombre d'echecs.

IL N'ECRIT RIEN DANS LA MEMOIRE DE FRED. Il travaille dans un dossier temporaire a lui.
Il OUVRE ~/Luciana seulement pour DIRE les chiffres (et il continue sans rien dire de faux
si ce dossier n'est pas accessible).

LANCER :
    python verifier_memoire2.py
"""

import json, math, os, re, subprocess, sys, tempfile, hashlib

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

RATES = []
PASSES = []


def controle(nom, condition, detail=""):
    if condition:
        PASSES.append(nom)
        print("  OK   %s" % nom)
    else:
        RATES.append(nom + ((" — " + detail) if detail else ""))
        print("  RATE %s%s" % (nom, ("  (" + detail + ")") if detail else ""))
    return bool(condition)


def titre(t):
    print("\n" + "=" * 78)
    print(" " + t)
    print("=" * 78)


# =====================================================================
#  UN MOTEUR DE SENS DE REMPLACEMENT, pour mesurer sans rien installer.
#
#  Il transforme un texte en empreinte normalisee de taille fixe, a partir de ses suites
#  de trois lettres. Il a donc le MEME defaut de fond que le vrai modele de Fred : plus un
#  texte est long, plus son empreinte se dilue, et plus sa ressemblance avec une question
#  courte s'ecrase. C'est exactement ce qu'il faut pour montrer l'avant / apres du point 3.
#
#  Si fastembed est installe, on refait la MEME mesure avec le VRAI moteur, et on le dit.
# =====================================================================
LARGEUR = 512


def moteur_de_remplacement(textes):
    out = []
    for t in textes:
        t = re.sub(r"[^a-z0-9 ]+", " ", str(t or " ").lower())
        t = re.sub(r"\s+", " ", t).strip() or " "
        v = [0.0] * LARGEUR
        for i in range(max(1, len(t) - 2)):
            g = t[i:i + 3].encode("utf-8", "replace")
            v[int(hashlib.md5(g).hexdigest()[:8], 16) % LARGEUR] += 1.0
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        out.append([x / n for x in v])
    return out


def vrai_moteur():
    """Le VRAI moteur de sens de Fred (fastembed + paraphrase-multilingual-MiniLM), si le
    paquet et le modele sont la. Rend None sinon -- et on le DIT, on ne fait pas semblant."""
    try:
        from fastembed import TextEmbedding
        m = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

        def vecteurs(textes):
            out = []
            for v in m.embed([str(t or " ")[:4000] for t in textes]):
                v = list(float(x) for x in v)
                n = math.sqrt(sum(x * x for x in v)) or 1.0
                out.append([x / n for x in v])
            return out
        vecteurs(["essai"])
        return vecteurs
    except Exception as ex:
        print("  (le vrai moteur de sens n'est pas disponible ici : %s)" % str(ex)[:90])
        return None


# =====================================================================
titre("0) LES FICHIERS SONT-ILS LA, ET S'OUVRENT-ILS ?")
# =====================================================================
modules = {}
for nom in ("biblio2_reglages", "biblio2_archiviste", "biblio2_plan",
            "biblio2_bibliothecaire", "biblio2_reprise"):
    try:
        modules[nom] = __import__(nom)
        controle("%s s'ouvre" % nom, True)
    except Exception as ex:
        modules[nom] = None
        controle("%s s'ouvre" % nom, False, str(ex)[:120])

if not all(modules.values()):
    print("\nUn fichier ne s'ouvre pas : la suite n'aurait aucun sens. J'arrete ici et je le dis.")
    print("\nTESTS QUI RATENT (%d) :\n  - %s" % (len(RATES), "\n  - ".join(RATES)))
    raise SystemExit(1)

reglages = modules["biblio2_reglages"]
arch = modules["biblio2_archiviste"]
plan_biblio = modules["biblio2_plan"]
bib = modules["biblio2_bibliothecaire"]
reprise = modules["biblio2_reprise"]

controle("reglage_biblio2.json existe", os.path.exists(reglages.FICHIER_REGLAGE))


# =====================================================================
titre("POINT 2) TOUS LES SEUILS DANS UN SEUL FICHIER, RELU A CHAQUE LANCEMENT")
# =====================================================================
v = reglages.lire(force=True)
print(reglages.dire_les_reglages())
print("")
controle("le fichier de reglage est bien lu (pas les valeurs de secours)",
         reglages.FICHIER_REGLAGE in str(v["_fichier_lu"]))
controle("le seuil d'entree vient du fichier", abs(v["seuil_confiance_entree"] - 0.55) < 1e-9)
controle("le curseur de sortie par defaut est a 0,35 (il n'est PAS remonte)",
         abs(v["curseur_sortie_defaut"] - 0.35) < 1e-9)
controle("l'archiviste lit le MEME seuil que le fichier",
         abs(arch.seuil_confiance() - v["seuil_confiance_entree"]) < 1e-9)
controle("le bibliothecaire lit le MEME plafond que le fichier",
         bib.plafond() == v["plafond_caracteres"])
controle("plus aucun seuil n'est en dur dans l'archiviste (il passe par le reglage)",
         arch.seuil_confiance() == reglages.seuil_confiance())

# un reglage abime ne doit rien casser : on verifie le filet
import biblio2_reglages as _r
_vrai = _r.FICHIER_REGLAGE
try:
    _r.FICHIER_REGLAGE = os.path.join(tempfile.mkdtemp(), "pas_la.json")
    secours = _r.lire(force=True)
    controle("reglage absent : on reprend les valeurs de secours, sans planter",
             abs(secours["seuil_confiance_entree"] - 0.55) < 1e-9)
finally:
    _r.FICHIER_REGLAGE = _vrai
    _r.lire(force=True)

print("\n  LE POINT IMPORTANT DE FRED : le seuil d'entree ne JETTE rien, il MARQUE.")
ok, propre, raison = arch.valider_jugement(
    {"categorie": "Famille", "sous_categorie": "Maman", "filtres": {"type": "fait"},
     "resume": "Un souvenir de maman.", "confiance": 0.10})
arbre_t = {}
rap = arch.ranger(arbre_t, {"texte": "Maman aimait les roses blanches.", "source": "essai"},
                  (ok, propre, raison))
controle("point 2 : une fiche dont l'IA doute RESTE dans son rayon (Famille / Maman)",
         rap["range_dans"].startswith("Famille / Maman"), rap["range_dans"])
controle("point 2 : elle porte l'etiquette « en suspens »", rap["en_suspens"] is True)
controle("point 2 : aucun souvenir ne disparait a l'entree",
         arch.compter(arbre_t)["fiches"] == 1)


# =====================================================================
titre("POINT 1) LE MARQUE-PAGE QUI DEBLOQUE L'ARCHIVISTE")
# =====================================================================
r1 = arch.repere_de("souvenirs", "J'ai  acheté une VOITURE rouge. ")
r2 = arch.repere_de("souvenirs", "j'ai acheté une voiture rouge.")
controle("le repere est STABLE (le meme souvenir donne le meme repere)", r1 == r2)
controle("le repere n'est PAS une position (il ne contient aucun numero d'ordre)",
         "#" in r1 and not r1.split("#", 1)[1].isdigit())
controle("la source fait partie du repere",
         arch.repere_de("souvenirs", "x") != arch.repere_de("conversation", "x"))

# le vrai test : on avale un passe, puis on relance sur le MEME passe
dossier = tempfile.mkdtemp(prefix="controle_memoire2_")
reprise.DOSSIER_BIBLIO2 = dossier
reprise.FICHIER_ARBRE = os.path.join(dossier, "arbre.json")
reprise.FICHIER_MARQUE_PAGE = os.path.join(dossier, "marque_page.json")
reprise.FICHIER_PLAN = os.path.join(dossier, "plan.json")
reprise.FICHIER_SIGNAL = os.path.join(dossier, "signal_plan.json")

BAVARDAGE = ("Alors ce matin je me suis leve tot, il faisait gris, j'ai pris un cafe et j'ai "
             "regarde par la fenetre, les voisins refaisaient leur toiture, ca tapait fort, "
             "apres j'ai range le garage un peu, enfin pas tout, il reste des cartons, et je me "
             "demandais s'il fallait repeindre le portail un de ces jours, ") * 6

PASSE = [
    ("souvenirs", "J'ai achete une voiture rouge, une Clio, en 2016."),
    ("souvenirs", "Ma fille est nee en 2009, un mardi matin."),
    ("souvenirs", "Je n'aime pas du tout le gout de la coriandre."),
    ("conversation", "Rendez-vous chez le docteur Martin a Lyon le 2 mars 2024."),
    ("conversation", BAVARDAGE),
    ("bibliotheque", "Informatique > Memoire de Luciana > curseur : le curseur de sortie de la "
                     "memoire est regle a 0,35 dans le fichier curseur.txt."),
]


def faux_passe():
    return ([{"texte": t, "source": src, "date": "",
              "repere": arch.repere_de(src, t)} for src, t in PASSE], [])


def faux_juge(s, _arbre):
    t = s["texte"].lower()
    if "voiture" in t:
        return {"categorie": "Vehicules", "sous_categorie": "Voitures",
                "filtres": {"date": "2016", "objet": "voiture rouge", "type": "achat"},
                "resume": "Clio rouge achetee en 2016.", "confiance": 0.9}
    if "fille" in t:
        return {"categorie": "Famille", "sous_categorie": "Ma fille",
                "filtres": {"date": "2009", "qui": ["ma fille"], "type": "evenement"},
                "resume": "Naissance de ma fille en 2009.", "confiance": 0.9}
    if "coriandre" in t:
        return {"categorie": "Gouts", "sous_categorie": "Cuisine",
                "filtres": {"objet": "coriandre", "type": "gout"},
                "resume": "Fred n'aime pas la coriandre.", "confiance": 0.40}
    if "docteur" in t:
        return {"categorie": "Sante", "sous_categorie": "Rendez-vous",
                "filtres": {"date": "2024-03-02", "ou": "Lyon", "qui": ["Dr Martin"],
                            "type": "medical"}, "resume": "RDV chez le Dr Martin a Lyon.",
                "confiance": 0.85}
    if "curseur" in t:
        return {"categorie": "Informatique", "sous_categorie": "Memoire de Luciana",
                "filtres": {"objet": "curseur de sortie", "type": "reglage"},
                "resume": "Le curseur de sortie de la memoire est a 0,35.", "confiance": 0.9}
    return {"categorie": "", "confiance": 0.15}


print("  --- premier passage : la bibliotheque est vide ---")
arbre = reprise.reprendre(faux_juge, sources=faux_passe)
c1 = arch.compter(arbre)
print("\n  --- deuxieme passage, sur le MEME passe (c'est LE test du point 1) ---")
arbre = reprise.reprendre(faux_juge, sources=faux_passe)
c2 = arch.compter(arbre)

print("")
controle("point 1 : les %d souvenirs du passe sont ranges" % len(PASSE),
         c1["fiches"] == len(PASSE), "%d ranges" % c1["fiches"])
controle("point 1 : chaque fiche porte un repere", c1["avec_repere"] == c1["fiches"])
controle("point 1 : relancer ne range RIEN deux fois (%d avant, %d apres)"
         % (c1["fiches"], c2["fiches"]), c2["fiches"] == c1["fiches"])
mp = json.load(open(reprise.FICHIER_MARQUE_PAGE, encoding="utf-8"))
controle("point 1 : le marque-page est ecrit, dans SON fichier", os.path.exists(reprise.FICHIER_MARQUE_PAGE))
controle("point 1 : il retient des REPERES, pas une position",
         mp["combien"] == len(PASSE) and "dernier_index" not in json.dumps(mp))
controle("point 1 : il avale bien LES TROIS sources du passe",
         set(mp["combien_par_source"]) == {"souvenirs", "conversation", "bibliotheque"},
         str(mp["combien_par_source"]))

# le marque-page perdu : l'arbre doit suffire a reprendre au bon endroit
os.remove(reprise.FICHIER_MARQUE_PAGE)
faits, d_ou = reprise.marque_page_charger(arbre=arbre)
controle("point 1 : marque-page perdu -> l'arbre dit la verite, rien ne sera refait",
         len(faits) == c1["fiches"] and d_ou["dans_l_arbre"] == c1["fiches"])
arbre = reprise.reprendre(faux_juge, sources=faux_passe)
controle("point 1 : et la reprise ne range toujours rien deux fois",
         arch.compter(arbre)["fiches"] == c1["fiches"])

print("\n  La demonstration du defaut d'avant (pour memoire) :")
print("    l'ancien marque-page retenait {\"dernier_index\": 30} -- une PLACE.")
print("    La liste saute les messages du programme, donc la 30e place changeait de")
print("    souvenir d'un lancement a l'autre, et la reprise s'arretait a 30 en croyant")
print("    avoir fini. Le repere, lui, ne bouge pas avec la liste.")


# =====================================================================
titre("POINT 4) LE PLAN DE LA BIBLIOTHEQUE, AUX QUATRE NIVEAUX")
# =====================================================================
plan = plan_biblio.charger(reprise.FICHIER_PLAN)
print(plan_biblio.texte_pour_le_bibliothecaire(plan))
print("\n  chiffres du plan : %s" % plan["chiffres"])
controle("point 4 : le plan est ecrit sur le disque", os.path.exists(reprise.FICHIER_PLAN))
controle("point 4 : niveau 1, les categories", plan["chiffres"]["rayons"] >= 4)
controle("point 4 : niveau 2, les sous-categories", plan["chiffres"]["sous_categories"] >= 4)
controle("point 4 : niveau 3, les filtres", plan["chiffres"]["filtres"] >= 4)
controle("point 4 : niveau 4, les sous-filtres", plan["chiffres"]["sous_filtres"] >= 4)
controle("point 4 : le plan compte toutes les fiches",
         plan["chiffres"]["fiches"] == c1["fiches"])
controle("point 4 : le plan NE CONTIENT PAS le texte des souvenirs (il reste une carte)",
         "voisins refaisaient" not in json.dumps(plan, ensure_ascii=False))
vu = bib.prendre_connaissance(reprise.FICHIER_PLAN, reprise.FICHIER_SIGNAL)
controle("point 4 : le bibliothecaire LIT ce plan pour chercher",
         "Vehicules" in vu["carte"] and "Voiture rouge" in vu["carte"])
controle("point 4 : la carte part bien dans sa demande a la petite IA",
         "Voiture rouge" in bib.construire_demande("ma voiture ?", vu["carte"]))
controle("point 4 : les niveaux 3 et 4 filtrent aussi la recherche",
         bib.chercher(arbre, {"filtre": "Achat", "sous_filtre": "Voiture rouge"})[1]
         ["candidats_dans_l_arbre"] == 1)
print("\n  L'etat d'avant, pour comparer : l'arbre de Fred avait 30 fiches et 2 rayons")
print("  racines seulement (« Informatique » et « Divers »), et aucun niveau 3 ni 4.")


# =====================================================================
titre("POINT 5) LA REMONTEE ARCHIVISTE -> BIBLIOTHECAIRE")
# =====================================================================
signal = plan_biblio.lire_signal(reprise.FICHIER_SIGNAL)
controle("point 5 : le signal existe, dans son fichier", os.path.exists(reprise.FICHIER_SIGNAL))
controle("point 5 : il est DATE", len(str(signal.get("quand") or "")) >= 16,
         str(signal.get("quand")))
controle("point 5 : il porte la version du plan", signal.get("version_du_plan", 0) >= 1)
controle("point 5 : le bibliothecaire le lit et sait depuis quand il est au courant",
         len(vu["au_courant_depuis"]) >= 16)

# on cree un etage NEUF et on verifie que le bibliothecaire en est prevenu, aux 4 niveaux
nouveau = {"texte": "J'ai pris une voiture bleue en 2020.", "source": "souvenirs"}
nouveau["repere"] = arch.repere_de("souvenirs", nouveau["texte"])
arch.ranger(arbre, nouveau, arch.valider_jugement(
    {"categorie": "Vehicules", "sous_categorie": "Voitures",
     "filtres": {"date": "2020", "objet": "voiture bleue", "type": "achat"},
     "resume": "Voiture bleue achetee en 2020.", "confiance": 0.9}))
p_av = plan_biblio.charger(reprise.FICHIER_PLAN)
p_ap, sig2 = plan_biblio.rafraichir(arbre, reprise.FICHIER_PLAN, reprise.FICHIER_SIGNAL)
controle("point 5 : un sous-filtre neuf est REMONTE, nomme",
         any("Voiture bleue" in n["chemin"] for n in sig2["nouveautes"]),
         str([n["dire"] for n in sig2["nouveautes"]]))
controle("point 5 : le signal dit clairement que le plan a change",
         sig2["le_plan_a_change"] is True)
print("\n  ce que le bibliothecaire lit : %s" % sig2["pour_le_bibliothecaire"])

# une categorie toute neuve : les 4 niveaux doivent remonter
neuf2 = {"texte": "J'ai signe chez le notaire Dupond a Grenoble.", "source": "souvenirs"}
neuf2["repere"] = arch.repere_de("souvenirs", neuf2["texte"])
arch.ranger(arbre, neuf2, arch.valider_jugement(
    {"categorie": "Papiers", "sous_categorie": "Notaire",
     "filtres": {"ou": "Grenoble", "qui": ["Me Dupond"], "type": "decision"},
     "resume": "Signature chez Me Dupond.", "confiance": 0.9}))
p_av3 = plan_biblio.charger(reprise.FICHIER_PLAN)
p_ap3, sig3 = plan_biblio.rafraichir(arbre, reprise.FICHIER_PLAN, reprise.FICHIER_SIGNAL)
controle("point 5 : une categorie neuve remonte aux QUATRE niveaux",
         {n["niveau"] for n in sig3["nouveautes"]} == {1, 2, 3, 4},
         str(sorted({n["niveau"] for n in sig3["nouveautes"]})))


# =====================================================================
titre("POINT 6) LE NOUVEAU PLAN REMPLACE L'ANCIEN, ET NE REMONTE QUE S'IL A CHANGE")
# =====================================================================
taille_avant = os.path.getsize(reprise.FICHIER_PLAN)
version_avant = plan_biblio.charger(reprise.FICHIER_PLAN)["version"]
p4, sig4 = plan_biblio.rafraichir(arbre, reprise.FICHIER_PLAN, reprise.FICHIER_SIGNAL)
controle("point 6 : rien n'a change -> la version du plan ne bouge pas",
         p4["version"] == version_avant, "%s -> %s" % (version_avant, p4["version"]))
controle("point 6 : rien n'a change -> le plan ne remonte PAS a Luciana",
         sig4["le_plan_a_change"] is False)
controle("point 6 : le plan REMPLACE l'ancien (le fichier ne gonfle pas)",
         os.path.getsize(reprise.FICHIER_PLAN) == taille_avant,
         "%d -> %d octets" % (taille_avant, os.path.getsize(reprise.FICHIER_PLAN)))
controle("point 6 : le signal garde SEULEMENT le dernier etat (il ne s'empile pas)",
         sig4["combien_de_nouveautes"] == 0)
controle("point 6 : l'empreinte porte la FORME, pas le nombre de fiches",
         plan_biblio.empreinte(p4["rayons"]) == p4["empreinte"])

# la preuve que le compteur de fiches ne fait pas « changer » le plan
import copy
arbre_b = copy.deepcopy(arbre)
jumeau = {"texte": "Encore un mot sur ma voiture rouge de 2016, pour le test.",
          "source": "souvenirs"}
jumeau["repere"] = arch.repere_de("souvenirs", jumeau["texte"])
arch.ranger(arbre_b, jumeau, arch.valider_jugement(
    {"categorie": "Vehicules", "sous_categorie": "Voitures",
     "filtres": {"date": "2016", "objet": "voiture rouge", "type": "achat"},
     "resume": "Encore la Clio rouge.", "confiance": 0.9}))
p5 = plan_biblio.construire(arbre_b, version_avant=p4["version"], empreinte_avant=p4["empreinte"])
controle("point 6 : une fiche en plus dans un tiroir EXISTANT ne fait pas remonter le plan",
         p5["empreinte"] == p4["empreinte"] and p5["version"] == p4["version"])
controle("point 6 : mais le plan compte bien la fiche en plus",
         p5["chiffres"]["fiches"] == p4["chiffres"]["fiches"] + 1)


# =====================================================================
titre("POINT 3) LE MOTEUR DE SCORE : LA MESURE AVANT / APRES")
# =====================================================================
QUESTIONS = [
    ("c'etait quoi la voiture rouge que j'avais achetee en 2016 ?", "Clio rouge"),
    ("il est regle a combien le curseur de ma memoire ?", "curseur de sortie"),
    ("quand est-ce que ma fille est nee ?", "ma fille"),
    ("comment s'appelle le docteur que je vois a Lyon ?", "Dr Martin"),
]
toutes = arch.toutes_les_fiches(arbre)
curseur = reglages.curseur_sortie()
print("  bibliotheque de mesure : %d fiches | curseur de sortie : %.2f" % (len(toutes), curseur))


def mesurer(moteur, comment):
    print("\n  --- %s ---" % comment)
    print("  %-52s %8s %8s %8s" % ("question", "AVANT", "APRES", "gain"))
    servies_avant = servies_apres = 0
    bonnes_avant, bonnes_apres = [], []
    for question, attendu in QUESTIONS:
        besoin = {}
        av = bib.noter_a_l_ancienne(question, toutes, moteur)
        ap = bib.noter(question, toutes, moteur, besoin=besoin)
        if av is None or ap is None:
            print("  (le moteur n'a pas repondu pour « %s »)" % question[:40])
            continue

        def score_de_la_bonne(scores):
            for (c, s, fi), sc in zip(toutes, scores):
                cible = ((fi.get("resume") or "") + " " + (fi.get("etiquette") or "")).lower()
                if attendu.lower() in cible:
                    return sc
            return 0.0

        b_av, b_ap = score_de_la_bonne(av), score_de_la_bonne(ap)
        bonnes_avant.append(b_av)
        bonnes_apres.append(b_ap)
        servies_avant += 1 if b_av >= curseur else 0
        servies_apres += 1 if b_ap >= curseur else 0
        print("  %-52s %8.3f %8.3f %+8.3f" % (question[:52], b_av, b_ap, b_ap - b_av))
    moy_av = sum(bonnes_avant) / max(1, len(bonnes_avant))
    moy_ap = sum(bonnes_apres) / max(1, len(bonnes_apres))
    print("  %-52s %8.3f %8.3f %+8.3f" % ("MOYENNE de la bonne fiche", moy_av, moy_ap,
                                          moy_ap - moy_av))
    print("  bonnes fiches qui PASSENT le curseur (%.2f) : %d/%d  ->  %d/%d"
          % (curseur, servies_avant, len(QUESTIONS), servies_apres, len(QUESTIONS)))
    return moy_av, moy_ap, servies_avant, servies_apres


moy_av, moy_ap, srv_av, srv_ap = mesurer(moteur_de_remplacement,
                                         "avec le moteur de remplacement (toujours disponible)")
print("")
controle("point 3 : la bonne fiche monte apres reparation", moy_ap > moy_av,
         "%.3f -> %.3f" % (moy_av, moy_ap))
controle("point 3 : au moins autant de bonnes fiches passent le curseur", srv_ap >= srv_av,
         "%d -> %d" % (srv_av, srv_ap))
controle("point 3 : toutes les bonnes fiches passent le curseur apres reparation",
         srv_ap == len(QUESTIONS), "%d/%d" % (srv_ap, len(QUESTIONS)))

# le long bavardage ne doit pas gagner
q_test = "c'etait quoi la voiture rouge que j'avais achetee en 2016 ?"
ap = bib.noter(q_test, toutes, moteur_de_remplacement, besoin={"objet": "voiture rouge"})
paires = sorted(zip(ap, toutes), key=lambda x: -x[0])
print("\n  les trois mieux notees pour « %s » :" % q_test[:46])
for sc, (c, s, fi) in paires[:3]:
    print("    %.3f  [%s / %s] %s" % (sc, c, s, (fi.get("resume") or fi.get("texte") or "")[:56]))
controle("point 3 : la bonne fiche arrive PREMIERE",
         "rouge" in ((paires[0][1][2].get("resume") or "")).lower(),
         (paires[0][1][2].get("resume") or "")[:50])
controle("point 3 : le long bavardage ne gagne pas",
         max((sc for sc, (c, s, fi) in paires if len(fi.get("texte") or "") > 500),
             default=0.0) < paires[0][0])
controle("point 3 : les scores restent entre 0 et 1", all(0.0 <= x <= 1.0 for x in ap))
controle("point 3 : une etiquette vide ne coute pas de points",
         (bib.noter("voiture rouge", [("X", "Y", {"texte": "ma voiture rouge"})],
                    moteur_de_remplacement) or [0])[0] > 0.3)
controle("point 3 : la prime des facettes est bien plafonnee",
         max(bib.noter(q_test, toutes, moteur_de_remplacement,
                       besoin={"objet": "voiture rouge", "date": "2016", "type": "achat"})) <= 1.0)
controle("point 3 : aucune fiche -> aucun score, aucun plantage",
         bib.noter("x", [], moteur_de_remplacement) == [])

# la meme mesure avec le VRAI moteur, si on peut
print("")
vrai = vrai_moteur()
if vrai is not None:
    r_moy_av, r_moy_ap, r_srv_av, r_srv_ap = mesurer(vrai, "avec le VRAI moteur de sens de Fred")
    print("")
    controle("point 3 (vrai moteur) : la bonne fiche monte", r_moy_ap > r_moy_av,
             "%.3f -> %.3f" % (r_moy_av, r_moy_ap))
else:
    print("  >>> A DIRE FRANCHEMENT : la mesure ci-dessus est faite avec un moteur de")
    print("      REMPLACEMENT, parce que fastembed et le modele de sens ne sont pas")
    print("      installes ici. Il a le meme defaut de fond que le vrai (un texte long")
    print("      dilue son empreinte), donc le SENS de l'avant/apres est bon -- mais les")
    print("      CHIFFRES exacts sur le PC de Fred seront differents. Pour les avoir en")
    print("      vrai, relancer ce script sur son PC : il prendra le vrai moteur tout seul.")


# =====================================================================
titre("LE CYCLE COMPLET : ranger, puis retrouver, puis servir")
# =====================================================================
def fausse_petite_ia(prompt):
    return json.dumps({"categorie": "Vehicules", "objet": "voiture rouge", "date": "2016"})


texte, rapport = bib.servir(arbre, "c'etait quoi ma voiture rouge de 2016 ?",
                            fausse_petite_ia, vecteurs_de=moteur_de_remplacement)
print("  rapport : candidats=%s, retenus=%s, meilleure pertinence=%s, curseur=%s, donnes=%s"
      % (rapport.get("candidats_dans_l_arbre"), rapport.get("retenus_apres_curseur"),
         rapport.get("meilleure_pertinence"), rapport.get("curseur"),
         rapport.get("donnes_a_luciana")))
print("  servi a Luciana :\n    %s" % (texte[:200].replace("\n", "\n    ") or "(rien)"))
controle("le cycle complet sert bien quelque chose", bool(texte.strip()))
controle("le cycle complet sert la BONNE fiche", "Clio" in texte or "rouge" in texte.lower())
controle("la fiche servie porte ses quatre niveaux", texte.count("/") >= 3)
controle("une fiche en suspens est servie en le DISANT",
         "en suspens" in bib._bloc("Gouts", "Cuisine",
                                   {"texte": "x", "en_suspens": True, "filtre": "Gout",
                                    "sous_filtre": "Coriandre"}))
texte_rien, rap_rien = bib.servir({}, "n'importe quoi", fausse_petite_ia,
                                  vecteurs_de=moteur_de_remplacement)
controle("une bibliotheque vide ne plante pas", texte_rien == "")


# =====================================================================
titre("LES AUTO-TESTS DE CHAQUE BRIQUE")
# =====================================================================
for fichier in ("biblio2_reglages.py", "biblio2_archiviste.py", "biblio2_plan.py",
                "biblio2_bibliothecaire.py"):
    try:
        p = subprocess.run([sys.executable, os.path.join(ICI, fichier)],
                           capture_output=True, text=True, timeout=300, cwd=ICI)
        sortie = (p.stdout or "") + (p.stderr or "")
        rates_dedans = [l.strip() for l in sortie.splitlines() if l.strip().startswith("RATE")]
        if p.returncode != 0:
            controle("l'auto-test de %s se termine bien" % fichier, False,
                     "code %d : %s" % (p.returncode, (p.stderr or "")[-200:].replace("\n", " ")))
        elif rates_dedans:
            controle("l'auto-test de %s passe en entier" % fichier, False,
                     "%d test(s) rate(s) dedans" % len(rates_dedans))
            for l in rates_dedans:
                print("       %s" % l)
        else:
            controle("l'auto-test de %s passe en entier" % fichier, True)
    except Exception as ex:
        controle("l'auto-test de %s a pu etre joue" % fichier, False, str(ex)[:120])

try:
    p = subprocess.run([sys.executable, os.path.join(ICI, "biblio2_reprise.py"), "--demo"],
                       capture_output=True, text=True, timeout=300, cwd=ICI)
    sortie = (p.stdout or "") + (p.stderr or "")
    rates_dedans = [l.strip() for l in sortie.splitlines() if l.strip().startswith("RATE")]
    controle("l'auto-test de biblio2_reprise.py (--demo) passe en entier",
             p.returncode == 0 and not rates_dedans,
             "code %d, %d rate(s)" % (p.returncode, len(rates_dedans)))
    for l in rates_dedans:
        print("       %s" % l)
except Exception as ex:
    controle("l'auto-test de biblio2_reprise.py a pu etre joue", False, str(ex)[:120])


# =====================================================================
titre("L'ETAT REEL SUR LE PC DE FRED (lecture seule, et on dit si on ne voit pas)")
# =====================================================================
import importlib
importlib.reload(reglages)
for nom, chemin in (("souvenirs.json", reglages.FICHIER_SOUVENIRS),
                    ("luciana_memoire.json", reglages.FICHIER_CONVERSATION),
                    ("l'ancienne bibliotheque", reglages.FICHIER_ANCIEN_INDEX),
                    ("bibliotheque2/arbre.json", reglages.FICHIER_ARBRE),
                    ("bibliotheque2/curseur.txt", reglages.FICHIER_CURSEUR),
                    ("bibliotheque2/avancee.json", reglages.FICHIER_AVANCEE_ANCIEN),
                    ("bibliotheque2/marque_page.json", reglages.FICHIER_MARQUE_PAGE),
                    ("bibliotheque2/plan.json", reglages.FICHIER_PLAN)):
    try:
        if os.path.exists(chemin):
            print("  vu      %-32s %9d octets" % (nom, os.path.getsize(chemin)))
        else:
            print("  absent  %-32s (pas encore cree)" % nom)
    except Exception as ex:
        print("  PAS VU  %-32s (%s)" % (nom, str(ex)[:60]))

print("\n  Si toutes les lignes disent « PAS VU », c'est que ce script tourne dans un")
print("  endroit qui n'a pas acces au dossier de Fred. Les chiffres reels (195 souvenirs,")
print("  60 dossiers, avancee.json) ne peuvent alors PAS etre mesures ici : il faut")
print("  lancer « python verifier_memoire2.py » sur son PC, puis")
print("  « python biblio2_reprise.py --chiffres » pour l'avant / apres en vrai.")


# =====================================================================
titre("CONCLUSION")
# =====================================================================
print("  tests joues   : %d" % (len(PASSES) + len(RATES)))
print("  tests passes  : %d" % len(PASSES))
print("  tests RATES   : %d" % len(RATES))
if RATES:
    print("\n  LES TESTS QUI RATENT :")
    for r in RATES:
        print("    - %s" % r)
    print("\n  >>> Il reste %d test(s) en echec. Ce n'est PAS tout vert." % len(RATES))
    raise SystemExit(1)
print("\n  >>> Les %d tests joues passent. (Et la mesure du point 3 est faite avec le" % len(PASSES))
print("      moteur disponible ici : la ligne qui le dit est plus haut.)")
raise SystemExit(0)
