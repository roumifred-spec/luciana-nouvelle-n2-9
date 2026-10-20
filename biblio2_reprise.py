# -*- coding: utf-8 -*-
"""
BRIQUE 3 — LA REPRISE DE L'EXISTANT : L'ARCHIVISTE AVALE TOUT LE PASSE.

LECTURE SEULE, SANS AUCUNE EXCEPTION. Ce fichier OUVRE la memoire vivante de Fred et
n'y ECRIT JAMAIS. Il n'ecrit que dans ~/Luciana/bibliotheque2, un dossier a nous.
La liste des fichiers qu'il ouvre est courte et elle est en haut de biblio2_reglages.py.


=====================================================================================
 CHANTIER DU 11/10/2026 — POINT 1 : LE MARQUE-PAGE QUI DEBLOQUE L'ARCHIVISTE
=====================================================================================

 LE DEFAUT (constate par Fred) : avancee.json contenait {"dernier_index": 30}. C'est une
 POSITION dans une liste, pas un souvenir. Et la liste BOUGE : la lecture saute les
 messages automatiques du programme (ceux qui commencent par « [ ») et les textes trop
 courts. Du coup la « 30e place » ne designait plus le meme souvenir d'un lancement a
 l'autre, et la reprise s'arretait toute seule a 30 -- en croyant avoir fini.

 LA REPARATION, EN TROIS MORCEAUX :

   1) LE REPERE, PAS LA PLACE. Le marque-page retient maintenant LA LISTE DES REPERES
      des souvenirs vraiment traites (voir arch.repere_de : une empreinte du texte).
      Une liste qui bouge ne deplace plus rien, et un souvenir deja range ne peut plus
      etre range deux fois.

   2) SON FICHIER A LUI : bibliotheque2/marque_page.json. L'ancien avancee.json n'est
      plus lu comme une position (il est garde sur le disque, on n'y touche pas).

   3) LA REPRISE SE RESOUDRE TOUTE SEULE. Au lancement, on ne croit pas aveuglement le
      marque-page : on lit AUSSI les reperes deja presents dans l'arbre, et on prend
      l'union des deux. Meme si le marque-page est perdu, abime ou vieux, l'archiviste
      sait exactement ce qui est deja range -- et il reprend au bon endroit.

 ET IL AVALE TOUT LE PASSE, LES TROIS SOURCES :
      souvenirs.json          les souvenirs de Fred (une liste de textes)
      luciana_memoire.json    le fil des conversations
      bibliotheque/           l'ancienne bibliotheque : l'index + les fiches .md

 LANCER (sur le PC de Fred) :
     python biblio2_reprise.py             # avale tout le passe, par paquets
     python biblio2_reprise.py 50          # ne fait que les 50 suivants (essai rapide)
     python biblio2_reprise.py --chiffres  # DIT l'etat, sans rien ecrire du tout
     python biblio2_reprise.py --demo      # essai sans DeepSeek et sans la memoire de Fred

NOTE IA : tout est ecrit en POSITIF (regle de Fred).
"""

import json, os, re, sys, time

import biblio2_archiviste as arch
import biblio2_plan as plan_biblio

try:
    import biblio2_reglages as reglages
except Exception:
    reglages = None

# --- les chemins viennent du tableau de bord commun (point 2) --------------------
if reglages is not None:
    DOSSIER = reglages.DOSSIER
    FICHIER_SOUVENIRS = reglages.FICHIER_SOUVENIRS
    FICHIER_CONVERSATION = reglages.FICHIER_CONVERSATION
    DOSSIER_ANCIENNE_BIBLIO = reglages.DOSSIER_ANCIENNE_BIBLIO
    FICHIER_ANCIEN_INDEX = reglages.FICHIER_ANCIEN_INDEX
    FICHIER_CLE_DEEPSEEK = reglages.FICHIER_CLE_DEEPSEEK
    DOSSIER_BIBLIO2 = reglages.DOSSIER_BIBLIO2
    FICHIER_ARBRE = reglages.FICHIER_ARBRE
    FICHIER_MARQUE_PAGE = reglages.FICHIER_MARQUE_PAGE
    FICHIER_PLAN = reglages.FICHIER_PLAN
    FICHIER_SIGNAL = reglages.FICHIER_SIGNAL
else:                                    # repli : le programme tient meme sans le reglage
    DOSSIER = os.path.join(os.path.expanduser("~"), "Luciana")
    FICHIER_SOUVENIRS = os.path.join(DOSSIER, "souvenirs.json")
    FICHIER_CONVERSATION = os.path.join(DOSSIER, "luciana_memoire.json")
    DOSSIER_ANCIENNE_BIBLIO = os.path.join(DOSSIER, "bibliotheque")
    FICHIER_ANCIEN_INDEX = os.path.join(DOSSIER_ANCIENNE_BIBLIO, "index.json")
    FICHIER_CLE_DEEPSEEK = os.path.join(DOSSIER, "cle_deepseek.txt")
    DOSSIER_BIBLIO2 = os.path.join(DOSSIER, "bibliotheque2")
    FICHIER_ARBRE = os.path.join(DOSSIER_BIBLIO2, "arbre.json")
    FICHIER_MARQUE_PAGE = os.path.join(DOSSIER_BIBLIO2, "marque_page.json")
    FICHIER_PLAN = os.path.join(DOSSIER_BIBLIO2, "plan.json")
    FICHIER_SIGNAL = os.path.join(DOSSIER_BIBLIO2, "signal_plan.json")

DEEPSEEK_BASE_URL = "https://api.deepseek.com/anthropic"
TEXTE_TROP_COURT = 15        # en dessous, ce n'est pas un souvenir, c'est un bout de phrase
CONTEXTE_MESSAGES = 2        # V180 : combien de messages d'avant l'archiviste lit pour comprendre


def _modele():
    try:
        return reglages.lire()["modele_ia"]
    except Exception:
        return "deepseek-flash"


def _paquet():
    try:
        return int(reglages.lire()["paquet_sauvegarde"])
    except Exception:
        return 25


def _sources_voulues():
    try:
        return reglages.lire()["reprise"]
    except Exception:
        return {"souvenirs_json": True, "conversation": True, "ancienne_bibliotheque": True}


# ---------------------------------------------------------------------
#  L'IA DEEPSEEK (REFLECHI) — seulement le SENS. Bornee, JSON robuste.
#  Ne plante jamais : au moindre souci -> confiance 0 -> la fiche est marquee en suspens
#  (et elle est quand meme RANGEE : l'entree ne jette rien).
# ---------------------------------------------------------------------

_client = {"obj": None}


def _lire_cle():
    try:
        return open(FICHIER_CLE_DEEPSEEK, encoding="utf-8-sig").read().strip()
    except Exception:
        return ""


def _client_deepseek():
    # 17/10/2026 : la cle est RELUE a chaque appel. Si elle a change pendant un long rangement,
    # la nouvelle est prise tout de suite (avant : l'ancienne restait, et c'etait le 401).
    cle = _lire_cle()
    if _client["obj"] is None or _client.get("cle") != cle:
        import anthropic   # importe seulement sur le PC de Fred (pas besoin en --demo)
        _client["obj"] = anthropic.Anthropic(api_key=cle, base_url=DEEPSEEK_BASE_URL)
        _client["cle"] = cle
    return _client["obj"]


def _extraire_json(texte):
    """Rend le premier objet JSON trouve dans le texte, ou None. Robuste."""
    if not texte:
        return None
    m = re.search(r"\{.*\}", texte, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def juger_deepseek(souvenir, arbre):
    """Un appel borne a DeepSeek pour le SENS d'un souvenir. Ne leve jamais.
    'arbre' = la bibliotheque deja construite, pour que l'IA REUTILISE les sous-categories."""
    try:
        cli = _client_deepseek()
        demande = arch.construire_demande(souvenir, arbre)
        rep = cli.messages.create(
            model=_modele(),
            # DeepSeek REFLECHI (choix de Fred) : on n'envoie RIEN sur la reflexion, il
            # reflechit par defaut. max_tokens assez grand pour reflechir + rendre le JSON,
            # mais SOUS le mur du SDK (~21000) pour eviter "Streaming is required".
            max_tokens=12000,
            system=[{"type": "text",
                     # V189 : la consigne de l'archiviste de Luminita (13/10), le rangement PAR LE SENS.
                     "text": "Tu ranges la memoire de quelqu'un, et tu la ranges PAR LE "
                             "SENS. Le sens, c'est ce qui reste quand on a change les mots. "
                             "Commence donc par comprendre de quoi ce morceau parle vraiment "
                             "et s'il a vraiment eu lieu. Reflechis, puis reponds en JSON "
                             "strict."}],
            messages=[{"role": "user", "content": demande}],
            timeout=120,                          # DeepSeek reflechi : on lui laisse le temps
        )
        brut = "".join(b.text for b in (rep.content or []) if getattr(b, "type", "") == "text")
        j = _extraire_json(brut)
        return j if isinstance(j, dict) else {"categorie": "", "confiance": 0.0}
    except Exception as ex:
        # un appel rate ne casse pas la chaine : cette fiche part en suspens, et elle est rangee
        return {"categorie": "", "confiance": 0.0, "_panne": str(ex)[:120]}


# =====================================================================
#  LES TROIS SOURCES DU PASSE — toutes en LECTURE SEULE.
# =====================================================================

# V189 : le meme juge, sous le nom qu'utilise l'outil de re-tri (biblio2_retri_par_sens.py).
juger_par_l_ia = juger_deepseek


def _depuis_souvenirs_json():
    """LES SOUVENIRS DE FRED (souvenirs.json). C'est une LISTE DE TEXTES : luciana.py les
    ajoute avec souvenirs.append(texte) et les dedoublonne sur le texte exact. Le repere
    par empreinte du texte est donc exactement la meme notion d'identite que la sienne.
    (Un vieux fichier pouvait contenir des objets : on sait les lire aussi.) Ne leve jamais."""
    out = []
    try:
        d = json.load(open(FICHIER_SOUVENIRS, encoding="utf-8-sig"))
    except Exception as ex:
        return out, "souvenirs.json : %s" % str(ex)[:120]
    for s in (d if isinstance(d, list) else []):
        texte = (s if isinstance(s, str) else str((s or {}).get("texte")
                 or (s or {}).get("fait") or (s or {}).get("content") or "")).strip()
        if len(texte) < TEXTE_TROP_COURT:
            continue
        out.append({"texte": texte, "source": "souvenirs", "date": "",
                    "repere": arch.repere_de("souvenirs", texte)})
    return out, ""


def _depuis_conversation():
    """LE FIL DES CONVERSATIONS (luciana_memoire.json). On saute les messages automatiques
    du programme (ils commencent par « [ ») et les bouts trop courts. ATTENTION, c'est tout
    le probleme d'avant : cette liste BOUGE. Elle n'est plus reperee par sa place, mais par
    l'empreinte du texte. Ne leve jamais."""
    out = []
    try:
        hist = json.load(open(FICHIER_CONVERSATION, encoding="utf-8-sig"))
    except Exception as ex:
        return out, "luciana_memoire.json : %s" % str(ex)[:120]
    precedents = []          # V180 : les messages juste avant, pour que l'archiviste comprenne
    for m in (hist if isinstance(hist, list) else []):
        texte = str((m or {}).get("content") or "").strip()
        qui = "Fred" if (m or {}).get("role") == "user" else "Luciana"
        if len(texte) < TEXTE_TROP_COURT or texte.startswith("["):
            if texte and not texte.startswith("["):
                precedents = (precedents + ["%s : %s" % (qui, texte)])[-CONTEXTE_MESSAGES:]
            continue
        out.append({"texte": texte, "source": "conversation",
                    "date": str((m or {}).get("date") or "")[:10],
                    "role": (m or {}).get("role") or "",
                    "contexte": list(precedents),
                    "repere": arch.repere_de("conversation", texte)})
        precedents = (precedents + ["%s : %s" % (qui, texte)])[-CONTEXTE_MESSAGES:]
    return out, ""


def _depuis_ancienne_bibliotheque():
    """L'ANCIENNE BIBLIOTHEQUE (bibliotheque/index.json + les fiches .md). On suit l'INDEX,
    donc on ne ramasse ni le journal ni le dossier anciennes_versions : seulement les fiches
    vivantes, une fois chacune.

    Le repere d'une fiche est son CHEMIN dans l'ancienne bibliotheque (rayon/dossier/fiche),
    pas son texte : une fiche dont Fred corrige une ligne reste LA MEME fiche, et elle ne
    sera pas rangee une deuxieme fois. Ne leve jamais.

    Format de l'index (celui qu'ecrit luciana.py) :
      {"rayons": {slug: {"nom","resume","dossiers": {slug: {"nom","resume",
                  "fiches": {slug: {"titre","resume"}}}}}}}"""
    out = []
    try:
        idx = json.load(open(FICHIER_ANCIEN_INDEX, encoding="utf-8-sig"))
    except Exception as ex:
        return out, "bibliotheque/index.json : %s" % str(ex)[:120]
    rayons = (idx or {}).get("rayons") if isinstance(idx, dict) else None
    if not isinstance(rayons, dict):
        return out, "bibliotheque/index.json : pas de rayons lisibles"
    for r_slug, R in rayons.items():
        if not isinstance(R, dict):
            continue
        r_nom = str(R.get("nom") or r_slug)
        for d_slug, D in (R.get("dossiers") or {}).items():
            if not isinstance(D, dict):
                continue
            d_nom = str(D.get("nom") or d_slug)
            for f_slug, F in (D.get("fiches") or {}).items():
                if not isinstance(F, dict):
                    continue
                f_nom = str(F.get("titre") or f_slug)
                chemin = os.path.join(DOSSIER_ANCIENNE_BIBLIO, str(r_slug), str(d_slug),
                                      str(f_slug) + ".md")
                corps = ""
                try:
                    with open(chemin, encoding="utf-8", errors="replace") as fh:
                        corps = fh.read()
                except Exception:
                    corps = ""
                resume = str(F.get("resume") or "")
                texte = ("%s > %s > %s\n%s\n%s"
                         % (r_nom, d_nom, f_nom, resume, corps)).strip()
                if len(texte) < TEXTE_TROP_COURT:
                    continue
                cle = "%s/%s/%s" % (r_slug, d_slug, f_slug)
                out.append({"texte": texte, "source": "bibliotheque", "date": "",
                            "repere": arch.repere_de("bibliotheque", cle),
                            "ancien_chemin": "%s > %s > %s" % (r_nom, d_nom, f_nom)})
    return out, ""


# =====================================================================
#  18/10/2026 (Fred) : TOUT CE QUI ENTRE VA A L'ARCHIVISTE, DANS LA BIBLIOTHEQUE EN SERVICE.
#  Ce qui sort de la vie du programme (une chose en cours finie, une mission close) n'est plus
#  ecrit dans la bibliotheque 1 (debranchee) : il est confie a l'archiviste. S'il ne peut pas le
#  ranger tout de suite (internet coupe, bibliotheque occupee), le morceau attend ici, dans une
#  simple LISTE D'ATTENTE (pas une bibliotheque : rien n'y est jamais lu par le bibliothecaire),
#  et l'archiviste la reprend a son passage suivant. Une fois range, il sort de la liste.
# =====================================================================
FICHIER_A_RANGER = os.path.join(DOSSIER_BIBLIO2, "a_ranger.jsonl")


def mettre_en_attente(texte, source, date=""):
    """Ajoute un morceau a ranger. Rend son repere. Ne leve jamais."""
    texte = str(texte or "").strip()
    if not texte:
        return ""
    r = arch.repere_de(source, texte)
    try:
        os.makedirs(os.path.dirname(FICHIER_A_RANGER), exist_ok=True)
        with open(FICHIER_A_RANGER, "a", encoding="utf-8") as f:
            f.write(json.dumps({"texte": texte, "source": source, "date": str(date or "")[:10],
                                "repere": r, "quand": time.strftime("%Y-%m-%d %H:%M:%S")},
                               ensure_ascii=False) + "\n")
    except Exception:
        return ""
    return r


def _depuis_la_liste_d_attente():
    """Les morceaux qui attendent d'etre ranges (lecture seule). Rend (souvenirs, souci)."""
    out, vus = [], set()
    try:
        with open(FICHIER_A_RANGER, encoding="utf-8") as f:
            for ligne in f:
                try:
                    d = json.loads(ligne)
                except Exception:
                    continue
                if isinstance(d, dict) and d.get("texte") and d.get("repere") and d["repere"] not in vus:
                    vus.add(d["repere"])
                    out.append({"texte": d["texte"], "source": d.get("source") or "souvenirs",
                                "date": d.get("date") or "", "repere": d["repere"]})
    except FileNotFoundError:
        return [], ""
    except Exception as ex:
        return out, "liste d'attente : %s" % str(ex)[:120]
    return out, ""


def sortir_de_l_attente_ce_qui_est_range():
    """Retire de la liste d'attente ce qui est maintenant dans la bibliotheque en service."""
    try:
        attente, _s = _depuis_la_liste_d_attente()
        if not attente:
            return 0
        ranges = arch.arbre_reperes(arch.arbre_charger(FICHIER_ARBRE))
        reste = [a for a in attente if a["repere"] not in ranges]
        tmp = FICHIER_A_RANGER + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for a in reste:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")
        os.replace(tmp, FICHIER_A_RANGER)
        return len(attente) - len(reste)
    except Exception:
        return 0


def tout_le_passe():
    """LES TROIS SOURCES MISES BOUT A BOUT, chacune en lecture seule. Rend
    (souvenirs, soucis) : 'soucis' DIT franchement ce qui n'a pas pu etre lu, au lieu de
    faire semblant que tout va bien. Ne leve jamais.

    Les doublons de repere a l'interieur d'un meme lot sont ecartes tout de suite : le
    meme texte present deux fois dans souvenirs.json ne donne qu'une fiche."""
    voulues = _sources_voulues()
    tout, soucis, vus = [], [], set()
    lots = []
    if voulues.get("souvenirs_json", True):
        lots.append(("souvenirs.json", _depuis_souvenirs_json))
    if voulues.get("conversation", True):
        lots.append(("luciana_memoire.json", _depuis_conversation))
    if voulues.get("ancienne_bibliotheque", True):
        lots.append(("l'ancienne bibliotheque", _depuis_ancienne_bibliotheque))
    lots.append(("la liste d'attente de l'archiviste", _depuis_la_liste_d_attente))   # 18/10/2026
    for nom, lire_lot in lots:
        lot, souci = lire_lot()
        if souci:
            soucis.append(souci)
        n_avant = len(tout)
        for s in lot:
            if s["repere"] in vus:
                continue
            vus.add(s["repere"])
            tout.append(s)
        print("  lu : %-24s %5d souvenir(s) utilisable(s)" % (nom, len(tout) - n_avant))
    return tout, soucis


# =====================================================================
#  POINT 1 — LE MARQUE-PAGE : les REPERES traites, dans son fichier a lui.
# =====================================================================

def marque_page_charger(chemin=None, arbre=None):
    """CE QUI EST DEJA RANGE. On prend L'UNION de deux choses :
      - les reperes ecrits dans marque_page.json ;
      - les reperes REELLEMENT presents dans l'arbre.
    C'est ce qui rend la reprise increvable : meme si le marque-page est perdu ou vieux,
    l'arbre dit la verite, et l'archiviste reprend au bon endroit. Ne leve jamais."""
    chemin = chemin or FICHIER_MARQUE_PAGE
    faits = set()
    try:
        d = json.load(open(chemin, encoding="utf-8-sig"))
        for _source, liste in ((d or {}).get("faits") or {}).items():
            for r in (liste or []):
                if r:
                    faits.add(str(r))
    except Exception:
        pass
    dans_l_arbre = set()
    if arbre is not None:
        try:
            dans_l_arbre = arch.arbre_reperes(arbre)
        except Exception:
            dans_l_arbre = set()
    return faits | dans_l_arbre, {"dans_le_marque_page": len(faits),
                                  "dans_l_arbre": len(dans_l_arbre)}


def marque_page_sauver(faits, chemin=None, chiffres=None):
    """ECRIT LE MARQUE-PAGE. Il REMPLACE le precedent (point 6 : pas d'empilement), et il
    est ecrit a cote puis bascule d'un coup : une coupure ne peut pas le laisser a moitie.
    Les reperes sont ranges par source, pour que Fred puisse LIRE ce qui a ete avale."""
    chemin = chemin or FICHIER_MARQUE_PAGE
    par_source = {}
    for r in sorted(faits or []):
        source = str(r).split("#", 1)[0] or "inconnu"
        par_source.setdefault(source, []).append(str(r))
    contenu = {
        "_a_quoi_ca_sert": ("LE MARQUE-PAGE DE L'ARCHIVISTE. Il retient LE REPERE de chaque "
                            "souvenir vraiment traite -- une empreinte du souvenir lui-meme, "
                            "pas sa place dans une liste. C'est ce qui permet de reprendre le "
                            "travail sans jamais ranger deux fois le meme souvenir, meme quand "
                            "la liste des messages bouge. Il REMPLACE l'ancien avancee.json, "
                            "qui ne retenait qu'une position (et bloquait la reprise a 30)."),
        "version": 2,
        "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
        "combien": len(faits or []),
        "combien_par_source": {k: len(v) for k, v in sorted(par_source.items())},
        "faits": {k: v for k, v in sorted(par_source.items())},
    }
    if chiffres:
        contenu["chiffres"] = chiffres
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(contenu, f, ensure_ascii=False, indent=1)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)
    return chemin


# =====================================================================
#  LA REPRISE ELLE-MEME.
# =====================================================================

def dire_les_chiffres(titre="ETAT"):
    """DIT l'etat, sans RIEN ecrire. C'est ce qui donne les chiffres avant / apres."""
    arbre = arch.arbre_charger(FICHIER_ARBRE)
    c = arch.compter(arbre)
    plan = plan_biblio.charger(FICHIER_PLAN)
    faits, d_ou = marque_page_charger(arbre=arbre)
    print("=== %s ===" % titre)
    print("  arbre            : %d fiche(s), %d rayon(s), %d tiroir(s), %d filtre(s), "
          "%d sous-filtre(s)" % (c["fiches"], c["rayons"], c["tiroirs"], c["filtres"],
                                 c["sous_filtres"]))
    print("  en suspens       : %d (un doute a trancher ; elles sont rangees, pas jetees)"
          % c["en_suspens"])
    print("  plan             : version %s, empreinte %s, %d rayon(s)"
          % (plan.get("version", 0), plan.get("empreinte", "(aucune)"),
             len(plan.get("rayons") or {})))
    print("  marque-page      : %d repere(s) connu(s)  (%d dans le fichier, %d dans l'arbre)"
          % (len(faits), d_ou["dans_le_marque_page"], d_ou["dans_l_arbre"]))
    ancien = os.path.join(DOSSIER_BIBLIO2, "avancee.json")
    if os.path.exists(ancien):
        try:
            v = json.load(open(ancien, encoding="utf-8-sig"))
            print("  avancee.json     : %s  (l'ancien marque-page par POSITION ; il n'est plus "
                  "lu, et il n'est pas touche)" % json.dumps(v, ensure_ascii=False))
        except Exception:
            print("  avancee.json     : present, illisible (il n'est plus lu de toute facon)")
    else:
        print("  avancee.json     : absent")
    return {"arbre": c, "plan": plan.get("chiffres") or {}, "reperes_connus": len(faits)}


def reprendre(juge, limite=None, sources=None):
    """17/10/2026 (Fred) : LE VERROU DE LA BIBLIOTHEQUE. Un seul a la fois ecrit dedans : si le
    re-tri est en train de mettre la bibliotheque re-triee en service, l'archiviste ne range RIEN
    et le dit (RuntimeError) ; il reessaiera. Le travail lui-meme est _reprendre_sous_verrou."""
    if not arch.verrou_prendre(DOSSIER_BIBLIO2, "l'archiviste (reprise)", attendre_secondes=0):
        raise RuntimeError("la bibliotheque est occupee (%s) : rien n'est range, on reessaiera"
                           % (arch.verrou_qui_le_tient(DOSSIER_BIBLIO2) or "verrou pris"))
    try:
        def juge_qui_tient_le_verrou(s, a):
            arch.verrou_rafraichir(DOSSIER_BIBLIO2)      # « je suis toujours la »
            return juge(s, a)
        return _reprendre_sous_verrou(juge, limite=limite, sources=sources,
                                      _juge_rafraichi=juge_qui_tient_le_verrou)
    finally:
        arch.verrou_rendre(DOSSIER_BIBLIO2)


def _reprendre_sous_verrou(juge, limite=None, sources=None, _juge_rafraichi=None):
    """L'ARCHIVISTE AVALE LE PASSE. 'juge(souvenir, arbre)' = l'IA (DeepSeek sur le PC de
    Fred, une fausse en --demo). Reprend exactement la ou il s'etait arrete, grace aux
    REPERES -- jamais grace a une position. Ne range jamais deux fois le meme souvenir."""
    os.makedirs(DOSSIER_BIBLIO2, exist_ok=True)
    arbre = arch.arbre_charger(FICHIER_ARBRE)
    plan_avant = plan_biblio.charger(FICHIER_PLAN)
    c_avant = arch.compter(arbre)

    print("=== AVANT ===")
    print("  arbre : %d fiche(s), %d rayon(s), %d tiroir(s) | plan version %s"
          % (c_avant["fiches"], c_avant["rayons"], c_avant["tiroirs"],
             plan_avant.get("version", 0)))

    faits, d_ou = marque_page_charger(arbre=arbre)
    print("  deja traite : %d repere(s) (%d lus dans le marque-page, %d retrouves dans l'arbre)"
          % (len(faits), d_ou["dans_le_marque_page"], d_ou["dans_l_arbre"]))

    print("\n=== LECTURE DU PASSE (lecture seule) ===")
    passe, soucis = (sources() if callable(sources) else tout_le_passe())
    a_faire = [s for s in passe if s["repere"] not in faits]
    if limite:
        a_faire = a_faire[:int(limite)]

    print("\n  souvenirs trouves en tout : %d" % len(passe))
    print("  deja ranges (on les saute) : %d" % (len(passe) - len([s for s in passe
                                                                   if s["repere"] not in faits])))
    print("  A RANGER MAINTENANT        : %d" % len(a_faire))
    for souci in soucis:
        print("  (source illisible, et je le dis : %s)" % souci)
    if not a_faire:
        print("\nTout le passe est deja range : il n'y a rien a refaire.")
        plan_apres, signal = plan_biblio.rafraichir(arbre, FICHIER_PLAN, FICHIER_SIGNAL)
        marque_page_sauver(faits, chiffres=arch.compter(arbre))
        return arbre

    paquet = _paquet()
    n_range = n_suspens = n_doublon = 0
    print("")
    for k, s in enumerate(a_faire, 1):
        j = arch.juger_avec_reessais(_juge_rafraichi or juge, s, arbre, dire=print)
        if isinstance(j, dict) and j.get("_panne"):
            # 17/10/2026 : CERVEAU INJOIGNABLE (internet, cle, serveur). Ce souvenir n'est PAS
            # range au fourre-tout et PAS marque comme fait : on sauve ce qui est fait et on
            # s'arrete. La prochaine fois, il reprend exactement ici.
            arch.arbre_sauver(FICHIER_ARBRE, arbre)
            marque_page_sauver(faits, chiffres=arch.compter(arbre))
            raise RuntimeError("%s. %d souvenir(s) range(s) avant l'arret, %d attendent : rien n'est "
                               "perdu, relancez pour reprendre" % (arch.phrase_de_la_panne(j["_panne"]),
                                                                    n_range, len(a_faire) - k + 1))
        ok, propre, raison = arch.valider_jugement(j)
        # LE PYTHON MET LA DATE (il la connait, c'est fiable), l'IA ne s'en occupe pas.
        if propre is not None and s.get("date"):
            propre.setdefault("filtres", {})["date"] = str(s["date"])[:10]
        rap = arch.ranger(arbre, s, (ok, propre, raison), reperes_deja=faits)
        if rap.get("deja_range"):
            n_doublon += 1
        else:
            n_range += 1
            if rap["en_suspens"]:
                n_suspens += 1
        if k % paquet == 0 or k == len(a_faire):
            arch.arbre_sauver(FICHIER_ARBRE, arbre)
            marque_page_sauver(faits, chiffres=arch.compter(arbre))
            print("  ... %d/%d ranges (%d en suspens)        " % (k, len(a_faire), n_suspens),
                  end="\r")

    # 17/10/2026 : les doublons d'accents fusionnes, le prenom remis (sans IA, rien de perdu).
    arch.nettoyer_la_bibliotheque(arbre)
    arch.arbre_sauver(FICHIER_ARBRE, arbre)
    # POINTS 4, 5 et 6 : on refabrique le plan, il REMPLACE l'ancien, et on PREVIENT le
    # bibliothecaire de tout ce qui vient d'etre cree.
    plan_apres, signal = plan_biblio.rafraichir(arbre, FICHIER_PLAN, FICHIER_SIGNAL)
    marque_page_sauver(faits, chiffres=arch.compter(arbre))

    c_apres = arch.compter(arbre)
    print("\n\n=== APRES ===")
    print("  ranges maintenant : %d   (dont %d en suspens : un doute a trancher, mais RANGES)"
          % (n_range, n_suspens))
    if n_doublon:
        print("  doublons evites   : %d (deja dans la bibliotheque)" % n_doublon)
    print("  arbre : %d fiche(s)  (avant : %d)" % (c_apres["fiches"], c_avant["fiches"]))
    print("  rayons : %d  (avant : %d)" % (c_apres["rayons"], c_avant["rayons"]))
    print("  tiroirs : %d  (avant : %d)" % (c_apres["tiroirs"], c_avant["tiroirs"]))
    print("  filtres : %d | sous-filtres : %d" % (c_apres["filtres"], c_apres["sous_filtres"]))
    print("  plan : version %s -> %s" % (plan_avant.get("version", 0),
                                         plan_apres.get("version", 0)))
    print("  remontee au bibliothecaire : %s" % signal.get("pour_le_bibliothecaire", ""))
    print("  marque-page : %d repere(s) -> %s" % (len(faits), FICHIER_MARQUE_PAGE))
    print("  arbre ecrit dans : %s" % FICHIER_ARBRE)
    print("  rayons : %s" % ", ".join(sorted(arbre.keys())))
    trop = arch.tiroirs_qui_debordent(arbre)
    if trop:
        print("  tiroirs trop pleins, a decouper : %s" % trop)
    return arbre


if __name__ == "__main__":
    if "--chiffres" in sys.argv:
        dire_les_chiffres("ETAT DE LA MEMOIRE 2 (rien n'est ecrit)")
        if reglages is not None:
            print("\n" + reglages.dire_les_reglages())
        raise SystemExit(0)

    if "--demo" in sys.argv:
        # ESSAI ICI, sans DeepSeek et SANS toucher a la memoire de Fred : on remplace les
        # trois sources par une fausse memoire, et on ecrit dans un dossier a cote.
        import tempfile
        DOSSIER_BIBLIO2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "_demo_bibliotheque2")
        FICHIER_ARBRE = os.path.join(DOSSIER_BIBLIO2, "arbre.json")
        FICHIER_MARQUE_PAGE = os.path.join(DOSSIER_BIBLIO2, "marque_page.json")
        FICHIER_PLAN = os.path.join(DOSSIER_BIBLIO2, "plan.json")
        FICHIER_SIGNAL = os.path.join(DOSSIER_BIBLIO2, "signal_plan.json")

        def faux_passe():
            textes = [
                ("souvenirs", "J'ai achete une voiture rouge, une Clio, en 2016."),
                ("souvenirs", "Ma fille est nee en 2009, un mardi matin."),
                ("conversation", "Rendez-vous chez le docteur Martin a Lyon le 2 mars."),
                ("conversation", "Je n'aime pas du tout le gout de la coriandre."),
                ("bibliotheque", "Informatique > Memoire > curseur : le curseur de sortie est "
                                 "regle a 0,35 dans curseur.txt."),
            ]
            return ([{"texte": t, "source": src, "date": "",
                      "repere": arch.repere_de(src, t)} for src, t in textes], [])

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
            if "docteur" in t:
                return {"categorie": "Sante", "sous_categorie": "Rendez-vous",
                        "filtres": {"ou": "Lyon", "qui": ["Dr Martin"], "type": "medical"},
                        "resume": "RDV chez le Dr Martin a Lyon.", "confiance": 0.8}
            if "coriandre" in t:
                return {"categorie": "Gouts", "sous_categorie": "Cuisine",
                        "filtres": {"objet": "coriandre", "type": "gout"},
                        "resume": "Fred n'aime pas la coriandre.", "confiance": 0.4}
            if "curseur" in t:
                return {"categorie": "Informatique", "sous_categorie": "Memoire de Luciana",
                        "filtres": {"objet": "curseur de sortie", "type": "reglage"},
                        "resume": "Le curseur de sortie est a 0,35.", "confiance": 0.9}
            return {"categorie": "", "confiance": 0.2}

        rate = []

        def controle(nom, condition):
            if condition:
                print("  OK   %s" % nom)
            else:
                print("  RATE %s" % nom)
                rate.append(nom)

        print("### PREMIER PASSAGE : la bibliotheque est vide ###\n")
        arbre = reprendre(faux_juge, sources=faux_passe)
        c1 = arch.compter(arbre)

        print("\n\n### DEUXIEME PASSAGE : on relance sur le MEME passe ###")
        print("### (c'est LE test du point 1 : rien ne doit etre range une deuxieme fois) ###\n")
        arbre2 = reprendre(faux_juge, sources=faux_passe)
        c2 = arch.compter(arbre2)

        print("\n=== CONTROLES ===")
        controle("point 1 : les 5 souvenirs du passe sont ranges", c1["fiches"] == 5)
        controle("point 1 : chaque fiche porte un repere stable", c1["avec_repere"] == 5)
        controle("point 1 : relancer ne range RIEN deux fois (5 avant, 5 apres)",
                 c2["fiches"] == c1["fiches"] == 5)
        controle("point 1 : le marque-page est ecrit, et il retient des REPERES",
                 os.path.exists(FICHIER_MARQUE_PAGE)
                 and json.load(open(FICHIER_MARQUE_PAGE, encoding="utf-8"))["combien"] == 5)
        controle("point 1 : le marque-page ne retient PLUS une position",
                 "dernier_index" not in open(FICHIER_MARQUE_PAGE, encoding="utf-8").read())
        controle("point 1 : les trois sources sont bien distinguees",
                 set(json.load(open(FICHIER_MARQUE_PAGE, encoding="utf-8"))["combien_par_source"])
                 == {"souvenirs", "conversation", "bibliotheque"})
        controle("point 2 : la fiche dont l'IA doute (coriandre, 0.40) est RANGEE dans Gouts",
                 "Gouts" in arbre and "Cuisine" in arbre["Gouts"]
                 and arbre["Gouts"]["Cuisine"][0]["en_suspens"] is True)
        controle("point 2 : aucun souvenir ne disparait a l'entree", c1["fiches"] == 5)
        controle("point 4 : le plan a bien les quatre niveaux",
                 plan_biblio.charger(FICHIER_PLAN)["chiffres"]["sous_filtres"] >= 5)
        controle("point 5 : le signal au bibliothecaire est ecrit et date",
                 len(plan_biblio.lire_signal(FICHIER_SIGNAL).get("quand") or "") >= 10)
        controle("point 6 : au 2e passage, le plan n'a PAS change -> il ne remonte pas a Luciana",
                 plan_biblio.lire_signal(FICHIER_SIGNAL)["le_plan_a_change"] is False)

        print("\n=== LE PLAN OBTENU ===")
        print(plan_biblio.texte_pour_le_bibliothecaire(plan_biblio.charger(FICHIER_PLAN)))
        print("\n%s" % ("TOUT EST PASSE." if not rate else
                        "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
        raise SystemExit(0)

    limite = None
    for a in sys.argv[1:]:
        if a.isdigit():
            limite = int(a)
    try:
        reprendre(juger_deepseek, limite=limite)
    except RuntimeError as ex:
        print("\n\n  ARRET : %s" % ex)
