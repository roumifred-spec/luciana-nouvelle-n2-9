# -*- coding: utf-8 -*-
"""LE COEUR DE LA NOUVELLE LUCIANA (les coulisses), reconstruit de zero le 19/10/2026.

L'ecran, la voix, le personnage, les boutons et les outils (ses mains, ses yeux) restent ceux de la
V198 : ils viennent de l'ancien programme, sans changement. Ici, il n'y a QUE ce qui etait bancal :
le trajet d'un message, la memoire, l'apprentissage, le choix des outils.

LES REGLES DECIDEES LE 19/10/2026, et ce fichier n'en trahit aucune :
 - UNE seule bibliotheque pour tout (souvenirs, regles, faits, personnes, savoir-faire, savoir-vivre).
 - RIEN N'EST JAMAIS COUPE : une fiche est donnee EN ENTIER ou pas du tout. La seule limite est le
   NOMBRE de fiches donnees d'un coup ; les autres sont nommees, et elle peut les ouvrir en entier.
 - Pas de noyau : tout arrive seulement quand ca sert, choisi PAR LE SENS (une phrase entiere, dans
   sa conversation), comme un psychologue, jamais mot par mot.
 - Le bibliothecaire lit LE MEME BLOC qu'elle (la conversation du jour, 50 000 a 80 000 car.) + le
   nouveau message. Elle repond d'abord de sa tete ; s'il apporte quelque chose, sa reponse de tete
   est jetee et elle repond avec les fiches EN ENTIER (mecanique V183).
 - Elle apprend TOUTE SEULE apres chaque echange (sans clic).
 - L'archiviste range au-dela de 80 000 caracteres, MOT POUR MOT, par le sens.
 - Le programme tient l'heure, les rappels, les listes.
 - Le panneau d'etat montre TOUTES les coulisses, en quantites.
"""
import os, json, time, re, threading, hashlib, base64, array, math, unicodedata, urllib.request
import plan     # le catalogue de la bibliotheque (piece 1 de la bibliotheque rangee, 20/10/2026)
import classement  # l'archiviste qui range et divise (piece 2)
import quotidien   # le journal du quotidien : le vital a l'heure exacte (piece 3)
import comprendre  # comprendre la situation avant de chercher (piece 4)
import personnes   # le registre des personnes (etape b) : qui parle, de qui on parle

L = None          # l'ancien programme (luciana.py), pose par brancher()

# LES CROCHETS : ce qui change d'une assistante a l'autre (Luciana, Luminita). Par defaut, rien ne
# change : c'est exactement la nouvelle Luciana. Le lanceur de Luminita y branche sa personnalite,
# ses prenoms (perso), sa langue, son mode enfant (outils permis, minuteur).
CROCHETS = {"perso": None, "personnalite": None, "contexte": None, "outils_permis": None,
            "avant_tour": None, "apres_tour": None}


def perso(texte):
    """Le crochet de l'assistante (ses prenoms a elle), PUIS le jeton {proprietaire}.
    Tout ce qui part au cerveau ou a l'ecran passe par ici : aucun prenom n'est ecrit dans le code."""
    f = CROCHETS.get("perso")
    try:
        t = f(texte) if (f and isinstance(texte, str)) else texte
    except Exception:
        t = texte
    return avec_le_nom(t) if isinstance(t, str) else t


def brancher(module, dossier=None):
    """Branche l'ancien programme. Sa memoire neuve = <son dossier>_neuve (~/Luciana_neuve, ~/Luminita_neuve)."""
    global L
    L = module
    poser_le_dossier(dossier or (str(getattr(module, "DOSSIER", "") or os.path.join(HOME, "Luciana")) + "_neuve"))


ICI = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")


def poser_le_dossier(d):
    global DOSSIER, F_CONVERSATION, F_RANGEMENT, F_FICHES, F_SENS, F_RAPPELS, F_COMPTEURS, F_TRACE, F_LISIBLE, D_JOURNAL
    DOSSIER = d
    os.makedirs(DOSSIER, exist_ok=True)
    F_CONVERSATION = os.path.join(DOSSIER, "conversation.jsonl")
    F_RANGEMENT = os.path.join(DOSSIER, "rangement.json")
    F_FICHES = os.path.join(DOSSIER, "bibliotheque.jsonl")
    F_SENS = os.path.join(DOSSIER, "sens_google.json")
    F_RAPPELS = os.path.join(DOSSIER, "rappels.json")
    F_COMPTEURS = os.path.join(DOSSIER, "compteurs.json")
    F_TRACE = os.path.join(DOSSIER, "trace_des_messages.jsonl")
    F_LISIBLE = os.path.join(DOSSIER, "MA BIBLIOTHEQUE (lisible).txt")
    D_JOURNAL = os.path.join(DOSSIER, "journal")
    _FICHES["liste"] = None
    plan.poser_le_dossier(DOSSIER)
    personnes.poser_le_dossier(DOSSIER)
    try:
        classement.oublier_la_session()
    except NameError:
        pass
    try:
        MOTEUR.cache = None
    except NameError:
        pass


_FICHES = {"liste": None, "mtime": None}
poser_le_dossier(os.path.join(HOME, "Luciana_neuve"))

_verrou_tour = threading.Lock()
_verrou_fichiers = threading.RLock()
_verrou_biblio = threading.RLock()


# =====================================================================================
#  FICHIERS
# =====================================================================================
def lire_json(chemin, defaut):
    try:
        with open(chemin, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return defaut


def ecrire_json(chemin, valeur):
    with _verrou_fichiers:
        tmp = chemin + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(valeur, f, ensure_ascii=False, indent=1)
        os.replace(tmp, chemin)


def ajouter_ligne(chemin, d):
    with _verrou_fichiers:
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")


def lire_lignes(chemin):
    out = []
    try:
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    try:
                        out.append(json.loads(ligne))
                    except Exception:
                        pass
    except Exception:
        pass
    return out


def sans_accents(t):
    return "".join(c for c in unicodedata.normalize("NFD", str(t or "").lower()) if unicodedata.category(c) != "Mn")


def maintenant():
    return time.strftime("%Y-%m-%d %H:%M")


def aujourdhui():
    return time.strftime("%Y-%m-%d")


# =====================================================================================
#  REGLAGES (nouvelle/reglages.json, relus a chaque message)
# =====================================================================================
DEFAUT = {"fenetre_max_caracteres": 80000, "fenetre_apres_rangement": 50000,
          "bibliothecaire_lit_combien": 30, "fiches_donnees_max": 10,
          "cerveau_bibliothecaire": "deepseek-flash", "reflexion_bibliothecaire": True,
          "cerveau_archiviste": "deepseek-flash", "apprentissage": True,
          "outils_proposes": 5, "outils_actifs_max": 10, "passage_caracteres": 1200,
          "bibliothecaire_plafond_secondes": 180, "relecture_des_regles": True,
          "diviser_a_partir_de": 40, "bibliotheque_rangee": False,
          "proprietaire": ""}


F_REGLAGES = os.path.join(ICI, "reglages.json")


def reglages():
    r = dict(DEFAUT)
    d = lire_json(F_REGLAGES, {})
    if isinstance(d, dict):
        for k in DEFAUT:
            if k in d:
                # Une valeur VIDE dans le fichier ne remplace pas celle du programme : « vide » veut dire
                # « pas renseigne », jamais « efface ». C'est ce qui protege le nom du proprietaire.
                if k == "proprietaire" and not str(d[k] or "").strip():
                    continue
                r[k] = d[k]
    return r


# ------------------------------------------------------------------------------ LE NOM DU PROPRIETAIRE
# C'est un produit a VENDRE : aucun prenom n'est ecrit dans le code. Le nom de celui a qui est cette
# assistante vit a UN SEUL endroit, reglages.json, cle « proprietaire », ecrit a l'installation et relu a
# chaque message. Partout ailleurs on ecrit le JETON « {proprietaire} », remplace au moment de parler.
JETON = "{proprietaire}"
NOM_PAR_DEFAUT = "le proprietaire"      # tant que personne n'a ete nomme : un mot neutre, jamais un prenom


_NOM = {"nom": None, "cle": None}       # relu des que reglages.json change (fichier, date, valeur du programme)


def proprietaire():
    """LE NOM DU PROPRIETAIRE, LU DANS LE REGLAGE (reglages.json, cle « proprietaire »).
    Reglage absent ou vide -> un mot neutre (« le proprietaire »), JAMAIS un prenom en dur.
    Cette fonction LIT seulement : elle n'ecrit jamais, donc un nom en place n'est jamais ecrase.
    Elle est appelee des milliers de fois (une fois par fiche) : le nom est garde en memoire et
    RELU des que reglages.json change (meme fonctionnement que la relecture des fiches)."""
    try:
        m = os.path.getmtime(F_REGLAGES)
    except Exception:
        m = None
    cle = (F_REGLAGES, m, DEFAUT.get("proprietaire"))
    if _NOM["nom"] is None or cle != _NOM["cle"]:
        try:
            nom = str(reglages().get("proprietaire") or "").strip()
        except Exception:
            nom = ""
        _NOM.update(nom=nom or NOM_PAR_DEFAUT, cle=cle)
    return _NOM["nom"]


def avec_le_nom(texte):
    """Remplace le jeton {proprietaire} par le nom du reglage. Un texte sans jeton n'est pas touche."""
    t = str(texte or "")
    return t.replace(JETON, proprietaire()) if JETON in t else t


def poser_le_proprietaire(nom):
    """A L'INSTALLATION SEULEMENT : ecrit le nom dans reglages.json s'il n'y est pas encore.
    UNE MISE A JOUR NE L'ECRASE JAMAIS : si un nom est deja ecrit, on le garde et on ne touche a rien.
    Rend (ecrit_ou_non, le nom en place)."""
    with _verrou_fichiers:
        d = lire_json(F_REGLAGES, {})
        if not isinstance(d, dict):
            return False, ""
        deja = str(d.get("proprietaire") or "").strip()
        if deja:
            return False, deja                      # deja nomme : on ne touche a rien
        nom = " ".join(str(nom or "").split())[:120]
        if not nom:
            return False, ""
        d["proprietaire"] = nom
        ecrire_json(F_REGLAGES, d)
        _NOM["nom"] = None                          # a relire : le nom vient de changer
        return True, nom


# =====================================================================================
#  LES COMPTEURS DES COULISSES (pour le panneau d'etat, remis a zero chaque jour)
# =====================================================================================
COULISSES = {"dernier": {}}


def compter(cle, n=1):
    with _verrou_fichiers:
        d = lire_json(F_COMPTEURS, {})
        if d.get("jour") != aujourdhui():
            d = {"jour": aujourdhui()}
        d[cle] = d.get(cle, 0) + n
        ecrire_json(F_COMPTEURS, d)


def compteurs_du_jour():
    d = lire_json(F_COMPTEURS, {})
    return d if d.get("jour") == aujourdhui() else {"jour": aujourdhui()}


# =====================================================================================
#  APPELS AUX CERVEAUX (par l'ancien programme : memes cles, meme menu, meme compte des depenses)
# =====================================================================================
def appel_simple(cerveau, systeme, contenu, quoi, reflechir=False, max_tokens=8000, timeout=180):
    """Un appel court, sans outils (bibliothecaire, archiviste). Rend (texte, panne)."""
    try:
        cli = L.client_de(cerveau)
        if cli is None:
            return "", "pas de cle pour %s" % cerveau
        try:
            cli = cli.with_options(max_retries=1, timeout=timeout)
        except Exception:
            pass
        requete = dict(model=L.modele_api(cerveau), system=[{"type": "text", "text": perso(systeme)}],
                       messages=[{"role": "user", "content": perso(contenu)}])
        requete.update(L._options_reflexion(cerveau) if reflechir else L._options_rangement_sans_reflexion(cerveau))
        rep = L._appel_cerveau(cli, cerveau, requete, max_tokens=max_tokens)
        try:
            cout = L.compter_depense(cerveau, getattr(rep, "usage", None), quoi=quoi)
            compter("usd_" + quoi, cout)
        except Exception:
            pass
        texte = "".join(getattr(b, "text", "") for b in (rep.content or []) if getattr(b, "type", "") == "text")
        return texte, ""
    except Exception as ex:
        ajouter_ligne(F_TRACE, {"date": maintenant(), "panne": quoi, "detail": str(ex)[:300]})
        return "", str(ex)[:200]


def json_dans(texte):
    m = re.search(r"\{.*\}", texte or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


# =====================================================================================
#  LE MOTEUR DE SENS (Google gemini-embedding-001, celui de l'ancienne).
#  LE SENS PAR PHRASE, PAS PAR MOT : chaque fiche est decoupee en passages qui suivent les
#  phrases (jamais un mot coupe), chaque passage a son empreinte de sens, et la fiche vaut son
#  meilleur passage. La question, elle, est la phrase ENTIERE du message, avec les deux messages d'avant.
#  En panne (pas de cle, pas d'internet) : on retombe sur les mots en commun, et c'est AFFICHE.
# =====================================================================================
class Moteur:
    URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents"
    DIM = 768

    def __init__(self):
        self.cache = None
        self.panne = ""
        self.verrou = threading.RLock()
        self.index_n = []          # numero de fiche de chaque passage
        self.index_v = []          # empreinte de chaque passage (listes, ou matrice numpy)
        self.index_fait = set()    # fiches deja indexees (n, date de version)
        self.matrice = None
        self.a_ecrire = 0

    def _charger(self):
        if self.cache is None:
            d = lire_json(F_SENS, {})
            self.cache = d if isinstance(d, dict) else {}

    def _ecrire(self, force=False):
        if self.a_ecrire and (force or self.a_ecrire >= 200):
            ecrire_json(F_SENS, self.cache)
            self.a_ecrire = 0

    @staticmethod
    def _cle(tache, texte):
        return hashlib.sha1((tache + "|" + texte).encode("utf-8")).hexdigest()

    @staticmethod
    def _coder(v):
        return base64.b64encode(array.array("f", v).tobytes()).decode("ascii")

    @staticmethod
    def _decoder(s):
        a = array.array("f")
        a.frombytes(base64.b64decode(s))
        return list(a)

    def _appeler(self, textes, tache):
        cle = L.lire_cle_gemini()
        if not cle:
            raise RuntimeError("il manque la cle Gemini (panneau Cles, nom « gemini »)")
        corps = {"requests": [{"model": "models/gemini-embedding-001", "content": {"parts": [{"text": t}]},
                               "taskType": tache, "outputDimensionality": self.DIM} for t in textes]}
        req = urllib.request.Request(self.URL, data=json.dumps(corps).encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json", "x-goog-api-key": cle})
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.loads(r.read().decode("utf-8"))
        emb = d.get("embeddings") or []
        if len(emb) != len(textes):
            raise RuntimeError("Google a rendu %d empreintes pour %d textes" % (len(emb), len(textes)))
        out = []
        for e in emb:
            v = e.get("values") or []
            n = math.sqrt(sum(x * x for x in v)) or 1.0
            out.append([x / n for x in v])
        return out

    def vecteurs(self, textes, tache="RETRIEVAL_DOCUMENT"):
        with self.verrou:
            self._charger()
            textes = [str(t or "")[:8000] or "(vide)" for t in textes]
            cles = [self._cle(tache, t) for t in textes]
            manquants = [i for i, k in enumerate(cles) if k not in self.cache]
            try:
                for debut in range(0, len(manquants), 100):
                    lot = manquants[debut:debut + 100]
                    for i, v in zip(lot, self._appeler([textes[i] for i in lot], tache)):
                        self.cache[cles[i]] = self._coder(v)
                        if tache == "RETRIEVAL_DOCUMENT":
                            self.a_ecrire += 1
                    self._ecrire()
                self.panne = ""
            except Exception as ex:
                self.panne = str(ex)[:200]
            return [self._decoder(self.cache[k]) if k in self.cache else None for k in cles]

    def indexer(self, liste_fiches):
        """Calcule les empreintes des passages des fiches pas encore indexees (une seule fois)."""
        with self.verrou:
            neuves = [f for f in liste_fiches if (f["n"], f.get("date"), f.get("etat")) not in self.index_fait]
            if not neuves:
                return
            textes, quoi = [], []
            for f in neuves:
                for p in passages(f):
                    textes.append(p)
                    quoi.append(f["n"])
            vs = self.vecteurs(textes) if textes else []
            if any(v is None for v in vs):
                return                  # panne : on reessaiera, et la recherche passe par les mots
            for n, v in zip(quoi, vs):
                self.index_n.append(n)
                self.index_v.append(v)
            for f in neuves:
                self.index_fait.add((f["n"], f.get("date"), f.get("etat")))
            self.matrice = None
            self._ecrire(force=True)

    def scores(self, question):
        """{numero de fiche: meilleur score de ses passages}, ou None si le moteur est en panne."""
        q = self.vecteurs([question], "RETRIEVAL_QUERY")[0]
        if q is None or not self.index_v:
            return None
        with self.verrou:
            try:
                import numpy as np
                if self.matrice is None:
                    self.matrice = np.array(self.index_v, dtype="float32")
                s = self.matrice.dot(np.array(q, dtype="float32")).tolist()
            except Exception:
                s = [sum(a * b for a, b in zip(q, v)) for v in self.index_v]
            meilleur = {}
            for n, x in zip(self.index_n, s):
                if x > meilleur.get(n, -9):
                    meilleur[n] = x
            return meilleur


MOTEUR = Moteur()


def passages(f):
    """Les passages d'une fiche, PAR PHRASES (jamais un mot coupe). Le sujet est un passage a lui seul."""
    taille = int(reglages()["passage_caracteres"])
    morceaux = [("%s : %s" % (nature_en_clair(f.get("nature"), "Fiche"), f.get("sujet", ""))).strip()]
    phrases = re.split(r"(?<=[\.\!\?\n])\s+", str(f.get("texte") or ""))
    courant = ""
    for ph in phrases:
        if courant and len(courant) + len(ph) > taille:
            morceaux.append(courant.strip())
            courant = ""
        courant += ph + " "
    if courant.strip():
        morceaux.append(courant.strip())
    return [m for m in morceaux if m]


def _mots(t):
    return set(re.findall(r"[a-z0-9]{4,}", sans_accents(t)))


def classer(question, liste):
    """Les fiches de 'liste', de la plus proche a la plus loin par le sens. Rend (liste, comment)."""
    if not liste:
        return [], "vide"
    MOTEUR.indexer(liste)
    sc = MOTEUR.scores(question)
    if sc is not None:
        return sorted(liste, key=lambda f: -sc.get(f["n"], -9)), "par le sens (Google)"
    mq = _mots(question)
    return sorted(liste, key=lambda f: -len(mq & _mots(f.get("sujet", "") + " " + f.get("texte", "")))), \
        "PAR LES MOTS (moteur de sens en panne : %s)" % (MOTEUR.panne or "?")


# =====================================================================================
#  LA BIBLIOTHEQUE : UNE SEULE, POUR TOUT. Rien ne s'efface : une fiche corrigee est « remplacee ».
# =====================================================================================
NATURES = {"souvenir": "Souvenir", "regle": "Regle de {proprietaire}", "fait": "Fait", "savoir_faire": "Savoir-faire",
           "personne": "Personne", "capacite": "Capacite", "savoir_vivre": "Savoir-vivre"}


def nature_en_clair(nature, defaut="?"):
    """Le nom affiche d'une nature de fiche, le jeton {proprietaire} deja remplace."""
    return avec_le_nom(NATURES.get(nature, defaut))


def _date_propre(d):
    """« 2026-10-19T14:50 » et « 2026-10-19 14:50:07 » deviennent « 2026-10-19 14:50 » (une seule facon d'ecrire)."""
    d = str(d or "").replace("T", " ").strip()
    return d[:16]


def _mtime_fiches():
    try:
        return os.path.getmtime(F_FICHES)
    except Exception:
        return None


def fiches(toutes=False):
    with _verrou_biblio:
        m = _mtime_fiches()
        # Relue si le fichier a change sur le disque : un AUTRE programme (l'import) a pu y ecrire pendant
        # qu'elle tournait (cause verifiee le 20/10 : elle voyait 667 fiches au lieu de 3 768).
        if _FICHES["liste"] is None or m != _FICHES["mtime"]:
            par_n = {}
            for d in lire_lignes(F_FICHES):
                if isinstance(d, dict) and d.get("n"):
                    d["date"] = _date_propre(d.get("date"))
                    par_n[int(d["n"])] = d
            _FICHES["liste"] = [par_n[k] for k in sorted(par_n)]
            _FICHES["mtime"] = m
        liste = _FICHES["liste"]
        return list(liste) if toutes else [f for f in liste if f.get("etat", "active") == "active"]


def marquer_remplacee(ancienne, par):
    """La fiche « ancienne » n'est plus vraie aujourd'hui : elle est marquee remplacee par « par ». Jamais effacee."""
    with _verrou_biblio:
        for v in fiches(toutes=True):
            if int(v["n"]) == int(ancienne) and v.get("etat", "active") == "active":
                ajouter_ligne(F_FICHES, dict(v, etat="remplacee", remplacee_par=int(par), remplacee_le=maintenant()))
                _FICHES["liste"] = None
                return True
    return False


def ecrire_fiche(nature, sujet, texte, remplace=0, source="", date=None):
    nature = sans_accents(nature).replace("-", "_").replace(" ", "_")
    with _verrou_biblio:
        toutes = fiches(toutes=True)
        n = 1 + max([int(f["n"]) for f in toutes] or [0])
        f = {"n": n, "date": _date_propre(date) or maintenant(), "nature": nature if nature in NATURES else "fait",
             "sujet": re.sub(r"\s+", " ", str(sujet or "")).strip(),
             "texte": str(texte or "").strip(), "etat": "active", "source": source}
        if remplace:
            for v in toutes:
                if int(v["n"]) == int(remplace) and v.get("etat", "active") == "active":
                    ajouter_ligne(F_FICHES, dict(v, etat="remplacee", remplacee_par=n, remplacee_le=maintenant()))
                    f["remplace"] = int(remplace)
        ajouter_ligne(F_FICHES, f)
        _FICHES["liste"] = None
    return f


def ecrire_lisible():
    try:
        lignes = ["MA BIBLIOTHEQUE (ecrite par le programme ; rien n'est jamais efface).", ""]
        for f in fiches(toutes=True):
            etat = "" if f.get("etat", "active") == "active" else "   <-- REMPLACEE par n%s" % f.get("remplacee_par")
            lignes.append("n%d [%s] (%s) %s%s" % (f["n"], nature_en_clair(f["nature"]), f["date"], f["sujet"], etat))
            lignes.append("    " + f["texte"].replace("\n", "\n    "))
            lignes.append("")
        with open(F_LISIBLE, "w", encoding="utf-8") as h:
            h.write(avec_le_nom("\n".join(lignes)))     # le jeton {proprietaire} remplace pour la lecture
    except Exception:
        pass
    plan.ecrire_le_plan_lisible(fiches(toutes=True), int(reglages()["diviser_a_partir_de"]))


def _rangee_ou(f):
    c = plan.chemin_de_la_fiche(f["n"])
    return (" {%s}" % " > ".join(c)) if c else ""


def fiche_en_entier(f):
    vital = " VITAL" if plan.vital_de(f["n"]) == "vital" else ""
    t = "--- n%d [%s%s] du %s%s : %s ---\n%s" % (f["n"], nature_en_clair(f["nature"]), vital, f["date"], _rangee_ou(f),
                                                f["sujet"], f["texte"])
    liens = plan.liens_de(f["n"])
    if f.get("remplace") or liens.get("remplace"):
        t += "\n(Cette fiche REMPLACE la n%s : c'est elle qui est vraie maintenant.)" % (f.get("remplace") or liens["remplace"])
    if liens.get("reprend"):
        t += ("\n(Ici on REVIENT a l'ancienne facon, ecrite dans la n%s : ouvre-la en entier si tu en as besoin.)"
              % liens["reprend"])
    if f.get("etat", "active") != "active":
        t += "\n(ATTENTION : cette fiche a ete REMPLACEE par la n%s.)" % f.get("remplacee_par")
    return t


def titre(f):
    return "n%d [%s, %s]%s %s" % (f["n"], nature_en_clair(f["nature"]), f["date"][:16], _rangee_ou(f), f["sujet"])


# =====================================================================================
#  LE BIBLIOTHECAIRE : il lit le MEME BLOC qu'elle + le nouveau message, et les fiches EN ENTIER
# =====================================================================================
def bibliothecaire(message, bloc, precedents, quand_elle_cherche="", compris=None):
    """Rend {"fiches": [(fiche, pourquoi)], "stats": {...}}. Ne leve jamais."""
    t0 = time.time()
    r = reglages()
    actives = fiches()
    stats = {"fiches_en_tout": len(actives), "candidats": 0, "lus_car": 0, "gardes": 0, "secondes": 0.0,
             "comment": "", "panne": ""}
    if not actives:
        stats["comment"] = "bibliotheque vide"
        return {"fiches": [], "stats": stats}
    if quand_elle_cherche:
        question = quand_elle_cherche
    elif compris and compris.get("de_quoi"):
        question = compris["de_quoi"]                  # piece 4 : la phrase de sens, pas un collage de messages
    else:
        question = " ".join([str(x) for x in precedents[-2:]] + [str(message or "")])
    ordre, comment = classer(question, actives)
    pile = ordre[:int(r["bibliothecaire_lit_combien"])]
    blocs = "\n\n".join("=== FICHE %d ===\n%s" % (k, fiche_en_entier(f)) for k, f in enumerate(pile, 1))
    stats.update(candidats=len(pile), lus_car=len(blocs), comment=comment)
    if quand_elle_cherche:
        consigne_besoin = ("CE QUE LUCIANA CHERCHE ELLE-MEME (elle a decide qu'il lui manque ca) : %s\n\n"
                           % quand_elle_cherche)
    else:
        consigne_besoin = ""
    contenu = (
        ("VOICI LA CONVERSATION EN COURS ENTRE {proprietaire} ET L'ASSISTANTE, mot pour mot (le meme bloc qu'elle a sous "
         "les yeux) :\n----- DEBUT -----\n" + bloc + "\n----- FIN -----\n\n") if bloc.strip() else "") + \
        "LE NOUVEAU MESSAGE DE {proprietaire} : " + str(message or "") + "\n\n" + consigne_besoin + \
        (("CE QUE LA PERSONNE VEUT DIRE (compris par le programme, en lisant toute la conversation) : %s\n\n"
          % comprendre.en_clair(compris)) if compris else "") + \
        ("VOICI %d FICHES DE SA BIBLIOTHEQUE, sorties par le moteur de sens. Lis-les EN ENTIER.\n\n%s\n\n"
         "TON TRAVAIL : tu es son bibliothecaire et tu juges comme un psychologue. Un mot n'a pas le meme sens "
         "dans toutes les phrases : c'est la phrase entiere qui vient d'etre ecrite, la situation et ce que la personne "
         "veut dire MAINTENANT "
         "qui comptent. Garde SEULEMENT les fiches qui aident vraiment Luciana a repondre OU A AGIR maintenant "
         "(ce que la personne veut dire, une regle qu'on lui a donnee, comment on fait une chose sur ce PC, ce qui y est "
         "installe, qui est une personne, ce qui a ete dit un autre jour). Si ce qu'il faut est DEJA dans la "
         "conversation, ou si les fiches parlent d'autre chose, ne garde rien. Pour un simple bonjour, rien. "
         "Si deux fiches se contredisent, garde la plus recente.\n"
         "Reponds UNIQUEMENT en JSON strict : {\"fiches\": [{\"n\": <numero de la liste>, \"pourquoi\": "
         "\"<en une phrase>\"}]} de la plus utile a la moins utile, ou {\"fiches\": []}." % (len(pile), blocs))
    brut, panne = appel_simple(r["cerveau_bibliothecaire"], "Tu es le bibliothecaire de Luciana. JSON strict.",
                               contenu, "bibliothecaire", reflechir=bool(r["reflexion_bibliothecaire"]),
                               timeout=float(r["bibliothecaire_plafond_secondes"]))
    d = json_dans(brut)
    gardees = []
    if d is None:
        stats["panne"] = panne or "reponse illisible"
    else:
        vus = set()
        for x in d.get("fiches") or []:
            try:
                k = int(x.get("n")) if isinstance(x, dict) else int(x)
            except Exception:
                continue
            if 1 <= k <= len(pile) and k not in vus:
                vus.add(k)
                gardees.append((pile[k - 1], str((x.get("pourquoi") if isinstance(x, dict) else "") or "")))
    stats.update(gardes=len(gardees), secondes=round(time.time() - t0, 1))
    return {"fiches": gardees, "stats": stats}


def texte_de_la_tete(brouillon):
    """Ce que dit la reponse de tete, ET les gestes qu'elle s'apprete a faire (outils), en clair."""
    morceaux = []
    for b in (getattr(brouillon, "content", None) or []):
        if getattr(b, "type", "") == "text":
            morceaux.append(getattr(b, "text", ""))
        elif getattr(b, "type", "") == "tool_use":
            morceaux.append("[elle s'apprete a utiliser l'outil %s avec : %s]"
                            % (getattr(b, "name", "?"), json.dumps(getattr(b, "input", {}), ensure_ascii=False)[:600]))
    return "\n".join(m for m in morceaux if m).strip()


def relecture(message, brouillon, deja=()):
    """V200 : quand elle a prepare sa reponse de tete, le bibliothecaire la RELIT avec TOUTES les
    regles de comportement de la bibliotheque (natures regle et savoir_vivre), EN ENTIER. Les regles qu'elle ne
    respecte pas sont rendues : la reponse de tete est alors jetee et elle repond avec elles sous les yeux
    (mecanique V183). Ce n'est pas un garde-fou : si tout est respecte, rien n'est ajoute.
    Pourquoi : le moteur de sens ne sort que les fiches proches du SUJET du message ; une regle comme
    « reponds court » ou « sous-traite a Claude Code » n'est proche d'aucun sujet, donc elle n'etait jamais lue.
    Rend ([(fiche, pourquoi)], stats). Ne leve jamais."""
    t0 = time.time()
    stats = {"regles_lues": 0, "violees": 0, "secondes": 0.0, "panne": ""}
    try:
        regles = [f for f in fiches() if f.get("nature") in ("regle", "savoir_vivre") and f.get("n") not in deja]
        tete = texte_de_la_tete(brouillon)
        if not regles or not tete:
            return [], stats
        blocs = "\n\n".join("=== REGLE %d ===\n%s" % (k, fiche_en_entier(f)) for k, f in enumerate(regles, 1))
        stats["regles_lues"] = len(regles)
        contenu = ("LE NOUVEAU MESSAGE DE {proprietaire} : %s\n\n"
                   "LA REPONSE QUE L'ASSISTANTE S'APPRETE A LUI DONNER (et les gestes qu'elle s'apprete a faire) :\n"
                   "----- DEBUT -----\n%s\n----- FIN -----\n\n"
                   "VOICI TOUTES LES REGLES QU'ON LUI A DONNEES, en entier :\n\n%s\n\n"
                   "TON TRAVAIL : dis quelles regles cette reponse ou ces gestes NE RESPECTENT PAS (longueur, nombre "
                   "de questions, ton, ce qu'elle doit deleguer ou chercher, ce qu'elle ne doit pas dire ou pas faire...). "
                   "Juge le SENS de la regle et la situation, comme un psychologue, pas les mots. Une regle qui ne "
                   "concerne pas ce moment ne compte pas. Si tout est respecte : {\"regles\": []}.\n"
                   "Reponds UNIQUEMENT en JSON strict : {\"regles\": [{\"n\": <numero>, \"pourquoi\": \"<en une phrase>\"}]}"
                   % (str(message or ""), tete[:12000], blocs))
        r = reglages()
        brut, panne = appel_simple(r["cerveau_bibliothecaire"], "Tu es le bibliothecaire de Luciana. JSON strict.",
                                   contenu, "relecture", reflechir=bool(r["reflexion_bibliothecaire"]),
                                   timeout=float(r["bibliothecaire_plafond_secondes"]))
        d = json_dans(brut)
        if d is None:
            stats["panne"] = panne or "reponse illisible"
            return [], stats
        violees, vus = [], set()
        for x in d.get("regles") or []:
            try:
                k = int(x.get("n")) if isinstance(x, dict) else int(x)
            except Exception:
                continue
            if 1 <= k <= len(regles) and k not in vus:
                vus.add(k)
                violees.append((regles[k - 1], "regle a respecter dans cette reponse : " +
                                str((x.get("pourquoi") if isinstance(x, dict) else "") or "")))
        stats["violees"] = len(violees)
        return violees, stats
    except Exception as ex:
        stats["panne"] = str(ex)[:200]
        return [], stats
    finally:
        stats["secondes"] = round(time.time() - t0, 1)


def bloc_des_fiches(gardees, pour_qui="pour la phrase ci-dessous"):
    """Les fiches EN ENTIER (jamais coupees). La seule limite : le nombre. Les suivantes sont nommees."""
    maxi = int(reglages()["fiches_donnees_max"])
    donnees, nommees = gardees[:maxi], gardees[maxi:]
    morceaux = ["CE QUE TA BIBLIOTHEQUE APPORTE %s (le bibliothecaire a lu ta conversation et ces fiches en "
                "entier ; chaque fiche est un document DATE, mot pour mot, pas forcement l'etat d'aujourd'hui ; "
                "si deux se contredisent, la plus recente compte) :" % pour_qui]
    for f, pourquoi in donnees:
        morceaux.append(fiche_en_entier(f) + (("\n(pourquoi elle sert : %s)" % pourquoi) if pourquoi else ""))
    if nommees:
        morceaux.append("AUSSI UTILES, a ouvrir en entier avec ouvrir_fiches si tu en as besoin : "
                        + " ; ".join(titre(f) for f, _p in nommees))
    return "\n\n".join(morceaux), len(donnees), sum(len(fiche_en_entier(f)) for f, _p in donnees)


def ouvrir(numeros):
    par_n = {int(f["n"]): f for f in fiches(toutes=True)}
    out = []
    for x in numeros if isinstance(numeros, list) else re.findall(r"\d+", str(numeros or "")):
        try:
            f = par_n.get(int(str(x).lstrip("nN")))
        except Exception:
            f = None
        if f:
            out.append(fiche_en_entier(f))
    compter("fiches_ouvertes", len(out))
    COULISSES["dernier"]["fiches_ouvertes"] = COULISSES["dernier"].get("fiches_ouvertes", 0) + len(out)
    return "\n\n".join(out) or "Aucune fiche avec ces numeros."


# =====================================================================================
#  LA CONVERSATION DU JOUR (la fenetre) + L'ARCHIVISTE
# =====================================================================================
def messages_tous():
    return lire_lignes(F_CONVERSATION)


def range_jusqu_a():
    return int(lire_json(F_RANGEMENT, {}).get("jusqu_a", 0))


def fenetre():
    j = range_jusqu_a()
    return [m for m in messages_tous() if int(m.get("n", 0)) > j]


def taille(m):
    return len(str(m.get("texte", ""))) + sum(len(str(a)) for a in (m.get("actions") or []))


def ajouter_message(role, texte, actions=None):
    with _verrou_fichiers:
        tous = messages_tous()
        n = 1 + (int(tous[-1]["n"]) if tous else 0)
        m = {"n": n, "role": role, "date": maintenant(), "texte": texte}
        if actions:
            m["actions"] = actions
        ajouter_ligne(F_CONVERSATION, m)
    return m


def note_du_programme(texte):
    """Ce que les taches de fond de la V198 ecrivaient dans l'ancienne memoire (rapport de chantier,
    resultat Grok, clic d'un bouton...) arrive ICI, dans la conversation du jour, pour qu'elle le voie."""
    try:
        ajouter_message("programme", str(texte or ""))
    except Exception:
        pass


def qui(m):
    return perso({"user": "{proprietaire}", "assistant": "Luciana"}.get(m["role"], "Le programme"))


def texte_de(m):
    t = "[%s] %s : %s" % (m.get("date", ""), qui(m), m.get("texte", ""))
    if m.get("actions"):
        t += "\n[Outils vraiment utilises : %s]" % " | ".join(str(a) for a in m["actions"])
    return t


_rangement = threading.Lock()


def ranger_si_besoin():
    if not _rangement.acquire(blocking=False):
        return
    try:
        r = reglages()
        fen = fenetre()
        total = sum(taille(m) for m in fen)
        if total <= int(r["fenetre_max_caracteres"]):
            return
        a_ranger, reste = [], total
        for m in fen:
            if reste <= int(r["fenetre_apres_rangement"]):
                break
            a_ranger.append(m)
            reste -= taille(m)
        while a_ranger and a_ranger[-1]["role"] == "user":
            a_ranger.pop()
        if not a_ranger:
            return
        tous = messages_tous()
        avant = [m for m in tous if int(m["n"]) < int(a_ranger[0]["n"])][-2:]
        for p in decouper(a_ranger, 20000):
            ok, nb = ranger_un_paquet(p, avant)
            if not ok:
                compter("rangements_en_panne")
                return
            ecrire_json(F_RANGEMENT, {"jusqu_a": int(p[-1]["n"]), "le": maintenant()})
            compter("messages_ranges", len(p))
            compter("souvenirs_crees", nb)
            avant = p[-2:]
        ecrire_lisible()
    finally:
        _rangement.release()


def decouper(liste, plafond):
    paquets, paquet, t = [], [], 0
    for m in liste:
        if paquet and t + taille(m) > plafond:
            paquets.append(paquet)
            paquet, t = [], 0
        paquet.append(m)
        t += taille(m)
    if paquet:
        paquets.append(paquet)
    return paquets


def ranger_un_paquet(paquet, avant, avec_lecons=False):
    """L'ARCHIVISTE : decoupe un paquet de messages en souvenirs PAR LE SENS. Chaque souvenir garde le
    texte des messages MOT POUR MOT. Rien ne se perd (le reste fait une fiche). Rend (ok, nb)."""
    r = reglages()
    contexte = "\n\n".join(texte_de(m) for m in avant)
    numerotes = "\n\n".join("#%d %s" % (m["n"], texte_de(m)) for m in paquet)
    lecons = ("\nAUSSI : ces messages sont de {proprietaire} LUI-MEME. Releve ce qu'ils APPRENNENT a l'assistante "
              "pour la suite "
              "(regle, fait, personne, savoir_faire, capacite, savoir_vivre), en une ou deux phrases chacune, avec "
              "le numero du message d'ou ca vient. Rien d'invente, seulement ce qui est vraiment dit.\n"
              "Ajoute dans le JSON : \"lecons\": [{\"nature\": \"...\", \"sujet\": \"...\", \"texte\": \"...\", "
              "\"message\": <numero>}]") if avec_lecons else ""
    contenu = (("POUR COMPRENDRE (deja range, ne pas reranger) :\n" + contexte + "\n\n") if contexte else "") + \
        "LES MESSAGES A RANGER (numerotes) :\n" + numerotes + "\n\n" + \
        ("TON TRAVAIL : tu es l'archiviste de cette memoire. Tu decoupes ces messages en SOUVENIRS, PAR LE SENS, comme un "
         "psychologue : un souvenir = un moment, un sujet, une histoire qui se tient (jamais un decoupage par "
         "mots). Chaque message doit aller dans au moins un souvenir. Pour chacun, un sujet clair en une phrase "
         "(qui, quoi, quand) qui permettra de le retrouver dans 60 ans." + lecons + "\n"
         "Reponds UNIQUEMENT en JSON strict : {\"souvenirs\": [{\"sujet\": \"...\", \"messages\": [<numeros>]}]"
         + (", \"lecons\": [...]" if avec_lecons else "") + "}")
    brut, _p = appel_simple(r["cerveau_archiviste"], "Tu es l'archiviste de cette memoire. JSON strict.",
                            contenu, "archiviste", reflechir=False, max_tokens=8000)
    d = json_dans(brut)
    if not isinstance(d, dict) or not isinstance(d.get("souvenirs"), list):
        ajouter_ligne(F_TRACE, {"date": maintenant(), "rangement": "panne, rien n'est marque range"})
        return False, 0
    par_n = {int(m["n"]): m for m in paquet}
    couverts, nb = set(), 0
    for s in d["souvenirs"]:
        nums = []
        for x in s.get("messages") or []:
            try:
                k = int(str(x).lstrip("#"))
            except Exception:
                continue
            if k in par_n and k not in nums:
                nums.append(k)
        if not nums:
            continue
        couverts.update(nums)
        ecrire_fiche("souvenir", s.get("sujet") or "Conversation",
                     "\n\n".join(texte_de(par_n[k]) for k in sorted(nums)),
                     source="archiviste", date=par_n[min(nums)].get("date"))
        nb += 1
    oublies = sorted(k for k in par_n if k not in couverts)
    if oublies:
        ecrire_fiche("souvenir", "Conversation du %s (le reste)" % str(par_n[oublies[0]].get("date"))[:10],
                     "\n\n".join(texte_de(par_n[k]) for k in oublies), source="archiviste",
                     date=par_n[oublies[0]].get("date"))
        nb += 1
    for x in (d.get("lecons") or []) if avec_lecons else []:
        if isinstance(x, dict) and str(x.get("texte") or "").strip():
            m = par_n.get(int(x.get("message") or 0)) if str(x.get("message") or "").isdigit() else None
            f = ecrire_fiche(x.get("nature") or "fait", x.get("sujet") or "", x["texte"],
                             source="tire des mots de {proprietaire}%s" % ((" (message du %s)" % m["date"]) if m else ""),
                             date=(m or {}).get("date"))
            compter("lecons_" + f["nature"])
    return True, nb


def apprendre(message_recu, reponse, actions):
    """APRES CHAQUE ECHANGE, en fond, sans clic : ce que ce moment APPREND."""
    r = reglages()
    msg = str(message_recu or "").strip()
    if not r.get("apprentissage") or not msg or msg.startswith("["):
        return
    try:
        lecons = [f for f in fiches() if f.get("nature") != "souvenir"]
        proches = ""
        if lecons:
            ordre, _c = classer(msg + "\n" + str(reponse)[:1500], lecons)
            proches = "\n".join("%s : %s" % (titre(f), f["texte"]) for f in ordre[:15])
        gestes = "\n".join("- %s" % str(a) for a in actions or []) or "(aucun outil)"
        contenu = (
            "CE QUE LA PERSONNE A ECRIT :\n" + msg + "\n\nLES GESTES VRAIMENT FAITS (ecrits par le programme) :\n" + gestes +
            "\n\nCE QUE L'ASSISTANTE A REPONDU :\n" + str(reponse) + "\n\nCE QU'ELLE SAIT DEJA ET QUI EST PROCHE :\n" +
            (proches or "(rien)") + "\n\n"
            "TON TRAVAIL : tu gardes SEULEMENT ce que ce moment APPREND a l'assistante pour la suite, comme une personne "
            "qui s'eduque -- surtout quand on la CORRIGE (« non », « je t'ai deja dit », « arrete de... », « tu as "
            "des mains, fais-le toi-meme »). Natures : regle, fait (vrai et durable, ex. « WhatsApp est installe sur "
            "le PC »), savoir_faire (comment on fait ici, seulement si les gestes montrent que ca a marche ou si "
            "on l'explique), capacite, personne (ce que la personne dit d'une AUTRE personne), savoir_vivre. Jamais ce que "
            "l'assistante affirme seule sans preuve. Une simple conversation ou une plaisanterie : rien. Deja su : rien. "
            "Si ca CORRIGE une fiche de la liste, donne son numero (sans le n) dans \"remplace\".\n"
            "Reponds UNIQUEMENT en JSON strict : {\"lecons\": [{\"nature\": \"...\", \"sujet\": \"...\", \"texte\": "
            "\"...\", \"remplace\": 0}]} ou {\"lecons\": []}")
        brut, _p = appel_simple(r["cerveau_archiviste"], "Tu es l'archiviste de cette memoire. JSON strict.", contenu,
                                "apprentissage", reflechir=False, max_tokens=3000)
        d = json_dans(brut) or {}
        appris = []
        for x in d.get("lecons") or []:
            if isinstance(x, dict) and str(x.get("texte") or "").strip():
                try:
                    remplace = int(str(x.get("remplace") or 0).lstrip("nN") or 0)
                except Exception:
                    remplace = 0
                f = ecrire_fiche(x.get("nature") or "fait", x.get("sujet") or "", x["texte"], remplace=remplace,
                                 source="appris le %s de : %s" % (maintenant(), msg[:300]))
                compter("lecons_" + f["nature"])
                appris.append(titre(f) + " : " + f["texte"])
        if appris:
            COULISSES["derniere_lecon"] = appris[-1]
            ecrire_lisible()
        compter("apprentissages_faits")
    except Exception as ex:
        ajouter_ligne(F_TRACE, {"date": maintenant(), "panne": "apprentissage", "detail": str(ex)[:300]})


# =====================================================================================
#  LES RAPPELS A L'HEURE (tenus par le programme ; dits par les pastilles de la V198 + le telephone)
# =====================================================================================
def outil_rappels(e):
    d = lire_json(F_RAPPELS, {"rappels": []})
    rs = d.get("rappels") or []
    a = sans_accents(e.get("action") or "lister")
    if a.startswith("ajout"):
        quand = str(e.get("quand") or "").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", quand):
            return "Donne 'quand' au format AAAA-MM-JJ HH:MM (ex. %s)." % maintenant()
        n = 1 + max([x["n"] for x in rs] or [0])
        rs.append({"n": n, "quand": quand, "texte": str(e.get("texte") or ""), "fait": False})
        ecrire_json(F_RAPPELS, {"rappels": rs})
        return "Rappel n%d enregistre pour le %s : c'est le PROGRAMME qui le dira a {proprietaire} a l'heure." % (n, quand)
    if a.startswith("retir"):
        for x in rs:
            if str(x["n"]) == str(e.get("numero")):
                x["fait"] = True
                ecrire_json(F_RAPPELS, {"rappels": rs})
                return "Rappel n%s retire." % x["n"]
        return "Pas de rappel avec ce numero."
    a_venir = [x for x in rs if not x["fait"]]
    return "\n".join("n%d le %s : %s" % (x["n"], x["quand"], x["texte"]) for x in a_venir) or "Aucun rappel a venir."


def boucle_horloge():
    while True:
        try:
            d = lire_json(F_RAPPELS, {"rappels": []})
            change = False
            for x in d.get("rappels") or []:
                if not x["fait"] and x["quand"] <= maintenant():
                    x["fait"] = True
                    change = True
                    texte = "Rappel (prevu le %s) : %s" % (x["quand"], x["texte"])
                    note_du_programme(texte)
                    try:
                        L.ajouter_evenement({"texte": texte, "titre": "⏰ " + x["texte"][:80]}, alerte=texte,
                                            genre="rappel")
                    except Exception:
                        pass
            if change:
                ecrire_json(F_RAPPELS, d)
        except Exception:
            pass
        time.sleep(30)


# =====================================================================================
#  LES OUTILS : ses outils de base toujours en main ; TOUS les autres outils de la V198 choisis PAR
#  LE SENS a chaque message (les 5 plus proches), ou trouves par elle (trouver_un_outil). Un outil
#  pris reste en main jusqu'au redemarrage (la liste ne fait que grandir : le cache, donc le cout, reste bas).
# =====================================================================================
OUTILS_NEUFS = [
    {"name": "chercher_dans_ma_bibliotheque",
     "description": "Cherche dans TA bibliotheque (souvenirs, regles de {proprietaire}, faits, personnes, savoir-faire). Le "
                    "bibliothecaire lit ta conversation et les fiches EN ENTIER et te rend celles qui servent, "
                    "datees, mot pour mot. Sers-t'en des qu'il te manque une chose de la vie de {proprietaire}, de vos projets, "
                    "de son PC ou du passe. N'invente jamais : cherche.",
     "input_schema": {"type": "object", "properties": {"question": {"type": "string", "description": "Ce qui te manque, en une phrase claire."}}, "required": ["question"]}},
    {"name": "ouvrir_fiches",
     "description": "Ouvre EN ENTIER des fiches de ta bibliotheque par leur numero (ex. [12, 40]).",
     "input_schema": {"type": "object", "properties": {"numeros": {"type": "array", "items": {"type": "integer"}}}, "required": ["numeros"]}},
    {"name": "retenir",
     "description": "Range TOUT DE SUITE dans ta bibliotheque une chose qu'on te demande de retenir, ou une "
                    "correction qu'il te donne. nature : regle, fait, savoir_faire, personne, capacite, savoir_vivre. "
                    "Si ca corrige une fiche, son numero dans 'remplace' (l'ancienne est marquee, jamais effacee).",
     "input_schema": {"type": "object", "properties": {"nature": {"type": "string"}, "sujet": {"type": "string"},
                                                       "texte": {"type": "string"}, "remplace": {"type": "integer"}},
                      "required": ["nature", "sujet", "texte"]}},
    {"name": "trouver_un_outil",
     "description": "Tu as beaucoup d'autres outils (mails, fichiers, documents, ecran, souris, navigateur, web, "
                    "agenda, drive, compta, video, Grok, chantiers Claude Code...). Decris ce que tu veux faire : "
                    "les outils qui conviennent sont mis dans ta main tout de suite. Ne dis JAMAIS que tu ne sais pas "
                    "faire une chose avant d'avoir cherche ici.",
     "input_schema": {"type": "object", "properties": {"besoin": {"type": "string"}}, "required": ["besoin"]}},
    {"name": "rappels",
     "description": "Les rappels a heure fixe, tenus par le PROGRAMME (il les dit a {proprietaire} a l'heure, et sur son "
                    "telephone). Actions : ajouter (quand = AAAA-MM-JJ HH:MM, texte), lister, retirer (numero).",
     "input_schema": {"type": "object", "properties": {"action": {"type": "string"}, "quand": {"type": "string"},
                                                       "texte": {"type": "string"}, "numero": {"type": "integer"}},
                      "required": ["action"]}},
]
# Les outils de la V198 qui restent TOUJOURS en main : ses listes (choses en cours, mission).
BASE_ANCIENS = ["choses_en_cours", "carnet_de_mission"]
# Les outils de la V198 qui NE SONT PAS repris : son ancienne memoire, remplacee par LA bibliotheque.
EXCLUS = {"fouiller_ma_bibliotheque", "chercher_dans_memoire", "retenir", "mettre_a_jour_souvenir",
          "anciennes_notes", "journal_de_bord", "consigne", "sujet_a_eviter", "recettes", "carnet_chantier",
          "sauvegarder_memoire", "restaurer_memoire", "mes_lecons"}
_EN_MAIN = []


def catalogue(cerveau):
    """Les outils de la V198 (dans la version du cerveau choisi), sans son ancienne memoire."""
    out = []
    liste = L.outils_pour(cerveau)
    if hasattr(L, "_perso_outils"):
        try:
            liste = L._perso_outils(liste)
        except Exception:
            pass
    for o in liste:
        nom = o.get("name") if isinstance(o, dict) else None
        if nom and nom not in EXCLUS:
            out.append(o)
    return out


def _texte_outil(o):
    return "%s : %s" % (o.get("name"), o.get("description") or o.get("name"))


_SENS_OUTILS = {}


def proposer_outils(besoin, cerveau, combien):
    cat = [o for o in catalogue(cerveau) if o.get("name") not in BASE_ANCIENS and o.get("input_schema")]
    permis = CROCHETS["outils_permis"]() if CROCHETS.get("outils_permis") else None
    if permis is not None:
        cat = [o for o in cat if o.get("name") in permis]
    if not cat:
        return []
    textes = [_texte_outil(o) for o in cat]
    q = MOTEUR.vecteurs([besoin], "RETRIEVAL_QUERY")[0]
    vs = MOTEUR.vecteurs(textes) if q is not None else [None]
    if q is not None and all(v is not None for v in vs):
        sc = [sum(a * b for a, b in zip(q, v)) for v in vs]
    else:
        mq = _mots(besoin)
        sc = [len(mq & _mots(t)) for t in textes]
    ordre = sorted(range(len(cat)), key=lambda i: -sc[i])
    return [cat[i] for i in ordre[:combien]]


def prendre_en_main(outils):
    plafond = int(reglages()["outils_actifs_max"])
    for o in outils:
        if o["name"] not in _EN_MAIN:
            _EN_MAIN.append(o["name"])
    while len(_EN_MAIN) > plafond:
        _EN_MAIN.pop(0)


def outils_du_tour(cerveau):
    cat = catalogue(cerveau)
    par_nom = {o.get("name"): o for o in cat}
    serveur = [o for o in cat if not o.get("input_schema")]        # ex. recherche web d'Anthropic
    neufs = [dict(o, description=perso(o["description"])) for o in OUTILS_NEUFS
             + ([quotidien.OUTIL] if reglages().get("bibliotheque_rangee") else [])]
    base = neufs + [par_nom[n] for n in BASE_ANCIENS if n in par_nom] + serveur
    tous = base + [par_nom[n] for n in _EN_MAIN if n in par_nom and par_nom[n] not in base]
    permis = CROCHETS["outils_permis"]() if CROCHETS.get("outils_permis") else None
    if permis is not None:                          # ex. Luminita en mode enfant : sa memoire seulement
        tous = [o for o in tous if o.get("name") in permis]
    return tous


def executer(nom, entree, cerveau):
    """Ce que rend un outil part sous les yeux de l'assistante : le jeton {proprietaire} y est remplace."""
    sortie = _executer(nom, entree, cerveau)
    return avec_le_nom(sortie) if isinstance(sortie, str) else sortie


def _executer(nom, entree, cerveau):
    entree = entree or {}
    if nom == "chercher_dans_ma_bibliotheque":
        compter("recherches")
        COULISSES["dernier"]["recherches"] = COULISSES["dernier"].get("recherches", 0) + 1
        rendu = bibliothecaire(entree.get("question") or "", TOUR.get("bloc", ""), TOUR.get("precedents", []),
                               quand_elle_cherche=str(entree.get("question") or ""))
        if not rendu["fiches"]:
            return ("Le bibliothecaire a lu %d fiches : aucune ne repond a « %s ». N'invente pas : dis-le."
                    % (rendu["stats"]["candidats"], entree.get("question")))
        texte, n, _c = bloc_des_fiches(rendu["fiches"], "pour ce que tu cherches")
        compter("fiches_donnees", n)
        return texte
    if nom == "ouvrir_fiches":
        return ouvrir(entree.get("numeros"))
    if nom == "retenir":
        try:
            remplace = int(entree.get("remplace") or 0)
        except Exception:
            remplace = 0
        f = ecrire_fiche(entree.get("nature") or "fait", entree.get("sujet"), entree.get("texte"), remplace=remplace,
                         source="retenir, demande pendant la conversation du %s" % maintenant())
        compter("lecons_" + f["nature"])
        ecrire_lisible()
        return "Range dans ta bibliotheque : fiche n%d [%s] %s." % (f["n"], nature_en_clair(f["nature"]), f["sujet"])
    if nom == "trouver_un_outil":
        trouves = proposer_outils(str(entree.get("besoin") or ""), cerveau, 5)
        prendre_en_main(trouves)
        compter("outils_trouves", len(trouves))
        return "Ces outils sont maintenant dans ta main :\n" + "\n".join(
            "- %s : %s" % (o["name"], str(o.get("description", ""))) for o in trouves)
    if nom == "rappels":
        return outil_rappels(entree)
    if nom == "journal_du_quotidien":
        return quotidien.lire(str(entree.get("jour") or "aujourd'hui"), str(entree.get("quoi") or ""))
    permis = CROCHETS["outils_permis"]() if CROCHETS.get("outils_permis") else None
    if permis is not None and nom not in permis:
        return "Cet outil n'est pas disponible ici."
    return L._executer_outil(nom, entree)


# =====================================================================================
#  LE TRAJET D'UN MESSAGE
# =====================================================================================
TOUR = {"bloc": "", "precedents": []}
MEMOIRE_EN_CLAIR = (
    "TA MEMOIRE, COMMENT ELLE MARCHE (c'est la verite, ecrite par le programme) : tu as UNE bibliotheque qui "
    "garde tout, mot pour mot et datee : vos conversations rangees (souvenirs), les regles de {proprietaire}, les faits, les "
    "personnes, les savoir-faire. A chaque message, ton bibliothecaire lit ta conversation et ta bibliotheque ; "
    "quand quelque chose sert, il te l'apporte EN ENTIER juste avant le message. Sers-toi d'abord de ta "
    "tete ; s'il te manque quoi que ce soit (la vie de {proprietaire}, vos projets, son PC, le passe), CHERCHE "
    "(chercher_dans_ma_bibliotheque) au lieu d'inventer ou de demander. Quand on te demande de retenir quelque "
    "chose ou te corrige, range-le tout de suite (retenir). Apres chaque echange, ton archiviste range aussi tout "
    "seul ce que tu as appris. Tes outils : les plus utiles pour ce message sont deja dans ta main ; les autres, "
    "trouve-les (trouver_un_outil) : tu as des mains et des yeux sur le PC de {proprietaire}.")


def personnalite():
    if CROCHETS.get("personnalite"):
        return CROCHETS["personnalite"]()
    try:
        return open(os.path.join(ICI, "personnalite.txt"), encoding="utf-8-sig").read().strip()
    except Exception:
        return "Tu es Luciana, l'assistante et l'amie de {proprietaire}. Tu tutoies cette personne, en francais."


def texte_du_bloc(fen):
    return "\n\n".join(texte_de(m) for m in fen)


def construire_messages(fen, contexte, image=None):
    msgs = []
    for m in fen:
        role = "assistant" if m["role"] == "assistant" else "user"
        if m["role"] == "user":
            d = str(m.get("date", ""))
            quand = ("%s/%s/%s %s" % (d[8:10], d[5:7], d[0:4], d[11:16])) if (reglages().get("bibliotheque_rangee")
                                                                                and len(d) >= 16) else d[11:16]
            texte = "%s [%s] : %s" % (proprietaire(), quand, m.get("texte", ""))
        elif m["role"] == "programme":
            texte = "[Le programme, %s] %s" % (m.get("date", ""), m.get("texte", ""))
        else:
            texte = m.get("texte", "")
        if m.get("actions"):
            texte += "\n\n[Journal du programme : outils vraiment utilises -> %s]" % " | ".join(m["actions"])
        if msgs and msgs[-1]["role"] == role:
            msgs[-1]["content"] += "\n\n" + texte
        else:
            msgs.append({"role": role, "content": texte})
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    if msgs and msgs[-1]["role"] == "user":
        msgs[-1]["content"] = contexte + "\n\n" + msgs[-1]["content"]
        if image and image.get("data"):
            msgs[-1]["content"] = [{"type": "image", "source": {"type": "base64",
                                                                "media_type": image.get("media_type", "image/jpeg"),
                                                                "data": image["data"]}},
                                   {"type": "text", "text": msgs[-1]["content"]}]
    return msgs


def _contexte_du_tour(vrai_message):
    if CROCHETS.get("contexte"):
        return perso(CROCHETS["contexte"](vrai_message))
    morceaux = [L._horodatage()]
    for f in (lambda: L.rappel_de_la_mission(vrai_message), lambda: L.texte_travaux_en_cours(),
              lambda: L.rappel_des_choses_en_cours(vrai_message)):
        try:
            x = f()
            if x:
                morceaux.append(x)
        except Exception:
            pass
    return "\n\n".join(morceaux)


def repondre(message, image=None):
    try:
        L._tour_commence()
    except Exception:
        pass
    try:
        with _verrou_tour:
            L._arret_oublier()
            try:
                return _tour(message, image)
            except L.ArretDemandeParFred:
                texte = "(Tu m'as demande d'arreter : je me suis arretee la. Rien d'autre n'a ete fait.)"
                ajouter_message("assistant", texte, COULISSES["dernier"].get("actions") or [])
                L._v180_ecrit(texte, etape="")
                return texte
    finally:
        try:
            L._tour_termine()
        except Exception:
            pass


def confier(texte, source="", quand=""):
    """Ce que la V198 confiait a son archiviste (une chose en cours finie, une mission close) va dans
    LA bibliotheque, EN ENTIER, comme un souvenir date. Rend (True, phrase vraie) ou (False, raison) :
    EXACTEMENT ce que la V198 attend de confier_a_l_archiviste."""
    try:
        premiere = (str(texte or "").strip().splitlines() or ["(sans titre)"])[0]
        f = ecrire_fiche("souvenir", premiere, texte, source=str(source or "confie par le programme"),
                         date=(str(quand)[:16] or None))
        ecrire_lisible()
        compter("souvenirs_crees")
        return True, "range dans ta bibliotheque (fiche n%d, en entier)" % f["n"]
    except Exception as ex:
        return False, "pas pu etre range dans la bibliotheque : %s" % str(ex)[:200]


def _tour(message, image):
    t0 = time.time()
    r = reglages()
    cerveau = L.lire_cerveau()
    cli = L.client_de(cerveau)
    if cli is None:
        return ("Il me manque la cle pour le cerveau choisi. Ouvre le bouton Cles en haut et colle-la "
                "(DeepSeek : sk-..., Claude : sk-ant-..., Gemini : AIza...).")
    if CROCHETS.get("avant_tour"):
        refus = CROCHETS["avant_tour"](message)
        if refus:
            return refus
    L._v180_ecrit("", etape="je lis ton message", nouveau_tour=True)
    vrai = not str(message or "").lstrip().startswith("[")
    texte_recu = message or ("[photo envoyee par {proprietaire}]" if image else "")
    precedents = [m["texte"] for m in fenetre() if m["role"] == "user"][-2:]
    m_recu = ajouter_message("user", texte_recu)
    compter("messages_recus" if vrai else "messages_du_programme")
    fen = fenetre()
    bloc = texte_du_bloc(fen)
    TOUR.update(bloc=bloc, precedents=precedents)
    D = COULISSES["dernier"] = {"quand": time.strftime("%H:%M:%S"), "cerveau": cerveau, "recherches": 0,
                                "fiches_ouvertes": 0, "actions": []}

    # LE BIBLIOTHECAIRE, EN MEME TEMPS qu'elle prepare sa reponse de tete (V183)
    rendu_biblio = {}

    def _fil():
        compris = None
        if r.get("bibliotheque_rangee"):             # piece 4 (eteinte dans la vraie Luciana tant que 3 a 6 ne sont pas finies)
            compris = comprendre.comprendre(message, bloc, m_recu.get("date"))
            # LE REGISTRE DES PERSONNES (etape b) : le programme tranche qui parle et de qui on parle, et
            # ecrit l'etiquette de ce message. Ce qu'il rend (la question a poser) n'est PAS encore utilise :
            # c'est pour un tour suivant (decide le 20/10).
            personnes.attribuer(m_recu["n"], m_recu.get("date"), compris)
            rendu_biblio["compris"] = compris
            if compris.get("vital"):                 # le vital : le journal du quotidien, lu par le PROGRAMME
                # seulement ce que la PERSONNE a dit avoir fait ou pas fait, sans ses mails a elle (decision du 20/10)
                rendu_biblio["journal"] = "\n\n".join(quotidien.lire(j, avec_mes_gestes=False) for j in
                                                       comprendre.jours_du_journal(compris, m_recu.get("date")))
        rendu_biblio.update(bibliothecaire(message, bloc, precedents, compris=compris))  # on cherche TOUJOURS
    fil = threading.Thread(target=_fil, daemon=True) if (vrai and str(message or "").strip()) else None
    if fil:
        fil.start()

    # SES OUTILS : les plus proches PAR LE SENS de la phrase entiere, mis dans sa main (sans IA)
    prendre_en_main(proposer_outils(" ".join(precedents[-1:] + [str(message or "")]), cerveau,
                                    int(r["outils_proposes"])))
    contexte = _contexte_du_tour(vrai)
    messages = construire_messages(fen, contexte, image)
    if L._demande_photo_ecran(message):
        try:
            shot = L.outil_regarder_ecran({})
            if isinstance(shot, dict) and shot.get("blocs"):
                messages.append({"role": "assistant", "content": "Je regarde ton ecran."})
                messages.append({"role": "user", "content": shot["blocs"]})
        except Exception:
            pass
    systeme = perso(personnalite() + "\n\n" + MEMOIRE_EN_CLAIR)
    outils = outils_du_tour(cerveau)
    anthropic_ici = (L.fournisseur_de(cerveau) == "anthropic")
    blocs_systeme = [{"type": "text", "text": systeme}]
    if anthropic_ici:
        blocs_systeme[0]["cache_control"] = {"type": "ephemeral", "ttl": "1h"}

    def requete():
        return dict(model=L.modele_api(cerveau), system=blocs_systeme, tools=outils_du_tour(cerveau),
                    messages=list(messages), **L._options_reflexion(cerveau))
    cout = 0.0
    premiere = None
    D["tete"] = "pas de bibliothecaire (message du programme)"
    if fil:
        L._v180_ecrit(etape="je reflechis")
        L._arret_si_fred_a_dit_stop("avant un appel au cerveau")
        try:
            brouillon = L._appel_cerveau(cli, cerveau, requete())
            cout += L.compter_depense(cerveau, getattr(brouillon, "usage", None), quoi="conversation")
        except L.ArretDemandeParFred:
            raise
        except Exception:
            brouillon = None
        L._v180_ecrit(etape="le bibliothecaire regarde dans ta memoire")
        fil.join(float(r["bibliothecaire_plafond_secondes"]))
        st = rendu_biblio.get("stats") or {"panne": "le bibliothecaire n'a pas fini a temps"}
        D["bibliothecaire"] = st
        if rendu_biblio.get("compris"):
            D["compris"] = rendu_biblio["compris"]
        journal_vital = rendu_biblio.get("journal") or ""
        gardees = rendu_biblio.get("fiches") or []
        if brouillon is not None and r.get("relecture_des_regles", True):
            L._v180_ecrit(etape="le bibliothecaire relit ma reponse avec tes regles")
            violees, st_rel = relecture(message, brouillon, deja={f.get("n") for f, _p in gardees})
            D["relecture"] = st_rel
            if violees:
                compter("relectures_regle_rappelee")
                gardees = violees + list(gardees)       # en tete : toujours donnees EN ENTIER
        if gardees or journal_vital:
            bloc_f, n_donnees, car_donnees = bloc_des_fiches(gardees) if gardees else ("", 0, 0)
            if journal_vital:
                bloc_f = journal_vital + ("\n\n" + bloc_f if bloc_f else "")
                D["journal_lu"] = True
            bloc_f = perso(bloc_f)
            messages[-1] = dict(messages[-1])
            if isinstance(messages[-1]["content"], list):
                messages[-1]["content"][-1]["text"] = contexte + "\n\n" + bloc_f + "\n\n" + \
                    messages[-1]["content"][-1]["text"][len(contexte) + 2:]
            else:
                messages[-1]["content"] = contexte + "\n\n" + bloc_f + "\n\n" + messages[-1]["content"][len(contexte) + 2:]
            D.update(tete="jetee : le bibliothecaire a apporte %d fiche(s)%s" % (len(gardees), " + le journal du quotidien" if journal_vital else ""),
                     fiches_donnees=n_donnees, fiches_donnees_car=car_donnees)
            compter("fiches_donnees", n_donnees)
            compter("tetes_jetees")
            L._v180_ecrit(etape="je reponds avec ta memoire")
        else:
            premiere = brouillon
            D["tete"] = "gardee : rien d'utile dans la bibliotheque" if brouillon is not None else "panne de la reponse de tete"
            compter("tetes_gardees")

    # CE QU'ELLE A SOUS LES YEUX (mesure exacte, pour le panneau)
    D["sous_les_yeux"] = {"personnalite_car": len(systeme), "conversation_car": len(bloc),
                          "conversation_messages": len(fen), "contexte_car": len(contexte),
                          "outils": len(outils_du_tour(cerveau)),
                          "outils_car": len(json.dumps(outils_du_tour(cerveau), ensure_ascii=False))}
    actions, reponse = [], None
    while True:
        L._arret_si_fred_a_dit_stop("avant un appel au cerveau")
        if premiere is not None:
            reponse, premiere = premiere, None
        else:
            L._v180_ecrit(etape="je reflechis")
            reponse = L._v180_appel_flux(cli, cerveau, requete())
            cout += L.compter_depense(cerveau, getattr(reponse, "usage", None), quoi="conversation")
        if reponse.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": reponse.content})
            continue
        if reponse.stop_reason != "tool_use":
            break
        messages.append({"role": "assistant", "content": reponse.content})
        resultats = []
        for b in reponse.content:
            if getattr(b, "type", "") != "tool_use":
                continue
            L._arret_si_fred_a_dit_stop("avant l'outil %s" % b.name, reponse, resultats, messages)
            L._v180_ecrit(etape="j'utilise l'outil %s" % b.name)
            try:
                sortie = executer(b.name, b.input, cerveau)
            except L.ArretDemandeParFred:
                L._arret_completer_les_tool_result(reponse, resultats, messages)
                raise
            except Exception as ex:
                sortie = "Erreur pendant %s : %s" % (b.name, ex)
            try:
                L.archiver_outil(b.name, b.input, sortie)
            except Exception:
                pass
            apercu = sortie.get("texte", "(image/document)") if isinstance(sortie, dict) else str(sortie)
            apercu = re.sub(r"\s+", " ", str(apercu)).strip()
            actions.append("%s : %s" % (b.name, apercu[:300]))
            D["actions"] = actions
            journal(b.name, b.input, apercu)
            contenu = sortie["blocs"] if (isinstance(sortie, dict) and sortie.get("blocs")) else (
                sortie.get("texte") if isinstance(sortie, dict) else sortie)
            resultats.append({"type": "tool_result", "tool_use_id": b.id, "content": contenu if contenu else "(vide)"})
        if not resultats:
            break
        messages.append({"role": "user", "content": resultats})

    texte = "".join(getattr(b, "text", "") for b in (reponse.content if reponse else [])
                    if getattr(b, "type", "") == "text").strip()
    texte, faux = L._retirer_appels_en_texte(texte)
    if faux:
        texte += "\n\n(Attention : je voulais utiliser l'outil %s, mais il n'a PAS ete lance.)" % ", ".join(faux)
    if reponse is not None and reponse.stop_reason == "max_tokens":
        texte += "\n\n(Attention : ma reponse a ete coupee, trop longue.)"
    if not texte:
        texte = "Je n'ai pas reussi a te repondre cette fois (reponse vide). Redis-le moi, s'il te plait."
    if CROCHETS.get("apres_tour"):
        try:
            texte = CROCHETS["apres_tour"](texte) or texte
        except Exception:
            pass
    ajouter_message("assistant", texte, actions)
    D.update(secondes=round(time.time() - t0, 1), usd=round(cout, 4), outils_utilises=len(actions))
    compter("usd_conversation", cout)
    L._DERNIER_TOUR.update(usd=round(cout, 6), secondes=round(time.time() - t0, 1), cerveau=cerveau,
                           libelle=L._info_cerveau(cerveau).get("libelle", cerveau))
    ajouter_ligne(F_TRACE, dict(D, date=maintenant(), message=str(message)[:200]))
    L._v180_ecrit(texte, etape="")
    try:
        L.enregistrer_le_pas_de_la_mission(texte_recu, actions)
    except Exception:
        pass
    threading.Thread(target=_apres_le_tour, args=(message, texte, actions, m_recu.get("date")), daemon=True).start()
    return texte


def _apres_le_tour(message, texte, actions, date_message=None):
    """En fond, apres chaque echange, DANS CET ORDRE : elle apprend, l'archiviste range la conversation si elle
    deborde, puis l'archiviste range dans le plan tout ce qui est neuf (et divise ce qui est trop plein)."""
    etapes = [lambda: apprendre(message, texte, actions), ranger_si_besoin]
    if reglages().get("bibliotheque_rangee"):           # eteint tant que les pieces 3 a 6 ne sont pas faites
        etapes.append(lambda: quotidien.noter_le_vital(message, date_message))
        etapes.append(lambda: classement.ranger_le_neuf())
    for etape in etapes:
        try:
            etape()
        except Exception as ex:
            ajouter_ligne(F_TRACE, {"date": maintenant(), "panne": "apres le tour", "detail": str(ex)[:300]})


def journal(nom, entree, apercu):
    try:
        os.makedirs(D_JOURNAL, exist_ok=True)
        ajouter_ligne(os.path.join(D_JOURNAL, aujourdhui() + ".jsonl"),
                      {"heure": time.strftime("%H:%M:%S"), "outil": nom, "entree": entree, "resultat": apercu[:500]})
        compter("outils_utilises")
    except Exception:
        pass


# =====================================================================================
#  LE PANNEAU DES COULISSES (des quantites, mesurees, jamais devinees)
# =====================================================================================
def coulisses():
    r = reglages()
    lignes = []
    D = COULISSES.get("dernier") or {}
    c = compteurs_du_jour()
    if D:
        y = D.get("sous_les_yeux") or {}
        lignes.append("DERNIER MESSAGE (%s, %s) :" % (D.get("quand", "?"), D.get("cerveau", "?")))
        if y:
            total = y.get("personnalite_car", 0) + y.get("conversation_car", 0) + y.get("contexte_car", 0) + \
                D.get("fiches_donnees_car", 0) + y.get("outils_car", 0)
            lignes.append("  Sous ses yeux : %d car. au total = personnalite %d + conversation %d (%d messages) + "
                          "heure/rappels %d + fiches %d (%d fiches entieres) + outils %d (%d outils)"
                          % (total, y.get("personnalite_car", 0), y.get("conversation_car", 0),
                             y.get("conversation_messages", 0), y.get("contexte_car", 0),
                             D.get("fiches_donnees_car", 0), D.get("fiches_donnees", 0), y.get("outils_car", 0),
                             y.get("outils", 0)))
        b = D.get("bibliothecaire") or {}
        if b:
            lignes.append("  Bibliothecaire : %d fiches en tout, %d sorties %s, lues en entier (%d car.), %d gardees, "
                          "%.1f s%s" % (b.get("fiches_en_tout", 0), b.get("candidats", 0), b.get("comment", ""),
                                        b.get("lus_car", 0), b.get("gardes", 0), b.get("secondes", 0),
                                        (" — PANNE : " + b["panne"]) if b.get("panne") else ""))
        lignes.append("  Reponse de tete : %s" % D.get("tete", "?"))
        lignes.append("  Elle a cherche %d fois, ouvert %d fiche(s), utilise %d outil(s) ; %.1f s, %.4f $"
                      % (D.get("recherches", 0), D.get("fiches_ouvertes", 0), D.get("outils_utilises", 0),
                         D.get("secondes", 0), D.get("usd", 0)))
    fen = fenetre()
    rg = lire_json(F_RANGEMENT, {})
    lignes.append("CONVERSATION DU JOUR : %d car. / %d (%d messages) ; dernier rangement : %s"
                  % (sum(taille(m) for m in fen), int(r["fenetre_max_caracteres"]), len(fen), rg.get("le", "jamais")))
    lignes.append("ARCHIVISTE aujourd'hui : %d message(s) ranges, %d souvenir(s) crees%s"
                  % (c.get("messages_ranges", 0), c.get("souvenirs_crees", 0),
                     (", %d panne(s)" % c["rangements_en_panne"]) if c.get("rangements_en_panne") else ""))
    appris = {k[7:]: v for k, v in c.items() if k.startswith("lecons_")}
    lignes.append("APPRENTISSAGE aujourd'hui : %d lecon(s)%s ; %d echange(s) relus"
                  % (sum(appris.values()), (" (" + ", ".join("%s %d" % (nature_en_clair(k, k), v)
                                                            for k, v in appris.items()) + ")") if appris else "",
                     c.get("apprentissages_faits", 0)))
    if COULISSES.get("derniere_lecon"):
        lignes.append("  Derniere lecon : %s" % COULISSES["derniere_lecon"])
    toutes = fiches(toutes=True)
    par = {}
    for f in toutes:
        if f.get("etat", "active") == "active":
            par[f["nature"]] = par.get(f["nature"], 0) + 1
    lignes.append("BIBLIOTHEQUE : %d fiche(s) actives (%s), %d remplacee(s)"
                  % (sum(par.values()), ", ".join("%s %d" % (nature_en_clair(k, k), v) for k, v in sorted(par.items())) or "vide",
                     len([f for f in toutes if f.get("etat", "active") != "active"])))
    lignes.append("AUJOURD'HUI : %d message(s) recu(s), %d tete(s) gardee(s), %d jetee(s), %d recherche(s), "
                  "%d fiche(s) donnees, %d outil(s) utilises, %d trouve(s)"
                  % (c.get("messages_recus", 0), c.get("tetes_gardees", 0), c.get("tetes_jetees", 0),
                     c.get("recherches", 0), c.get("fiches_donnees", 0), c.get("outils_utilises", 0),
                     c.get("outils_trouves", 0)))
    lignes.append("COUT aujourd'hui : conversation %.3f $, bibliothecaire %.3f $, archiviste %.3f $, apprentissage %.3f $"
                  % (c.get("usd_conversation", 0), c.get("usd_bibliothecaire", 0), c.get("usd_archiviste", 0),
                     c.get("usd_apprentissage", 0)))
    lignes.append("MOTEUR DE SENS : %s ; outils en main : %d (%s)"
                  % ("Google OK" if not MOTEUR.panne else "EN PANNE -> recherche par les mots (%s)" % MOTEUR.panne,
                     len(_EN_MAIN), ", ".join(_EN_MAIN[-8:])))
    if plan.etat_du_plan():                             # un refus d'ecrire le plan : jamais en silence
        lignes.append("PLAN DE LA BIBLIOTHEQUE : " + plan.etat_du_plan())
    return lignes
