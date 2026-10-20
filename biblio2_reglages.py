# -*- coding: utf-8 -*-
"""
LE TABLEAU DE BORD COMMUN DE LA MEMOIRE 2 (point 2 du chantier du 11/10/2026).

CE QUE CA FAIT, ET RIEN D'AUTRE : ca lit reglage_biblio2.json, et ca le donne a tout
le monde. Il n'y a plus un seul seuil ecrit en dur dans le code des quatre roles.

POURQUOI UN SEUL FICHIER : la regle de Fred, « TOUT LE MONDE AU COURANT DE TOUT ».
L'archiviste, la bibliotheque, le bibliothecaire et la porte de sortie lisent LA MEME
LIGNE du MEME fichier. Plus de « lui il pouvait pas, il etait pas au courant » : si le
seuil change, il change pour les quatre en meme temps.

RELU A CHAQUE LANCEMENT : lire() relit le fichier sur le disque (avec un petit cache
d'une seconde, pour ne pas relire 200 fois pendant un seul rangement). Fred change un
nombre, il relance, c'est pris en compte.

LE FILET EST ENTIER : fichier absent, JSON abime, cle manquante, valeur farfelue ->
on rend la valeur par defaut et on continue. Ce module ne leve JAMAIS.

NOTE IA : tout est ecrit en POSITIF (regle de Fred).
"""

import json, os, time

HOME = os.path.expanduser("~")
DOSSIER = os.path.join(HOME, "Luciana")              # la memoire vivante : LECTURE SEULE
DOSSIER_CODE = os.path.dirname(os.path.abspath(__file__))

# --- LA MEMOIRE VIVANTE DE FRED : on l'OUVRE, on ne l'ECRIT JAMAIS ---------------
FICHIER_SOUVENIRS = os.path.join(DOSSIER, "souvenirs.json")          # les 195 souvenirs
FICHIER_CONVERSATION = os.path.join(DOSSIER, "luciana_memoire.json")  # le fil des messages
DOSSIER_ANCIENNE_BIBLIO = os.path.join(DOSSIER, "bibliotheque")       # 60 dossiers + index
FICHIER_ANCIEN_INDEX = os.path.join(DOSSIER_ANCIENNE_BIBLIO, "index.json")
FICHIER_CLE_DEEPSEEK = os.path.join(DOSSIER, "cle_deepseek.txt")

# --- NOTRE DOSSIER A NOUS : le seul endroit ou la memoire 2 ecrit -----------------
DOSSIER_BIBLIO2 = os.path.join(DOSSIER, "bibliotheque2")
FICHIER_ARBRE = os.path.join(DOSSIER_BIBLIO2, "arbre.json")        # la bibliotheque (role 2)
FICHIER_MARQUE_PAGE = os.path.join(DOSSIER_BIBLIO2, "marque_page.json")  # le repere (point 1)
FICHIER_PLAN = os.path.join(DOSSIER_BIBLIO2, "plan.json")          # le plan 4 niveaux (point 4)
FICHIER_SIGNAL = os.path.join(DOSSIER_BIBLIO2, "signal_plan.json")  # la remontee (point 5)
FICHIER_CURSEUR = os.path.join(DOSSIER_BIBLIO2, "curseur.txt")     # la porte de sortie
FICHIER_AVANCEE_ANCIEN = os.path.join(DOSSIER_BIBLIO2, "avancee.json")  # l'ancien marque-page
FICHIER_MARQUEUR_BRANCHE = os.path.join(DOSSIER_BIBLIO2, "BRANCHE.txt")

FICHIER_REGLAGE = os.path.join(DOSSIER_CODE, "reglage_biblio2.json")

# =====================================================================================
#  L'INTERRUPTEUR DU BLOC DE QUESTIONS DE L'ARCHIVISTE (chantier du 12/10/2026).
#  C'EST LA SEULE CHOSE QUI DECIDE, ET IL EST ETEINT D'ORIGINE.
# =====================================================================================
#
#  LE DEFAUT, CONSTATE PENDANT PLUSIEURS JOURS : le BLOC DE QUESTIONS de l'archiviste
#  (« ou ranger ce souvenir ? », avec un rayon propose) remontait DIRECTEMENT DANS LE
#  CONTEXTE DE LUCIANA, colle a ses messages avec Fred, et par GROS PAQUETS. Resultat :
#  elle repondait a ces questions AU MILIEU des phrases de Fred, elle n'arrivait plus a
#  travailler, et Fred ne pouvait plus communiquer avec elle.
#
#  POURQUOI LE PREMIER DEBRANCHEMENT N'ETAIT PAS SOLIDE : il tenait a l'ABSENCE d'un
#  fichier drapeau (~/Luciana/bibliotheque2/QUESTIONS.txt) dans le dossier de DONNEES.
#  Un fichier absent, ca se recree — au demarrage, par un bouton, par un script d'essai —
#  et le defaut revenait aussitot, tout seul.
#
#  MAINTENANT, C'EST UN REGLAGE EXPLICITE ET PERSISTANT, DANS reglage_biblio2.json :
#
#        "questions_de_l_archiviste": { "bloc_dans_le_contexte": false }
#
#    - ETEINT D'ORIGINE. Reglage absent, fichier abime, cle manquante, valeur farfelue :
#      c'est ETEINT. Il faut l'ecrire EXPRESSEMENT pour allumer (voir _vrai_explicite).
#    - ETEINT = LE BLOC N'EST JAMAIS INJECTE, QUOI QU'IL ARRIVE. Et un vieux QUESTIONS.txt
#      qui traine encore sur le disque NE CHANGE PLUS RIEN DU TOUT : depuis le 12/10/2026,
#      plus une seule ligne de code ne le LIT pour decider, et plus une seule ligne de code
#      ne l'ECRIT. LE REGLAGE EST LA SEULE CHOSE QUI COMPTE.
#    - RIEN NE SE PERD. On eteint un AFFICHAGE, on ne detruit AUCUNE donnee : les questions
#      deja ecrites (questions.json), les reponses deja donnees (reponses.json), les fiches
#      en attente (lot_pour_le_proprietaire.json) et la bibliotheque (arbre.json) restent
#      INTACTES sur le disque, exactement comme elles sont.
#    - LE PROGRAMME NE RALLUME JAMAIS CET INTERRUPTEUR TOUT SEUL. Une seule fonction de
#      tout le programme sait l'ECRIRE, regler_le_bloc_de_questions(), et elle n'est
#      appelee QUE depuis la ligne de commande (les deux boutons de Fred), avec un
#      garde-fou de confirmation en plus. Aucun autre endroit ne l'appelle.
#    - ET IL RESTE ACTIONNABLE. Le jour ou Fred voudra rebrancher ce mecanisme, il met
#      true — bouton « Brancher les questions », ou la ligne a la main dans
#      reglage_biblio2.json — et c'est reparti, SANS RETOUCHER UNE LIGNE DE CODE.
#
#  LE RESTE DE LA MEMOIRE 2 N'EST PAS CONCERNE : le bibliothecaire qui sert les souvenirs
#  PAR SENS, les consignes, les carnets et la memoire longue continuent exactement comme
#  avant. Seul le bloc de questions disparait du contexte de Luciana.
CLE_QUESTIONS = "questions_de_l_archiviste"
CLE_BLOC_DANS_LE_CONTEXTE = "bloc_dans_le_contexte"

# Les valeurs par defaut : EXACTEMENT celles d'aujourd'hui, pour qu'un fichier de reglage
# absent ne change strictement rien au comportement.
DEFAUT = {
    "seuil_confiance_entree": 0.55,
    "curseur_sortie_defaut": 0.35,
    "debordement_tiroir": 200,
    "plafond_caracteres": 40000,
    "paquet_sauvegarde": 25,
    "score": {
        "poids_etiquette": 1.0,
        "poids_texte": 0.9,
        "prime_par_facette": 0.04,
        "prime_facette_maxi": 0.12,
        "morceau_maxi": 700,
        "morceaux_par_fiche_maxi": 40,
    },
    "reprise": {"souvenirs_json": True, "conversation": True, "ancienne_bibliotheque": True},
    "modele_ia": "deepseek-flash",
    # ETEINT D'ORIGINE, ET C'EST LE POINT IMPORTANT : un reglage absent ou abime laisse le
    # bloc de questions ETEINT. Il ne peut pas se rallumer par accident.
    CLE_QUESTIONS: {CLE_BLOC_DANS_LE_CONTEXTE: False},
}

_CACHE = {"quand": 0.0, "valeurs": None}


def _nombre(v, defaut, mini=None, maxi=None):
    """Rend un nombre utilisable, quoi qu'il arrive. Ne leve jamais."""
    try:
        x = float(str(v).replace(",", "."))
    except Exception:
        return defaut
    if x != x:                       # un "pas un nombre" (NaN) : on reprend le defaut
        return defaut
    if mini is not None:
        x = max(mini, x)
    if maxi is not None:
        x = min(maxi, x)
    return x


def _vrai_explicite(v):
    """VRAI SEULEMENT SI C'EST ECRIT EXPRESSEMENT. TOUT LE RESTE EST FAUX.

    C'EST L'INVERSE DE LA LECTURE HABITUELLE, ET C'EST VOULU. Pour un interrupteur qui doit
    rester ETEINT, une valeur manquante, vide, abimee ou incomprehensible ne doit JAMAIS
    pouvoir valoir « allume » : sinon un fichier a moitie ecrit rallumerait le defaut tout
    seul. Seuls true, 1, oui, on, vrai ou allume — ecrits en clair — allument.
    Ne leve jamais : au moindre pepin, c'est ETEINT."""
    try:
        if v is True:
            return True
        if v is False or v is None:
            return False
        return str(v).strip().lower() in ("true", "1", "oui", "on", "vrai", "allume")
    except Exception:
        return False


def lire(force=False):
    """LES REGLAGES, relus sur le disque. Rend toujours un dictionnaire complet et sain :
    chaque valeur est bornee, et toute valeur manquante reprend son defaut. Ne leve jamais.
    Le petit cache d'une seconde evite de relire le fichier a chaque souvenir d'un paquet."""
    if not force and _CACHE["valeurs"] is not None and (time.time() - _CACHE["quand"]) < 1.0:
        return _CACHE["valeurs"]
    brut = {}
    try:
        with open(FICHIER_REGLAGE, encoding="utf-8-sig") as f:
            d = json.load(f)
        if isinstance(d, dict):
            brut = d
    except Exception:
        brut = {}

    sc_brut = brut.get("score") if isinstance(brut.get("score"), dict) else {}
    rp_brut = brut.get("reprise") if isinstance(brut.get("reprise"), dict) else {}
    qu_brut = brut.get(CLE_QUESTIONS) if isinstance(brut.get(CLE_QUESTIONS), dict) else {}
    d_sc, d_rp = DEFAUT["score"], DEFAUT["reprise"]

    v = {
        # L'ENTREE NE JETTE RIEN : ce seuil ne fait que POSER L'ETIQUETTE « en suspens ».
        "seuil_confiance_entree": _nombre(brut.get("seuil_confiance_entree"),
                                          DEFAUT["seuil_confiance_entree"], 0.0, 1.0),
        "curseur_sortie_defaut": _nombre(brut.get("curseur_sortie_defaut"),
                                         DEFAUT["curseur_sortie_defaut"], 0.0, 1.0),
        "debordement_tiroir": int(_nombre(brut.get("debordement_tiroir"),
                                          DEFAUT["debordement_tiroir"], 1, 1000000)),
        "plafond_caracteres": int(_nombre(brut.get("plafond_caracteres"),
                                          DEFAUT["plafond_caracteres"], 500, 10000000)),
        "paquet_sauvegarde": int(_nombre(brut.get("paquet_sauvegarde"),
                                         DEFAUT["paquet_sauvegarde"], 1, 100000)),
        "score": {
            "poids_etiquette": _nombre(sc_brut.get("poids_etiquette"), d_sc["poids_etiquette"], 0.0, 4.0),
            "poids_texte": _nombre(sc_brut.get("poids_texte"), d_sc["poids_texte"], 0.0, 4.0),
            "prime_par_facette": _nombre(sc_brut.get("prime_par_facette"), d_sc["prime_par_facette"], 0.0, 1.0),
            "prime_facette_maxi": _nombre(sc_brut.get("prime_facette_maxi"), d_sc["prime_facette_maxi"], 0.0, 1.0),
            "morceau_maxi": int(_nombre(sc_brut.get("morceau_maxi"), d_sc["morceau_maxi"], 50, 100000)),
            "morceaux_par_fiche_maxi": int(_nombre(sc_brut.get("morceaux_par_fiche_maxi"),
                                                   d_sc["morceaux_par_fiche_maxi"], 1, 10000)),
        },
        "reprise": {
            "souvenirs_json": bool(rp_brut.get("souvenirs_json", d_rp["souvenirs_json"])),
            "conversation": bool(rp_brut.get("conversation", d_rp["conversation"])),
            "ancienne_bibliotheque": bool(rp_brut.get("ancienne_bibliotheque",
                                                      d_rp["ancienne_bibliotheque"])),
        },
        "modele_ia": str(brut.get("modele_ia") or DEFAUT["modele_ia"]).strip() or DEFAUT["modele_ia"],
        # L'INTERRUPTEUR DU BLOC DE QUESTIONS DE L'ARCHIVISTE : ETEINT TANT QUE CE N'EST PAS
        # ECRIT EXPRESSEMENT. C'est la seule chose qui decide si ce bloc peut remonter dans
        # le contexte de Luciana (explication complete en haut de ce fichier).
        CLE_QUESTIONS: {
            CLE_BLOC_DANS_LE_CONTEXTE: _vrai_explicite(
                qu_brut.get(CLE_BLOC_DANS_LE_CONTEXTE)),
        },
        "_fichier_lu": FICHIER_REGLAGE if brut else "(reglage absent : valeurs par defaut)",
    }
    _CACHE.update(quand=time.time(), valeurs=v)
    return v


def nom_du_proprietaire():
    """17/10/2026 : le prenom du proprietaire, pour que l'archiviste ecrive « Fred » et pas
    « le proprietaire » dans les fiches de Luciana."""
    return "Fred"


def seuil_confiance():
    """LE SEUIL D'ENTREE. Il ne sert QU'A MARQUER « en suspens » : la fiche reste rangee
    a sa place dans la bibliotheque. Aucun souvenir ne disparait a l'entree."""
    return lire()["seuil_confiance_entree"]


def curseur_sortie():
    """LA PORTE DE SORTIE. Le maitre est curseur.txt (le bouton de Fred) ; le reglage ne
    sert que si ce fichier manque. Borne a [0, 1]. Ne leve jamais, et ne remonte jamais
    de lui-meme la valeur choisie par Fred."""
    try:
        with open(FICHIER_CURSEUR, encoding="utf-8-sig") as f:
            return min(1.0, max(0.0, float(f.read().strip().replace(",", "."))))
    except Exception:
        return lire()["curseur_sortie_defaut"]


#  LA PHRASE D'EXPLICATION POSEE DANS reglage_biblio2.json A COTE DE L'INTERRUPTEUR, pour
#  que le fichier de reglage se suffise a lui-meme : Fred doit pouvoir l'ouvrir et comprendre
#  sans ouvrir le code.
_EXPLICATION_DU_REGLAGE = (
    "L'INTERRUPTEUR DU BLOC DE QUESTIONS DE L'ARCHIVISTE, ET LA SEULE CHOSE QUI COMPTE. "
    "false = le bloc de questions (« ou ranger ce souvenir ? ») n'est JAMAIS injecte dans le "
    "contexte de Luciana. C'est l'etat voulu depuis le 12/10/2026 : par gros paquets, ces "
    "questions arrivaient au milieu des phrases de Fred et empechaient de travailler. "
    "ETEINT D'ORIGINE : si cette ligne manque, si elle est abimee, ou si le fichier entier "
    "manque, c'est ETEINT. Un vieux fichier QUESTIONS.txt qui traine dans "
    "~/Luciana/bibliotheque2 ne change plus rien : plus aucune ligne de code ne le lit, et "
    "plus aucune ligne de code ne l'ecrit. RIEN NE SE PERD quand c'est eteint : les "
    "questions deja ecrites, les reponses deja donnees et les fiches en attente restent "
    "intactes sur le disque. POUR REBRANCHER UN JOUR : mettre true ici (ou double-cliquer "
    "« Brancher les questions »), sans toucher au code.")


def bloc_de_questions_dans_le_contexte():
    """L'INTERRUPTEUR DU BLOC DE QUESTIONS DE L'ARCHIVISTE, relu A CHAQUE message, ET LA
    SEULE CHOSE QUI DECIDE SI CE BLOC PEUT REMONTER DANS LE CONTEXTE DE LUCIANA.

    Rend True UNIQUEMENT si reglage_biblio2.json le dit EXPRESSEMENT. Dans tous les autres
    cas — reglage absent, JSON abime, cle manquante, valeur farfelue, pepin quelconque —
    il rend False, c'est-a-dire ETEINT, et le bloc n'est PAS injecte.

    UN VIEUX FICHIER QUESTIONS.txt SUR LE DISQUE NE CHANGE RIEN : il n'est plus lu nulle
    part. Ne leve jamais."""
    try:
        return bool(lire()[CLE_QUESTIONS][CLE_BLOC_DANS_LE_CONTEXTE])
    except Exception:
        return False


def dire_l_etat_du_bloc_de_questions():
    """L'ETAT DE L'INTERRUPTEUR, EN CLAIR, POUR FRED, SANS RIEN ECRIRE. Ne leve jamais."""
    try:
        allume = bloc_de_questions_dans_le_contexte()
        return ("LE BLOC DE QUESTIONS DE L'ARCHIVISTE EST %s.\n"
                "  reglage lu dans : %s\n"
                "  la ligne qui decide : \"%s\" -> \"%s\" = %s\n"
                "  %s"
                % ("BRANCHE" if allume else "DEBRANCHE",
                   lire()["_fichier_lu"], CLE_QUESTIONS, CLE_BLOC_DANS_LE_CONTEXTE,
                   "true" if allume else "false",
                   ("Les questions de l'archiviste remontent dans le contexte de Luciana."
                    if allume else
                    "Aucune question ne remonte dans le contexte de Luciana. Les questions "
                    "deja ecrites, les reponses deja donnees et les fiches en attente "
                    "restent intactes sur le disque.")))
    except Exception as ex:
        return "Etat illisible : %s" % str(ex)[:160]


def regler_le_bloc_de_questions(allume, confirme_par_le_proprietaire=False):
    """ECRIT L'INTERRUPTEUR DANS reglage_biblio2.json. Rend (c_est_fait, phrase_pour_Fred).

    LA SEULE FONCTION DE TOUT LE PROGRAMME QUI SAIT ECRIRE CET INTERRUPTEUR, et elle n'est
    appelee QUE depuis la ligne de commande, en bas de ce fichier, c'est-a-dire par les deux
    boutons de Fred (« Brancher les questions » / « Debrancher les questions »). AUCUN AUTRE
    ENDROIT DU PROGRAMME NE L'APPELLE : c'est ce qui garantit que le programme ne peut pas
    se rallumer tout seul, ni au demarrage ni a aucun autre moment.

    LE GARDE-FOU 'confirme_par_le_proprietaire' EST LA POUR CA : meme un appel fait par
    distraction, ou ajoute un jour par erreur, ne change rien du tout sans ce mot-la.

    ELLE NE TOUCHE QUE CETTE LIGNE-LA. Le reste du fichier de reglage est relu et reecrit a
    l'identique, commentaires compris. ELLE N'OUVRE AUCUNE DONNEE DE FRED, ni en lecture ni
    en ecriture : elle ne connait que reglage_biblio2.json, qui est a cote du code.
    Ne leve jamais."""
    if confirme_par_le_proprietaire is not True:
        return (False, "Rien n'a change : cet interrupteur ne s'ecrit que sur une demande "
                       "explicite du proprietaire.")
    voulu = bool(allume)
    try:
        d = {}
        try:
            with open(FICHIER_REGLAGE, encoding="utf-8-sig") as f:
                lu = json.load(f)
            if isinstance(lu, dict):
                d = lu
        except Exception:
            d = {}
        bloc = d.get(CLE_QUESTIONS)
        if not isinstance(bloc, dict):
            bloc = {}
        bloc[CLE_BLOC_DANS_LE_CONTEXTE] = voulu
        bloc.setdefault("_bloc_dans_le_contexte", _EXPLICATION_DU_REGLAGE)
        d[CLE_QUESTIONS] = bloc
        d["modifie_le"] = time.strftime("%Y-%m-%d")
        #  ECRITURE DE REMPLACEMENT : on ecrit a cote, puis on bascule d'un coup. Une coupure
        #  de courant ne peut pas laisser le reglage a moitie ecrit (et un reglage a moitie
        #  ecrit serait relu comme ETEINT, jamais comme allume).
        tmp = FICHIER_REGLAGE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        os.replace(tmp, FICHIER_REGLAGE)
        lire(force=True)
        return (True, dire_l_etat_du_bloc_de_questions())
    except Exception as ex:
        return (False, "Le reglage n'a pas pu etre ecrit (%s). RIEN N'A CHANGE, et le bloc "
                       "de questions reste dans l'etat ou il etait." % str(ex)[:160])


def plafond():
    return lire()["plafond_caracteres"]


def reglages_score():
    return lire()["score"]


def dire_les_reglages():
    """Une phrase claire, pour Fred, qui DIT d'ou viennent les nombres utilises."""
    v = lire()
    return ("Reglages lus dans : %s\n"
            "  seuil d'entree (marque « en suspens », ne jette rien) : %.2f\n"
            "  curseur de sortie en service : %.2f  (maitre : %s)\n"
            "  plafond envoye a Luciana : %d caracteres\n"
            "  tiroir trop plein au-dela de : %d fiches\n"
            "  sauvegarde tous les : %d souvenirs\n"
            "  score : etiquette x%.2f, texte x%.2f, prime par facette %.2f (maxi %.2f)"
            % (v["_fichier_lu"], v["seuil_confiance_entree"], curseur_sortie(),
               FICHIER_CURSEUR if os.path.exists(FICHIER_CURSEUR) else "reglage_biblio2.json",
               v["plafond_caracteres"], v["debordement_tiroir"], v["paquet_sauvegarde"],
               v["score"]["poids_etiquette"], v["score"]["poids_texte"],
               v["score"]["prime_par_facette"], v["score"]["prime_facette_maxi"]))


if __name__ == "__main__":
    import sys

    #  =====================================================================
    #  LA LIGNE DE COMMANDE : C'EST PAR ICI, ET PAR ICI SEULEMENT, QUE
    #  L'INTERRUPTEUR DU BLOC DE QUESTIONS S'ECRIT.
    #  =====================================================================
    #  Les deux boutons de Fred (« Brancher les questions » / « Debrancher les questions »)
    #  appellent ces trois commandes-la, et rien d'autre. Le programme lui-meme, quand il
    #  tourne, ne passe JAMAIS par ici : il ne fait que LIRE le reglage.
    _args = [str(a).strip().lower() for a in sys.argv[1:]]
    if "--allumer-les-questions" in _args or "--eteindre-les-questions" in _args:
        _veut_allumer = "--allumer-les-questions" in _args
        _ok, _phrase = regler_le_bloc_de_questions(_veut_allumer,
                                                   confirme_par_le_proprietaire=True)
        print(_phrase)
        raise SystemExit(0 if _ok else 1)
    if "--etat-des-questions" in _args:
        print(dire_l_etat_du_bloc_de_questions())
        raise SystemExit(0)

    print(dire_les_reglages())
    print()
    print(dire_l_etat_du_bloc_de_questions())
    print("\n=== CONTROLES ===")
    v = lire(force=True)
    assert 0.0 <= v["seuil_confiance_entree"] <= 1.0
    assert 0.0 <= v["curseur_sortie_defaut"] <= 1.0
    assert v["curseur_sortie_defaut"] <= 0.35 + 1e-9, \
        "le curseur par defaut reste a 0.35 au plus : on ne remonte pas le reglage de Fred"
    assert v["plafond_caracteres"] > 0 and v["paquet_sauvegarde"] > 0
    assert isinstance(v["score"]["morceau_maxi"], int)
    print("OK : le fichier de reglage est lu, borne, et complet meme s'il manque des cles.")

    #  =====================================================================
    #  LES CONTROLES DU 12/10/2026 : L'INTERRUPTEUR EST ETEINT D'ORIGINE, ET
    #  RIEN NE PEUT L'ALLUMER PAR ACCIDENT.
    #  =====================================================================
    print("\n=== CONTROLES DE L'INTERRUPTEUR DU BLOC DE QUESTIONS ===")

    #  1) Il faut l'ecrire EXPRESSEMENT pour allumer. Tout le reste est ETEINT.
    for _mauvais in (None, "", " ", "false", "non", "0", "peut-etre", [], {}, 0, 2,
                     "vraiment pas", "FALSE"):
        assert _vrai_explicite(_mauvais) is False, \
            "une valeur qui ne dit pas clairement « allume » doit laisser ETEINT : %r" % (
                _mauvais,)
    for _bon in (True, "true", "TRUE", " Oui ", "1", "on", "vrai", "allume"):
        assert _vrai_explicite(_bon) is True, "ecrit en clair, ca doit allumer : %r" % (_bon,)
    print("  OK   il faut ecrire true (ou oui/1/on/vrai) EXPRESSEMENT pour allumer ; une "
          "valeur absente, vide ou abimee laisse ETEINT")

    #  2) LE FICHIER DE REGLAGE ENTIEREMENT ABSENT : c'est ETEINT. On le prouve en faisant
    #     pointer la lecture vers un fichier qui n'existe pas. ON N'ECRIT RIEN, ET ON NE
    #     TOUCHE A AUCUNE DONNEE : on remet le vrai chemin juste apres.
    _vrai_chemin = FICHIER_REGLAGE
    FICHIER_REGLAGE = os.path.join(DOSSIER_CODE, "_reglage_qui_n_existe_pas.json")
    assert lire(force=True)[CLE_QUESTIONS][CLE_BLOC_DANS_LE_CONTEXTE] is False
    assert bloc_de_questions_dans_le_contexte() is False
    FICHIER_REGLAGE = _vrai_chemin
    lire(force=True)
    print("  OK   reglage entierement absent : le bloc de questions est ETEINT (il ne peut "
          "pas se rallumer parce qu'un fichier manque)")

    #  3) LE GARDE-FOU DU SEUL ECRIVAIN : sans la confirmation du proprietaire, l'ecriture
    #     ne fait RIEN. Ce controle n'ecrit donc rien non plus.
    _avant = bloc_de_questions_dans_le_contexte()
    _fait, _dit = regler_le_bloc_de_questions(True)
    assert _fait is False and bloc_de_questions_dans_le_contexte() == _avant, \
        "sans confirmation explicite, l'interrupteur ne doit pas bouger"
    print("  OK   le programme ne peut pas rallumer l'interrupteur tout seul : sans la "
          "confirmation explicite du proprietaire, l'ecriture ne fait rien")

    #  4) L'ETAT LIVRE AUJOURD'HUI : ETEINT.
    print("  %s l'etat livre aujourd'hui : le bloc de questions est %s"
          % ("OK  " if not bloc_de_questions_dans_le_contexte() else "NOTE",
             "DEBRANCHE" if not bloc_de_questions_dans_le_contexte() else "BRANCHE"))
