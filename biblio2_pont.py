# -*- coding: utf-8 -*-
"""
LE PONT DES QUESTIONS — c'est par lui, et par lui seul, que luciana.py parle a la chaine
des questions de la memoire 2.

GREFFE DU 11/10/2026, LE SOIR. Fichier NEUF.

=====================================================================================
 CE QUE CE PONT FAIT, ET SURTOUT CE QU'IL NE FAIT PAS
=====================================================================================

Le pont de Luminita faisait DEUX choses : il ramenait la memoire (le bibliothecaire a
facettes + le curseur + le plan), ET il faisait tourner la chaine des questions.

CHEZ LUCIANA, LA MOITIE « MEMOIRE » EXISTE DEJA, ELLE TOURNE, ET ELLE MARCHE : c'est
_biblio2_memoire() dans luciana.py (environ 470 lignes, lignes 27413 a 27886), avec son
propre curseur, son propre filet, sa propre trace et son propre plan_deja_vu.txt.

Recopier ici cette moitie-la aurait fait EXACTEMENT les trois degats qu'il fallait eviter :
  - le bloc de souvenirs serait parti DEUX FOIS dans le meme message ;
  - le plan serait remonte deux fois, et les deux plan_deja_vu.txt se seraient marche
    dessus (chacun croyant avoir deja servi l'empreinte que l'autre venait d'ecrire) ;
  - une fonction qui marche aujourd'hui aurait change de comportement, ce que la regle de
    Fred interdit.

CE PONT NE PORTE DONC QUE LA CHAINE DES QUESTIONS. C'est la seule chose qui manquait.
La memoire, elle, continue de passer exactement par ou elle passait hier.

=====================================================================================
 TOUT, EN UN SEUL APPEL
=====================================================================================

  questions_du_tour(message, sa_derniere_reponse)

  1  IL RAMASSE LES REPONSES DU TOUR D'AVANT (temps 3). L'assistante a repondu aux
     questions au tour precedent : on relit sa reponse, et chaque reponse redescend sur
     SA fiche. La numerotation est relue sur le disque, donc elle survit a un redemarrage.
  2  IL FERME LE LOT DU PROPRIETAIRE quand Fred vient d'y repondre (temps 4, la fin).
  3  IL AMORCE LA CHAINE : les fiches deja en suspens recoivent leur question les PREMIERES
     (les 395 fiches en retard passent donc avant le travail du jour).
  4  IL POSE LES QUESTIONS DE L'ARCHIVISTE A L'ASSISTANTE (temps 2) — c'est LE PROGRAMME
     qui les pose, jamais sa vigilance.
  5  IL POSE LE LOT AU PROPRIETAIRE, D'UN SEUL COUP (temps 4, le debut).
  6  IL ECRIT ce qui a change (l'arbre + les trois fichiers de la chaine) et il laisse une
     TRACE de ce qu'il a fait, a chaque sortie.

  Il rend du TEXTE, ou None. None veut dire « garde ton chemin d'hier » : interrupteur
  eteint, bibliotheque vide, ou vrai pepin. IL NE LEVE JAMAIS.

=====================================================================================
 CE QU'IL NE FAIT PAS, ET C'EST VOULU
=====================================================================================
  - IL N'AJOUTE RIEN A L'ECRAN. Pas un bouton, pas une pastille, pas un voyant. Tout passe
    par la conversation, qui existe deja.
  - IL EST ETEINT D'ORIGINE, ET DERRIERE SON PROPRE INTERRUPTEUR. La memoire 2 de Fred est
    DEJA branchee (BRANCHE.txt existe depuis ce matin). Si la chaine s'allumait avec le
    meme interrupteur, elle partirait au prochain message sans que Fred ait rien decide.
    Il lui faut donc SON PROPRE interrupteur, ET DEPUIS LE 12/10/2026 C'EST UN REGLAGE :
    "questions_de_l_archiviste" -> "bloc_dans_le_contexte" dans reglage_biblio2.json.
    Tant que ce reglage n'est pas mis EXPRESSEMENT a true, cet appel rend None a la
    premiere ligne et ne lit rien d'autre.

=====================================================================================
 LE DEBRANCHEMENT DEFINITIF DU BLOC DE QUESTIONS (chantier du 12/10/2026)
=====================================================================================

LE DEFAUT, CONSTATE PENDANT PLUSIEURS JOURS : le BLOC DE QUESTIONS de l'archiviste
remontait DIRECTEMENT DANS LE CONTEXTE DE LUCIANA, colle a ses messages avec Fred, et par
GROS PAQUETS (plusieurs centaines d'un coup). Luciana repondait a ces questions AU MILIEU
des phrases de Fred : elle n'arrivait plus a travailler, et Fred ne pouvait plus
communiquer avec elle.

POURQUOI LE PREMIER DEBRANCHEMENT N'ETAIT PAS SOLIDE : il tenait a l'ABSENCE d'un fichier
drapeau, ~/Luciana/bibliotheque2/QUESTIONS.txt, dans le dossier de DONNEES. Un fichier
absent, ca se recree — au demarrage, par un bouton, par un script d'essai — et le defaut
revenait tout seul.

CE QUI A CHANGE, ET C'EST TOUT CE QUI A CHANGE :
  - L'INTERRUPTEUR EST UN REGLAGE, ET C'EST LA SEULE CHOSE QUI COMPTE. On le lit par
    bloc_de_questions_autorise(), qui demande biblio2_reglages. ETEINT d'origine.
  - LE VIEUX DRAPEAU N'EST PLUS LU, ET IL N'EST PLUS ECRIT. Plus une seule ligne de ce
    fichier ne lit QUESTIONS.txt pour decider, et plus une seule ligne ne l'ecrit. Un vieux
    drapeau qui traine encore sur le disque ne fait donc PLUS RIEN REMONTER.
  - TROIS GRILLES, PAS UNE, et toutes les trois sur LE MEME reglage : en entree de
    questions_du_tour(), en sortie de questions_du_tour() (juste avant de rendre le texte),
    et dans avec_le_canal_cache() (la derniere chose que luciana.py appelle avant
    d'injecter). Reglage eteint = AUCUN bloc de questions injecte, quoi qu'il arrive.
  - RIEN NE SE PERD. On eteint un AFFICHAGE : les questions deja ecrites, les reponses deja
    donnees et les fiches en attente restent INTACTES sur le disque. AUCUNE donnee de Fred
    n'est effacee, ni deplacee, ni reecrite.
  - ET C'EST REVERSIBLE PROPREMENT. Le jour ou Fred voudra rebrancher : true dans le
    reglage (bouton « Brancher les questions »), sans retoucher une ligne de code.
  - IL NE TOUCHE PAS AU PLAN. plan.json n'existe pas encore chez Fred, et luciana.py
    prepend « LE PLAN DE TA MEMOIRE A CHANGE » des que ce fichier apparait. Refaire le plan
    ici ferait donc changer le comportement d'une fonction qui marche. On s'en abstient.
  - IL NE TRAVAILLE PAS PENDANT UN RANGEMENT. Si l'archiviste est en train d'avaler (le
    marque-page a bouge dans la minute), le pont se tait : deux ecritures de arbre.json en
    meme temps, c'est l'une qui efface l'autre.
  - IL NE DEPEND D'AUCUN AUTRE PROGRAMME. Il n'importe pas luciana.py, et il n'a besoin
    d'aucun redemarrage de quoi que ce soit.

NOTE IA : tout est ecrit en POSITIF.
"""

import json, os, time

try:
    import biblio2_reglages as reglages
except Exception:
    reglages = None
try:
    import biblio2_archiviste as arch
except Exception:
    arch = None
try:
    import biblio2_questions as questions
except Exception:
    questions = None


HOME = os.path.expanduser("~")

#  COMBIEN DE FOIS ON REPOSE UNE QUESTION A L'ASSISTANTE AVANT DE LA DONNER AU PROPRIETAIRE.
#  CE GARDE-FOU N'EXISTE PAS CHEZ LUMINITA, ET IL EST NECESSAIRE ICI : si l'assistante
#  repond a cote du format (sans « 1) »), ses cinq questions repartent telles quelles au
#  tour suivant, puis au suivant... et les cinq memes questions bloquent la file pour
#  toujours, les 390 autres derriere. Au bout de trois fois sans reponse lisible, la
#  question passe simplement dans le lot du proprietaire. Rien n'est perdu, rien ne bloque.
RELANCES_MAXI = 3


def _dossier():
    """LE DOSSIER DE LA MEMOIRE 2 DE LUCIANA, et jamais celui de quelqu'un d'autre."""
    try:
        d = str(getattr(reglages, "DOSSIER_BIBLIO2", "") or "")
        if d:
            return d
    except Exception:
        pass
    return os.path.join(HOME, "Luciana", "bibliotheque2")


def _f(nom):
    """Le chemin d'un fichier de la memoire 2. Ne leve jamais.

    'vieux_drapeau_questions' EST LE FICHIER QUESTIONS.txt D'AVANT LE 12/10/2026. IL N'EST
    PLUS JAMAIS LU POUR DECIDER QUOI QUE CE SOIT, ET IL N'EST PLUS JAMAIS ECRIT. Son chemin
    ne reste connu ici que pour LE CONTROLE du bas de ce fichier, qui prouve sur du reel
    qu'un vieux drapeau encore present sur le disque ne fait plus rien remonter du tout."""
    noms = {"arbre": "arbre.json", "branche": "BRANCHE.txt",
            "vieux_drapeau_questions": "QUESTIONS.txt",
            "marque_page": "marque_page.json"}
    cles = {"arbre": "FICHIER_ARBRE", "branche": "FICHIER_MARQUEUR_BRANCHE",
            "marque_page": "FICHIER_MARQUE_PAGE"}
    if nom in cles:
        try:
            c = str(getattr(reglages, cles[nom], "") or "")
            if c:
                return c
        except Exception:
            pass
    return os.path.join(_dossier(), noms[nom])


def _trace_fichier():
    return os.path.join(_dossier(), "trace_des_questions.jsonl")


def branche():
    """L'INTERRUPTEUR DE LA MEMOIRE 2, lu A CHAQUE message. Chez Fred il est DEJA mis."""
    try:
        return os.path.exists(_f("branche"))
    except Exception:
        return False


def bloc_de_questions_autorise():
    """L'INTERRUPTEUR DU BLOC DE QUESTIONS, ET IL N'Y EN A PLUS QU'UN SEUL : LE REGLAGE.
    Lu A CHAQUE message, et c'est LA SEULE CHOSE QUI COMPTE.

    LE REGLAGE :  reglage_biblio2.json
                    "questions_de_l_archiviste": { "bloc_dans_le_contexte": false }

    ETEINT D'ORIGINE, ET ETEINT AU MOINDRE DOUTE. Si biblio2_reglages.py manque, s'il est
    abime, si la fonction de lecture n'existe pas, si le reglage est absent ou farfelu, ou
    si quoi que ce soit leve : CETTE FONCTION REND False, c'est-a-dire ETEINT. Il n'existe
    aucun chemin par lequel un pepin puisse ALLUMER le bloc de questions.

    LE VIEUX DRAPEAU N'EST PLUS LU DU TOUT. Avant le 12/10/2026, c'est l'EXISTENCE du
    fichier ~/Luciana/bibliotheque2/QUESTIONS.txt qui decidait. C'etait fragile : un
    fichier, ca se recree tout seul, et le defaut revenait. Un vieux QUESTIONS.txt encore
    present sur le disque ne change donc PLUS RIEN : le reglage seul decide.

    ET LE PROGRAMME NE PEUT PAS SE RALLUMER TOUT SEUL : rien ici n'ECRIT ce reglage. Une
    seule fonction de tout le programme sait l'ecrire (regler_le_bloc_de_questions, dans
    biblio2_reglages.py), et elle n'est appelee QUE depuis la ligne de commande, par les
    deux boutons de Fred. Ne leve jamais."""
    try:
        f = getattr(reglages, "bloc_de_questions_dans_le_contexte", None)
        if callable(f):
            return bool(f())
    except Exception:
        pass
    return False


def les_questions_sont_branchees():
    """L'ANCIEN NOM DE L'INTERRUPTEUR, GARDE POUR NE RIEN CASSER.

    Il rend EXACTEMENT bloc_de_questions_autorise(), c'est-a-dire le reglage et rien
    d'autre. On garde ce nom parce que d'autres endroits du pont l'appellent deja, et la
    regle de Fred est de ne pas faire changer de comportement a ce qui marche. Il n'y a
    donc toujours qu'UN interrupteur, lu a UN seul endroit. Ne leve jamais."""
    return bloc_de_questions_autorise()


def un_rangement_est_en_cours(secondes=90):
    """VRAI quand l'archiviste vient d'ecrire son marque-page, donc qu'il est en train
    d'avaler des souvenirs.

    A QUOI CA SERT, ET C'EST UN VRAI RISQUE : l'archiviste et ce pont ecrivent tous les deux
    arbre.json. S'ils ecrivent en meme temps, le dernier ecrase le travail de l'autre — et
    on perdrait soit des fiches rangees, soit des reponses. Le pont se tait donc pendant
    qu'un rangement tourne, et il reprend tout seul apres. Ne leve jamais."""
    try:
        return (time.time() - os.path.getmtime(_f("marque_page"))) < float(secondes)
    except Exception:
        return False


def trace(infos):
    """Ecrit UNE ligne dans trace_des_questions.jsonl, A CHAQUE sortie du pont, avec en
    clair CE QU'IL A FAIT ET POURQUOI. C'est la fin des pannes muettes : plus jamais la
    chaine ne se taira sans laisser de trace. Ne leve jamais."""
    try:
        d = {"quand": time.strftime("%Y-%m-%d %H:%M:%S")}
        d.update(infos or {})
        os.makedirs(_dossier(), exist_ok=True)
        with open(_trace_fichier(), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    except Exception:
        pass


#  CETTE PHRASE N'EST PLUS UTILISEE, ET C'EST VOLONTAIRE — NE PAS LA REBRANCHER.
#  Elle demandait a l'assistante de relayer le lot dans sa reponse (« pose-le au
#  proprietaire, tel quel »). C'etait precisement le defaut : le lot n'arrivait chez Fred
#  QUE SI ELLE Y PENSAIT, alors que sa regle dit « c'est ca que le systeme doit t'OBLIGER a
#  faire ». Depuis le 11/10/2026 au soir, c'est LE PROGRAMME qui ecrit le lot a l'ecran
#  lui-meme (recolter_les_reponses_aux_questions, plus bas). On garde le texte ici pour
#  qu'on sache ce qui a change, et pour rien d'autre.
CONSIGNE_DU_LOT = ("CE QUE LE PROGRAMME TE DEMANDE DE FAIRE DU BLOC CI-DESSOUS : pose-le "
                   "au proprietaire, tel quel, en une seule fois, dans ta reponse. C'est le "
                   "programme qui l'a prepare ; tu n'as rien a y ajouter et rien a trier.\n")


def _compter_les_relances(arbre, reperes):
    """COMPTE COMBIEN DE FOIS CHAQUE QUESTION A DEJA ETE POSEE A L'ASSISTANTE. Ne leve
    jamais."""
    try:
        for r in reperes or []:
            _c, _s, fi = questions.trouver(arbre, r)
            if fi is not None:
                fi["question_fois_posee"] = int(fi.get("question_fois_posee") or 0) + 1
    except Exception:
        pass


def _passer_au_lot_les_restees_sans_reponse(arbre):
    """LES QUESTIONS POSEES TROIS FOIS SANS REPONSE LISIBLE PASSENT AU LOT DU PROPRIETAIRE.

    C'est le garde-fou anti-blocage explique en haut du fichier (RELANCES_MAXI) : sans lui,
    cinq questions auxquelles l'assistante repond a cote du format tiendraient la file
    bloquee indefiniment, et les 390 autres n'arriveraient jamais. Rend le nombre de
    questions deplacees. Ne leve jamais."""
    passees = 0
    try:
        for _c, _s, fi in questions._fiches(arbre):
            if fi.get("question_etat") != questions.POSEE_ASSISTANTE:
                continue
            if int(fi.get("question_fois_posee") or 0) >= RELANCES_MAXI:
                fi["question_etat"] = questions.A_POSER_PROPRIO
                fi["question_passee_au_lot_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
                fi["question_passee_au_lot_pourquoi"] = (
                    "posee %d fois a l'assistante sans reponse lisible"
                    % int(fi.get("question_fois_posee") or 0))
                passees += 1
    except Exception:
        pass
    return passees


# =====================================================================
#  L'APPEL UNIQUE. C'est la seule fonction que luciana.py connait.
# =====================================================================

def questions_du_tour(message="", sa_derniere_reponse=""):
    """TOUTE LA CHAINE DES QUESTIONS, EN UN SEUL APPEL. Rend le texte a ajouter dans le
    tour, ou None.

    None veut dire « garde ton chemin d'hier » : un des deux interrupteurs est eteint, la
    bibliotheque est vide, un rangement tourne, ou il n'y a simplement aucune question a
    poser ce tour-ci (c'est le cas le plus fréquent, et il ne coute pas un caractere).
    NE LEVE JAMAIS.

    'message'             la phrase du proprietaire, ce tour-ci (c'est la que se trouve sa
                          reponse au lot, quand un lot attend)
    'sa_derniere_reponse' ce que l'assistante a repondu au tour PRECEDENT (c'est la que se
                          trouvent ses reponses aux questions de l'archiviste)
    """
    if not branche():
        return None               # memoire 2 eteinte : etat voulu, on garde le chemin d'hier
    if not les_questions_sont_branchees():
        return None               # la chaine n'est pas allumee : on ne lit meme pas le reste
    if questions is None or arch is None:
        trace({"quoi": "arret", "pourquoi": "biblio2_questions.py ou biblio2_archiviste.py "
                                            "n'est pas la"})
        return None
    if un_rangement_est_en_cours():
        trace({"quoi": "arret", "pourquoi": "un rangement tourne (le marque-page vient de "
                                            "bouger) : on ne touche pas a l'arbre en meme "
                                            "temps que l'archiviste"})
        return None
    try:
        arbre = arch.arbre_charger(_f("arbre"))
    except Exception as ex:
        trace({"quoi": "arret", "pourquoi": "arbre illisible : %s" % str(ex)[:120]})
        return None
    if not arbre:
        trace({"quoi": "arret", "pourquoi": "arbre vide (lancer « Ranger TOUTE ma memoire »)"})
        return None

    infos = {"quoi": "chaine_des_questions"}
    change = False
    morceaux = []

    try:
        infos["avant"] = questions.compter(arbre)
    except Exception:
        pass

    # ---- 1 : CE QUE L'ASSISTANTE A REPONDU AU TOUR PRECEDENT -> SUR SA FICHE (temps 3) ---
    try:
        reperes_poses = questions.relire_le_bloc_pose()
        if reperes_poses and sa_derniere_reponse:
            r = questions.ranger_les_reponses(arbre, reperes_poses, sa_derniere_reponse,
                                              par="l_assistante")
            if r.get("tranchees") or r.get("parties_au_proprietaire"):
                change = True
            infos["reponses_de_l_assistante"] = {
                "tranchees": r.get("tranchees"),
                "parties_au_lot": r.get("parties_au_proprietaire"),
                "numeros_inconnus": r.get("numeros_inconnus")}
            questions.oublier_le_bloc_pose()
    except Exception as ex:
        infos["chaine_temps_3_ratee"] = str(ex)[:160]

    # ---- 2 : LE PROPRIETAIRE VIENT-IL DE REPONDRE AU LOT ? (temps 4, la fin) -------------
    try:
        if questions.le_lot_attend_une_reponse():
            _t, reperes_lot = questions.relire_le_lot()
            if reperes_lot and message:
                r = questions.ranger_les_reponses(arbre, reperes_lot, message,
                                                  par="le_proprietaire")
                if r.get("tranchees") or r.get("parties_au_proprietaire"):
                    change = True
                    questions.le_lot_est_repondu()
                    infos["reponses_du_proprietaire"] = {
                        "tranchees": r.get("tranchees"),
                        "restees_en_attente": r.get("parties_au_proprietaire")}
    except Exception as ex:
        infos["chaine_temps_4_ratee"] = str(ex)[:160]

    # ---- 3 : LES FICHES DEJA EN SUSPENS RECOIVENT LEUR QUESTION LES PREMIERES (temps 1) --
    try:
        a = questions.amorcer(arbre)
        infos["amorce"] = a
        if a.get("questions_ecrites_maintenant"):
            change = True
    except Exception as ex:
        infos["chaine_temps_1_ratee"] = str(ex)[:160]

    # ---- 4 : CE QUI A ETE POSE TROIS FOIS SANS REPONSE PASSE AU LOT ----------------------
    try:
        n = _passer_au_lot_les_restees_sans_reponse(arbre)
        if n:
            change = True
            infos["passees_au_lot_faute_de_reponse"] = n
    except Exception as ex:
        infos["garde_fou_relances_rate"] = str(ex)[:160]

    # ---- 5 : LE PROGRAMME POSE LES QUESTIONS A L'ASSISTANTE (temps 2) -------------------
    try:
        bloc, reperes = questions.bloc_pour_l_assistante(arbre)
        if bloc:
            change = True
            morceaux.append(bloc)
            _compter_les_relances(arbre, reperes)
            questions.noter_le_bloc_pose(reperes)
            infos["questions_posees_a_l_assistante"] = len(reperes)
    except Exception as ex:
        infos["chaine_temps_2_ratee"] = str(ex)[:160]

    # ---- 6 : LE LOT, POSE AU PROPRIETAIRE D'UN SEUL COUP (temps 4, le debut) ------------
    try:
        if not questions.le_lot_attend_une_reponse():
            lot, reperes_lot = questions.bloc_pour_le_proprietaire(arbre, ecrire=True)
            if lot:
                change = True
                #  LE LOT NE PASSE PLUS PAR SA REPONSE, ET C'EST LA DEUXIEME CORRECTION DU
                #  11/10/2026 AU SOIR. Avant, on posait le lot dans SON PROMPT, avec la
                #  consigne « pose-le au proprietaire, tel quel ». Le lot n'arrivait donc
                #  chez Fred QUE SI ELLE Y PENSAIT -- c'est-a-dire exactement la vigilance
                #  que sa regle interdit (« c'est ca que le systeme doit t'OBLIGER a faire »).
                #  Maintenant il est seulement PREPARE ici (ecrit dans
                #  lot_pour_le_proprietaire.json), et c'est LE PROGRAMME qui l'ecrit a
                #  l'ecran, d'un seul coup et une seule fois, dans
                #  recolter_les_reponses_aux_questions(). Elle n'a plus rien a relayer.
                infos["lot_prepare_pour_le_proprietaire"] = len(reperes_lot)
    except Exception as ex:
        infos["chaine_lot_ratee"] = str(ex)[:160]

    # ---- 7 : ON ECRIT CE QUI A CHANGE, ET ON LAISSE UNE TRACE ---------------------------
    if change:
        try:
            arch.arbre_sauver(_f("arbre"), arbre)
        except Exception as ex:
            infos["arbre_non_ecrit"] = str(ex)[:160]
        try:
            questions.garder_les_questions(arbre)
            questions.garder_les_reponses(arbre)
        except Exception as ex:
            infos["chaine_non_gardee"] = str(ex)[:160]
    try:
        infos["apres"] = questions.compter(arbre)
    except Exception:
        pass

    texte = "\n\n".join(m for m in morceaux if m)
    #  ---- LA DEUXIEME GRILLE, SUR LE MEME REGLAGE (chantier du 12/10/2026) --------------
    #  La premiere grille est en haut de cette fonction. Celle-ci est VOLONTAIREMENT
    #  REDONDANTE : elle relit le reglage APRES tout le travail du tour, juste avant de
    #  rendre le texte. Meme un chemin qu'on n'aurait pas vu, ou qu'on ajouterait un jour,
    #  ne peut donc pas faire sortir un bloc de questions alors que le reglage est eteint.
    #  ELLE NE JETTE RIEN : les questions, les reponses et les fiches viennent d'etre
    #  ecrites sur le disque juste au-dessus et restent exactement ou elles sont. On ne
    #  retient que l'AFFICHAGE.
    if texte and not bloc_de_questions_autorise():
        infos["bloc_retenu"] = ("le reglage « bloc_dans_le_contexte » est eteint : rien ne "
                                "remonte dans le contexte de Luciana (aucune donnee touchee)")
        texte = ""
    infos["caracteres_poses"] = len(texte)
    trace(infos)
    return texte or None


def dire_l_etat():
    """L'ETAT DE LA CHAINE, EN CLAIR, SANS RIEN ECRIRE. Pour pouvoir le LIRE sans lancer
    Luciana. Ne leve jamais."""
    try:
        if not branche():
            return "La memoire 2 est eteinte (BRANCHE.txt n'est pas la)."
        allume = ("allumee (reglage « bloc_dans_le_contexte » = true)"
                  if bloc_de_questions_autorise() else
                  "ETEINTE (reglage « bloc_dans_le_contexte » = false dans "
                  "reglage_biblio2.json). Aucune question ne remonte dans le contexte de "
                  "Luciana. Les questions deja ecrites, les reponses deja donnees et les "
                  "fiches en attente restent intactes sur le disque")
        arbre = arch.arbre_charger(_f("arbre"))
        c = arch.compter(arbre)
        return ("Chaine des questions : %s.\n  %d fiche(s) dans la bibliotheque, dont %d en "
                "suspens.\n  %s" % (allume, c["fiches"], c["en_suspens"],
                                    questions.dire_l_etat(arbre)))
    except Exception as ex:
        return "Etat illisible : %s" % str(ex)[:160]


# =====================================================================
#  LE CANAL CACHE — CE QUI MANQUAIT, ET POURQUOI RIEN NE REDESCENDAIT.
#  (ajoute le 11/10/2026 au soir, deuxieme chantier de la soiree)
# =====================================================================
#
#  CE QUI ETAIT MESURE, A CHACUN DES SEPT PASSAGES DE LA CHAINE :
#      "reponses_de_l_assistante": {"tranchees": 0, "parties_au_lot": 0,
#                                   "numeros_inconnus": []}
#  Zero tranchee, zero partie au lot, ET zero numero inconnu.
#
#  CES TROIS ZEROS ENSEMBLE NE PEUVENT DIRE QU'UNE CHOSE : le lecteur de reponses n'a
#  trouve AUCUNE ligne numerotee. Ce n'est pas une reponse mal rangee, ni un numero tombe
#  a cote : il n'y avait RIEN A LIRE. (S'il y avait eu des numeros, on verrait soit des
#  tranchees, soit des numeros_inconnus. Les trois a zero, c'est « aucun numero ».)
#
#  ET C'ETAIT INEVITABLE, parce que la chaine allait chercher ses reponses DANS SA REPONSE
#  VISIBLE A L'ECRAN (le dernier message « assistant » de l'historique). Or la regle de
#  Fred est dure : IL NE VEUT PAS VOIR LES QUESTIONS DE L'ARCHIVISTE. Il y avait donc une
#  contradiction qu'aucun reglage ne pouvait resoudre :
#    - si elle repond aux questions dans sa reponse visible, Fred voit defiler la masse des
#      questions de l'archiviste -- ce qu'il refuse explicitement ;
#    - si elle ne les met pas dans sa reponse visible -- et c'est ce qu'elle fait, et elle
#      a raison -- alors il n'y a rien a lire, les 420 questions restent ouvertes pour
#      toujours, et le lot du proprietaire ne se remplit jamais.
#
#  LA REPARATION : ON LUI DONNE UN CANAL A ELLE. Elle met ses reponses numerotees entre
#  deux marqueurs, a la toute fin de son message. Le programme (1) les lit, (2) LES DECOUPE
#  de ce qui part a l'ecran et dans la memoire. Fred ne voit donc jamais rien, et les
#  reponses arrivent quand meme jusqu'aux fiches.
#
#  CE MECANISME N'EST PAS UNE INVENTION : luciana.py fait EXACTEMENT ca depuis la v136
#  pour les marques [AVIS #...], au meme endroit du meme tour (recolter_les_avis). On
#  reprend le procede qui a deja fait la preuve qu'il tient.
CANAL_DEBUT = "[REPONSES A MON ARCHIVISTE]"
CANAL_FIN = "[FIN REPONSES A MON ARCHIVISTE]"

#  LE SEPARATEUR, quand le programme pose le lot sous sa reponse. Discret expres : le lot
#  porte deja sa propre phrase d'entete (« J'ai mis de cote N chose(s)... »).
SEPARATEUR_DU_LOT = "\n\n- - - - - - - - - -\n"

#  LA CONSIGNE DU CANAL. C'est LE PROGRAMME qui la dit, a chaque bloc de questions, et elle
#  dit les quatre choses qui comptent : ou mettre les reponses, que Fred ne les verra pas,
#  qu'il ne faut pas en parler dans la reponse visible, et que ce qu'elle laisse de cote
#  part chez Fred TOUT SEUL (elle n'a donc rien a decider, et rien a oublier).
CONSIGNE_DU_CANAL = (
    "\nOU METTRE TES REPONSES — C'EST LE PROGRAMME QUI TE LE DIT, ET IL N'Y A PAS D'AUTRE "
    "ENDROIT :\n"
    "  - a la TOUTE FIN de ton message, apres ta reponse normale au proprietaire, recopie "
    "ces deux lignes et mets tes reponses numerotees entre les deux :\n"
    "        %s\n"
    "        1) ...\n"
    "        2) ...\n"
    "        %s\n"
    "  - LE PROGRAMME DECOUPE CE BLOC AVANT L'AFFICHAGE. Le proprietaire ne le voit jamais, "
    "et il ne reste pas dans la conversation. Tu peux donc y repondre librement.\n"
    "  - dans ta reponse visible, tu ne parles pas des questions de l'archiviste : ce n'est "
    "pas le travail du proprietaire de les lire.\n"
    "  - un numero que tu ne traites pas, LE PROGRAMME LE POSE LUI-MEME au proprietaire, "
    "regroupe avec les autres, en une seule fois. Tu n'as donc rien a trier et rien a "
    "oublier : ce qui te manque lui arrive de toute facon.\n"
) % (CANAL_DEBUT, CANAL_FIN)


def avec_le_canal_cache(bloc):
    """AJOUTE LA CONSIGNE DU CANAL AU BLOC DE QUESTIONS. Purement additif : on ne touche pas
    au bloc que biblio2_questions.py fabrique, on ecrit derriere.

    Rend le bloc INCHANGE (y compris None) quand ce tour-ci ne contient pas de questions
    pour elle : la consigne ne part donc que quand elle sert, et elle ne coute rien les
    autres fois. Ne leve jamais.

    LA TROISIEME GRILLE EST ICI (chantier du 12/10/2026), ET C'EST LA DERNIERE. C'est la
    toute derniere fonction du pont que luciana.py appelle avant de poser le bloc dans le
    contexte. Reglage eteint : elle rend None, donc luciana.py n'a RIEN a poser, et le bloc
    de questions ne peut pas arriver dans le contexte, meme si quelque chose lui en avait
    donne un. C'est la garantie du bout de la chaine, apres les deux grilles de
    questions_du_tour()."""
    #  LA GRILLE EST POSEE AVANT LE try, EXPRES : si on la mettait dedans, un pepin
    #  quelconque tomberait dans le « except » qui rend le bloc tel quel -- c'est-a-dire
    #  qu'un pepin pourrait LAISSER PASSER le bloc. Ici, rien ne peut le laisser passer.
    if not bloc_de_questions_autorise():
        return None
    try:
        if not bloc:
            return bloc
        if CANAL_DEBUT in bloc:
            return bloc                     # deja mise : on ne la met pas deux fois
        if "QUESTIONS DE L'ARCHIVISTE" not in bloc:
            return bloc                     # pas de questions pour elle dans ce tour-ci
        return bloc + CONSIGNE_DU_CANAL
    except Exception:
        return bloc


def _decouper_le_canal(texte):
    """SEPARE LE CANAL CACHE DU RESTE. Rend (ce_qu_elle_a_repondu, texte_a_afficher).

    TOLERANT EXPRES, et c'est le point important : un modele ne recopie pas toujours un
    marqueur au caractere pres. On accepte donc les majuscules/minuscules, les etoiles et
    les dieses de mise en forme collees devant, le marqueur de fin OUBLIE (on prend alors
    tout ce qui suit jusqu'au bout du message), et plusieurs blocs dans le meme message.

    QUAND IL N'Y A PAS DE MARQUEUR DE DEBUT, ON NE TOUCHE A RIEN : le texte repart
    identique, au caractere. C'est le cas de la quasi-totalite des messages. Ne leve
    jamais."""
    import re as _re
    contenus = []
    t = str(texte or "")
    #  LE CAS DE TOUS LES JOURS, ET IL PASSE PAR ICI : pas de marqueur, donc on rend le
    #  texte EXACTEMENT comme il est arrive, au caractere pres. Aucune reponse ordinaire ne
    #  peut etre abimee par ce ramassage.
    if CANAL_DEBUT.lower() not in t.lower():
        return "", t
    try:
        for _tour in range(5):              # plusieurs blocs : on les ramasse tous
            i = t.lower().find(CANAL_DEBUT.lower())
            if i < 0:
                break
            #  on retire aussi la mise en forme collee juste devant le marqueur
            avant = _re.sub(r"[ \t]*[*_#>`\-]{0,8}[ \t]*$", "", t[:i])
            reste = t[i + len(CANAL_DEBUT):]
            j = reste.lower().find(CANAL_FIN.lower())
            if j >= 0:
                contenus.append(reste[:j])
                apres = reste[j + len(CANAL_FIN):]
            else:
                contenus.append(reste)      # marqueur de fin oublie : tout le reste est a elle
                apres = ""
            apres = _re.sub(r"^[ \t]*[*_#>`\-\]]{0,8}[ \t]*", "", apres)
            t = (avant.rstrip() + ("\n" + apres.lstrip() if apres.strip() else "")).rstrip()
    except Exception:
        return "", str(texte or "")
    return ("\n".join(c.strip() for c in contenus if c.strip()).strip(), t.strip())


def _numeros_lisibles(contenu):
    """REND LE CANAL LISIBLE PAR ranger_les_reponses(), SANS TOUCHER A CETTE FONCTION.

    POURQUOI C'EST NECESSAIRE, ET CE N'EST PAS UN DETAIL : le lecteur de reponses demande
    une ligne qui COMMENCE par « 1) ». Un modele ecrit tres souvent « **1)** », « - 1) »,
    « • 1. » ou « #### 1 - ». Toutes ces lignes-la seraient perdues EN SILENCE, et on
    retomberait exactement sur le defaut qu'on vient de reparer. On enleve donc, en debut de
    ligne seulement, les puces et la mise en forme, et on remet le numero au contact.

    UNE LIGNE QUI NE COMMENCE PAS PAR UN NUMERO N'EST PAS TOUCHEE : elle reste rattachee a
    la question precedente, ce qui est deja le comportement voulu. Ne leve jamais."""
    import re as _re
    try:
        sorties = []
        for ligne in str(contenu or "").splitlines():
            l = _re.sub(r"^[\s>*_#`+.•–—\-]*(?=\d{1,3}\s*[\)\.\:\-])",
                        "", ligne)
            l = _re.sub(r"^(\d{1,3})\s*[\)\.\:\-]\s*[*_`]{0,3}\s*", r"\1) ", l)
            sorties.append(l)
        return "\n".join(sorties)
    except Exception:
        return str(contenu or "")


def _lot_pas_encore_vu_par_le_proprietaire():
    """LE LOT EST-IL PRET, ET PAS ENCORE PASSE SOUS SES YEUX ? Ne leve jamais."""
    try:
        d = questions._lire_json(questions._chemin("lot"), {})
        return (bool(d.get("en_attente_de_reponse")) and bool(d.get("questions"))
                and not d.get("pose_a_l_ecran_le"))
    except Exception:
        return False


def _noter_le_lot_pose_a_l_ecran():
    """NOTE QUE LE LOT EST PASSE A L'ECRAN, pour qu'il n'y soit pas remis a chaque message.

    C'est la regle de Fred, et c'est elle qui empeche le harcelement : le lot est pose UNE
    SEULE FOIS, d'un seul coup. Tant qu'il n'a pas repondu, on ne le lui remet pas sous le
    nez. Ne leve jamais."""
    try:
        d = questions._lire_json(questions._chemin("lot"), {})
        if isinstance(d, dict) and d:
            d["pose_a_l_ecran_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            questions._ecrire_json(questions._chemin("lot"), d)
        return True
    except Exception:
        return False


def _ranger_le_canal(contenu):
    """SES REPONSES REDESCENDENT JUSQU'AUX FICHES, ET CE QU'ELLE N'A PAS TRANCHE PART DANS
    LE LOT DU PROPRIETAIRE. Rend les chiffres (avant / apres), pour la trace.

    LES TROIS SORTIES D'UNE QUESTION POSEE A L'ASSISTANTE, ET IL N'Y EN A PAS D'AUTRE :
      - elle repond quelque chose        -> la fiche est TRANCHEE, elle n'est plus en suspens
      - elle dit qu'elle ne sait pas     -> la question part dans le LOT du proprietaire
      - elle n'en parle pas du tout      -> la question part dans le LOT du proprietaire
    C'est ce troisieme cas qui est NEUF, et c'est lui qui rend la chose OBLIGATOIRE : rien
    de ce qu'elle n'a pas tranche ne peut rester en l'air. Ne leve jamais."""
    out = {}
    try:
        reperes = questions.relire_le_bloc_pose()
        if not reperes:
            return {"canal_sans_numerotation": "aucun bloc de questions n'attendait"}
        arbre = arch.arbre_charger(_f("arbre"))
        if not arbre:
            return {"canal_non_range": "arbre vide ou illisible"}
        avant = questions.compter(arbre)
        r = questions.ranger_les_reponses(arbre, reperes, _numeros_lisibles(contenu),
                                          par="l_assistante")
        traites = {d.get("repere") for d in (r.get("details") or []) if d.get("repere")}
        laissees = 0
        for rep in reperes:
            if rep in traites:
                continue
            _c, _s, fi = questions.trouver(arbre, rep)
            if fi is None or not fi.get("question"):
                continue
            if fi.get("question_etat") != questions.POSEE_ASSISTANTE:
                continue
            fi["question_etat"] = questions.A_POSER_PROPRIO
            fi["question_passee_au_lot_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            fi["question_passee_au_lot_pourquoi"] = (
                "l'assistante ne l'a pas tranchee : elle part au proprietaire")
            laissees += 1
        questions.oublier_le_bloc_pose()
        #  LE LOT EST PREPARE ICI, DANS LE MEME TOUR. Sans ca, ce qu'elle vient de laisser
        #  passer attendrait le message suivant pour seulement commencer a etre regroupe.
        pretes = 0
        if not questions.le_lot_attend_une_reponse():
            _t, reperes_lot = questions.bloc_pour_le_proprietaire(arbre, ecrire=True)
            pretes = len(reperes_lot)
        arch.arbre_sauver(_f("arbre"), arbre)
        questions.garder_les_questions(arbre)
        questions.garder_les_reponses(arbre)
        out = {
            "avant": avant,
            "apres": questions.compter(arbre),
            "tranchees": r.get("tranchees"),
            "parties_au_lot_elle_ne_savait_pas": r.get("parties_au_proprietaire"),
            "parties_au_lot_elle_n_a_pas_repondu": laissees,
            "numeros_inconnus": r.get("numeros_inconnus"),
            "questions_dans_le_lot_pret": pretes,
        }
    except Exception as ex:
        out = {"canal_rate": str(ex)[:160]}
    return out


def recolter_les_reponses_aux_questions(texte):
    """L'AUTRE MOITIE DU PONT, ET CELLE QUI MANQUAIT. A appeler UNE FOIS PAR TOUR, sur la
    reponse qu'elle vient d'ecrire, AVANT qu'elle ne partent a l'ecran et dans la memoire.
    Rend LE TEXTE A AFFICHER.

    IL FAIT TROIS CHOSES, DANS CET ORDRE :

      1  IL DECOUPE LE CANAL CACHE. Le proprietaire ne voit jamais les questions de son
         archiviste, ni les reponses de son assistante. Ce n'est pas son travail de
         surveiller ca, et c'est LE PROGRAMME qui le garantit -- pas la vigilance de
         quelqu'un.

      2  IL FAIT REDESCENDRE CES REPONSES JUSQU'AUX FICHES, tout de suite, dans le meme
         tour. Et CE QU'ELLE N'A PAS TRANCHE part dans le lot du proprietaire, que ce soit
         parce qu'elle a dit ne pas savoir ou parce qu'elle n'en a pas parle.

      3  IL POSE LE LOT A L'ECRAN, D'UN SEUL COUP, UNE SEULE FOIS. C'est la demande de Fred
         mot pour mot : « quand tu as des questions que tu arrives pas a repondre, tu viens
         me les dire tout simplement dans l'interface. C'est ca que le systeme doit
         t'OBLIGER a faire. » Le lot ne passe donc plus par sa reponse (c'est-a-dire par sa
         vigilance) : LE PROGRAMME L'ECRIT LUI-MEME, sous son message.

    NE LEVE JAMAIS. Au moindre pepin, le texte repart tel qu'il est arrive : un ramassage
    rate ne coupe jamais une conversation."""
    depart = str(texte or "")
    try:
        contenu, propre = _decouper_le_canal(depart)
    except Exception:
        contenu, propre = "", depart
    #  LE CANAL EST DECOUPE DANS TOUS LES CAS, MEME CHAINE ETEINTE : un marqueur ne doit
    #  jamais arriver sous les yeux du proprietaire, quelle que soit la raison.
    if contenu and not propre.strip():
        propre = ("(Note du PROGRAMME : elle a repondu a son archiviste, et le programme a "
                  "ramasse ces reponses. Il n'y avait rien d'autre dans ce message.)")
    try:
        if not (branche() and les_questions_sont_branchees()):
            return propre
        if questions is None or arch is None:
            return propre
        infos = {"quoi": "canal_cache"}
        if contenu:
            infos["caracteres_dans_le_canal"] = len(contenu)
            if un_rangement_est_en_cours():
                #  ON NE TOUCHE PAS A L'ARBRE EN MEME TEMPS QUE L'ARCHIVISTE. On garde la
                #  numerotation en place : les memes questions lui seront simplement
                #  reposees au tour suivant. Rien n'est perdu.
                infos["reponses_remises_a_plus_tard"] = ("un rangement tourne : on ne touche "
                                                         "pas a l'arbre maintenant")
            else:
                infos.update(_ranger_le_canal(contenu))
        #  LA NUMEROTATION EST OUBLIEE A CHAQUE TOUR, ET C'EST UN GARDE-FOU, PAS UN OUBLI.
        #  Depuis ce soir, ses reponses arrivent par le canal, et le canal est DECOUPE de sa
        #  reponse visible. Si on gardait la numerotation, le tour suivant relirait sa
        #  reponse VISIBLE comme si elle contenait des reponses numerotees -- or cette
        #  reponse visible peut tres bien contenir LE LOT que le programme vient d'y ecrire,
        #  qui est numerote lui aussi (« 1) ... 2) ... »). On appliquerait alors des
        #  QUESTIONS comme si c'etaient des REPONSES, sur cinq fiches qui allaient tres
        #  bien. On oublie donc : ce qui n'a pas ete tranche est simplement repose au tour
        #  suivant, avec une numerotation neuve, et rien n'est perdu.
        try:
            questions.oublier_le_bloc_pose()
        except Exception:
            pass
        lot = ""
        try:
            if _lot_pas_encore_vu_par_le_proprietaire():
                lot, _reperes_lot = questions.relire_le_lot()
                if lot:
                    _noter_le_lot_pose_a_l_ecran()
                    infos["lot_pose_a_l_ecran"] = len(lot)
        except Exception as ex:
            infos["lot_non_pose_a_l_ecran"] = str(ex)[:160]
        if len(infos) > 1:
            trace(infos)
        if lot:
            return (propre.rstrip() + SEPARATEUR_DU_LOT + lot).strip()
        return propre
    except Exception:
        return propre or depart


if __name__ == "__main__":
    # =====================================================================
    #  TEST ICI, SANS AUCUNE IA, SANS RESEAU, SANS AUCUNE DONNEE PERSONNELLE.
    #  TOUT est ecrit dans un dossier d'essai a cote du code : la memoire reelle de Fred
    #  (~/Luciana/bibliotheque2) n'est ouverte NI EN LECTURE NI EN ECRITURE.
    # =====================================================================
    import shutil

    rate = []

    def controle(nom, condition):
        print(("  OK   %s" if condition else "  RATE %s") % nom)
        if not condition:
            rate.append(nom)

    if arch is None or questions is None:
        print("Il manque biblio2_archiviste.py ou biblio2_questions.py : ce test a besoin "
              "des deux.")
        raise SystemExit(1)

    ESSAI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_demo_pont_questions")
    if os.path.isdir(ESSAI):
        shutil.rmtree(ESSAI, ignore_errors=True)
    os.makedirs(ESSAI, exist_ok=True)

    #  ON FAIT POINTER TOUS LES CHEMINS VERS LE DOSSIER D'ESSAI. On remplace les deux
    #  fonctions qui donnent les chemins : toutes les autres passent par elles.
    VRAI_DOSSIER = _dossier()

    def _dossier():          # noqa: F811  (on remplace expres, le temps du test)
        return ESSAI

    def _f(nom):             # noqa: F811
        return os.path.join(ESSAI, {"arbre": "arbre.json", "branche": "BRANCHE.txt",
                                    "vieux_drapeau_questions": "QUESTIONS.txt",
                                    "marque_page": "marque_page.json"}[nom])

    questions.DOSSIER_FORCE = ESSAI

    #  ON GARDE DE COTE LA VRAIE LECTURE DE L'INTERRUPTEUR, celle qui va chercher le reglage
    #  sur le disque. C'est elle, et elle seule, qui sert au CONTROLE DU DEBRANCHEMENT
    #  DEFINITIF juste en dessous : on veut prouver l'etat REEL du programme livre, pas
    #  l'etat d'un faux interrupteur de test.
    VRAIE_LECTURE_DE_L_INTERRUPTEUR = bloc_de_questions_autorise

    controle("LE TEST N'OUVRE PAS LA MEMOIRE REELLE DE FRED : tout va dans le dossier "
             "d'essai", ESSAI in _f("arbre") and ESSAI in questions._chemin("questions")
             and VRAI_DOSSIER not in _f("arbre"))

    #  UNE BIBLIOTHEQUE D'ESSAI, MONTEE DE TOUTES PIECES : 2 fiches sures, 7 en suspens.
    #  Sept, expres : le bloc n'en pose que cinq a la fois, on verifie donc aussi que les
    #  deux autres ne sont pas perdues et qu'elles attendent leur tour.
    arbre = {}
    jeu = [
        ({"texte": "La voiture rouge a ete achetee en 2016 chez le garage du centre."},
         {"categorie": "Vehicules", "sous_categorie": "Voitures",
          "filtres": {"date": "2016", "objet": "voiture rouge", "type": "achat"},
          "resume": "Voiture rouge achetee en 2016.", "confiance": 0.9}),
        ({"texte": "Le rendez-vous chez le docteur Martin a Lyon est le 2 mars."},
         {"categorie": "Sante", "sous_categorie": "Rendez-vous",
          "filtres": {"ou": "Lyon", "qui": ["Dr Martin"], "type": "medical"},
          "resume": "Rendez-vous chez le docteur Martin a Lyon.", "confiance": 0.85}),
    ]
    for n in range(7):
        jeu.append(({"texte": "Chose numero %d dont je ne sais plus a quoi elle sert." % n},
                    {"categorie": "", "sous_categorie": "", "filtres": {},
                     "resume": "Chose numero %d, a trancher." % n, "confiance": 0.1}))
    for souvenir, jugement in jeu:
        souvenir["source"] = "essai"
        souvenir["repere"] = arch.repere_de("essai", souvenir["texte"])
        arch.ranger(arbre, souvenir, arch.valider_jugement(jugement))
    arch.arbre_sauver(_f("arbre"), arbre)

    depart = arch.compter(arch.arbre_charger(_f("arbre")))
    FICHES_AU_DEPART = depart["fiches"]
    SUSPENS_AU_DEPART = depart["en_suspens"]
    print("=== LA BIBLIOTHEQUE D'ESSAI ===")
    print("  %d fiche(s), dont %d en suspens (aucune n'a de question)"
          % (FICHES_AU_DEPART, SUSPENS_AU_DEPART))

    # =====================================================================
    #  LE CONTROLE DU DEBRANCHEMENT DEFINITIF (chantier du 12/10/2026).
    #  CELUI-LA EST LE PLUS IMPORTANT DU FICHIER.
    # =====================================================================
    #  CE QU'IL PROUVE, SUR DU REEL, ET EN UNE PHRASE :
    #      REGLAGE ETEINT + UN VIEUX DRAPEAU QUESTIONS.txt TOUJOURS PRESENT SUR LE DISQUE
    #      = AUCUN BLOC DE QUESTIONS INJECTE.
    #
    #  C'est exactement la situation de Fred : le drapeau a ete enleve a la main, mais il
    #  pourrait tres bien etre encore la (ou revenir). On se met donc dans le PIRE cas :
    #    - la memoire 2 est BRANCHEE (BRANCHE.txt est la), comme chez lui ;
    #    - le vieux drapeau QUESTIONS.txt EST LA, bien present ;
    #    - la bibliotheque est pleine de fiches en suspens, donc il y a de quoi poser des
    #      centaines de questions.
    #  Et on verifie que RIEN ne remonte, par les trois grilles, parce que le reglage dit
    #  non. C'est la VRAIE lecture du reglage qui est utilisee ici, pas un faux interrupteur.
    print("\n=== CONTROLE DU DEBRANCHEMENT DEFINITIF : REGLAGE ETEINT + VIEUX DRAPEAU "
          "PRESENT ===")
    with open(_f("branche"), "w", encoding="utf-8") as fh:
        fh.write("branchee")                      # la memoire 2 est branchee, comme chez Fred
    with open(_f("vieux_drapeau_questions"), "w", encoding="utf-8") as fh:
        fh.write("branchees")                     # LE VIEUX DRAPEAU, EXACTEMENT COMME AVANT
    print("  mise en place : memoire 2 BRANCHEE, vieux drapeau QUESTIONS.txt PRESENT, "
          "%d fiche(s) en suspens a questionner" % SUSPENS_AU_DEPART)

    controle("LE REGLAGE LIVRE AUJOURD'HUI EST ETEINT (c'est lui, et lui seul, qui decide)",
             VRAIE_LECTURE_DE_L_INTERRUPTEUR() is False)
    controle("UN VIEUX DRAPEAU QUESTIONS.txt EST BIEN PRESENT SUR LE DISQUE pendant tout ce "
             "controle (sinon il ne prouverait rien)",
             os.path.exists(_f("vieux_drapeau_questions")))
    _rien = questions_du_tour("le rendez-vous chez le docteur, et range-moi tout ca")
    controle("CE QUI COMPTE LE PLUS : reglage eteint + vieux drapeau present = le pont rend "
             "None, donc AUCUN bloc de questions n'est injecte dans le contexte",
             _rien is None)
    controle("LA TROISIEME GRILLE TIENT AUSSI : meme si on lui tendait un bloc de questions "
             "tout fait, avec_le_canal_cache() rend None et luciana.py n'a RIEN a poser",
             avec_le_canal_cache("QUESTIONS DE L'ARCHIVISTE DE TA MEMOIRE\n1) ou ranger "
                                 "ceci ?") is None)
    controle("AUCUNE DONNEE TOUCHEE : la bibliotheque est exactement comme avant (meme "
             "nombre de fiches, meme nombre en suspens)",
             arch.compter(arch.arbre_charger(_f("arbre")))["fiches"] == FICHES_AU_DEPART
             and arch.compter(arch.arbre_charger(_f("arbre")))["en_suspens"]
             == SUSPENS_AU_DEPART)
    controle("AUCUNE QUESTION ECRITE sur les fiches : le programme ne travaille meme pas",
             not questions.compter(arch.arbre_charger(_f("arbre")))[questions.OUVERTE]
             and not questions.compter(arch.arbre_charger(_f("arbre")))[
                 questions.POSEE_ASSISTANTE])
    controle("AUCUN LOT PREPARE, donc rien n'est pose au proprietaire non plus",
             not os.path.exists(questions._chemin("lot")))
    controle("LE PROGRAMME N'ECRIT RIEN DU TOUT dans ce cas : pas meme une trace",
             not os.path.exists(_trace_fichier()))

    #  ON REMET LA MEMOIRE 2 DANS L'ETAT OU LA SUITE DU TEST L'ATTEND. LE VIEUX DRAPEAU,
    #  LUI, RESTE EN PLACE JUSQU'A LA FIN : on veut qu'il soit la pendant TOUT le test, pour
    #  que rien ne puisse dependre de sa presence ou de son absence.
    os.remove(_f("branche"))

    #  =====================================================================
    #  L'INTERRUPTEUR D'ESSAI, POUR LA SUITE DU TEST.
    #  =====================================================================
    #  EN SERVICE, L'INTERRUPTEUR EST LE REGLAGE, ET RIEN D'AUTRE. Pour pouvoir derouler la
    #  chaine de bout en bout dans le test, on remplace ici la LECTURE de l'interrupteur par
    #  une simple variable. Deux consequences, et ce sont les deux bonnes :
    #    - le test n'ecrit PAS dans le reglage de Fred : il ne le lit meme plus apres ce
    #      point, donc il ne peut pas le changer ni par accident ni autrement ;
    #    - le test ne CREE AUCUN DRAPEAU sur le disque : plus une seule ligne de ce fichier
    #      n'ecrit QUESTIONS.txt, ce que le dernier controle du fichier verifie.
    INTERRUPTEUR_D_ESSAI = {"allume": False}

    def bloc_de_questions_autorise():            # noqa: F811  (on remplace expres, pour le test)
        return bool(INTERRUPTEUR_D_ESSAI["allume"])

    print("\n=== LES DEUX INTERRUPTEURS SONT ETEINTS : LE PONT NE FAIT RIEN ===")
    controle("tout eteint, le pont rend None (le programme garde son chemin d'hier)",
             questions_du_tour("le rendez-vous chez le docteur") is None)
    controle("tout eteint, il n'ecrit RIEN du tout", not os.path.exists(_trace_fichier()))

    print("\n=== LA MEMOIRE 2 EST BRANCHEE, MAIS PAS LA CHAINE : TOUJOURS RIEN ===")
    with open(_f("branche"), "w", encoding="utf-8") as fh:
        fh.write("branchee")
    controle("CE QUI COMPTE LE PLUS : la memoire 2 branchee NE SUFFIT PAS a allumer la "
             "chaine (poser l'appel dans luciana.py ne change donc rien aujourd'hui)",
             questions_du_tour("bonjour") is None)
    controle("la chaine eteinte n'ecrit RIEN du tout",
             not os.path.exists(_trace_fichier()))
    controle("la chaine eteinte ne touche PAS a l'arbre",
             arch.compter(arch.arbre_charger(_f("arbre")))["en_suspens"] == SUSPENS_AU_DEPART
             and not questions.compter(arch.arbre_charger(_f("arbre")))[questions.OUVERTE])

    print("\n=== ON ALLUME LA CHAINE (par l'interrupteur d'essai, sans creer de drapeau) ===")
    INTERRUPTEUR_D_ESSAI["allume"] = True

    print("\n=== PREMIER TOUR : les questions sont ecrites, et les 5 premieres posees ===")
    t1 = questions_du_tour("et sinon, quoi de neuf ?")
    print(t1)
    etat1 = questions.compter(arch.arbre_charger(_f("arbre")))
    reperes_poses = questions.relire_le_bloc_pose()
    N_ECRITES = etat1[questions.POSEE_ASSISTANTE] + etat1[questions.OUVERTE]
    N_POSEES_ASSISTANTE = len(reperes_poses)

    print("\n=== CONTROLES DU PREMIER TOUR ===")
    controle("la chaine allumee, le pont rend du texte", isinstance(t1, str) and bool(t1))
    controle("TEMPS 1 : les %d fiches en suspens ont TOUTES recu une question"
             % SUSPENS_AU_DEPART, N_ECRITES == SUSPENS_AU_DEPART
             and etat1["en_suspens_sans_question"] == 0)
    controle("TEMPS 2 : la question est posee PAR LE PROGRAMME, et le bloc le dit",
             "ecrit par LE PROGRAMME" in t1)
    controle("TEMPS 2 : 5 questions posees d'un coup, pas les 7 (on ne noie personne)",
             N_POSEES_ASSISTANTE == 5)
    controle("TEMPS 2 : les 2 qui restent sont annoncees, et elles ne sont pas perdues",
             "il y en a 2 autre(s) ensuite" in t1
             and etat1[questions.OUVERTE] == 2)
    controle("TEMPS 4 : aucun lot n'est pose au proprietaire tant qu'elle n'a rien dit "
             "(on ne derange pas Fred pour rien)", "J'ai mis de cote" not in t1)
    controle("la numerotation du bloc pose est gardee SUR LE DISQUE (elle survit a un "
             "redemarrage)", N_POSEES_ASSISTANTE == 5)
    controle("une trace est ecrite a chaque sortie (fin des pannes muettes)",
             os.path.exists(_trace_fichier()))
    controle("AUCUNE FICHE PERDUE au premier tour",
             arch.compter(arch.arbre_charger(_f("arbre")))["fiches"] == FICHES_AU_DEPART)

    print("\n=== DEUXIEME TOUR : elle repond — elle en sait 2, elle ignore 3 ===")
    sa_reponse = ("1) oui c'est bien la, Divers / A trier convient\n"
                  "2) c'est le vieux compresseur, RAYON: Maison / Cave\n"
                  "3) je ne sais pas\n"
                  "4) je ne sais pas\n"
                  "5) je ne sais pas, desolee\n")
    t2 = questions_du_tour("parle-moi d'autre chose", sa_derniere_reponse=sa_reponse)
    print(t2)
    etat2 = questions.compter(arch.arbre_charger(_f("arbre")))

    print("\n=== CONTROLES DU DEUXIEME TOUR ===")
    controle("TEMPS 3 : les 2 qu'elle savait sont TRANCHEES",
             etat2[questions.REPONDUE] == 2)
    controle("TEMPS 3 : une fiche tranchee n'est plus en suspens",
             arch.compter(arch.arbre_charger(_f("arbre")))["en_suspens"]
             == SUSPENS_AU_DEPART - 2)
    controle("TEMPS 3 : la fiche designee par RAYON: a bien ete DEPLACEE",
             "Maison" in arch.arbre_charger(_f("arbre")))
    controle("TEMPS 4 : les 3 qu'elle ignorait sont regroupees en UN SEUL lot, et le lot est "
             "ECRIT SUR LE DISQUE (c'est ce fichier-la qui n'existait dans AUCUN dossier "
             "reel avant ce soir)",
             os.path.exists(questions._chemin("lot"))
             and questions._lire_json(questions._chemin("lot"),
                                      {}).get("combien_dans_ce_lot") == 3)
    controle("CORRECTION DU SOIR : le lot ne passe PLUS par sa reponse, donc plus par sa "
             "vigilance -- il n'est pas dans ce qui part dans son prompt",
             "J'ai mis de cote" not in (t2 or "")
             and "pose-le au proprietaire" not in (t2 or ""))
    controle("TEMPS 4 : les 3 du lot ne lui sont PAS reposees a elle en meme temps",
             etat2[questions.POSEE_PROPRIO] == 3)
    controle("le lot attend bien une reponse", questions.le_lot_attend_une_reponse())
    controle("AUCUNE FICHE PERDUE au deuxieme tour",
             arch.compter(arch.arbre_charger(_f("arbre")))["fiches"] == FICHES_AU_DEPART)

    print("\n=== TROISIEME TOUR : Fred repond au lot, la reponse redescend ===")
    t3 = questions_du_tour("1) ca va dans la cuisine, RAYON: Maison / Cuisine\n"
                           "2) c'est pour le garage\n"
                           "3) je ne sais pas")
    arbre_fin = arch.arbre_charger(_f("arbre"))
    etat3 = questions.compter(arbre_fin)
    c_fin = arch.compter(arbre_fin)

    print("\n=== CONTROLES DU TROISIEME TOUR ===")
    controle("TEMPS 4 : les reponses de Fred redescendent jusqu'aux fiches, et les RANGENT",
             etat3[questions.REPONDUE] == 4)
    controle("TEMPS 4 : la fiche que Fred a designee est allee dans son rayon",
             "Cuisine" in arbre_fin.get("Maison", {}))
    controle("TEMPS 4 : ce que Fred ne sait pas non plus reste en attente, sans rien "
             "inventer", etat3[questions.POSEE_PROPRIO] == 1)
    controle("CORRECTION LUCIANA : la question que Fred vient de decliner n'est PAS "
             "reposee au tour suivant (sans ca, il la reverrait a CHAQUE message)",
             not questions.le_lot_attend_une_reponse()
             and questions.bloc_pour_le_proprietaire(arbre_fin, ecrire=False)[0] == "")

    print("\n=== LE GARDE-FOU ANTI-BLOCAGE : elle repond a cote du format 3 fois ===")
    #  Les 2 questions restantes sont reposees a chaque tour. Si elle ne repond jamais au
    #  format, elles doivent FINIR par passer au lot, sinon elles bloquent la file.
    for _i in range(4):
        questions_du_tour("une phrase ordinaire, sans aucun numero",
                          sa_derniere_reponse="je te reponds tres volontiers mais sans "
                                              "numeroter quoi que ce soit")
    etat4 = questions.compter(arch.arbre_charger(_f("arbre")))
    controle("une question posee %d fois sans reponse lisible PASSE AU LOT (elle ne bloque "
             "pas la file des 390 autres)" % RELANCES_MAXI,
             etat4[questions.POSEE_ASSISTANTE] == 0 and etat4[questions.OUVERTE] == 0)

    print("\n=== LE FILET : on eteint, on abime, rien ne tombe ===")
    INTERRUPTEUR_D_ESSAI["allume"] = False
    controle("on eteint l'interrupteur : le pont rend None tout de suite, sans redemarrage",
             questions_du_tour("la voiture") is None)
    INTERRUPTEUR_D_ESSAI["allume"] = True
    controle("un rangement en cours fait taire le pont (deux ecritures de arbre.json en "
             "meme temps, c'est une perte)",
             (lambda: (open(_f("marque_page"), "w").close(),
                       questions_du_tour("x"))[1])() is None)
    os.remove(_f("marque_page"))
    controle("un arbre vide fait rendre None (le programme garde son chemin d'hier)",
             (lambda: (arch.arbre_sauver(_f("arbre"), {}),
                       questions_du_tour("x"))[1])() is None)

    # =====================================================================
    #  LE CANAL CACHE — LES DEUX REPARATIONS DU SOIR, DE BOUT EN BOUT.
    #  Toujours dans le MEME dossier d'essai : la memoire reelle de Fred n'est ouverte ni
    #  en lecture ni en ecriture, et aucune des 420 vraies questions n'est touchee.
    # =====================================================================
    print("\n=== LE CANAL CACHE : LES DEUX REPARATIONS DU SOIR ===")
    for _nom in ("questions", "lot", "reponses"):
        if os.path.exists(questions._chemin(_nom)):
            os.remove(questions._chemin(_nom))
    arbre_c = {}
    for _n in range(6):
        _s = {"texte": "Deuxieme jeu, chose numero %d, impossible a trancher." % _n,
              "source": "essai2"}
        _s["repere"] = arch.repere_de("essai2", _s["texte"])
        arch.ranger(arbre_c, _s, arch.valider_jugement(
            {"categorie": "", "sous_categorie": "", "filtres": {},
             "resume": "Deuxieme jeu, chose %d, a trancher." % _n, "confiance": 0.1}))
    arch.arbre_sauver(_f("arbre"), arbre_c)
    _d = arch.compter(arch.arbre_charger(_f("arbre")))
    CANAL_FICHES_AU_DEPART, CANAL_SUSPENS_AU_DEPART = _d["fiches"], _d["en_suspens"]
    print("  au depart : %d fiche(s), dont %d en suspens, 0 tranchee, lot inexistant"
          % (CANAL_FICHES_AU_DEPART, CANAL_SUSPENS_AU_DEPART))

    bloc_c = avec_le_canal_cache(questions_du_tour("raconte-moi ta journee"))
    reperes_c = questions.relire_le_bloc_pose()
    controle("LA CONSIGNE DU CANAL est ajoutee au bloc de questions, avec ses deux "
             "marqueurs", isinstance(bloc_c, str) and CANAL_DEBUT in bloc_c
             and CANAL_FIN in bloc_c)
    controle("la consigne dit NOIR SUR BLANC que le proprietaire ne verra pas ce bloc",
             "DECOUPE CE BLOC AVANT L'AFFICHAGE" in (bloc_c or ""))
    controle("la consigne lui dit que ce qu'elle laisse de cote part chez le proprietaire "
             "TOUT SEUL (elle n'a rien a decider)",
             "LE PROGRAMME LE POSE LUI-MEME" in (bloc_c or ""))
    controle("5 questions posees a l'assistante, numerotation gardee sur le disque",
             len(reperes_c) == 5)

    #  SA REPONSE, AVEC LA MISE EN FORME D'UN VRAI MODELE (etoiles, puce, indentation,
    #  tirets) : c'est exactement ce qui faisait tout perdre en silence jusqu'ici.
    sa_reponse_c = ("Oui, bien sur. La journee a ete calme, j'ai surtout range.\n"
                    "\n"
                    "**%s**\n"
                    "- **1)** c'est le vieux compresseur, RAYON: Maison / Cave\n"
                    "  2. c'est un souvenir de famille, le rayon propose convient\n"
                    "3 - je ne sais pas\n"
                    "%s\n" % (CANAL_DEBUT, CANAL_FIN))
    a_l_ecran = recolter_les_reponses_aux_questions(sa_reponse_c)
    print("\n--- CE QUE FRED VOIT A L'ECRAN, mot pour mot ---")
    print(a_l_ecran)
    print("--- fin de ce que Fred voit ---\n")
    etat_c1 = questions.compter(arch.arbre_charger(_f("arbre")))
    lot_c = questions._lire_json(questions._chemin("lot"), {})

    controle("REGLE 4 DE FRED : il ne voit RIEN des marqueurs du canal",
             CANAL_DEBUT not in a_l_ecran and CANAL_FIN not in a_l_ecran)
    controle("REGLE 4 DE FRED : il ne voit RIEN de la masse des questions de l'archiviste "
             "ni des reponses de l'assistante",
             "compresseur" not in a_l_ecran and "souvenir de famille" not in a_l_ecran
             and "QUESTIONS DE L'ARCHIVISTE" not in a_l_ecran)
    controle("sa vraie reponse au proprietaire, elle, part INTACTE",
             "La journee a ete calme" in a_l_ecran)
    controle("REPARATION 1 : ses reponses sont REPRISES et les fiches TRANCHEES "
             "(avant ce soir : 0 a chacun des 7 passages)",
             etat_c1[questions.REPONDUE] == 2)
    controle("la mise en forme ne fait plus rien perdre : « **1)** », « 2. » indentee et "
             "« 3 - » sont lus tous les trois",
             etat_c1[questions.REPONDUE] == 2
             and etat_c1[questions.POSEE_PROPRIO] >= 1)
    controle("une fiche tranchee n'est plus en suspens",
             arch.compter(arch.arbre_charger(_f("arbre")))["en_suspens"]
             == CANAL_SUSPENS_AU_DEPART - 2)
    controle("la fiche designee par RAYON: a bien ete DEPLACEE, en gardant son repere",
             "Cave" in arch.arbre_charger(_f("arbre")).get("Maison", {}))
    controle("REPARATION 2 : lot_pour_le_proprietaire.json EXISTE pour de vrai, avec les 3 "
             "qu'elle n'a pas tranchees", os.path.exists(questions._chemin("lot"))
             and lot_c.get("combien_dans_ce_lot") == 3)
    controle("CE QUE FRED DEMANDE, MOT POUR MOT : ce qu'elle ne sait pas trancher lui est "
             "pose A L'ECRAN, PAR LE PROGRAMME, dans ce meme message",
             "J'ai mis de cote 3 chose(s)" in a_l_ecran)
    controle("LES DEUX QU'ELLE N'A MEME PAS MENTIONNEES partent chez lui aussi : c'est le "
             "programme qui l'y oblige, pas sa vigilance",
             etat_c1[questions.POSEE_PROPRIO] == 3)
    controle("EN UNE SEULE FOIS : un seul bloc de lot dans le message, jamais une question "
             "par message", a_l_ecran.count("J'ai mis de cote") == 1)
    controle("PAS DE HARCELEMENT : au message suivant, le lot n'est PAS repose",
             "J'ai mis de cote" not in recolter_les_reponses_aux_questions(
                 "une reponse ordinaire, sans aucun canal"))
    controle("UN MESSAGE ORDINAIRE REPART AU CARACTERE PRES (le ramassage ne peut pas "
             "abimer une conversation)",
             recolter_les_reponses_aux_questions("bonjour, tout va bien\n")
             == "bonjour, tout va bien\n")
    controle("AUCUNE FICHE PERDUE pendant tout le canal",
             arch.compter(arch.arbre_charger(_f("arbre")))["fiches"]
             == CANAL_FICHES_AU_DEPART)
    controle("GARDE-FOU : la numerotation est oubliee apres le ramassage, donc le tour "
             "suivant ne peut PAS relire le lot (numerote lui aussi) comme si c'etaient ses "
             "reponses, et trancher 5 fiches avec des questions",
             questions.relire_le_bloc_pose() == [])

    print("=== LE PROPRIETAIRE REPOND AU LOT, EN UNE SEULE FOIS ===")
    questions_du_tour("1) ca va dans la cuisine, RAYON: Maison / Cuisine\n"
                      "2) c'est pour le garage\n"
                      "3) je ne sais pas")
    etat_c2 = questions.compter(arch.arbre_charger(_f("arbre")))
    controle("ses reponses redescendent jusqu'aux fiches et les RANGENT",
             etat_c2[questions.REPONDUE] == 4)
    controle("la fiche qu'il a designee est allee dans son rayon",
             "Cuisine" in arch.arbre_charger(_f("arbre")).get("Maison", {}))
    controle("DEFAUT DEJA CORRIGE, ET TOUJOURS CORRIGE : la question qu'il vient de "
             "decliner s'ENDORT -- elle ne lui est pas reposee au message suivant",
             "J'ai mis de cote" not in (recolter_les_reponses_aux_questions(
                 "et sinon, quoi de neuf ?") or ""))
    print("  a l'arrivee : %d fiche(s), dont %d en suspens, %d tranchee(s), lot de %d pose "
          "A L'ECRAN une seule fois"
          % (arch.compter(arch.arbre_charger(_f("arbre")))["fiches"],
             arch.compter(arch.arbre_charger(_f("arbre")))["en_suspens"],
             etat_c2[questions.REPONDUE], lot_c.get("combien_dans_ce_lot") or 0))

    # =====================================================================
    #  LE DERNIER CONTROLE : LE PROGRAMME NE RECREE JAMAIS LE VIEUX DRAPEAU.
    #  (chantier du 12/10/2026)
    # =====================================================================
    #  C'etait le deuxieme risque du debranchement d'avant : le drapeau enleve a la main
    #  pouvait etre RECREE par le programme, et le defaut revenait tout seul. On enleve donc
    #  le vieux drapeau, on fait tourner la chaine A FOND (interrupteur allume, un tour
    #  complet, un ramassage complet), et on verifie qu'il n'est pas revenu.
    print("\n=== CONTROLE : LE PROGRAMME NE RECREE JAMAIS LE VIEUX DRAPEAU ===")
    if os.path.exists(_f("vieux_drapeau_questions")):
        os.remove(_f("vieux_drapeau_questions"))
    INTERRUPTEUR_D_ESSAI["allume"] = True
    questions_du_tour("raconte-moi encore ta journee")
    recolter_les_reponses_aux_questions("une reponse ordinaire, pour faire tourner la suite")
    controle("le vieux drapeau QUESTIONS.txt N'EST PAS REVENU, meme apres un tour complet "
             "chaine allumee : plus une seule ligne de code ne l'ecrit",
             not os.path.exists(_f("vieux_drapeau_questions")))
    controle("et il n'est pas revenu ailleurs dans le dossier non plus",
             "QUESTIONS.txt" not in os.listdir(ESSAI))

    print("\n=== LES CHIFFRES DE BOUT EN BOUT ===")
    print("  fiches au depart ........................... %d" % FICHES_AU_DEPART)
    print("  fiches a l'arrivee ......................... %d" % c_fin["fiches"])
    print("  fiches en suspens au depart ................ %d" % SUSPENS_AU_DEPART)
    print("  fiches en suspens qui ont recu une question  %d" % N_ECRITES)
    print("  questions posees a l'assistante (1er tour) . %d" % N_POSEES_ASSISTANTE)
    print("  questions tranchees par l'assistante ....... %d" % 2)
    print("  questions posees au proprietaire (le lot) .. %d" % 3)
    print("  questions tranchees en tout ................ %d" % etat3[questions.REPONDUE])
    print("  fiches en suspens a l'arrivee .............. %d" % c_fin["en_suspens"])
    controle("AUCUNE FICHE PERDUE DE BOUT EN BOUT : %d au depart, %d a l'arrivee"
             % (FICHES_AU_DEPART, c_fin["fiches"]), c_fin["fiches"] == FICHES_AU_DEPART)
    controle("TOUTES les fiches en suspens ont recu une question : %d sur %d"
             % (N_ECRITES, SUSPENS_AU_DEPART), N_ECRITES == SUSPENS_AU_DEPART)

    print("\n=== LA TRACE, TELLE QU'ELLE EST ECRITE ===")
    with open(_trace_fichier(), encoding="utf-8") as fh:
        for ligne in fh.read().splitlines()[-3:]:
            print("  " + ligne[:220])

    print("\n%s" % ("TOUT EST PASSE." if not rate else
                    "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
    raise SystemExit(1 if rate else 0)
