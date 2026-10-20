# -*- coding: utf-8 -*-
"""
BRIQUE 1 — L'ARCHIVISTE.  Voie a part : il ne touche RIEN de la memoire vivante.

GREFFE DU 11/10/2026 — MORCEAU 1 (a) : la memoire 2 reparee le matin du 11/10, posee chez
Luminita. Fichier NEUF : s'il n'est pas la, le programme fait ce qu'il faisait hier.

LE PARTAGE DU TRAVAIL (la cle) :
  - LE PYTHON tient la STRUCTURE solide : l'arbre, le rangement, les compteurs, le
    decoupage, les secours. Deterministe : il n'oublie jamais, il ne bugue pas au sens.
  - LA PETITE IA ne fait QUE le SENS : "ce souvenir parle de quoi, il va dans quel tiroir ?".
    Elle repond dans un FORMAT STRICT (JSON) que le Python verifie et rattrape.

CE QUE FAIT L'ARCHIVISTE, ET RIEN D'AUTRE : il RECOIT un souvenir, il le RANGE, il
l'ETIQUETTE PAR SENS, et il TIENT LE PLAN. (Le bibliothecaire, lui, ira CHERCHER : c'est
la brique 2, un autre fichier.)

LES DEUX REPARATIONS DU 11/10/2026, CELLES QUE FRED A DEMANDEES POUR LUMINITA :

  (point 1) LE MARQUE-PAGE EST UNE EMPREINTE DU SOUVENIR LUI-MEME. Chaque fiche porte un
      'repere' : une empreinte calculee sur le TEXTE du souvenir, pas sur sa place dans une
      liste. L'ancien marque-page retenait une POSITION ({"dernier_index": 30}) ; mais la
      liste bouge, donc la « 30e place » ne designait plus la meme chose et la reprise
      s'arretait toute seule a 30 en croyant avoir fini. Avec le repere : une liste qui
      bouge ne deplace plus rien, et un souvenir deja range ne peut plus etre range deux
      fois.

  (point 3) LE MOTEUR DE SCORE EST CORRIGE : etiquette_de() fabrique la phrase COURTE qui
      resume la fiche. C'est elle que le moteur de sens compare a la question, au lieu du
      texte brut — court contre court, le seul regime ou ce modele de sens est bon. Tout le
      travail de l'archiviste (rayon, tiroir, filtre, sous-filtre, resume, objet, personnes,
      lieu) entre enfin dans le calcul, au lieu d'etre jete au moment de chercher.

  (et avec elles) PLUS AUCUN SEUIL EN DUR, ET L'ENTREE NE JETTE PLUS RIEN. Le seuil est lu
      dans reglage_biblio2.json a chaque appel. Une fiche dont l'IA doute RESTE a sa place,
      avec une simple etiquette de doute : elle ne part plus au fourre-tout et elle ne perd
      plus le rayon que l'IA avait propose.

  (et) LES QUATRE NIVEAUX. Chaque fiche porte son 'filtre' (niveau 3) et son 'sous_filtre'
      (niveau 4), en plus du rayon et du tiroir. C'est ce que le plan (biblio2_plan.py)
      assemble en categorie > sous-categorie > filtre > sous-filtre > la fiche.

------------------------------------------------------------------------------
CE QUI A ETE CHANGE EN VENANT CHEZ LUMINITA (regle : elle nait vierge)
------------------------------------------------------------------------------
  - plus une seule mention de Fred ni de Luciana : on parle du PROPRIETAIRE, celui ou
    celle a qui la Luminita appartient ;
  - les chemins viennent de biblio2_reglages.py, et ils designent ~/Luminita.
AUCUNE autre ligne de mecanique n'a ete touchee : le rangement, les reperes, les quatre
niveaux et l'etiquette de sens sont ceux du 11/10, mot pour mot.

NOTE IA : on ecrit TOUT en POSITIF. « Choisis la categorie la plus proche » — jamais
« ne te trompe pas de categorie ». Les negations se perdent, donc on ne s'en sert pas.
"""

import hashlib, json, os, re, threading, time, unicodedata

try:
    import biblio2_reglages as reglages
except Exception:                       # le fichier de reglage n'est pas la : on tient quand meme
    reglages = None

# ---------------------------------------------------------------------
#  LE CONTRAT DE L'IA : ce qu'elle rend pour CHAQUE souvenir, en JSON strict.
#  Si elle sort du contrat, le Python rattrape (sans jamais perdre le souvenir).
#
#    {
#      "categorie":      "<le grand rayon : ex. Sante, Famille, Travail, Fournisseurs...>",
#      "sous_categorie": "<plus fin : ex. Rendez-vous medecin, Maman, Les travaux...>",
#      "filtres": {
#          "date":  "<AAAA-MM-JJ ou une periode, ou vide si inconnue>",
#          "qui":   ["<personnes / societes citees>"],
#          "ou":    "<lieu, ou vide>",
#          "objet": "<la chose concrete : 'voiture rouge', un medicament..., ou vide>",
#          "type":  "<fait | decision | evenement | gout | promesse | achat | medical...>"
#      },
#      "resume":    "<une phrase courte, ce que ce souvenir dit>",
#      "confiance": <0.0 a 1.0 : a quel point l'IA est sure de son rangement>
#    }
# ---------------------------------------------------------------------

SEUIL_CONFIANCE_DEFAUT = 0.55   # ne sert que si le fichier de reglage manque
DEBORDEMENT_TIROIR_DEFAUT = 200
DIVERS = "Divers"               # le fourre-tout, dernier recours (jamais perdu, jamais au pif)
A_TRIER = "A trier"             # le tiroir du fourre-tout quand l'IA n'a propose aucun rayon

# =====================================================================
#  LA MISE DE COTE : CE QUI N'A PAS EXISTE (travail 2 du 13/10/2026).
#
#  LE TROU QU'ON BOUCHE : une conversation ou l'assistante s'est trompee, ou a invente, ou a
#  parti en delire, ENTRAIT DANS LA BIBLIOTHEQUE COMME UN FAIT. Plus jamais. Ces morceaux-la
#  vont dans un rayon a part, ils portent « a trancher par le proprietaire », et c'est LUI
#  qui dit si ca compte.
#
#  ET ILS NE SONT PAS JETES : leur texte reste ENTIER, a leur place, consultable. Mis de
#  cote veut dire « pas range comme un fait » — jamais « efface ».
A_VERIFIER = "A verifier"
A_CONFIRMER = "A confirmer par le proprietaire"


def seuil_confiance():
    """LE SEUIL D'ENTREE, lu dans le fichier de reglage A CHAQUE APPEL.
    IL NE JETTE RIEN : il ne fait que poser l'etiquette « en suspens » sur une fiche dont
    l'IA doute. La fiche reste dans la bibliotheque, a sa place. Ne leve jamais."""
    try:
        return reglages.seuil_confiance()
    except Exception:
        return SEUIL_CONFIANCE_DEFAUT


def debordement_tiroir():
    """Le nombre de fiches au-dela duquel un tiroir est signale trop plein. Lu au reglage."""
    try:
        return int(reglages.lire()["debordement_tiroir"])
    except Exception:
        return DEBORDEMENT_TIROIR_DEFAUT


# =====================================================================
#  POINT 1 — LE REPERE STABLE : l'identite d'un souvenir, pas sa place.
#  C'est LE MARQUE-PAGE EN EMPREINTE DU SOUVENIR LUI-MEME que Fred a demande.
# =====================================================================

def repere_de(source, texte_ou_cle):
    """L'IDENTIFIANT STABLE d'un souvenir : 'source#empreinte'. Deux souvenirs au texte
    identique ont le meme repere (c'est voulu : c'est le meme souvenir). Ne leve jamais.

    'source' dit D'OU il vient ('souvenirs', 'conversation', 'bibliotheque'), pour qu'on
    puisse toujours dire ce qui a ete avale et ce qui reste."""
    base = re.sub(r"\s+", " ", str(texte_ou_cle or "")).strip().lower()
    emp = hashlib.sha1(base.encode("utf-8", "replace")).hexdigest()[:16]
    return "%s#%s" % (str(source or "inconnu").strip() or "inconnu", emp)


def arbre_reperes(arbre):
    """TOUS les reperes deja presents dans l'arbre, en un ensemble. C'est le garde-fou
    « jamais deux fois » : on le calcule UNE FOIS avant un gros rangement, et chaque
    insertion est alors instantanee. Ne leve jamais."""
    vus = set()
    for _cat, _sous, fi in toutes_les_fiches(arbre):
        r = fi.get("repere")
        if r:
            vus.add(r)
    return vus


def toutes_les_fiches(arbre):
    """TOUTES les fiches de l'arbre : [(categorie, sous_categorie, fiche), ...].
    Le seul endroit qui sait comment l'arbre est pose sur le disque. Ne leve jamais."""
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


def _vide(x):
    return x is None or (isinstance(x, str) and not x.strip())


# =====================================================================
#  UN FAIT POSE ET UNE CONVERSATION, CE N'EST PAS LA MEME CHOSE
#  (travail 2 du 13/10/2026).
#
#  LE DEFAUT QU'ON REPARE : tout arrivait par la meme porte, avec le meme mot « souvenir »
#  pose comme une evidence. Un fait que le proprietaire a POSE expres (« ma fille est nee en
#  2009 ») et un BOUT DE CONVERSATION (« ah bon, et sinon il parait que... ») n'ont pourtant
#  ni la meme valeur, ni la meme duree de vie, ni le meme risque : dans une conversation, il
#  y a aussi ce que l'ASSISTANTE a dit -- et elle peut s'etre trompee.
#
#  On dit donc au cerveau D'OU vient le morceau, et on lui demande de le traiter en
#  consequence. C'est le Python qui le sait de facon sure (c'est lui qui lit les sources),
#  donc ce n'est jamais devine.
# =====================================================================

NATURE_FAIT = "fait pose"
NATURE_CONVERSATION = "morceau de conversation"
NATURE_ANCIENNE_FICHE = "ancienne fiche de la bibliotheque"
NATURE_INCONNUE = "origine inconnue"


def _nature_du_souvenir(souvenir):
    """DE QUELLE NATURE est ce qui arrive, d'apres sa SOURCE (ce que le Python sait de facon
    sure). Ne leve jamais."""
    s = str((souvenir or {}).get("source") or "").strip().lower()
    if s.startswith("conversation"):
        return NATURE_CONVERSATION
    if s.startswith("souvenir"):
        return NATURE_FAIT
    if s.startswith("biblio"):
        return NATURE_ANCIENNE_FICHE
    return NATURE_INCONNUE


def _consigne_de_nature(nature, souvenir):
    """CE QU'ON DEMANDE EN PLUS AU CERVEAU, selon la nature du morceau. Tout en POSITIF.
    Ne leve jamais."""
    if nature == NATURE_FAIT:
        return ("CE QUE TU AS SOUS LES YEUX : un FAIT que le proprietaire a POSE EXPRES dans "
                "sa memoire. Traite-le comme une chose qu'il tient pour vraie, et range-le "
                "comme un fait durable.")
    if nature == NATURE_CONVERSATION:
        qui = str((souvenir or {}).get("role") or "").strip().lower()
        de_qui = ("Ce passage a ete dit par L'ASSISTANTE." if qui == "assistant"
                  else "Ce passage a ete dit par LE PROPRIETAIRE." if qui == "user"
                  else "Ce passage vient du fil de la conversation.")
        return ("CE QUE TU AS SOUS LES YEUX : un MORCEAU DE CONVERSATION, pas un fait pose. "
                "%s Dans une conversation il y a de tout : des choses vraies, des hypotheses, "
                "des plaisanteries, des idees abandonnees en cours de route, et parfois des "
                "choses que l'assistante a dites de travers ou inventees. Garde ce qui a "
                "VRAIMENT eu lieu et ce qui tient debout demain ; mets le reste de cote avec "
                "a_existe = false, et dis pourquoi." % de_qui)
    if nature == NATURE_ANCIENNE_FICHE:
        return ("CE QUE TU AS SOUS LES YEUX : une ANCIENNE FICHE, deja rangee autrefois dans "
                "l'ancienne bibliotheque. Son premier titre est en haut du texte : il te dit "
                "comment elle etait classee avant. Tu peux le reprendre ou le corriger, selon "
                "ce que le texte dit vraiment.")
    return ("CE QUE TU AS SOUS LES YEUX : un morceau de memoire dont l'origine n'est pas "
            "connue. Juge-le sur son contenu seul.")


def _normaliser_qui(v):
    """'qui' doit etre une LISTE de noms. L'IA la rend parfois en texte ('elle et moi') :
    si on bouclait dessus on obtenait des lettres isolees. Ici on recolle proprement."""
    if isinstance(v, str):
        parts = re.split(r"\s*(?:,|/|;| et | & )\s*", v)
        return [p.strip() for p in parts if p.strip()]
    if isinstance(v, (list, tuple)):
        noms = [str(x).strip() for x in v if str(x).strip()]
        # garde-fou : si c'est une liste de lettres isolees (vieux bug), on recolle en un mot
        if noms and all(len(n) == 1 for n in noms):
            return ["".join(noms)]
        return noms
    return []


def _nettoyer_chemin(categorie, sous_categorie):
    """Le chemin dans l'arbre = (categorie / sous_categorie). Toujours deux etages,
    jamais vide : si l'IA n'a rien donne de sur, on tombe dans Divers. POSITIF : on garde
    toujours quelque chose de valide."""
    # 17/10/2026 : la liste montree au cerveau porte le nombre de fiches « Nom (12) » ;
    # s'il le recopie dans le nom, on le retire.
    cat = re.sub(r"\s*\(\d+\)\s*$", "", (categorie or "").strip()) or DIVERS
    sous = re.sub(r"\s*\(\d+\)\s*$", "", (sous_categorie or "").strip()) or A_TRIER
    return cat, sous


# =====================================================================
#  17/10/2026 (Fred) : UN NOM, C'EST UN SENS -- PAS DES ACCENTS NI DES MAJUSCULES.
#  Le defaut vu chez Fred : « Developpement d'assistante IA », la meme chose avec accents, et une
#  troisieme avec une autre apostrophe = trois rayons pour une seule chose. Desormais, un nom
#  propose qui ne differe d'un nom existant QUE par les accents, les majuscules, l'apostrophe ou
#  les espaces REPREND le nom existant. Et les doublons deja faits se fusionnent (sans IA).
# =====================================================================

def cle_de_nom(nom):
    """Le nom sans accents, sans majuscules, apostrophes et espaces unifies. Ne leve jamais."""
    try:
        t = unicodedata.normalize("NFKD", str(nom or ""))
        t = "".join(c for c in t if not unicodedata.combining(c))
        t = re.sub("[\u2019\u2018\u02bc`\u00b4]", "'", t).lower()
        return re.sub(r"\s+", " ", t).strip(" .,;:-'\"")
    except Exception:
        return str(nom or "").strip().lower()


def _nom_qui_existe(nom, existants):
    """Le nom deja present qui a la meme cle, sinon le nom propose tel quel."""
    k = cle_de_nom(nom)
    for e in existants or []:
        if cle_de_nom(e) == k:
            return e
    return nom


def _nom_du_proprietaire():
    """Le prenom du proprietaire (Luciana : Fred ; Luminita : le prenom de sa fiche), ou ""."""
    try:
        return str(reglages.nom_du_proprietaire() or "").strip()
    except Exception:
        return ""


def _avec_le_prenom(texte, prenom=None):
    """Remplace « le proprietaire » par son prenom, quand on le connait. Ne leve jamais."""
    prenom = _nom_du_proprietaire() if prenom is None else prenom
    if not prenom or not isinstance(texte, str):
        return texte
    try:
        def _remplace(m):
            avant = {"du": "de ", "au": "\u00e0 ", "le": "", "la": ""}[m.group(1).lower()]
            res = avant + prenom
            return res.upper() if m.group(0).isupper() else res
        return re.sub(r"\b(du|au|le|la)\s+propri[e\u00e9]taire\b", _remplace, texte, flags=re.I)
    except Exception:
        return texte


def nettoyer_la_bibliotheque(arbre):
    """SANS IA, SANS RIEN PERDRE : (1) fusionne les rayons et tiroirs qui ne different que par les
    accents, les majuscules ou l'apostrophe (le nom le plus garni est garde) ; (2) remet le prenom
    du proprietaire a la place de « le proprietaire » dans ce que l'archiviste a ECRIT (resume,
    sens, raisons) -- jamais dans le texte d'origine. Rend {"fusions": n, "prenoms": n}."""
    rapport = {"fusions": 0, "prenoms": 0}
    try:
        def _garni(v):
            return sum(len(l) for l in v.values() if isinstance(l, list)) if isinstance(v, dict) else 0
        touches = set()
        groupes = {}
        for cat, v in list(arbre.items()):
            if isinstance(v, dict):
                groupes.setdefault(cle_de_nom(cat), []).append(cat)
        for noms in groupes.values():
            if len(noms) < 2:
                continue
            garde = max(noms, key=lambda c: (_garni(arbre[c]), c))
            for c in noms:
                if c == garde:
                    continue
                for sous, fiches in arbre[c].items():
                    if isinstance(fiches, list):
                        if not isinstance(arbre[garde].get(sous), list):
                            arbre[garde][sous] = []
                        arbre[garde][sous].extend(fiches)
                        touches.add((garde, sous))
                del arbre[c]
                rapport["fusions"] += 1
        for cat, v in arbre.items():
            if not isinstance(v, dict):
                continue
            g2 = {}
            for sous, fiches in list(v.items()):
                if isinstance(fiches, list):
                    g2.setdefault(cle_de_nom(sous), []).append(sous)
            for noms in g2.values():
                if len(noms) < 2:
                    continue
                garde = max(noms, key=lambda x: (len(v[x]), x))
                for x in noms:
                    if x != garde:
                        v[garde].extend(v[x])
                        del v[x]
                        rapport["fusions"] += 1
                touches.add((cat, garde))
        prenom = _nom_du_proprietaire()
        for cat, sous, fi in toutes_les_fiches(arbre):
            change = (cat, sous) in touches
            if prenom:
                for champ in ("resume", "sens", "pourquoi_en_suspens", "remplace", "pourquoi_pas_sur"):
                    ancien = fi.get(champ)
                    if isinstance(ancien, str) and ancien:
                        nouveau = _avec_le_prenom(ancien, prenom)
                        if nouveau != ancien:
                            fi[champ] = nouveau
                            change = True
                            rapport["prenoms"] += 1
            if change:
                fi["etiquette"] = etiquette_de(cat, sous, fi)
    except Exception:
        pass
    return rapport


# =====================================================================
#  17/10/2026 (Fred) : UNE PANNE PASSAGERE NE DOIT PAS TOUT ARRETER, ET LE MESSAGE DIT VRAI.
#  Un appel trop lent, une coupure d'une seconde, un serveur charge : on attend et on reessaie
#  (REESSAIS_ATTENTES). Une cle refusee (401) ou plus de credit (402) : on s'arrete tout de suite.
# =====================================================================
REESSAIS_ATTENTES = (20, 60, 180)        # secondes d'attente avant chaque nouvel essai


def nature_de_la_panne(texte):
    """D'apres la reponse exacte du serveur : cle_refusee, credit, trop_de_demandes, trop_lent,
    reseau, serveur, ou autre. Ne leve jamais."""
    t = str(texte or "").lower()
    if " 401" in t or "code: 401" in t or "authentication" in t or "invalid api key" in t or "unauthorized" in t:
        return "cle_refusee"
    if " 402" in t or "code: 402" in t or "insufficient balance" in t or "balance" in t:
        return "credit"
    if " 429" in t or "code: 429" in t or "rate limit" in t or "too many" in t:
        return "trop_de_demandes"
    if "timed out" in t or "timeout" in t:
        return "trop_lent"
    if "connection" in t or "connect" in t or "getaddrinfo" in t or "network" in t or "resolve" in t:
        return "reseau"
    if any(x in t for x in (" 500", " 502", " 503", " 504", " 529", "overloaded", "server error")):
        return "serveur"
    return "autre"


_PHRASES_PANNE = {
    "cle_refusee": "le cerveau a REFUSE la cle (erreur 401) : elle est fausse, supprimee ou remplacee chez le fournisseur",
    "credit": "il n'y a plus de credit sur le compte du cerveau (erreur 402)",
    "trop_de_demandes": "le cerveau a recu trop de demandes et a dit d'attendre (erreur 429), meme apres plusieurs essais",
    "trop_lent": "le cerveau n'a pas repondu a temps, meme apres plusieurs essais",
    "reseau": "pas de connexion internet vers le cerveau, meme apres plusieurs essais",
    "serveur": "le serveur du cerveau est en panne ou surcharge, meme apres plusieurs essais",
    "autre": "le cerveau n'a pas pu repondre",
}


def phrase_de_la_panne(texte):
    """La phrase vraie, pour l'ecran, suivie du detail tel quel."""
    return "%s (detail : %s)" % (_PHRASES_PANNE.get(nature_de_la_panne(texte), _PHRASES_PANNE["autre"]),
                                 str(texte or "")[:200])


def juger_avec_reessais(juge, souvenir, arbre, dire=None, attendre=None):
    """Appelle le juge ; sur une panne PASSAGERE, attend et reessaie (REESSAIS_ATTENTES). Rend le
    dernier jugement (qui peut encore porter « _panne » si ca a persiste). Ne leve pas de lui-meme."""
    attendre = attendre or time.sleep
    j = juge(souvenir, arbre)
    for pause in REESSAIS_ATTENTES:
        if not (isinstance(j, dict) and j.get("_panne")):
            return j
        if nature_de_la_panne(j["_panne"]) in ("cle_refusee", "credit"):
            return j
        if dire:
            try:
                dire("(le cerveau n'a pas repondu : %s -- je reessaie dans %d s)" % (str(j["_panne"])[:100], pause))
            except Exception:
                pass
        attendre(pause)
        j = juge(souvenir, arbre)
    return j


def _oui_non(v, defaut=True):
    """Lit un oui/non rendu par le cerveau, sous toutes ses formes (True, "oui", "non",
    "false", 1, 0...). Rend 'defaut' quand il n'a rien dit de clair. Ne leve jamais.

    LE DEFAUT EST « OUI » POUR « ca a existe » : un cerveau muet ne doit pas faire mettre de
    cote un vrai souvenir. La mise de cote se fait sur un NON FRANC, jamais sur un silence."""
    if v is True or v is False:
        return v
    try:
        t = str(v).strip().lower()
    except Exception:
        return defaut
    if not t:
        return defaut
    if t in ("oui", "true", "vrai", "1", "sur", "certain", "reel", "confirme"):
        return True
    if t in ("non", "false", "faux", "0", "pas sur", "invente", "errone", "douteux",
             "pas reel", "delire"):
        return False
    return defaut


def valider_jugement(j):
    """Le Python VERIFIE la reponse du cerveau. Rend (sans_doute, jugement_propre, raison).

    'sans_doute=False' ne veut PAS dire « ce souvenir part au fourre-tout ». Ca veut dire
    « on pose l'etiquette EN SUSPENS dessus ». Le rangement, lui, se fait a l'endroit propose
    par le cerveau. Aucun souvenir ne disparait a l'entree, et aucun ne perd son rayon a
    cause d'un doute.

    LE TRI PAR SENS A L'ENTREE (travail 2 du 13/10/2026). On relit QUATRE reponses de plus,
    et elles comptent autant que le rayon :
      - 'de_quoi_on_parle' : LE SENS, redit SANS reprendre les mots du proprietaire. C'est
        « ce qui reste quand on a change les mots », et c'est ce qui servira a RETROUVER la
        fiche. Une fiche sans cette phrase est marquee en suspens : le cerveau a range sans
        avoir compris, et on le DIT au lieu de faire comme si ;
      - 'a_existe' : est-ce que cette chose a VRAIMENT eu lieu ? Un NON FRANC envoie la
        fiche dans « A verifier / A confirmer par le proprietaire », JAMAIS dans un rayon de
        faits, et elle remonte au proprietaire pour qu'il tranche ;
      - 'tient_demain' : est-ce que ca tient encore demain (un fait durable) ou est-ce que
        c'est un moment qui passe ;
      - 'remplace' : ce que ce souvenir REMPLACE, quand il corrige quelque chose de plus
        ancien. On le garde ecrit : on ne devine pas tout seul quelle vieille fiche effacer.

    Ne leve JAMAIS : une reponse abimee devient un rangement en suspens, pas un plantage."""
    if not isinstance(j, dict):
        return False, None, "la reponse du cerveau n'est pas un objet JSON"
    cat, sous = _nettoyer_chemin(j.get("categorie"), j.get("sous_categorie"))
    filtres = j.get("filtres") if isinstance(j.get("filtres"), dict) else {}
    #  LE SENS, redit autrement. On accepte les deux noms : celui de la demande d'aujourd'hui
    #  ('de_quoi_on_parle') et le nom court ('sens'), pour qu'une vieille reponse passe aussi.
    sens = str(j.get("de_quoi_on_parle") or j.get("sens") or "").strip()
    a_existe = _oui_non(j.get("a_existe"), True)
    tient_demain = _oui_non(j.get("tient_demain"), True)
    propre = {
        "categorie": cat,
        "sous_categorie": sous,
        "filtres": {
            "date":  str(filtres.get("date") or "").strip(),
            "qui":   _normaliser_qui(filtres.get("qui")),
            "ou":    str(filtres.get("ou") or "").strip(),
            "objet": str(filtres.get("objet") or "").strip(),
            "type":  str(filtres.get("type") or "").strip(),
        },
        "resume": str(j.get("resume") or "").strip(),
        "sens": sens,
        "nature": str(j.get("nature") or "").strip(),
        "a_existe": bool(a_existe),
        "tient_demain": bool(tient_demain),
        "remplace": str(j.get("remplace") or "").strip(),
        "pourquoi_pas_sur": str(j.get("pourquoi_pas_sur") or "").strip(),
    }
    try:
        conf = float(j.get("confiance"))
    except Exception:
        conf = 0.0
    propre["confiance"] = conf
    seuil = seuil_confiance()

    #  (1) CE QUI N'A PAS EXISTE PASSE AVANT TOUT LE RESTE. Une conversation fausse, une
    #  erreur ou un delire de l'assistante ne devient JAMAIS un fait, meme si le cerveau
    #  avait propose un beau rayon et une confiance de 0,95. On le met de cote, le texte
    #  entier a sa place, et on le remonte au proprietaire.
    if not a_existe:
        propre["categorie"] = A_VERIFIER
        propre["sous_categorie"] = A_CONFIRMER
        propre["a_trancher_par_le_proprietaire"] = True
        pourquoi = propre["pourquoi_pas_sur"] or "le cerveau ne retrouve pas que ca a eu lieu"
        return False, propre, ("ca n'a peut-etre pas existe (%s) : mis de cote dans "
                               "« %s / %s », le texte entier a sa place, et c'est au "
                               "proprietaire de trancher" % (pourquoi, A_VERIFIER, A_CONFIRMER))

    #  (2) aucun rayon propose : le fourre-tout, et on le DIT.
    if _vide(j.get("categorie")):
        return False, propre, ("le cerveau n'a propose aucun rayon (rangee dans « %s / %s », "
                               "a trancher)" % (DIVERS, A_TRIER))

    #  (3) LE SENS MANQUE : le cerveau a range sans redire de quoi ca parle. La fiche reste
    #  a sa place, et elle est marquee — c'est exactement le defaut qu'on veut voir, au lieu
    #  d'une fiche rangee « au mot » qu'on croira bien rangee.
    if not sens:
        return False, propre, ("le cerveau n'a pas redit de quoi ca parle : la fiche reste "
                               "dans « %s / %s », marquee en suspens (rangee au mot, pas au "
                               "sens)" % (cat, sous))

    #  (4) le doute ordinaire sur le rangement.
    if conf < seuil:
        return False, propre, ("le cerveau hesite (confiance %.2f, repere %.2f) : la fiche "
                               "reste dans « %s / %s », marquee en suspens"
                               % (conf, seuil, cat, sous))
    return True, propre, ""


# =====================================================================
#  LES NIVEAUX 3 ET 4 : le filtre et le sous-filtre.
#
#  La bibliotheque est une marketplace a etages :
#      categorie > sous-categorie > filtre > sous-filtre > la fiche.
#  Les deux premiers niveaux viennent du SENS (l'IA les nomme). Les deux suivants, le
#  PYTHON les deduit des facettes, de facon deterministe -- donc toujours les memes, et
#  jamais inventes deux fois sous deux noms differents.
#
#    niveau 3, LE FILTRE      = la NATURE de la chose (fait, decision, achat, medical...)
#    niveau 4, LE SOUS-FILTRE = la chose PRECISE (l'objet, sinon la personne, sinon le
#                               lieu, sinon l'annee)
# =====================================================================

FILTRE_PAR_DEFAUT = "Fait"
SOUS_FILTRE_PAR_DEFAUT = "General"


def _titre(x, maxi=60):
    """Un nom d'etage propre : court, lisible, toujours le meme pour la meme chose."""
    s = re.sub(r"\s+", " ", str(x or "")).strip(" .,;:-")
    if not s:
        return ""
    s = s[:maxi].strip()
    return s[:1].upper() + s[1:]


def niveaux_3_et_4(filtres):
    """Rend (filtre, sous_filtre) a partir des facettes de la fiche. Deterministe : la
    meme fiche donne toujours les memes deux etages. Ne leve jamais."""
    f = filtres if isinstance(filtres, dict) else {}
    filtre = _titre(f.get("type")) or FILTRE_PAR_DEFAUT
    qui = f.get("qui")
    qui_1 = _titre(qui[0]) if isinstance(qui, (list, tuple)) and qui else ""
    annee = ""
    m = re.search(r"(1[89]\d\d|20\d\d|21\d\d)", str(f.get("date") or ""))
    if m:
        annee = m.group(1)
    sous_filtre = (_titre(f.get("objet")) or qui_1 or _titre(f.get("ou")) or annee
                   or SOUS_FILTRE_PAR_DEFAUT)
    return filtre, sous_filtre


# =====================================================================
#  POINT 3 — L'ETIQUETTE DE SENS : la phrase COURTE qui represente la fiche.
#
#  LE DEFAUT MESURE : sur un vrai message, 30 candidats, meilleure pertinence 0,492 sur 1.
#  La cause n'etait pas le curseur, c'etait CE QU'ON COMPARAIT : on mettait face a la
#  question le TEXTE BRUT du souvenir -- long, bavard, plein d'autre chose. Le modele de
#  sens (paraphrase-multilingual-MiniLM) est fait pour comparer deux textes COURTS entre
#  eux ; un texte long dilue tout et les scores s'ecrasent vers 0,45-0,50.
#
#  L'ETIQUETTE rassemble tout le travail de sens deja fait par l'archiviste -- le rayon,
#  le tiroir, le filtre, le sous-filtre, le resume, l'objet, les personnes, le lieu --
#  en une phrase courte et dense. Jusqu'ici ce travail etait entierement jete au moment
#  de chercher : on ne notait que resume + texte.
# =====================================================================

def etiquette_de(cat, sous, fiche):
    """LA PHRASE COURTE QUI REPRESENTE LA FICHE, pour la comparer a la question.
    C'est LE MEME code pour l'archiviste et pour le bibliothecaire : les deux parlent donc
    exactement de la meme chose (regle « tout le monde au courant de tout »).
    Ne leve jamais ; rend "" si vraiment rien n'est etiquetable."""
    fi = fiche if isinstance(fiche, dict) else {}
    f = fi.get("filtres") if isinstance(fi.get("filtres"), dict) else {}
    filtre = fi.get("filtre") or ""
    sous_filtre = fi.get("sous_filtre") or ""
    if not filtre or not sous_filtre:
        filtre, sous_filtre = niveaux_3_et_4(f)
    qui = f.get("qui") if isinstance(f.get("qui"), (list, tuple)) else []
    bouts = [
        _titre(cat, 80), _titre(sous, 80), _titre(filtre, 80), _titre(sous_filtre, 80),
        #  LE SENS EN TETE DE L'ETIQUETTE (travail 2 du 13/10/2026) : la phrase qui redit de
        #  quoi ca parle SANS reprendre les mots du proprietaire. C'est elle qui fait que la
        #  recherche tombe juste quand le proprietaire redit la meme chose avec d'autres
        #  mots — « le sens, c'est ce qui reste quand on a change les mots ».
        str(fi.get("sens") or "").strip(),
        str(fi.get("resume") or "").strip(),
        _titre(f.get("objet"), 80),
        ", ".join(str(x).strip() for x in qui if str(x).strip())[:80],
        _titre(f.get("ou"), 80),
    ]
    vus, propres = set(), []
    for b in bouts:
        b = re.sub(r"\s+", " ", str(b or "")).strip(" .,;:-")
        cle = b.lower()
        if b and cle not in vus:          # on ne repete pas deux fois la meme chose
            vus.add(cle)
            propres.append(b)
    return " — ".join(propres)[:600]


# ---------------------------------------------------------------------
#  L'ARBRE : tenu par le Python, sur le disque. Un simple JSON, deterministe.
#  arbre[categorie][sous_categorie] = [ {fiche}, ... ]
#  et CHAQUE fiche porte ses niveaux 3 et 4 ('filtre', 'sous_filtre') + son 'repere'.
#
#  POURQUOI L'ARBRE SUR LE DISQUE GARDE DEUX ETAGES : le programme descend l'arbre en deux
#  etages (arbre[cat][sous] = une LISTE de fiches). Si on imbriquait physiquement quatre
#  etages dans arbre.json, le programme se mettrait a lire des noms de filtres a la place de
#  fiches, et il tomberait en panne au premier message. Les quatre niveaux vivent donc DANS
#  la fiche et DANS le plan (biblio2_plan.py). Rien n'est perdu, et rien ne casse.
# ---------------------------------------------------------------------

def arbre_charger(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def arbre_sauver(chemin, arbre):
    """Ecriture SURE : on ecrit a cote, puis on remplace d'un coup. Une coupure de courant
    au mauvais moment ne peut pas laisser un arbre a moitie ecrit."""
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(arbre, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)


def ranger(arbre, souvenir, jugement_ok_propre, reperes_deja=None):
    """LE RANGEMENT DETERMINISTE. 'jugement_ok_propre' = (sans_doute, propre, raison).
    Cree les etages manquants tout seul. Rend un petit rapport clair.

    POSITIF partout, et AUCUN souvenir perdu :
      - l'IA a propose un rayon : la fiche va la, meme si l'IA doutait (elle porte alors
        l'etiquette « en suspens », et elle reste consultable comme les autres) ;
      - l'IA n'a propose aucun rayon : la fiche va dans « Divers / A trier », et elle est
        signalee -- elle attend qu'on tranche, elle n'est pas jetee.

    POINT 1 — JAMAIS DEUX FOIS : si le repere du souvenir est deja dans la bibliotheque,
    on ne range pas une deuxieme fois et on le DIT ('deja_range': True)."""
    sans_doute, propre, raison = jugement_ok_propre
    if propre is None:
        propre = {"categorie": DIVERS, "sous_categorie": A_TRIER,
                  "filtres": {}, "resume": "", "confiance": 0.0}
    cat = propre.get("categorie") or DIVERS
    sous = propre.get("sous_categorie") or A_TRIER
    # 17/10/2026 : meme nom aux accents / majuscules / apostrophe pres -> le nom qui existe deja.
    if cat not in arbre:
        cat = _nom_qui_existe(cat, [c for c, v in (arbre or {}).items() if isinstance(v, dict)])
    if isinstance((arbre or {}).get(cat), dict) and sous not in arbre[cat]:
        sous = _nom_qui_existe(sous, list(arbre[cat].keys()))
    en_suspens = not sans_doute

    texte = str((souvenir or {}).get("texte") or "")
    repere = (souvenir or {}).get("repere") or repere_de((souvenir or {}).get("source") or "inconnu",
                                                          texte or (souvenir or {}).get("id"))

    # --- POINT 1 : le garde-fou « jamais deux fois » -------------------------------
    deja = reperes_deja if reperes_deja is not None else arbre_reperes(arbre)
    if repere in deja:
        return {"range_dans": "", "etages_crees": [], "en_suspens": False,
                "alerte_assistante": "", "nb_dans_le_tiroir": 0,
                "repere": repere, "deja_range": True}

    filtres = propre.get("filtres") or {}
    filtre, sous_filtre = niveaux_3_et_4(filtres)

    fiche = {
        #  LE TEXTE ENTIER, MOT POUR MOT. On ne le resume pas, on ne le coupe pas, on ne le
        #  reecrit pas : on l'etiquette, et c'est tout. (Garde-fou de Fred : ne perdre aucun mot.)
        "texte": texte,
        "filtres": filtres,
        "resume": propre.get("resume") or "",
        "confiance": propre.get("confiance", 0.0),
        "en_suspens": en_suspens,
        "pourquoi_en_suspens": raison if en_suspens else "",
        "source": (souvenir or {}).get("source") or "",
        "repere": repere,                       # point 1 : l'identite stable
        "filtre": filtre,                       # niveau 3
        "sous_filtre": sous_filtre,             # niveau 4
        #  LE TRI PAR SENS A L'ENTREE (travail 2 du 13/10/2026) : ce que le cerveau a
        #  COMPRIS, garde sur la fiche, pour qu'on puisse le relire et le contredire.
        "sens": propre.get("sens") or "",                   # de quoi ca parle, redit autrement
        "nature": propre.get("nature") or _nature_du_souvenir(souvenir),
        "a_existe": bool(propre.get("a_existe", True)),     # est-ce que ca a eu lieu
        "tient_demain": bool(propre.get("tient_demain", True)),
        "remplace": propre.get("remplace") or "",           # ce que ca remplace, s'il y a
        "a_trancher_par_le_proprietaire": bool(propre.get("a_trancher_par_le_proprietaire")),
    }
    fiche["etiquette"] = etiquette_de(cat, sous, fiche)   # point 3 : la phrase de sens

    # Le Python cree l'etage s'il manque : l'arbre GRANDIT tout seul.
    cree = []
    if cat not in arbre or not isinstance(arbre.get(cat), dict):
        arbre[cat] = {}
        cree.append("rayon « %s »" % cat)
    if sous not in arbre[cat] or not isinstance(arbre[cat].get(sous), list):
        arbre[cat][sous] = []
        cree.append("tiroir « %s / %s »" % (cat, sous))
    # niveaux 3 et 4 : on DIT qu'ils apparaissent, pour que le bibliothecaire soit prevenu
    deja_filtres = {(f.get("filtre"), f.get("sous_filtre")) for f in arbre[cat][sous]}
    if (filtre, sous_filtre) not in deja_filtres:
        cree.append("filtre « %s / %s / %s / %s »" % (cat, sous, filtre, sous_filtre))

    arbre[cat][sous].append(fiche)
    deja.add(repere)

    return {
        "range_dans": "%s / %s / %s / %s" % (cat, sous, filtre, sous_filtre),
        "etages_crees": cree,
        "en_suspens": en_suspens,
        "alerte_assistante": raison if en_suspens else "",
        "nb_dans_le_tiroir": len(arbre[cat][sous]),
        "repere": repere,
        "deja_range": False,
        #  travail 2 du 13/10/2026 : on DIT ce qui a ete mis de cote, et ce qui a ete compris.
        "mis_de_cote": bool(fiche["a_trancher_par_le_proprietaire"]),
        "sens": fiche["sens"],
        "remplace": fiche["remplace"],
    }


def tiroirs_qui_debordent(arbre, seuil=None):
    """Le Python SURVEILLE. Rend la liste des tiroirs trop pleins, a proposer a l'IA pour
    DECOUPER (la coupe elle-meme sera faite par le Python). C'est l'auto-organisation.
    Le seuil vient du fichier de reglage."""
    if seuil is None:
        seuil = debordement_tiroir()
    trop_pleins = []
    for cat, sous_cats in (arbre or {}).items():
        if not isinstance(sous_cats, dict):
            continue
        for sous, fiches in sous_cats.items():
            if isinstance(fiches, list) and len(fiches) > seuil:
                trop_pleins.append({"rayon": cat, "tiroir": sous, "nombre": len(fiches)})
    return trop_pleins


def compter(arbre):
    """LES CHIFFRES DE L'ARBRE, pour pouvoir DIRE l'avant / apres. Ne leve jamais."""
    fiches = toutes_les_fiches(arbre)
    tiroirs = {(c, s) for c, s, _f in fiches}
    filtres = {(c, s, f.get("filtre") or "") for c, s, f in fiches}
    sous_filtres = {(c, s, f.get("filtre") or "", f.get("sous_filtre") or "") for c, s, f in fiches}
    return {
        "fiches": len(fiches),
        "rayons": len([c for c, v in (arbre or {}).items() if isinstance(v, dict)]),
        "tiroirs": len(tiroirs),
        "filtres": len(filtres),
        "sous_filtres": len(sous_filtres),
        "en_suspens": len([1 for _c, _s, f in fiches if f.get("en_suspens")]),
        "avec_repere": len([1 for _c, _s, f in fiches if f.get("repere")]),
        #  LES CHIFFRES DU TRI PAR SENS (travail 2 du 13/10/2026).
        "avec_le_sens": len([1 for _c, _s, f in fiches if str(f.get("sens") or "").strip()]),
        "mis_de_cote": len([1 for _c, _s, f in fiches
                            if f.get("a_trancher_par_le_proprietaire")]),
        "qui_ne_tiennent_pas_demain": len([1 for _c, _s, f in fiches
                                           if f.get("tient_demain") is False]),
        "remplacements_annonces": len([1 for _c, _s, f in fiches
                                       if str(f.get("remplace") or "").strip()]),
    }


def a_remonter_au_proprietaire(arbre):
    """CE QUI ATTEND LE PROPRIETAIRE : les morceaux mis de cote parce qu'ils n'ont peut-etre
    pas existe (une conversation fausse, une erreur ou un delire de l'assistante). Rend
    [(categorie, sous_categorie, fiche), ...]. Leur texte est ENTIER, a sa place : il n'y a
    rien a recuperer, il y a seulement a TRANCHER. Ne leve jamais."""
    return [(c, s, f) for c, s, f in toutes_les_fiches(arbre)
            if f.get("a_trancher_par_le_proprietaire")]


def remplacements_annonces(arbre):
    """CE QUE LE CERVEAU A DIT ETRE REMPLACE, sans que rien n'ait ete efface. Rend
    [(categorie, sous_categorie, fiche, ce_que_ca_remplace), ...].

    POURQUOI LE PROGRAMME N'EFFACE RIEN TOUT SEUL : deviner quelle vieille fiche doit sauter,
    c'est deviner. On garde donc les DEUX, on ecrit ce que le cerveau a compris, et c'est le
    proprietaire qui tranche. Ne leve jamais."""
    out = []
    for c, s, f in toutes_les_fiches(arbre):
        r = str(f.get("remplace") or "").strip()
        if r:
            out.append((c, s, f, r))
    return out


# =====================================================================
#  LE VERROU DE LA BIBLIOTHEQUE (17/10/2026, demande de Fred).
#
#  LE RISQUE REPARE : l'archiviste du jour garde la bibliotheque en memoire pendant qu'il range
#  (plusieurs minutes), puis il l'ecrit. Si, pendant ce temps, le re-tri mettait la bibliotheque
#  re-triee en service, l'archiviste la reecrivait par-dessus avec l'ancienne.
#  LA REGLE : UN SEUL A LA FOIS ECRIT DANS LA BIBLIOTHEQUE. Un petit fichier « verrou » a cote
#  d'arbre.json dit qui ecrit. Celui qui le trouve pris attend (le re-tri) ou reessaie plus tard
#  (l'archiviste du jour : rien n'est marque, ses messages restent dans la fenetre).
#  UN VERROU OUBLIE (programme ferme en plein travail) ne bloque pas pour toujours : celui qui le
#  tient le rafraichit a chaque souvenir ; sans nouvelle depuis VERROU_PERIME_SECONDES, il est
#  considere comme abandonne et repris.
# =====================================================================
VERROU_NOM = "bibliotheque_en_ecriture.verrou"
VERROU_PERIME_SECONDES = 30 * 60
_VERROUS_TENUS = {}           # chemin -> [fil qui le tient, nombre de prises]
_VERROUS_GARDE = threading.Lock()


def _verrou_chemin(dossier):
    return os.path.join(str(dossier or "."), VERROU_NOM)


def verrou_qui_le_tient(dossier):
    """Ce qui est ecrit dans le verrou (qui, depuis quand), ou "" s'il est libre. Ne leve jamais."""
    try:
        with open(_verrou_chemin(dossier), encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def verrou_prendre(dossier, qui, attendre_secondes=0, dire=None):
    """Prend le verrou de la bibliotheque. Rend True si on le tient. 'attendre_secondes' = combien
    de temps on attend qu'il se libere (None = autant qu'il faut). Le meme fil peut le reprendre
    (il compte). Ne leve jamais."""
    chemin = _verrou_chemin(dossier)
    moi = threading.get_ident()
    with _VERROUS_GARDE:
        tenu = _VERROUS_TENUS.get(chemin)
        if tenu and tenu[0] == moi:
            tenu[1] += 1
            return True
    debut, deja_dit = time.time(), 0.0
    while True:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
            fd = os.open(chemin, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            try:
                os.write(fd, ("%s, depuis le %s" % (qui, time.strftime("%Y-%m-%d %H:%M:%S"))).encode("utf-8"))
            finally:
                os.close(fd)
            with _VERROUS_GARDE:
                _VERROUS_TENUS[chemin] = [moi, 1]
            return True
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(chemin) > VERROU_PERIME_SECONDES:
                    os.remove(chemin)          # abandonne depuis longtemps : on le reprend
                    continue
            except FileNotFoundError:
                continue
            except Exception:
                pass
        except Exception:
            return False
        if attendre_secondes is not None and time.time() - debut >= attendre_secondes:
            return False
        if dire and time.time() - deja_dit >= 60:
            deja_dit = time.time()
            try:
                dire(verrou_qui_le_tient(dossier))
            except Exception:
                pass
        time.sleep(2)


def verrou_rafraichir(dossier):
    """« Je suis toujours la » : remet l'heure du verrou a maintenant, si on le tient. Ne leve jamais."""
    chemin = _verrou_chemin(dossier)
    try:
        with _VERROUS_GARDE:
            tenu = _VERROUS_TENUS.get(chemin)
        if tenu and tenu[0] == threading.get_ident():
            os.utime(chemin, None)
    except Exception:
        pass


def verrou_rendre(dossier):
    """Rend le verrou (a la derniere prise du meme fil, le fichier est efface). Ne leve jamais."""
    chemin = _verrou_chemin(dossier)
    try:
        with _VERROUS_GARDE:
            tenu = _VERROUS_TENUS.get(chemin)
            if not tenu or tenu[0] != threading.get_ident():
                return
            tenu[1] -= 1
            if tenu[1] > 0:
                return
            del _VERROUS_TENUS[chemin]
        os.remove(chemin)
    except Exception:
        pass


# ---------------------------------------------------------------------
#  L'APPEL A L'IA — borne, en positif, JSON strict.
# ---------------------------------------------------------------------

def construire_demande(souvenir, arbre):
    """LA DEMANDE AU CERVEAU REFLECHI — LE TRI PAR SENS A L'ENTREE.
    (travaux 1, 2 et 5 du 13/10/2026)

    ------------------------------------------------------------------------------
     TRAVAIL 1 — LE PLAFOND DES 4000 CARACTERES EST ENLEVE
    ------------------------------------------------------------------------------
    Jusqu'au 13/10/2026, cette fonction finissait par  [:4000]  : le texte d'une
    conversation etait COUPE NET a 4000 caracteres avant meme d'arriver au cerveau. Le
    cerveau jugeait donc un morceau, et il le jugeait en croyant tenir le tout. C'est de la
    compression, et Fred la refuse : ZERO PLAFOND SUR LES DISCUSSIONS. Le texte part
    maintenant ENTIER, mot pour mot.

    ------------------------------------------------------------------------------
     TRAVAIL 2 — ON NE DEMANDE PLUS « RANGE CE SOUVENIR »
    ------------------------------------------------------------------------------
    L'ancienne demande disait « Range ce souvenir » : elle posait le mot SOUVENIR comme une
    evidence. L'archiviste ne jugeait donc jamais ce qui entrait — il cherchait seulement un
    tiroir. C'etait LE trou. Maintenant on lui demande D'ABORD de COMPRENDRE, et quatre
    reponses comptent autant que le tiroir :

      1  DE QUOI ON PARLAIT VRAIMENT, redit SANS reprendre les mots du proprietaire. C'est la
         definition du sens donnee par Fred : « le sens, c'est ce qui reste quand on a change
         les mots ». Redire avec d'autres mots est la seule preuve qu'on a compris.
      2  EST-CE QUE C'EST REEL. Une conversation fausse, une erreur ou un delire de
         l'assistante ne devient JAMAIS un fait : a_existe = false, et ca part de cote.
      3  EST-CE QUE CA TIENT DEBOUT DEMAIN (un fait durable, ou un moment qui passe).
      4  QU'EST-CE QUE CA REMPLACE (quand ca corrige quelque chose de plus ancien).

    Et on lui dit D'OU vient le morceau, pour qu'il traite DIFFEREMMENT un fait pose et une
    conversation (voir _consigne_de_nature).

    On lui montre aussi les categories ET les sous-categories DEJA la, pour qu'il REUTILISE
    ce qui existe avant d'en creer une neuve -- sinon il invente dix noms pour la meme chose.

    NOTE : tout est en POSITIF, et le mot « mots-cles » n'apparait nulle part -- c'est le
    contraire du travail demande (voir le travail 5 du 13/10/2026)."""
    lignes = []
    for rayon, sous in (arbre or {}).items():
        if rayon in (DIVERS, A_VERIFIER):
            continue   # le fourre-tout et la mise de cote sont RESERVES au programme : on ne
                       # les propose pas au cerveau, pour qu'il n'y range jamais lui-meme.
        noms = (", ".join("%s (%d)" % (s, len(f) if isinstance(f, list) else 0) for s, f in sous.items())
                if isinstance(sous, dict) else "")
        lignes.append("- %s : %s" % (rayon, noms or "(aucune sous-categorie encore)"))
    liste = "\n".join(lignes) or "(la bibliotheque est encore vide)"
    nature = _nature_du_souvenir(souvenir)
    gabarit = (
        "Tu es l'archiviste de la memoire du proprietaire, et tu RANGES PAR LE SENS.\n\n"
        "LE SENS, C'EST CE QUI RESTE QUAND ON A CHANGE LES MOTS. Tu commences donc par "
        "COMPRENDRE de quoi ce morceau de memoire parle vraiment, et tu le REDIS AVEC "
        "D'AUTRES MOTS QUE CEUX QUI SONT ECRITS : c'est la seule preuve que tu as compris. "
        "Le tiroir vient ensuite.\n\n"
        "%s\n\n"
        "LES QUATRE CHOSES QUE TU REGARDES AVANT DE RANGER :\n"
        "  1. DE QUOI ON PARLE VRAIMENT — redis-le en tes propres mots, en une phrase "
        "complete et precise, en nommant les choses meme si elles ne sont pas nommees dans le "
        "texte. Ecris-la dans « de_quoi_on_parle ».\n"
        "  2. EST-CE QUE CA A EU LIEU — « a_existe » vaut true pour ce qui a vraiment eu "
        "lieu, et false pour une hypothese, une plaisanterie, une idee abandonnee, une erreur "
        "ou une invention de l'assistante. Quand tu mets false, dis en une phrase pourquoi "
        "dans « pourquoi_pas_sur ». Le programme met alors ce morceau DE COTE, entier, et il "
        "le remonte au proprietaire pour qu'il tranche : il ne devient jamais un fait.\n"
        "  3. EST-CE QUE CA TIENT DEBOUT DEMAIN — « tient_demain » vaut true pour ce qui "
        "reste vrai dans un an (une date de naissance, un gout, une adresse), et false pour "
        "un moment qui passe (une humeur du jour, un rendez-vous deja passe).\n"
        "  4. QU'EST-CE QUE CA REMPLACE — si ce morceau CORRIGE ou MET A JOUR quelque chose "
        "de plus ancien, ecris dans « remplace » ce qu'il remplace, en une phrase. Sinon "
        "laisse vide. Le programme garde ta phrase et la montre au proprietaire : c'est lui "
        "qui decide ce qui saute.\n\n"
        "LA BIBLIOTHEQUE est une marketplace a etages : categorie -> sous-categorie -> "
        "filtres (date, qui, ou, objet, type).\n"
        "Categories et sous-categories qui existent deja, avec leur nombre de fiches entre "
        "parentheses. REUTILISE la categorie qui convient, en recopiant son nom EXACTEMENT. "
        "La sous-categorie, elle, doit etre PRECISE : le sujet exact de ce morceau (un projet, "
        "une personne, un probleme, un outil, une decision precise), pas un grand theme. "
        "Reutilise une sous-categorie de la liste seulement si elle designe exactement ce "
        "sujet ; sinon cree-en une nouvelle, precise, dans la bonne categorie. Une "
        "sous-categorie qui contient deja beaucoup de fiches est sans doute un theme trop "
        "large : cherche le sujet plus precis.\n%s\n\n"
        "LE MORCEAU DE MEMOIRE, EN ENTIER :\n%s\n\n"
        "Reponds UNIQUEMENT en JSON strict, avec ces champs : de_quoi_on_parle (une phrase, "
        "en tes mots), a_existe (true ou false), pourquoi_pas_sur (une phrase, ou vide), "
        "tient_demain (true ou false), remplace (une phrase, ou vide), nature (ce que c'est, "
        "en deux ou trois mots), categorie, sous_categorie, filtres {date, qui (une LISTE de "
        "noms), ou, objet, type}, resume (une phrase), confiance (0 a 1).\n"
        "Mets une confiance basse quand tu hesites : le programme rangera quand meme le "
        "morceau a l'endroit que tu proposes, en le marquant pour qu'on tranche.")
    # 17/10/2026 : « le proprietaire » devient son prenom (Fred chez Luciana) -- dans la demande
    # seulement : la liste des rayons et le texte du souvenir passent tels quels.
    return (_avec_le_prenom(gabarit)
            % (_avec_le_prenom(_consigne_de_nature(nature, souvenir)), liste,
               str((souvenir or {}).get("texte") or ""))) + _contexte_du_souvenir(souvenir)


def _contexte_du_souvenir(souvenir):
    """V180 (decide avec Fred) : LE CONTEXTE AUTOUR. Un psychologue ne comprend pas « oui, c'est
    ca qui me fait mal » sans la phrase d'avant. Quand le souvenir vient de la conversation, on
    montre a l'archiviste les messages juste avant, EN ENTIER, pour qu'il comprenne de quoi on
    parle. Ils servent a COMPRENDRE et a ranger : ils ne sont PAS recopies dans la fiche (la fiche
    garde le texte du souvenir, mot pour mot, et rien d'autre)."""
    ctx = (souvenir or {}).get("contexte") or []
    if not ctx:
        return ""
    return ("\n\nPOUR COMPRENDRE (les messages juste avant ce souvenir, dans la conversation ; ils "
            "ne sont pas a ranger, seulement a lire) :\n" + "\n\n".join(str(x) for x in ctx))


if __name__ == "__main__":
    # =====================================================================
    #  TEST ICI, SANS AUCUNE IA ET SANS AUCUNE DONNEE PERSONNELLE : une FAUSSE IA
    #  (deterministe) prouve que la mecanique Python tient -- rangement, 4 niveaux,
    #  repere, jamais deux fois, et « rien ne disparait a l'entree ».
    # =====================================================================
    def fausse_ia(souvenir, rayons_existants):
        """Imite le cerveau reflechi juste pour le test (aucun appel reseau, aucune cle).
        Il rend le CONTRAT COMPLET du 13/10/2026 : de_quoi_on_parle, a_existe,
        tient_demain, remplace -- en plus du tiroir."""
        t = (souvenir.get("texte") or "").lower()
        #  CES DEUX CAS-CI PASSENT EN PREMIER, et c'est voulu : le morceau qui CORRIGE la
        #  voiture, et celui qui n'a PAS existe, parlent tous les deux de la voiture. Les
        #  regarder apres le mot « voiture » les aurait rendus invisibles.
        #
        #  CE QUI N'A PAS EXISTE (travail 2) : l'assistante a invente une conversation. Le
        #  cerveau le voit, et ca ne doit JAMAIS devenir un fait.
        if "jamais eu lieu" in t or "je n'ai jamais dit" in t:
            return {"de_quoi_on_parle": "Un echange que l'assistante a fabrique de toutes "
                                        "pieces et attribue au proprietaire.",
                    "a_existe": False,
                    "pourquoi_pas_sur": "le proprietaire dit lui-meme que cet echange n'a pas "
                                        "eu lieu",
                    "tient_demain": False, "remplace": "", "nature": "erreur de l'assistante",
                    "categorie": "Famille", "sous_categorie": "Vacances",
                    "filtres": {"type": "evenement"}, "resume": "Un ete en Italie.",
                    "confiance": 0.95}
        #  CE QUI REMPLACE QUELQUE CHOSE (travail 2, 4e question).
        if "ce n'est plus" in t or "maintenant c'est" in t:
            return {"de_quoi_on_parle": "Le changement du moyen de deplacement habituel du "
                                        "proprietaire.",
                    "a_existe": True, "tient_demain": True,
                    "remplace": "l'ancienne fiche qui disait que la voiture rouge etait "
                                "toujours la",
                    "nature": "mise a jour",
                    "categorie": "Vehicules", "sous_categorie": "Voitures",
                    "filtres": {"date": "2026", "objet": "velo", "type": "decision"},
                    "resume": "Le velo remplace la voiture.", "confiance": 0.9}
        if "voiture" in t or "auto" in t:
            return {"de_quoi_on_parle": "L'acquisition d'un vehicule personnel de teinte "
                                        "ecarlate au milieu des annees 2010.",
                    "a_existe": True, "tient_demain": True, "remplace": "",
                    "nature": "fait pose",
                    "categorie": "Vehicules", "sous_categorie": "Voitures",
                    "filtres": {"date": "2015", "qui": [], "ou": "", "objet": "voiture rouge",
                                "type": "achat"}, "resume": "Achat d'une voiture rouge.",
                    "confiance": 0.9}
        if "medecin" in t or "docteur" in t:
            return {"de_quoi_on_parle": "Une consultation programmee avec un praticien, dans "
                                        "une grande ville de la vallee du Rhone.",
                    "a_existe": True, "tient_demain": False, "remplace": "",
                    "nature": "fait pose",
                    "categorie": "Sante", "sous_categorie": "Rendez-vous",
                    "filtres": {"date": "2024-03-02", "qui": ["Dr Martin"], "ou": "Lyon",
                                "objet": "", "type": "medical"}, "resume": "RDV chez le medecin.",
                    "confiance": 0.8}
        # le cerveau a un rayon en tete mais il hesite : la fiche doit RESTER dans ce rayon,
        # marquee en suspens -- elle ne doit PAS partir au fourre-tout.
        if "peut-etre" in t:
            return {"de_quoi_on_parle": "Un sejour d'enfance chez une aieule, a une date que "
                                        "le proprietaire ne retrouve pas.",
                    "a_existe": True, "tient_demain": True,
                    "categorie": "Famille", "sous_categorie": "Souvenirs",
                    "filtres": {"type": "evenement"}, "resume": "Un souvenir de famille.",
                    "confiance": 0.20}
        # le cerveau ne propose aucun rayon : la fiche va dans Divers / A trier, et on le DIT
        return {"categorie": "", "sous_categorie": "", "filtres": {}, "resume": "",
                "confiance": 0.2}

    souvenirs = [
        {"texte": "J'ai achete une voiture rouge, une Clio, en 2015.", "source": "souvenirs"},
        {"texte": "Rendez-vous chez le docteur Martin a Lyon le 2 mars.", "source": "souvenirs"},
        {"texte": "Peut-etre un ete chez ma grand-mere, je ne sais plus l'annee.",
         "source": "souvenirs"},
        {"texte": "Heu, machin truc, je sais plus trop ce que c'etait.", "source": "conversation"},
        {"texte": "Tu m'as dit qu'on avait passe l'ete en Italie : je n'ai jamais dit ca, "
                  "cette conversation n'a jamais eu lieu.", "source": "conversation"},
        {"texte": "La voiture rouge, ce n'est plus ca : maintenant c'est le velo tous les jours.",
         "source": "souvenirs"},
    ]
    for s in souvenirs:
        s["repere"] = repere_de(s["source"], s["texte"])

    arbre, rate = {}, []
    print("=== RANGEMENT (fausse IA, aucune donnee personnelle) ===")
    print(" (seuil d'entree lu au reglage : %.2f -- il marque, il ne jette pas)" % seuil_confiance())
    for s in souvenirs:
        rap = ranger(arbre, s, valider_jugement(fausse_ia(s, arbre)))
        print("  %-55s -> %s%s" % (s["texte"][:53], rap["range_dans"],
                                   "   [EN SUSPENS : %s]" % rap["alerte_assistante"]
                                   if rap["en_suspens"] else ""))

    print("\n=== LES CHIFFRES DE L'ARBRE ===")
    print(compter(arbre))

    print("\n=== CONTROLES ===")

    def controle(nom, condition):
        print(("  OK   %s" if condition else "  RATE %s") % nom)
        if not condition:
            rate.append(nom)

    controle("le rayon Vehicules existe", "Vehicules" in arbre and "Voitures" in arbre["Vehicules"])
    controle("le rayon Sante existe", "Sante" in arbre)
    controle("la fiche dont l'IA doute RESTE dans Famille / Souvenirs (elle ne part pas au fourre-tout)",
             "Famille" in arbre and "Souvenirs" in arbre.get("Famille", {})
             and len(arbre["Famille"]["Souvenirs"]) == 1)
    controle("cette fiche porte bien l'etiquette « en suspens »",
             arbre.get("Famille", {}).get("Souvenirs", [{}])[0].get("en_suspens") is True)
    controle("aucun souvenir ne disparait a l'entree (6 entres, 6 ranges)",
             compter(arbre)["fiches"] == len(souvenirs))
    controle("la fiche sans aucun rayon va dans Divers / A trier",
             A_TRIER in arbre.get(DIVERS, {}))
    controle("les niveaux 3 et 4 sont poses",
             arbre["Vehicules"]["Voitures"][0]["filtre"] == "Achat"
             and arbre["Vehicules"]["Voitures"][0]["sous_filtre"] == "Voiture rouge")
    controle("point 3 : l'etiquette de sens est courte et porte le rayon + le resume",
             "Vehicules" in arbre["Vehicules"]["Voitures"][0]["etiquette"]
             and "voiture rouge" in arbre["Vehicules"]["Voitures"][0]["etiquette"].lower()
             and len(arbre["Vehicules"]["Voitures"][0]["etiquette"]) < 400)
    controle("les facettes sont bien gardees",
             arbre["Vehicules"]["Voitures"][0]["filtres"]["objet"] == "voiture rouge")

    # =====================================================================
    #  TRAVAIL 1 (13/10/2026) — ZERO PLAFOND SUR LES DISCUSSIONS
    # =====================================================================
    print("\n=== TRAVAIL 1 : LE PLAFOND DES 4000 CARACTERES ===")
    _longue = {"texte": "Ceci est une tres longue conversation. " * 500,   # ~19 500 caracteres
               "source": "conversation"}
    _demande_longue = construire_demande(_longue, arbre)
    controle("le texte entier arrive au cerveau : la discussion de %d caracteres n'est PAS "
             "coupee" % len(_longue["texte"]),
             _longue["texte"].strip() in _demande_longue)
    controle("plus aucune coupe a 4000 caracteres (la demande est plus longue que 4000)",
             len(_demande_longue) > 4000 + 4000)
    controle("la derniere phrase de la discussion arrive bien, elle aussi",
             _demande_longue.count("Ceci est une tres longue conversation.") == 500)

    # =====================================================================
    #  TRAVAIL 2 (13/10/2026) — LE TRI PAR SENS A L'ENTREE
    # =====================================================================
    print("\n=== TRAVAIL 2 : LE TRI PAR SENS A L'ENTREE ===")
    _d = construire_demande(souvenirs[0], arbre)
    controle("la demande pose LA DEFINITION DU SENS (ce qui reste quand on a change les mots)",
             "CHANGE LES MOTS" in _d.upper())
    controle("la demande demande DE QUOI ON PARLE VRAIMENT, redit autrement",
             "de_quoi_on_parle" in _d and "tes propres mots" in _d)
    controle("la demande demande SI CA A EU LIEU", "a_existe" in _d)
    controle("la demande demande SI CA TIENT DEBOUT DEMAIN", "tient_demain" in _d)
    controle("la demande demande CE QUE CA REMPLACE", "remplace" in _d)
    controle("la demande ne pose PLUS « range ce souvenir » comme une evidence",
             "Range ce souvenir" not in _d)

    _d_fait = construire_demande({"texte": "x", "source": "souvenirs"}, arbre)
    _d_conv = construire_demande({"texte": "x", "source": "conversation"}, arbre)
    controle("un FAIT POSE et une CONVERSATION recoivent deux demandes DIFFERENTES",
             _d_fait != _d_conv)
    controle("le fait pose est annonce comme un fait pose", "a POSE EXPRES" in _d_fait)
    controle("la conversation est annoncee comme une conversation, avec son risque",
             "MORCEAU DE CONVERSATION" in _d_conv and "inventees" in _d_conv)

    _fiche_fausse = arbre.get(A_VERIFIER, {}).get(A_CONFIRMER, [{}])[0]
    controle("CE QUI N'A PAS EXISTE est mis de cote dans « %s / %s »" % (A_VERIFIER, A_CONFIRMER),
             A_VERIFIER in arbre and A_CONFIRMER in arbre.get(A_VERIFIER, {}))
    controle("ce qui n'a pas existe n'est JAMAIS range comme un fait (pas dans Famille)",
             not any("Italie" in str(f.get("texte") or "")
                     for f in arbre.get("Famille", {}).get("Vacances", []))
             and "Vacances" not in arbre.get("Famille", {}))
    controle("ce qui n'a pas existe est remonte au proprietaire pour qu'il tranche",
             _fiche_fausse.get("a_trancher_par_le_proprietaire") is True
             and _fiche_fausse.get("en_suspens") is True)
    controle("et son texte reste ENTIER, mot pour mot (rien n'est perdu, rien n'est reecrit)",
             _fiche_fausse.get("texte") == souvenirs[4]["texte"])
    controle("une confiance de 0,95 ne sauve pas ce qui n'a pas existe",
             _fiche_fausse.get("confiance") == 0.95
             and _fiche_fausse.get("a_existe") is False)
    controle("le programme DIT combien de morceaux attendent le proprietaire",
             compter(arbre)["mis_de_cote"] == 1 and len(a_remonter_au_proprietaire(arbre)) == 1)

    _v = arbre["Vehicules"]["Voitures"][0]
    controle("LE SENS est garde sur la fiche, redit sans les mots du proprietaire",
             "ecarlate" in _v.get("sens", "") and "Clio" not in _v.get("sens", ""))
    controle("LE SENS entre dans l'etiquette : c'est lui qui fera retrouver la fiche",
             "ecarlate" in _v.get("etiquette", ""))
    controle("une fiche rangee SANS que le cerveau ait redit le sens est marquee en suspens",
             valider_jugement({"categorie": "Sante", "sous_categorie": "x",
                               "confiance": 0.99})[0] is False)
    controle("« ca tient debout demain » est garde (le rendez-vous passe ne tient pas)",
             arbre["Sante"]["Rendez-vous"][0].get("tient_demain") is False
             and _v.get("tient_demain") is True)
    controle("CE QUE CA REMPLACE est garde ecrit, et rien n'est efface tout seul",
             compter(arbre)["remplacements_annonces"] == 1
             and len(remplacements_annonces(arbre)) == 1
             and compter(arbre)["fiches"] == len(souvenirs))
    controle("un cerveau muet sur « a_existe » ne fait PAS mettre un vrai souvenir de cote "
             "(le silence ne met rien de cote, seul un NON FRANC le fait)",
             valider_jugement({"categorie": "Sante", "sous_categorie": "x",
                               "de_quoi_on_parle": "un rendez-vous", "confiance": 0.9})[0] is True)

    # =====================================================================
    #  TRAVAIL 5 (13/10/2026) — LE MOT CONTRADICTOIRE
    # =====================================================================
    print("\n=== TRAVAIL 5 : LE MOT CONTRADICTOIRE ===")
    controle("la demande de l'archiviste ne parle PAS de mots-cles",
             "mot-cle" not in _d.lower() and "mots-cles" not in _d.lower()
             and "mot cle" not in _d.lower())

    # POINT 1 : le repere est stable, et un souvenir deja range ne repart pas une 2e fois
    r1 = repere_de("souvenirs", "J'ai  achete une VOITURE rouge. ")
    r2 = repere_de("souvenirs", "j'ai achete une voiture rouge.")
    controle("point 1 : le meme souvenir donne le meme repere (espaces et majuscules sans effet)",
             r1 == r2)
    controle("point 1 : la source fait partie du repere",
             repere_de("souvenirs", "x") != repere_de("conversation", "x"))
    avant = compter(arbre)["fiches"]
    rap2 = ranger(arbre, souvenirs[0], valider_jugement(fausse_ia(souvenirs[0], arbre)))
    controle("point 1 : un souvenir deja range n'est JAMAIS range deux fois",
             rap2.get("deja_range") is True and compter(arbre)["fiches"] == avant)
    print("\nTiroirs qui debordent (seuil %d) : %s"
          % (debordement_tiroir(), tiroirs_qui_debordent(arbre) or "aucun"))
    print("\n%s" % ("TOUT EST PASSE." if not rate else
                    "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
