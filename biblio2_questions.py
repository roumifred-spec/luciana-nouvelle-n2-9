# -*- coding: utf-8 -*-
"""
BRIQUE 5 — LA CHAINE DES QUESTIONS.  (demande de Fred du 11/10/2026)

PORTE CHEZ LUCIANA LE 11/10/2026, LE SOIR. Fichier NEUF : s'il n'est pas la, l'archiviste
fait exactement ce qu'il faisait avant (il marque la fiche « en suspens » et il continue).
Il ne peut donc rien casser.

CE QUI A ETE ADAPTE EN ARRIVANT CHEZ LUCIANA (dit franchement, pour qu'on puisse verifier) :
  - LE DOSSIER. Les trois fichiers de la chaine sont ecrits dans le dossier de LUCIANA,
    c'est-a-dire reglages.DOSSIER_BIBLIO2 = ~/Luciana/bibliotheque2. Le dossier d'une autre
    memoire n'est jamais nomme ici, et aucun chemin n'est ecrit en dur ailleurs.
  - LES TROIS CHEMINS. biblio2_reglages.py de Luciana ne connait pas FICHIER_QUESTIONS,
    FICHIER_LOT_PROPRIO ni FICHIER_REPONSES. On les demande donc avec getattr : s'ils
    existent un jour, ils sont pris ; sinon on les fabrique a partir de DOSSIER_BIBLIO2.
    On n'a donc eu A TOUCHER NI biblio2_reglages.py NI reglage_biblio2.json.
  - LES TROIS NOMBRES. biblio2_reglages.py de Luciana ne connait pas reglages_questions().
    Meme traitement : getattr, et a defaut les valeurs par defaut d'ici.

TOUT LE RESTE EST INCHANGE, et chaque fonction appelee a ete verifiee une par une dans la
base de Luciana : arch.toutes_les_fiches, arch.etiquette_de, arch.DIVERS, arch.repere_de,
arch.ranger, arch.valider_jugement, arch.compter — les sept existent, avec la meme
signature et les memes noms de champs.


=====================================================================================
 LE DEFAUT QU'ON REPARE, DIT SIMPLEMENT
=====================================================================================

Avant : quand l'archiviste tombait sur une fiche qu'il ne savait pas trancher, il la
rangeait quand meme, il collait dessus l'etiquette « en suspens »... ET PERSONNE NE LUI
REPONDAIT JAMAIS. La fiche restait en suspens pour toujours, en silence. Le doute etait
bien note, mais il ne remontait a personne. (Chez Fred, au 11/10/2026 : 395 fiches dans ce
cas, et aucune question jamais posee.)

Maintenant, la question remonte, et elle redescend. En quatre temps, et jamais autrement :

  TEMPS 1 — L'ARCHIVISTE ECRIT SA QUESTION, COLLEE A LA FICHE.
      Il ne met plus la fiche de cote en silence. Il ECRIT, DANS LA FICHE ELLE-MEME, la
      question qui l'empeche de trancher. La question voyage donc avec la fiche : on ne
      peut plus perdre l'une sans perdre l'autre, et on ne peut plus avoir une question
      qui ne sait plus de quelle fiche elle parle.

  TEMPS 2 — LE PROGRAMME POSE LA QUESTION A L'ASSISTANTE. C'EST LE PROGRAMME, JAMAIS SA
      VIGILANCE. C'est le point le plus important de tout ce fichier. Une question posee
      « par sa vigilance » est une phrase ecrite dans son prompt : elle l'oublie, ou elle
      se laisse attendrir, ou elle decide que ce n'est pas le moment. Ici c'est le PROGRAMME
      qui fabrique le bloc de questions et qui le pose. Aucune phrase ne peut l'annuler.
      (C'est la meme lecon que le coffre-fort et que le minuteur parental.)

  TEMPS 3 — ELLE REPOND A CE QU'ELLE SAIT, ET SA REPONSE REPART AVEC LA FICHE.
      La reponse est ecrite DANS la fiche, l'archiviste la range pour de bon, et la fiche
      n'est plus en suspens. Ce qu'elle NE SAIT PAS n'est pas jete : il passe au temps 4.

  TEMPS 4 — CE QU'ELLE NE SAIT PAS EST RAMASSE EN UN SEUL LOT, ET POSE AU PROPRIETAIRE
      D'UN SEUL COUP. JAMAIS QUESTION PAR QUESTION. C'est la deuxieme regle dure de Fred :
      on ne harcele pas le proprietaire avec une question, puis une autre, puis une autre.
      On attend, on ramasse, et on pose TOUT en une seule fois. Le proprietaire repond, la
      reponse REDESCEND jusqu'a la fiche, et la fiche est rangee.

  ET AU DEMARRAGE : LES FICHES DEJA EN SUSPENS SONT LES PREMIERES SERVIES.
      amorcer() passe sur toute la bibliotheque, ecrit une question sur chaque fiche deja
      en suspens qui n'en a pas encore, et les met EN TETE de la file. C'est la demande
      explicite de Fred : le retard existant passe avant le travail du jour.


=====================================================================================
 CE QUE CE FICHIER NE FAIT PAS, ET C'EST VOULU
=====================================================================================

  - IL N'AJOUTE RIEN A L'ECRAN. Pas de bouton, pas de pastille, pas de voyant. Les
    questions passent par la CONVERSATION, qui existe deja. On n'ajoute a l'interface que
    ce qui a ete demande.
  - IL NE DECIDE RIEN TOUT SEUL. Il ne devine pas une reponse, il ne choisit pas un rayon
    « au plus probable ». Une question sans reponse reste une question.
  - IL NE PERD JAMAIS UNE FICHE. Toutes les ecritures remplacent d'un coup (on ecrit a
    cote, puis on bascule). Un deplacement de fiche garde son repere : elle ne peut donc
    pas etre rangee deux fois.
  - IL NE LEVE JAMAIS. Au moindre souci, il rend "" ou une liste vide, et l'archiviste
    continue comme avant.

NOTE IA : tout est ecrit en POSITIF. On dit « reponds par ce que tu sais » — jamais
« ne reponds pas n'importe quoi ». Les negations se perdent, donc on ne s'en sert pas.
"""

import json, os, time

try:
    import biblio2_archiviste as arch
except Exception:
    arch = None
try:
    import biblio2_reglages as reglages
except Exception:
    reglages = None


# ---------------------------------------------------------------------
#  LES CINQ ETATS D'UNE QUESTION. Il n'y en a pas d'autres, et c'est voulu :
#  a tout moment on peut DIRE ou en est chaque fiche, sans deviner.
# ---------------------------------------------------------------------
OUVERTE = "ouverte"                      # l'archiviste vient de l'ecrire
POSEE_ASSISTANTE = "posee_a_l_assistante"   # le programme l'a posee a l'assistante
A_POSER_PROPRIO = "a_poser_au_proprietaire"  # elle ne savait pas : ca part dans le lot
POSEE_PROPRIO = "posee_au_proprietaire"  # le lot est parti, d'un seul coup
REPONDUE = "repondue"                    # tranchee, et la fiche est rangee

ETATS = (OUVERTE, POSEE_ASSISTANTE, A_POSER_PROPRIO, POSEE_PROPRIO, REPONDUE)

#  =====================================================================
#  COMMENT ON RECONNAIT UN « JE NE SAIS PAS », ET POURQUOI C'EST FAIT AINSI
#  =====================================================================
#  LE PIEGE A EVITER, ET IL EST SERIEUX : si on cherchait simplement les mots « je ne sais
#  pas » QUELQUE PART dans la reponse, alors « je ne sais pas si c'est Lyon ou Paris, mais
#  c'est bien un rendez-vous medical » serait pris pour une absence de reponse — alors que
#  c'est une VRAIE reponse, et une bonne. On perdrait l'information, et on irait deranger le
#  proprietaire pour rien.
#
#  LA REGLE RETENUE : on enleve de la reponse tous les mots qui ne portent AUCUNE
#  information (les politesses, la negation, les mots de remplissage). S'il ne reste RIEN,
#  c'est un « je ne sais pas ». S'il reste le moindre mot qui dit quelque chose, c'est une
#  VRAIE reponse, et on la garde.
#
#  Du coup : « Je ne sais pas, desolee. » est bien un « je ne sais pas » ; « je ne sais plus
#  l'annee mais c'est Famille » est une vraie reponse. Et un numero qu'on laisse simplement
#  SANS REPONSE n'est pas touche du tout : sa fiche reste exactement ou elle est.
MOTS_SANS_INFORMATION = {
    "je", "j", "ne", "n", "pas", "plus", "rien", "sais", "savoir", "peux", "ignore", "l",
    "aucune", "aucun", "idee", "idée", "la", "le", "les", "ca", "ça", "cela", "dessus",
    "desole", "desolee", "désolé", "désolée", "pardon", "malheureusement", "vraiment",
    "du", "tout", "de", "a", "à", "y", "en", "c", "est", "ce", "pour", "moment", "instant",
    "hesite", "hésite", "hesitant", "me", "souviens", "connais", "vois", "crois", "tres",
    "très", "bien", "sur", "sûr", "sure", "sûre", "et", "ou", "mais", "donc", "alors",
}

#  LE MARQUEUR POUR CHANGER DE RAYON. Volontairement explicite : sans marqueur, on ne
#  deplace RIEN. Une phrase ordinaire qui contient une barre oblique (« 2 h / jour », « et/ou »,
#  « Famille / Souvenirs est le bon rayon ») ne peut donc pas faire bouger une fiche par
#  accident. La reponse SANS marqueur veut dire « oui, ce rayon-la convient ».
MARQUEUR_RAYON = "RAYON:"

DEFAUT_QUESTIONS_PAR_TOUR = 5
DEFAUT_LOT_MAXI = 40

#  =====================================================================
#  QUAND LE PROPRIETAIRE DIT « JE NE SAIS PAS », SA QUESTION S'ENDORT.
#  =====================================================================
#  CORRECTION APPORTEE EN ARRIVANT CHEZ LUCIANA (defaut trouve en relisant le deroule tour
#  par tour, et qui n'etait pas visible dans le test d'origine : son lot d'essai ne
#  contenait qu'une seule question, donc le cas ne se presentait jamais).
#
#  LE DEFAUT : une question a laquelle le proprietaire venait de repondre « je ne sais pas »
#  restait dans l'etat « posee au proprietaire »... et repartait donc DANS LE LOT SUIVANT,
#  c'est-a-dire au tour d'apres. Il se la voyait reposer a chaque message, indefiniment.
#  C'est exactement le harcelement que la regle de Fred interdit : « on ne harcele pas le
#  proprietaire avec une question, puis une autre, puis une autre ».
#
#  LA CORRECTION : une question qu'il a declinee S'ENDORT pour quelques jours. Elle n'est
#  pas jetee, elle n'est pas oubliee — elle reste lisible dans questions.json, et elle
#  reviendra d'elle-meme dans un lot plus tard. Il a juste la paix entre temps.
SOMMEIL_APRES_UN_REFUS_JOURS = 7


def _reglages():
    """LES TROIS NOMBRES DE LA CHAINE. Ne leve jamais.

    ADAPTATION CHEZ LUCIANA : son biblio2_reglages.py n'a pas de reglages_questions(). On le
    demande donc avec getattr. S'il n'est pas la — c'est le cas aujourd'hui — on prend les
    valeurs par defaut d'ici. On n'a ainsi eu a toucher ni biblio2_reglages.py, ni
    reglage_biblio2.json (que Fred a demande de laisser tranquille)."""
    defauts = {"questions_par_tour": DEFAUT_QUESTIONS_PAR_TOUR,
               "lot_proprietaire_maxi": DEFAUT_LOT_MAXI,
               "les_en_suspens_d_abord": True}
    try:
        f = getattr(reglages, "reglages_questions", None)
        if callable(f):
            v = f() or {}
            return {
                "questions_par_tour": int(v.get("questions_par_tour")
                                          or defauts["questions_par_tour"]),
                "lot_proprietaire_maxi": int(v.get("lot_proprietaire_maxi")
                                             or defauts["lot_proprietaire_maxi"]),
                "les_en_suspens_d_abord": bool(v.get("les_en_suspens_d_abord", True)),
            }
    except Exception:
        pass
    return defauts


#  LE DOSSIER FORCE. Il reste vide en service : les chemins viennent alors du reglage, donc
#  de ~/Luciana/bibliotheque2. Le test de ce fichier le fait pointer vers un dossier a
#  cote, pour n'ecrire NULLE PART dans la memoire reelle de personne.
DOSSIER_FORCE = ""

NOMS_DES_FICHIERS = {"questions": "questions.json",
                     "lot": "lot_pour_le_proprietaire.json",
                     "reponses": "reponses.json"}

NOMS_DES_REGLAGES = {"questions": "FICHIER_QUESTIONS",
                     "lot": "FICHIER_LOT_PROPRIO",
                     "reponses": "FICHIER_REPONSES"}


def dossier_de_la_memoire():
    """LE DOSSIER DE LA MEMOIRE 2 DE LUCIANA, ET JAMAIS CELUI DE QUELQU'UN D'AUTRE.

    Le maitre est biblio2_reglages.DOSSIER_BIBLIO2, qui vaut ~/Luciana/bibliotheque2. Le
    dernier recours le refabrique a l'identique. Aucun autre dossier n'est nomme dans ce
    fichier. Ne leve jamais."""
    try:
        d = str(getattr(reglages, "DOSSIER_BIBLIO2", "") or "")
        if d:
            return d
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), "Luciana", "bibliotheque2")


def _chemin(nom, defaut_dossier=None):
    """Le chemin d'un des trois fichiers de la chaine. Ne leve jamais."""
    if DOSSIER_FORCE:
        return os.path.join(DOSSIER_FORCE, NOMS_DES_FICHIERS[nom])
    try:
        c = str(getattr(reglages, NOMS_DES_REGLAGES[nom], "") or "")
        if c:
            return c
    except Exception:
        pass
    return os.path.join(defaut_dossier or dossier_de_la_memoire(), NOMS_DES_FICHIERS[nom])


def _ecrire_json(chemin, contenu):
    """ECRITURE DE REMPLACEMENT : on ecrit a cote, puis on bascule d'un coup. Une coupure
    de courant ne peut pas laisser le fichier a moitie ecrit. Rend True si c'est ecrit."""
    try:
        dossier = os.path.dirname(os.path.abspath(chemin))
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        tmp = chemin + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(contenu, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, chemin)
        return True
    except Exception:
        return False


def _lire_json(chemin, defaut):
    try:
        with open(chemin, encoding="utf-8-sig") as f:
            d = json.load(f)
        return d if isinstance(d, type(defaut)) else defaut
    except Exception:
        return defaut


def _fiches(arbre):
    """Toutes les fiches : [(cat, sous, fiche), ...]. On passe par l'archiviste (le seul
    qui sait comment l'arbre est pose sur le disque) ; s'il manque, on sait le faire ici."""
    if arch is not None:
        try:
            return arch.toutes_les_fiches(arbre)
        except Exception:
            pass
    out = []
    for cat, sous_cats in (arbre or {}).items():
        if not isinstance(sous_cats, dict):
            continue
        for sous, fiches in sous_cats.items():
            if not isinstance(fiches, list):
                continue
            for fi in fiches:
                if isinstance(fi, dict):
                    out.append((cat, sous, fi))
    return out


def _etiquette(cat, sous, fiche):
    if arch is not None:
        try:
            return arch.etiquette_de(cat, sous, fiche)
        except Exception:
            pass
    return str(fiche.get("resume") or fiche.get("texte") or "")[:300]


# =====================================================================
#  TEMPS 1 — L'ARCHIVISTE ECRIT SA QUESTION, COLLEE A LA FICHE.
# =====================================================================

def question_de(cat, sous, fiche, raison=""):
    """LA QUESTION QUE L'ARCHIVISTE ECRIT, en clair, pour CETTE fiche-la.

    Elle dit trois choses, et rien de plus : CE QU'IL A SOUS LES YEUX (un extrait du
    souvenir), OU IL L'A POSE EN ATTENDANT, et CE QU'IL LUI MANQUE POUR TRANCHER. Elle est
    courte expres : une question longue n'obtient pas de reponse.

    Ne leve jamais ; rend "" si vraiment il n'y a rien a demander."""
    try:
        fi = fiche if isinstance(fiche, dict) else {}
        extrait = str(fi.get("resume") or fi.get("texte") or "").strip()
        extrait = " ".join(extrait.split())[:220]
        if not extrait:
            return ""
        pourquoi = str(raison or fi.get("pourquoi_en_suspens")
                       or fi.get("alerte_luciana") or "").strip()
        divers = (arch.DIVERS if arch is not None else "Divers")
        if str(cat) == divers:
            manque = ("Dans quel rayon ce souvenir doit-il aller ? Je l'ai pose dans "
                      "« %s / %s » en attendant, pour ne pas le perdre." % (cat, sous))
        else:
            manque = ("Est-ce que « %s / %s » est le bon rayon pour ce souvenir, ou faut-il "
                      "le mettre ailleurs ?" % (cat, sous))
        return ("Ce souvenir : « %s »\n%s%s"
                % (extrait, manque,
                   ("\n(ce qui m'a fait hesiter : %s)" % pourquoi) if pourquoi else ""))
    except Exception:
        return ""


def ecrire_la_question(cat, sous, fiche, raison=""):
    """COLLE LA QUESTION A LA FICHE. C'est le geste du temps 1, et il tient en une ligne de
    pensee : la question VIT DANS la fiche, jamais a cote.

    Rend True si une question vient d'etre ecrite, False si la fiche en avait deja une (on
    ne la reecrit pas : la reecrire effacerait l'etat ou elle en est). Ne leve jamais."""
    try:
        if not isinstance(fiche, dict):
            return False
        if fiche.get("question") and fiche.get("question_etat") in ETATS:
            return False                        # elle en a deja une, et elle suit son chemin
        q = question_de(cat, sous, fiche, raison)
        if not q:
            return False
        fiche["question"] = q
        fiche["question_etat"] = OUVERTE
        fiche["question_ecrite_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
        fiche["question_reponse"] = ""
        fiche["question_repondue_par"] = ""
        return True
    except Exception:
        return False


def amorcer(arbre):
    """LES FICHES DEJA EN SUSPENS SONT LES PREMIERES SERVIES. (demande explicite de Fred)

    A appeler au DEMARRAGE de l'archiviste, avant tout nouveau rangement. On passe sur toute
    la bibliotheque et on ECRIT une question sur chaque fiche deja en suspens qui n'en a pas
    encore. Comme la file est servie dans l'ordre de l'arbre, et que ces fiches sont les plus
    anciennes, elles passent devant le travail du jour, sans qu'on ait a tenir une file a
    part. Rend les chiffres, pour pouvoir DIRE l'avant / apres. Ne leve jamais."""
    ecrites = deja = 0
    try:
        for cat, sous, fi in _fiches(arbre):
            if not fi.get("en_suspens"):
                continue
            if ecrire_la_question(cat, sous, fi):
                ecrites += 1
            else:
                deja += 1
    except Exception:
        pass
    return {"questions_ecrites_maintenant": ecrites, "en_avaient_deja_une": deja,
            "en_suspens_en_tout": ecrites + deja}


# ---------------------------------------------------------------------
#  LA FILE : les questions dans l'ordre, les plus anciennes d'abord.
# ---------------------------------------------------------------------

def en_sommeil(fiche):
    """VRAI quand cette question dort encore (le proprietaire l'a declinee recemment).

    Voir l'explication en haut du fichier (SOMMEIL_APRES_UN_REFUS_JOURS) : sans ce
    sommeil, une question qu'il vient de decliner lui serait reposee au tour suivant, puis
    au suivant, indefiniment. Ne leve jamais : au moindre doute, la question est reveillee
    (on prefere la reposer un jour trop tot que la perdre)."""
    try:
        jusqu_au = str((fiche or {}).get("question_en_sommeil_jusqu_au") or "")
        if not jusqu_au:
            return False
        return time.strftime("%Y-%m-%d %H:%M:%S") < jusqu_au
    except Exception:
        return False


def _file(arbre, etats):
    """Les fiches dont la question est dans un des etats demandes, DANS L'ORDRE DE L'ARBRE
    (donc les plus anciennement rangees d'abord). Rend [(cat, sous, fiche), ...].

    LES QUESTIONS QUI DORMENT SONT MISES DE COTE : le proprietaire vient de les decliner,
    on ne les lui repose pas tout de suite. Elles reviendront d'elles-memes."""
    out = []
    for cat, sous, fi in _fiches(arbre):
        if fi.get("question") and fi.get("question_etat") in etats and not en_sommeil(fi):
            out.append((cat, sous, fi))
    return out


def compter(arbre):
    """L'ETAT DE LA CHAINE, en chiffres. Pour dire l'avant / apres sans deviner."""
    c = {e: 0 for e in ETATS}
    sans_question = 0
    for _cat, _sous, fi in _fiches(arbre):
        etat = fi.get("question_etat")
        if fi.get("question") and etat in c:
            c[etat] += 1
        elif fi.get("en_suspens"):
            sans_question += 1
    c["en_suspens_sans_question"] = sans_question
    return c


# =====================================================================
#  TEMPS 2 — LE PROGRAMME POSE LES QUESTIONS A L'ASSISTANTE.
#  C'EST LE PROGRAMME QUI LES POSE. JAMAIS SA VIGILANCE.
# =====================================================================

#  CES DEUX PHRASES SONT LA CONVENTION, ET ELLES SONT DITES A CHAQUE FOIS. On ne suppose
#  jamais qu'elle « sait deja comment repondre » : le programme le lui rappelle a chaque
#  bloc. C'est ce qui rend la lecture des reponses SURE au lieu d'etre une devinette.
COMMENT_REPONDRE = (
    "Comment repondre :\n"
    "  - une ligne par question, le numero devant : « 1) ... »\n"
    "  - pour ranger ailleurs, finis la ligne par : %s LeRayon / LeTiroir\n"
    "  - si le rayon propose convient, reponds simplement, sans %s\n"
    "  - si tu n'as pas l'information, ecris « je ne sais pas »\n"
    "  - un numero que tu laisses de cote reste exactement ou il est : rien n'est perdu\n"
) % (MARQUEUR_RAYON, MARQUEUR_RAYON)

ENTETE_ASSISTANTE = (
    "QUESTIONS DE L'ARCHIVISTE DE TA MEMOIRE (ce bloc est ecrit par LE PROGRAMME, "
    "pas par toi).\n"
    "L'archiviste a range ces souvenirs, et sur chacun il lui manque une chose pour "
    "terminer. Reponds par ce que tu sais. Pour celles ou tu n'as pas l'information, le "
    "programme les rassemblera et les posera au proprietaire en une seule fois : tu n'as "
    "pas a t'en occuper.\n"
    + COMMENT_REPONDRE
)


def bloc_pour_l_assistante(arbre, combien=None):
    """LE BLOC QUE LE PROGRAMME POSE A L'ASSISTANTE dans le tour. Rend (texte, reperes).

    'reperes' est la liste, DANS L'ORDRE DES NUMEROS, des reperes des fiches concernees :
    c'est elle qui permettra de faire redescendre chaque reponse SUR LA BONNE FICHE.

    Rend ("", []) quand il n'y a rien a demander — et c'est le cas normal : la plupart des
    tours n'ont aucune question, et le bloc ne coute alors pas un seul caractere.

    CE BLOC NE PART QU'AVEC LES QUESTIONS OUVERTES OU DEJA POSEES A ELLE. Ce qui attend le
    proprietaire n'y revient jamais : on ne lui repose pas une question qu'elle a deja dit
    ne pas savoir. Ne leve jamais."""
    try:
        if combien is None:
            combien = int(_reglages()["questions_par_tour"])
        file = _file(arbre, (OUVERTE, POSEE_ASSISTANTE))
        if not file:
            return "", []
        lot = file[:max(1, int(combien))]
        lignes, reperes = [], []
        for n, (cat, sous, fi) in enumerate(lot, 1):
            lignes.append("%d) %s" % (n, fi.get("question") or ""))
            reperes.append(fi.get("repere") or "")
            fi["question_etat"] = POSEE_ASSISTANTE
            fi["question_posee_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
        reste = len(file) - len(lot)
        fin = ("\n(il y en a %d autre(s) ensuite : le programme te les posera plus tard, "
               "quelques-unes a la fois.)" % reste) if reste > 0 else ""
        return ENTETE_ASSISTANTE + "\n".join(lignes) + fin, reperes
    except Exception:
        return "", []


# =====================================================================
#  TEMPS 3 — SA REPONSE REPART AVEC LA FICHE, ET L'ARCHIVISTE LA RANGE.
# =====================================================================

def _dit_qu_elle_ne_sait_pas(reponse):
    """VRAI quand la reponse ne porte AUCUNE information. Voir l'explication en haut du
    fichier (MOTS_SANS_INFORMATION) : on enleve les politesses, la negation et le
    remplissage ; s'il ne reste rien, c'est un « je ne sais pas ». Ne leve jamais."""
    import re as _re
    try:
        mots = _re.findall(r"[0-9a-zA-Zàâäçéèêëîïôöûùüÿñ]+", str(reponse or "").lower())
        return not [m for m in mots if m not in MOTS_SANS_INFORMATION]
    except Exception:
        return True


def _lire_le_rayon(reponse):
    """LE RAYON OU DEPLACER LA FICHE, lu dans la reponse — ET SEULEMENT SUR MARQUEUR
    EXPLICITE (« RAYON: LeRayon / LeTiroir », en fin de ligne). Rend (categorie, tiroir), ou
    ("", "") quand il n'y a pas de marqueur.

    POURQUOI UN MARQUEUR, ET PAS UNE SIMPLE BARRE OBLIQUE : une phrase ordinaire en contient
    tres souvent une (« 2 h / jour », « et/ou », « Famille / Souvenirs est le bon rayon »).
    Sans marqueur, on deplacerait des fiches par accident, vers des tiroirs aux noms
    absurdes. Sans marqueur, la fiche est donc tranchee LA OU ELLE EST — ce qui est le sens
    normal de « oui, ce rayon-la convient ». Ne leve jamais."""
    import re as _re
    try:
        m = _re.search(r"rayon\s*[:=]\s*([^/\n;]{1,40}?)\s*/\s*([^\n;,]{1,40}?)\s*$",
                       str(reponse or ""), _re.IGNORECASE)
        if not m:
            return "", ""
        return m.group(1).strip(" .,;:"), m.group(2).strip(" .,;:")
    except Exception:
        return "", ""


def trouver(arbre, repere):
    """Rend (categorie, sous_categorie, fiche) pour ce repere, ou (None, None, None).
    Ne leve jamais."""
    try:
        for cat, sous, fi in _fiches(arbre):
            if fi.get("repere") == repere:
                return cat, sous, fi
    except Exception:
        pass
    return None, None, None


def deplacer(arbre, repere, vers_categorie, vers_sous_categorie):
    """DEPLACE la fiche dans un autre rayon, en GARDANT SON REPERE (elle ne peut donc pas
    etre rangee deux fois). Cree les etages manquants. Rend l'ancien chemin, ou "" si rien
    n'a bouge. Ne leve jamais.

    On enleve d'abord, on remet ensuite, et on remet TOUJOURS : il n'y a aucun instant ou
    la fiche n'est nulle part dans l'arbre en memoire."""
    try:
        cat, sous, fi = trouver(arbre, repere)
        if fi is None:
            return ""
        vers_cat = str(vers_categorie or "").strip() or cat
        vers_sous = str(vers_sous_categorie or "").strip() or sous
        if (vers_cat, vers_sous) == (cat, sous):
            return ""
        if not isinstance(arbre.get(vers_cat), dict):
            arbre[vers_cat] = {}
        if not isinstance(arbre[vers_cat].get(vers_sous), list):
            arbre[vers_cat][vers_sous] = []
        arbre[vers_cat][vers_sous].append(fi)
        try:
            arbre[cat][sous] = [x for x in arbre[cat][sous] if x is not fi]
        except Exception:
            pass
        #  l'etiquette de sens porte le rayon : elle doit suivre le deplacement, sinon le
        #  moteur de score continuerait de comparer la question a l'ancien rayon.
        fi["etiquette"] = _etiquette(vers_cat, vers_sous, fi)
        return "%s / %s" % (cat, sous)
    except Exception:
        return ""


def ranger_la_reponse(arbre, repere, reponse, par="l_assistante",
                      vers_categorie="", vers_sous_categorie=""):
    """LA REPONSE REDESCEND JUSQU'A LA FICHE, ET LA FICHE EST RANGEE. C'est le geste qui
    termine la chaine, et c'est le seul endroit qui leve l'etiquette « en suspens ».

    Rend un petit rapport clair : ce qui a ete fait, et ou la fiche se trouve maintenant.
    Ne leve jamais.

    DEUX CAS, ET DEUX SEULEMENT :
      - la reponse dit quelque chose : la fiche est tranchee, elle n'est plus en suspens,
        et si la reponse donne un autre rayon, la fiche y est DEPLACEE ;
      - la reponse dit « je ne sais pas » : la fiche RESTE en suspens, sa question passe
        au lot du proprietaire, et rien n'est perdu."""
    try:
        cat, sous, fi = trouver(arbre, repere)
        if fi is None:
            return {"fait": False, "pourquoi": "cette fiche n'est plus dans la bibliotheque"}
        #  LA CHAINE NE REPOND QU'AUX QUESTIONS QU'ELLE A POSEES. Une fiche qui n'a jamais eu
        #  de question n'est pas touchee : sans ce garde-fou, une reponse mal numerotee
        #  pourrait marquer « tranchee » une fiche qui allait tres bien.
        if not fi.get("question"):
            return {"fait": False, "pourquoi": "cette fiche n'a pas de question ouverte",
                    "ou": "%s / %s" % (cat, sous)}
        if _dit_qu_elle_ne_sait_pas(reponse):
            if par == "l_assistante":
                fi["question_etat"] = A_POSER_PROPRIO
                fi["question_passee_au_lot_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
                return {"fait": True, "tranchee": False, "part_au_proprietaire": True,
                        "ou": "%s / %s" % (cat, sous)}
            # LE PROPRIETAIRE LUI-MEME NE SAIT PAS. On n'invente rien a sa place : la
            # question reste la, entiere, et sa fiche ne bouge pas. Mais ELLE S'ENDORT
            # quelques jours, sinon elle lui serait reposee au tour suivant, et au suivant,
            # indefiniment (voir SOMMEIL_APRES_UN_REFUS_JOURS en haut du fichier).
            fi["question_etat"] = POSEE_PROPRIO
            fi["question_declinee_fois"] = int(fi.get("question_declinee_fois") or 0) + 1
            fi["question_declinee_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            fi["question_en_sommeil_jusqu_au"] = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(time.time() + SOMMEIL_APRES_UN_REFUS_JOURS * 86400))
            return {"fait": True, "tranchee": False, "part_au_proprietaire": True,
                    "mise_en_sommeil_jusqu_au": fi["question_en_sommeil_jusqu_au"],
                    "ou": "%s / %s" % (cat, sous)}

        ancien = deplacer(arbre, repere, vers_categorie, vers_sous_categorie)
        cat, sous, fi = trouver(arbre, repere)
        fi["question_reponse"] = " ".join(str(reponse).split())[:1000]
        fi["question_repondue_par"] = par
        fi["question_etat"] = REPONDUE
        fi["question_repondue_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
        fi["question_en_sommeil_jusqu_au"] = ""   # tranchee : elle n'a plus a dormir
        fi["en_suspens"] = False
        fi["pourquoi_en_suspens"] = ""
        #  ADAPTATION CHEZ LUCIANA : son archiviste ecrit AUSSI le motif du doute dans
        #  'alerte_luciana' (biblio2_archiviste.py, ligne 404). Si on ne l'effacait pas ici,
        #  une fiche tranchee continuerait d'afficher « [EN SUSPENS : ...] » dans les
        #  rapports de reprise. On leve donc les DEUX etiquettes, pas une seule.
        if "alerte_luciana" in fi:
            fi["alerte_luciana"] = ""
        fi["tranche_par"] = par
        fi["etiquette"] = _etiquette(cat, sous, fi)
        return {"fait": True, "tranchee": True, "part_au_proprietaire": False,
                "ou": "%s / %s" % (cat, sous),
                "deplacee_depuis": ancien, "par": par}
    except Exception as ex:
        return {"fait": False, "pourquoi": str(ex)[:160]}


def ranger_les_reponses(arbre, reperes, texte_de_la_reponse, par="l_assistante"):
    """LES REPONSES NUMEROTEES, RELUES ET RANGEES D'UN COUP.

    'reperes' = la liste rendue par bloc_pour_l_assistante() ou par bloc_pour_le_proprietaire()
    'texte_de_la_reponse' = ce qui a ete repondu, en clair, une ligne par numero :
          1) c'est un souvenir de famille
          2) je ne sais pas
          3) Sante / Rendez-vous

    LA LECTURE EST VOLONTAIREMENT GENEREUSE : un numero suivi de « ) », « . », « - » ou
    « : » suffit. Une ligne sans numero lisible est rattachee a la question precedente
    (c'est ce qui arrive quand une reponse tient sur deux lignes). Une reponse pour un
    numero qui n'existe pas est IGNOREE et DITE, jamais appliquee au hasard.

    Quand une reponse contient « RAYON: RAYON / TIROIR », on y lit le rayon ou deplacer la
    fiche. Ne leve jamais."""
    import re as _re
    rapport = {"tranchees": 0, "parties_au_proprietaire": 0, "numeros_inconnus": [],
               "details": []}
    try:
        reperes = list(reperes or [])
        lignes = [l for l in str(texte_de_la_reponse or "").splitlines()]
        par_numero, dernier = {}, None
        for ligne in lignes:
            m = _re.match(r"\s*(\d{1,3})\s*[\)\.\:\-]\s*(.*)$", ligne)
            if m:
                dernier = int(m.group(1))
                par_numero[dernier] = m.group(2).strip()
            elif dernier is not None and ligne.strip():
                par_numero[dernier] = (par_numero.get(dernier, "") + " " + ligne.strip()).strip()
        for numero, reponse in sorted(par_numero.items()):
            if not (1 <= numero <= len(reperes)):
                rapport["numeros_inconnus"].append(numero)
                continue
            #  LE DEPLACEMENT NE SE FAIT QUE SUR MARQUEUR EXPLICITE (« RAYON: X / Y »).
            vers_cat, vers_sous = _lire_le_rayon(reponse)
            r = ranger_la_reponse(arbre, reperes[numero - 1], reponse, par=par,
                                  vers_categorie=vers_cat, vers_sous_categorie=vers_sous)
            if r.get("tranchee"):
                rapport["tranchees"] += 1
            elif r.get("part_au_proprietaire"):
                rapport["parties_au_proprietaire"] += 1
            rapport["details"].append({"numero": numero, "repere": reperes[numero - 1],
                                       "resultat": r})
    except Exception as ex:
        rapport["pourquoi"] = str(ex)[:160]
    return rapport


# =====================================================================
#  TEMPS 4 — UN SEUL LOT POUR LE PROPRIETAIRE. JAMAIS QUESTION PAR QUESTION.
# =====================================================================

ENTETE_PROPRIO = (
    "J'ai mis de cote %d chose(s) que je n'arrive pas a classer toute seule, et je te les "
    "demande TOUTES EN UNE SEULE FOIS — comme ca tu n'y reviens qu'une fois, et je ne te "
    "coupe pas vingt fois dans ta journee.\n"
    "Reponds a celles que tu veux. Celles que tu laisses de cote restent exactement ou "
    "elles sont, rien n'est perdu.\n"
    + COMMENT_REPONDRE
)


def bloc_pour_le_proprietaire(arbre, combien=None, ecrire=True):
    """LE LOT, RAMASSE ET POSE D'UN SEUL COUP. Rend (texte, reperes).

    C'est la regle dure de Fred : ce que l'assistante ne sait pas est RAMASSE, et pose au
    proprietaire EN UN SEUL LOT, jamais question par question. Tant qu'il n'y a rien dans le
    lot, cette fonction rend ("", []) — et c'est le cas normal.

    'ecrire' ecrit aussi le lot dans lot_pour_le_proprietaire.json, pour qu'on puisse le
    relire plus tard meme si le tour s'est mal passe. Le fichier REMPLACE le precedent : il
    ne s'empile pas. Ne leve jamais."""
    try:
        r = _reglages()
        if combien is None:
            combien = int(r["lot_proprietaire_maxi"])
        #  ce qui attend le proprietaire : ce qu'elle ne savait pas, et ce qui lui avait
        #  deja ete pose sans reponse (on le repose, dans le MEME lot, pas a part).
        file = _file(arbre, (A_POSER_PROPRIO, POSEE_PROPRIO))
        if not file:
            return "", []
        lot = file[:max(1, int(combien))]
        reste = len(file) - len(lot)
        lignes, reperes, pour_le_fichier = [], [], []
        for n, (cat, sous, fi) in enumerate(lot, 1):
            lignes.append("%d) %s" % (n, fi.get("question") or ""))
            reperes.append(fi.get("repere") or "")
            pour_le_fichier.append({"numero": n, "repere": fi.get("repere") or "",
                                    "ou_elle_est": "%s / %s" % (cat, sous),
                                    "question": fi.get("question") or "",
                                    "depuis": fi.get("question_ecrite_le") or ""})
            fi["question_etat"] = POSEE_PROPRIO
            fi["question_posee_au_proprietaire_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
        fin = ("\n(il y en a %d autre(s) encore : je te les demanderai dans un prochain lot, "
               "jamais une par une.)" % reste) if reste > 0 else ""
        texte = (ENTETE_PROPRIO % len(lot)) + "\n".join(lignes) + fin
        if ecrire:
            _ecrire_json(_chemin("lot"), {
                "_a_quoi_ca_sert": ("LE LOT DE QUESTIONS POSE AU PROPRIETAIRE, D'UN SEUL "
                                    "COUP. Ce fichier REMPLACE le precedent : il n'y a "
                                    "jamais deux lots en meme temps. Les reponses "
                                    "redescendent ensuite jusqu'aux fiches, et les fiches "
                                    "sont rangees."),
                "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
                #  on attend sa reponse : c'est ce drapeau qui dit au programme de lire la
                #  prochaine reponse numerotee du proprietaire comme une reponse A CE LOT.
                "en_attente_de_reponse": True,
                "combien_dans_ce_lot": len(lot),
                "combien_attendent_encore": reste,
                "questions": pour_le_fichier,
                "texte_tel_qu_il_est_pose": texte,
            })
        return texte, reperes
    except Exception:
        return "", []


def noter_le_bloc_pose(reperes):
    """GARDE LA NUMEROTATION DU DERNIER BLOC POSE A L'ASSISTANTE, sur le disque.

    A QUOI CA SERT, ET C'EST LE COEUR DU TEMPS 3 : elle repond au tour SUIVANT. Entre les
    deux, le programme a pu etre relance. Sans cette trace, la reponse « 1) ... » ne saurait
    plus de quelle fiche elle parle, et on perdrait la reponse — ou bien, pire, on
    l'appliquerait a la mauvaise fiche. Avec elle, les numeros survivent a tout.

    Le fichier REMPLACE le precedent : il n'y a jamais deux numerotations en meme temps.
    Ne leve jamais."""
    d = _lire_json(_chemin("questions"), {})
    if not isinstance(d, dict):
        d = {}
    d["dernier_bloc_pose"] = {"quand": time.strftime("%Y-%m-%d %H:%M:%S"),
                              "reperes": [str(r) for r in (reperes or [])]}
    _ecrire_json(_chemin("questions"), d)
    return len(reperes or [])


def relire_le_bloc_pose():
    """LA NUMEROTATION DU DERNIER BLOC POSE A L'ASSISTANTE. Rend la liste des reperes, dans
    l'ordre des numeros, ou [] s'il n'y a rien en attente. Ne leve jamais."""
    try:
        d = _lire_json(_chemin("questions"), {})
        return [str(r) for r in ((d.get("dernier_bloc_pose") or {}).get("reperes") or [])]
    except Exception:
        return []


def oublier_le_bloc_pose():
    """EFFACE LA NUMEROTATION une fois les reponses rangees, pour qu'une reponse ne soit
    jamais relue deux fois. Ne leve jamais."""
    try:
        d = _lire_json(_chemin("questions"), {})
        if isinstance(d, dict) and "dernier_bloc_pose" in d:
            d.pop("dernier_bloc_pose", None)
            _ecrire_json(_chemin("questions"), d)
        return True
    except Exception:
        return False


def le_lot_attend_une_reponse():
    """VRAI quand un lot a ete pose au proprietaire et qu'on attend encore sa reponse.
    Ne leve jamais."""
    try:
        d = _lire_json(_chemin("lot"), {})
        return bool(d.get("en_attente_de_reponse")) and bool(d.get("questions"))
    except Exception:
        return False


def le_lot_est_repondu():
    """NOTE QUE LE LOT A RECU SA REPONSE : on ne le reposera pas en boucle. Ne leve jamais."""
    try:
        d = _lire_json(_chemin("lot"), {})
        if isinstance(d, dict):
            d["en_attente_de_reponse"] = False
            d["repondu_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _ecrire_json(_chemin("lot"), d)
        return True
    except Exception:
        return False


def relire_le_lot():
    """RELIT LE DERNIER LOT POSE AU PROPRIETAIRE, tel qu'il a ete ecrit sur le disque.
    Rend (texte, reperes).

    A QUOI CA SERT, ET C'EST IMPORTANT : entre le moment ou le lot est pose et le moment ou
    le proprietaire repond, il peut se passer des heures — et le programme peut avoir ete
    relance entre temps. Sans ce relecteur, la numerotation du lot serait perdue et la
    reponse « 1) ... » ne saurait plus de quelle fiche elle parle. Avec lui, les numeros
    survivent a un redemarrage. Ne leve jamais."""
    d = _lire_json(_chemin("lot"), {})
    try:
        questions = d.get("questions") or []
        reperes = [str(q.get("repere") or "") for q in questions]
        return str(d.get("texte_tel_qu_il_est_pose") or ""), reperes
    except Exception:
        return "", []


def garder_les_questions(arbre):
    """ECRIT LA LISTE DES QUESTIONS OUVERTES dans questions.json, pour qu'on puisse la LIRE
    sans lancer le programme. La verite reste DANS les fiches : ce fichier est une vue, et
    il REMPLACE le precedent. Rend le nombre de questions ecrites. Ne leve jamais."""
    try:
        ouvertes = []
        for cat, sous, fi in _fiches(arbre):
            if fi.get("question") and fi.get("question_etat") != REPONDUE:
                ouvertes.append({"repere": fi.get("repere") or "",
                                 "ou_elle_est": "%s / %s" % (cat, sous),
                                 "etat": fi.get("question_etat") or "",
                                 "question": fi.get("question") or "",
                                 "depuis": fi.get("question_ecrite_le") or "",
                                 #  pour pouvoir LIRE, sans lancer le programme, quelles
                                 #  questions dorment parce qu'elles ont ete declinees
                                 "dort_jusqu_au": (fi.get("question_en_sommeil_jusqu_au")
                                                   or "") if en_sommeil(fi) else ""})
        #  ON GARDE LA NUMEROTATION DU DERNIER BLOC POSE. Sans cette precaution, reecrire la
        #  vue des questions effacerait les numeros en attente, et la reponse de l'assistante
        #  au tour suivant ne saurait plus de quelle fiche elle parle.
        ancien = _lire_json(_chemin("questions"), {})
        contenu = {
            "_a_quoi_ca_sert": ("LES QUESTIONS DE L'ARCHIVISTE QUI ATTENDENT ENCORE UNE "
                                "REPONSE. Chaque question vit DANS sa fiche : ce fichier "
                                "n'est qu'une vue, pour pouvoir la LIRE d'un coup d'oeil. "
                                "Il REMPLACE le precedent, il ne s'empile pas."),
            "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
            "combien": len(ouvertes),
            "les_cinq_etats": list(ETATS),
            "questions": ouvertes,
        }
        if isinstance(ancien, dict) and ancien.get("dernier_bloc_pose"):
            contenu["dernier_bloc_pose"] = ancien["dernier_bloc_pose"]
        _ecrire_json(_chemin("questions"), contenu)
        return len(ouvertes)
    except Exception:
        return 0


def garder_les_reponses(arbre):
    """GARDE LA TRACE DE CE QUI A ETE TRANCHE, dans reponses.json. Ce n'est pas la chaine
    elle-meme (la verite reste DANS les fiches) : c'est une trace lisible, pour pouvoir
    relire plus tard qui a tranche quoi, et quand. Le fichier REMPLACE le precedent.
    Rend le nombre de reponses gardees. Ne leve jamais."""
    try:
        tranchees = []
        for cat, sous, fi in _fiches(arbre):
            if fi.get("question_etat") == REPONDUE and fi.get("question_reponse"):
                tranchees.append({"repere": fi.get("repere") or "",
                                  "ou": "%s / %s" % (cat, sous),
                                  "question": fi.get("question") or "",
                                  "reponse": fi.get("question_reponse") or "",
                                  "par": fi.get("question_repondue_par") or "",
                                  "quand": fi.get("question_repondue_le") or ""})
        _ecrire_json(_chemin("reponses"), {
            "_a_quoi_ca_sert": ("LES QUESTIONS DEJA TRANCHEES, et par qui. La verite vit "
                                "DANS les fiches de la bibliotheque ; ce fichier est une "
                                "trace lisible, pour pouvoir relire l'histoire des "
                                "decisions. Il REMPLACE le precedent, il ne s'empile pas."),
            "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
            "combien": len(tranchees),
            "tranchees": tranchees,
        })
        return len(tranchees)
    except Exception:
        return 0


def dire_l_etat(arbre):
    """L'ETAT DE LA CHAINE, en une phrase lisible. Pour les chiffres avant / apres."""
    c = compter(arbre)
    return ("chaine des questions : %d ouverte(s), %d posee(s) a l'assistante, "
            "%d en attente du lot, %d posee(s) au proprietaire, %d tranchee(s)"
            "%s"
            % (c[OUVERTE], c[POSEE_ASSISTANTE], c[A_POSER_PROPRIO], c[POSEE_PROPRIO],
               c[REPONDUE],
               (" | %d fiche(s) en suspens n'ont pas encore de question (lancez amorcer())"
                % c["en_suspens_sans_question"]) if c["en_suspens_sans_question"] else ""))


if __name__ == "__main__":
    # =====================================================================
    #  TEST ICI, SANS AUCUNE IA, SANS RESEAU, SANS AUCUNE DONNEE PERSONNELLE.
    #  On fabrique une petite bibliotheque de toutes pieces, on fait tourner la chaine
    #  des quatre temps, et on verifie chaque regle que Fred a posee.
    #  RIEN N'EST ECRIT DANS ~/Luciana/bibliotheque2 : les trois fichiers de la chaine
    #  sont ecrits dans un dossier d'essai, a cote du code.
    # =====================================================================
    rate = []

    def controle(nom, condition):
        print(("  OK   %s" if condition else "  RATE %s") % nom)
        if not condition:
            rate.append(nom)

    if arch is None:
        print("biblio2_archiviste.py est introuvable : ce test a besoin de lui.")
        raise SystemExit(1)

    #  ON N'ECRIT NULLE PART DANS UNE MEMOIRE REELLE : les trois fichiers de la chaine sont
    #  ecrits dans un dossier a cote du code, le temps du test.
    DOSSIER_FORCE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "_demo_chaine_des_questions")
    controle("LE TEST N'OUVRE PAS LA MEMOIRE REELLE : les trois fichiers vont dans le "
             "dossier d'essai", "_demo_chaine_des_questions" in _chemin("questions"))

    #  Une bibliotheque d'essai : deux fiches sures, trois fiches en suspens.
    arbre = {}
    essais = [
        ({"texte": "La voiture rouge a ete achetee en 2016.", "source": "essai"},
         {"categorie": "Vehicules", "sous_categorie": "Voitures",
          "filtres": {"date": "2016", "objet": "voiture rouge", "type": "achat"},
          "resume": "Voiture rouge achetee en 2016.", "confiance": 0.9}),
        ({"texte": "Rendez-vous chez le docteur Martin a Lyon le 2 mars.", "source": "essai"},
         {"categorie": "Sante", "sous_categorie": "Rendez-vous",
          "filtres": {"ou": "Lyon", "qui": ["Dr Martin"], "type": "medical"},
          "resume": "Rendez-vous medical a Lyon.", "confiance": 0.85}),
        # celle-ci : l'IA a un rayon en tete mais elle hesite -> en suspens, a sa place
        ({"texte": "Peut-etre un ete chez ma grand-mere, je ne sais plus l'annee.",
          "source": "essai"},
         {"categorie": "Famille", "sous_categorie": "Souvenirs",
          "filtres": {"type": "evenement"}, "resume": "Un ete chez ma grand-mere.",
          "confiance": 0.20}),
        # celle-ci : aucun rayon propose -> Divers / A trier, et on le DIT
        ({"texte": "Le truc bleu de la cave, je ne sais plus a quoi il sert.",
          "source": "essai"},
         {"categorie": "", "sous_categorie": "", "filtres": {}, "resume": "",
          "confiance": 0.2}),
        # et celle-ci aussi : aucun rayon propose
        ({"texte": "Il faudra repenser au dossier du mois dernier, celui qui traine.",
          "source": "essai"},
         {"categorie": "", "sous_categorie": "", "filtres": {}, "resume": "",
          "confiance": 0.1}),
    ]
    for souvenir, jugement in essais:
        souvenir["repere"] = arch.repere_de("essai", souvenir["texte"])
        arch.ranger(arbre, souvenir, arch.valider_jugement(jugement))

    fiches_au_depart = arch.compter(arbre)["fiches"]
    suspens_au_depart = arch.compter(arbre)["en_suspens"]

    print("=== AVANT LA CHAINE ===")
    print("  %d fiche(s) rangee(s), dont %d en suspens" % (fiches_au_depart, suspens_au_depart))
    print("  %s" % dire_l_etat(arbre))

    print("\n=== TEMPS 1 : L'ARCHIVISTE ECRIT SES QUESTIONS (les en suspens d'abord) ===")
    chiffres_amorce = amorcer(arbre)
    print("  %s" % chiffres_amorce)
    print("  %s" % dire_l_etat(arbre))

    print("\n=== TEMPS 2 : LE PROGRAMME POSE LES QUESTIONS A L'ASSISTANTE ===")
    bloc, reperes = bloc_pour_l_assistante(arbre)
    print(bloc)

    print("\n=== TEMPS 3 : ELLE REPOND A CE QU'ELLE SAIT ===")
    sa_reponse = ("1) c'est un souvenir de famille, Famille / Souvenirs est le bon rayon\n"
                  "2) je ne sais pas\n"
                  "3) je ne sais pas\n")
    print(sa_reponse)
    r3 = ranger_les_reponses(arbre, reperes, sa_reponse, par="l_assistante")
    print("  -> %d tranchee(s), %d partie(s) au lot du proprietaire"
          % (r3["tranchees"], r3["parties_au_proprietaire"]))
    print("  %s" % dire_l_etat(arbre))

    print("\n=== TEMPS 4 : UN SEUL LOT, POSE AU PROPRIETAIRE D'UN SEUL COUP ===")
    lot, reperes_lot = bloc_pour_le_proprietaire(arbre, ecrire=True)
    print(lot)
    print("  (le lot est aussi ecrit dans %s)" % _chemin("lot"))

    print("\n=== LE PROPRIETAIRE REPOND, ET LA REPONSE REDESCEND JUSQU'A LA FICHE ===")
    sa_reponse_a_lui = ("1) c'est le vieux compresseur, RAYON: Maison / Cave\n"
                        "2) je ne sais pas\n")
    print(sa_reponse_a_lui)
    r4 = ranger_les_reponses(arbre, reperes_lot, sa_reponse_a_lui, par="le_proprietaire")
    print("  -> %d tranchee(s), %d restee(s) en attente" % (r4["tranchees"],
                                                            r4["parties_au_proprietaire"]))

    print("\n=== APRES ===")
    c_fin = arch.compter(arbre)
    print("  %d fiche(s) rangee(s)  (avant : %d)" % (c_fin["fiches"], fiches_au_depart))
    print("  %d en suspens          (avant : %d)" % (c_fin["en_suspens"], suspens_au_depart))
    print("  %s" % dire_l_etat(arbre))

    print("\n=== CONTROLES ===")
    cc = compter(arbre)

    controle("TEMPS 1 : chaque fiche en suspens a recu une question, COLLEE A LA FICHE",
             chiffres_amorce["questions_ecrites_maintenant"] == suspens_au_depart
             and cc["en_suspens_sans_question"] == 0)
    controle("TEMPS 1 : la question est DANS la fiche (pas dans un fichier a cote)",
             all(fi.get("question") for _c, _s, fi in _fiches(arbre)
                 if fi.get("question_etat")))
    controle("TEMPS 1 : relancer amorcer() ne reecrit AUCUNE question (l'etat n'est pas perdu)",
             amorcer(arbre)["questions_ecrites_maintenant"] == 0)

    controle("TEMPS 2 : le bloc est bien ecrit PAR LE PROGRAMME, et il le dit",
             "ecrit par LE PROGRAMME" in bloc)
    controle("TEMPS 2 : le bloc pose au plus 'questions_par_tour' questions d'un coup",
             len(reperes) <= int(_reglages()["questions_par_tour"]))
    controle("TEMPS 2 : chaque question posee est rattachee a un repere de fiche",
             len(reperes) == len([l for l in bloc.splitlines()
                                  if l[:2].strip().rstrip(')').isdigit()]))

    controle("TEMPS 3 : ce qu'elle savait est TRANCHE, et la fiche n'est plus en suspens",
             r3["tranchees"] == 1
             and arbre["Famille"]["Souvenirs"][0]["en_suspens"] is False
             and arbre["Famille"]["Souvenirs"][0]["question_etat"] == REPONDUE)
    controle("TEMPS 3 : sa reponse est gardee DANS la fiche, avec qui a repondu",
             arbre["Famille"]["Souvenirs"][0]["question_reponse"]
             and arbre["Famille"]["Souvenirs"][0]["question_repondue_par"] == "l_assistante")
    controle("TEMPS 3 : ce qu'elle ne savait pas part au lot, et la fiche RESTE en suspens",
             r3["parties_au_proprietaire"] == 2)

    #  VERIFIE CHEZ LUCIANA : une fiche tranchee ne doit garder AUCUN motif de doute, sinon
    #  les rapports de reprise continueraient d'afficher « [EN SUSPENS : ...] » pour une
    #  fiche pourtant reglee. Les deux noms sont controles : 'pourquoi_en_suspens' (le seul
    #  que l'archiviste ecrive vraiment sur la fiche) et 'alerte_luciana' (qu'il n'ecrit que
    #  dans son rapport, mais on le controle quand meme, par precaution).
    controle("une fiche tranchee ne garde plus aucun motif de doute (ni "
             "'pourquoi_en_suspens', ni 'alerte_luciana')",
             not arbre["Famille"]["Souvenirs"][0].get("pourquoi_en_suspens")
             and not arbre["Famille"]["Souvenirs"][0].get("alerte_luciana"))

    controle("TEMPS 4 : le lot est pose EN UNE SEULE FOIS (un seul bloc, pas deux)",
             lot.count("J'ai mis de cote") == 1)
    controle("TEMPS 4 : le lot dit combien de choses il contient",
             "%d chose(s)" % len(reperes_lot) in lot)
    controle("TEMPS 4 : une question deja posee a l'assistante ne revient JAMAIS vers elle",
             bloc_pour_l_assistante(arbre)[0] == "")
    controle("TEMPS 4 : la reponse du proprietaire redescend jusqu'a la fiche, et la RANGE",
             r4["tranchees"] == 1
             and "Maison" in arbre and "Cave" in arbre.get("Maison", {})
             and arbre["Maison"]["Cave"][0]["en_suspens"] is False
             and arbre["Maison"]["Cave"][0]["question_repondue_par"] == "le_proprietaire")
    controle("TEMPS 4 : ce qu'il ne sait pas non plus reste en attente, sans rien inventer",
             r4["parties_au_proprietaire"] == 1)

    #  CORRECTION APPORTEE EN ARRIVANT CHEZ LUCIANA. Le test d'origine ne pouvait pas voir
    #  ce defaut : son lot ne contenait qu'une question, donc le cas « le proprietaire
    #  decline » ne se presentait jamais avec un lot encore vivant derriere.
    controle("CORRECTION LUCIANA : une question que le proprietaire vient de decliner "
             "S'ENDORT (elle n'est pas jetee, elle est mise de cote)",
             bool(r4["details"][-1]["resultat"].get("mise_en_sommeil_jusqu_au")))
    controle("CORRECTION LUCIANA : elle ne lui est donc PAS reposee tout de suite — c'est "
             "la fin du harcelement question par question",
             bloc_pour_le_proprietaire(arbre, ecrire=False)[0] == "")
    controle("CORRECTION LUCIANA : la question qui dort n'est PAS perdue, elle reste "
             "lisible avec sa fiche",
             any(fi.get("question") and fi.get("question_en_sommeil_jusqu_au")
                 for _c, _s, fi in _fiches(arbre)))

    controle("AUCUNE FICHE PERDUE : autant de fiches a la fin qu'au debut",
             c_fin["fiches"] == fiches_au_depart)
    controle("AUCUN DOUBLE RANGEMENT : les reperes sont tous differents",
             len({fi.get("repere") for _c, _s, fi in _fiches(arbre)}) == c_fin["fiches"])
    controle("UNE FICHE DEPLACEE GARDE SON REPERE (elle ne peut pas etre rangee deux fois)",
             arbre["Maison"]["Cave"][0]["repere"]
             == arch.repere_de("essai", "Le truc bleu de la cave, je ne sais plus a quoi il sert."))
    controle("UNE FICHE DEPLACEE A SON ETIQUETTE DE SENS REFAITE (avec son nouveau rayon)",
             "Maison" in arbre["Maison"]["Cave"][0]["etiquette"])
    controle("LE COMPTE DES EN SUSPENS A BAISSE DE 2 (les deux tranchees)",
             c_fin["en_suspens"] == suspens_au_depart - 2)

    controle("un numero qui n'existe pas est IGNORE et DIT, jamais applique au hasard",
             ranger_les_reponses(arbre, ["x"], "9) n'importe quoi")["numeros_inconnus"] == [9])
    controle("une reponse qui commence par « je ne sais pas » mais qui APPORTE quelque chose "
             "reste une VRAIE reponse (le piege a eviter)",
             not _dit_qu_elle_ne_sait_pas("je ne sais pas si c'est Lyon ou Paris, "
                                          "mais c'est bien un rendez-vous medical"))
    controle("« Je ne sais pas, desolee. » est bien reconnu comme un « je ne sais pas »",
             _dit_qu_elle_ne_sait_pas("Je ne sais pas, desolee."))
    controle("une reponse vide compte comme « je ne sais pas »", _dit_qu_elle_ne_sait_pas(""))
    controle("une fiche qui n'a JAMAIS eu de question n'est pas touchee par une reponse "
             "mal numerotee",
             ranger_les_reponses(arbre, [arbre["Sante"]["Rendez-vous"][0].get("repere")],
                                 "1) n'importe quoi")["tranchees"] == 0
             and not arbre["Sante"]["Rendez-vous"][0].get("question_etat"))
    controle("une phrase ordinaire avec une barre oblique ne DEPLACE AUCUNE fiche "
             "(il faut le marqueur RAYON:)",
             _lire_le_rayon("Famille / Souvenirs est le bon rayon") == ("", "")
             and _lire_le_rayon("c'est ca, RAYON: Maison / Cave") == ("Maison", "Cave"))
    controle("sans aucune question, le bloc ne coute pas un seul caractere",
             bloc_pour_l_assistante({})[0] == "")
    controle("sur un arbre abime, la chaine ne leve pas et rend du vide",
             bloc_pour_l_assistante({"x": "pas un dictionnaire"})[0] == ""
             and compter(None)[OUVERTE] == 0)

    controle("LE LOT SURVIT A UN REDEMARRAGE : relu sur le disque, il rend les MEMES "
             "numeros et les MEMES fiches",
             relire_le_lot()[1] == reperes_lot and relire_le_lot()[0] == lot)
    n_q = garder_les_questions(arbre)
    n_r = garder_les_reponses(arbre)
    #  LA VUE COMPTE TOUTES LES QUESTIONS PAS ENCORE TRANCHEES, Y COMPRIS CELLES QUI
    #  DORMENT : une question endormie attend toujours une reponse, elle doit donc rester
    #  lisible dans questions.json. (C'est pour cela qu'on ne compare pas a _file(), qui
    #  met expres les endormies de cote avant de POSER un bloc.)
    pas_encore_tranchees = len([1 for _c, _s, fi in _fiches(arbre)
                                if fi.get("question") and fi.get("question_etat") != REPONDUE])
    controle("les questions qui attendent encore sont LISIBLES dans questions.json "
             "(y compris celles qui dorment)",
             os.path.exists(_chemin("questions")) and n_q == pas_encore_tranchees)
    controle("les questions tranchees sont LISIBLES dans reponses.json, avec qui a tranche",
             os.path.exists(_chemin("reponses")) and n_r == 2)
    controle("les trois fichiers REMPLACENT le precedent (ils ne s'empilent pas)",
             garder_les_questions(arbre) == n_q and garder_les_reponses(arbre) == n_r)

    controle("VIERGE : ni Fred ni Luciana ne sont nommes dans ce qui est POSE",
             "Fred" not in bloc and "Luciana" not in bloc
             and "Fred" not in lot and "Luciana" not in lot)
    controle("RIEN NE S'ALLUME : la chaine ne rend que du TEXTE, aucun voyant, aucun bouton",
             isinstance(bloc, str) and isinstance(lot, str))

    print("\n%s" % ("TOUT EST PASSE." if not rate else
                    "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
    raise SystemExit(1 if rate else 0)
