# -*- coding: utf-8 -*-
"""LE REGISTRE DES PERSONNES -- etape b, decidee le 20/10/2026.

LA REGLE : la memoire ne suppose PERSONNE. Ni un proprietaire, ni l'assistante, ni « deux personnes ». Le registre est
OUVERT : un nombre quelconque de personnes, il grandit a l'usage, et une machine neuve part VIDE.

  - personnes.json (a part de la bibliotheque : une liste d'identites ne se melange pas avec des souvenirs) : chaque
    personne a un numero (p1, p2...), ses appellations (et QUI les emploie : « maman » dit par p2), ses liens, ses
    roles (« proprietaire » est une donnee, pas une structure), et comment elle est entree (dit / deduit / import).
    Rien n'est jamais efface. Les FAITS sur une personne vont dans la bibliotheque, pas ici.
  - qui_parle.jsonl : pour chaque message, QUI PARLE (un numero ou « inconnu »), COMMENT on le sait (dit / deduit /
    deduit (suite) / inconnu) et DE QUI on parle. Une etiquette : le texte du message n'est jamais touche.

C'est l'etape « comprendre » qui DEDUIT (avant la reponse, sans appel de plus). Le PROGRAMME, ici, tient les regles :
  - « deduit » n'est jamais « prouve » : « dit » est une parole, pas une verification ;
  - personne ne se deduit -> « inconnu », on ne devine pas ; deux personnes collent -> une question ;
  - la suite silencieuse (meme personne qu'au message d'avant) est refusee apres un redemarrage, un changement de date
    ou 3 heures de silence. Une signature claire (prenom, « c'est moi », « je suis l'infirmiere ») fait toujours
    re-deduire, meme 30 secondes apres.
"""
import os, json, time, datetime, threading, shutil, unicodedata

F_REGISTRE = ""
F_QUI = ""
F_TRACE = ""
SILENCE_HEURES = 3
_verrou = threading.RLock()
_CACHE = {"reg": None, "mtime": None, "illisible": ""}
DEMARRAGE = {"le": time.strftime("%Y-%m-%d %H:%M")}     # Luciana a demarre a cette heure-la (redemarrage = nouvelle session)


class RegistreProtege(Exception):
    """Le programme refuse d'ecrire : il ecraserait un registre qui existe."""


def poser_le_dossier(d):
    global F_REGISTRE, F_QUI, F_TRACE
    F_REGISTRE = os.path.join(d, "personnes.json")
    F_QUI = os.path.join(d, "qui_parle.jsonl")
    F_TRACE = os.path.join(d, "trace_des_messages.jsonl")
    _CACHE.update(reg=None, mtime=None, illisible="")


def poser_demarrage(le):
    """Pour les essais : l'heure (fictive) a laquelle le programme a demarre."""
    DEMARRAGE["le"] = str(le)[:16]


def _maintenant():
    return time.strftime("%Y-%m-%d %H:%M")


def _dire(phrase):
    try:
        print("REGISTRE : " + phrase)
    except Exception:
        pass
    try:
        with open(F_TRACE, "a", encoding="utf-8") as f:
            f.write(json.dumps({"date": _maintenant(), "panne": "registre", "detail": phrase}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _net(t):
    t = unicodedata.normalize("NFD", " ".join(str(t or "").lower().split()))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").strip(" .,;:!?«»\"'")


# ------------------------------------------------------------------------------ le fichier (jamais perdu)
def _vide():
    return {"version": 1, "personnes": {}}


def _lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        d = json.load(f)
    if not isinstance(d, dict) or not isinstance(d.get("personnes", {}), dict):
        raise ValueError("ce n'est pas un registre")
    return d


def charger():
    with _verrou:
        try:
            m = os.path.getmtime(F_REGISTRE)
        except Exception:
            m = None
        if _CACHE["reg"] is None or m != _CACHE["mtime"]:
            r, illisible = _vide(), ""
            if m is not None:
                try:
                    r["personnes"] = _lire(F_REGISTRE).get("personnes") or {}
                except Exception as ex:
                    illisible = str(ex)[:200]
                    _dire("personnes.json est ABIME (%s) : je n'y ecris plus rien. La derniere bonne version est "
                          "personnes.json.copie (a remettre a sa place, Luciana fermee)." % illisible)
            _CACHE.update(reg=r, mtime=m, illisible=illisible)
        return _CACHE["reg"]


def _sauver(r):
    with _verrou:
        if _CACHE.get("illisible"):
            raise RegistreProtege("personnes.json est abime : rien n'est ecrit")
        if os.path.exists(F_REGISTRE):
            try:
                avant = _lire(F_REGISTRE)
            except Exception as ex:
                _CACHE["illisible"] = str(ex)[:200]
                _dire("personnes.json est ABIME (%s) : rien n'est ecrit, la copie n'est pas touchee." % str(ex)[:200])
                raise RegistreProtege("personnes.json abime : rien n'est ecrit")
            if avant.get("personnes") and not r.get("personnes"):
                _dire("refus : le registre a ecrire est VIDE alors que personnes.json ne l'est pas. Rien n'est ecrit.")
                raise RegistreProtege("registre vide refuse")
            shutil.copy2(F_REGISTRE, F_REGISTRE + ".copie")     # seulement apres une lecture saine
        tmp = F_REGISTRE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1)
        os.replace(tmp, F_REGISTRE)
        try:
            _CACHE["mtime"] = os.path.getmtime(F_REGISTRE)
        except Exception:
            pass
        _CACHE["reg"] = r


# ------------------------------------------------------------------------------ les personnes
def personnes():
    return charger()["personnes"]


def ajouter_personne(appellation, comment="deduit", par="", lien="", message_n=0, date=""):
    """Une personne de plus (jamais deux fois d'office : c'est l'appelant qui a verifie qu'elle est nouvelle).
    comment = comment elle est entree : « dit » (elle s'est nommee), « deduit », « import »."""
    with _verrou:
        r = charger()
        n = 1 + max([int(k[1:]) for k in r["personnes"] if k[1:].isdigit()] or [0])
        pid = "p%d" % n
        r["personnes"][pid] = {
            "appellations": [{"nom": " ".join(str(appellation).split())[:120], "par": par or "", "le": date or _maintenant()}],
            "liens": ([{"texte": str(lien)[:200], "le": date or _maintenant()}] if lien else []),
            "roles": [], "entree": comment, "apparue_le": date or _maintenant(), "apparue_message": int(message_n or 0)}
        _sauver(r)
        return pid


def ajouter_appellation(pid, nom, par=""):
    with _verrou:
        r = charger()
        p = r["personnes"].get(pid)
        nom = " ".join(str(nom or "").split())[:120]
        if not p or not nom:
            return
        if any(_net(a["nom"]) == _net(nom) and a.get("par", "") == (par or "") for a in p["appellations"]):
            return
        p["appellations"].append({"nom": nom, "par": par or "", "le": _maintenant()})
        _sauver(r)


def ajouter_lien(pid, texte):
    with _verrou:
        r = charger()
        p = r["personnes"].get(pid)
        if p and texte and not any(_net(l["texte"]) == _net(texte) for l in p["liens"]):
            p["liens"].append({"texte": str(texte)[:200], "le": _maintenant()})
            _sauver(r)


def poser_role(pid, role):
    """Un role est une DONNEE (ex. « proprietaire ») : il peut changer, l'ancien reste note."""
    with _verrou:
        r = charger()
        p = r["personnes"].get(pid)
        if p and role and not any(x["role"] == role and not x.get("fin") for x in p["roles"]):
            p["roles"].append({"role": str(role), "le": _maintenant()})
            _sauver(r)


ROLE_PROPRIETAIRE = "proprietaire"


def qui_est_le_proprietaire():
    """Le pN qui porte le role « proprietaire », ou « » s'il n'y en a pas.
    « proprietaire » est une DONNEE d'une personne du registre, pas une place fixe du programme."""
    for pid in sorted(personnes(), key=lambda k: int(k[1:]) if k[1:].isdigit() else 0):
        if any(x.get("role") == ROLE_PROPRIETAIRE and not x.get("fin")
               for x in personnes()[pid].get("roles", [])):
            return pid
    return ""


def poser_le_proprietaire(nom, comment="dit (import)", date="", message_n=0):
    """A L'IMPORT : la personne a qui est cette memoire entre au registre (p1 sur une machine neuve).
    Ses propres messages la nomment : « dit », et on dit d'ou ca vient : « (import) ».
    JAMAIS DEUX FOIS : si quelqu'un porte deja le role, on le garde. Si une seule personne porte deja ce
    nom, on lui pose le role (pas de double). Si plusieurs le portent, on ne choisit pas a sa place.
    Rend (pid ou « », ce qui a ete fait)."""
    with _verrou:
        deja = qui_est_le_proprietaire()
        nom = " ".join(str(nom or "").split())[:120]
        if deja:
            if nom and not any(_net(a["nom"]) == _net(nom) for a in personnes()[deja]["appellations"]):
                ajouter_appellation(deja, nom)
                return deja, "role deja en place ; « %s » ajoute a ses appellations" % nom
            return deja, "role deja en place"
        if not nom:
            return "", "aucun nom donne : rien n'est ecrit"
        memes = trouver(nom)
        if len(memes) == 1:
            poser_role(memes[0], ROLE_PROPRIETAIRE)
            return memes[0], "role pose sur %s, deja au registre" % memes[0]
        if len(memes) > 1:
            return "", "%d personnes portent « %s » : je ne choisis pas a ta place" % (len(memes), nom)
        pid = ajouter_personne(nom, comment, message_n=message_n, date=date)
        poser_role(pid, ROLE_PROPRIETAIRE)
        return pid, "personne creee"


def trouver(nom):
    """Les personnes qui ont deja cette appellation (sans accents ni majuscules)."""
    n = _net(nom)
    if not n:
        return []
    return sorted(pid for pid, p in personnes().items() if any(_net(a["nom"]) == n for a in p["appellations"]))


def homonymes(pid):
    """Les AUTRES personnes qui portent un des noms de pid (ses noms a elle, pas « maman » dit par quelqu'un).
    C'est le PROGRAMME qui compte : une seule personne de ce nom -> on prend ; deux ou plus -> on demande, sauf si
    la conversation les distingue."""
    p = personnes().get(pid)
    if not p:
        return []
    noms = {_net(a["nom"]) for a in p["appellations"] if not a.get("par")}
    return sorted(q for q, x in personnes().items() if q != pid
                  and any(_net(a["nom"]) in noms for a in x["appellations"] if not a.get("par")))


def combien_de_ce_nom(nom):
    """COMBIEN de personnes du registre portent ce nom (leur nom a elles, pas « maman » dit par quelqu'un).
    0 = personne ne le porte ; 1 = une seule ; 2 ou plus = on ne choisit pas a sa place, on demande.
    ON NE FUSIONNE JAMAIS : deux personnes du meme prenom restent deux fiches distinctes."""
    return trouver(nom)


def nom_de(pid):
    p = personnes().get(pid)
    return p["appellations"][0]["nom"] if p and p["appellations"] else ""


def en_texte():
    """Le registre en clair, pour l'etape « comprendre » (dix personnes = environ 1 000 caracteres)."""
    lignes = []
    for pid in sorted(personnes(), key=lambda k: int(k[1:]) if k[1:].isdigit() else 0):
        p = personnes()[pid]
        noms = ", ".join("« %s »%s" % (a["nom"], (" (pour %s)" % a["par"]) if a.get("par") else "") for a in p["appellations"])
        t = "%s : %s ; entree : %s, le %s" % (pid, noms, p.get("entree", "?"), str(p.get("apparue_le", ""))[:10])
        if p.get("liens"):
            t += " ; liens : " + " ; ".join(l["texte"] for l in p["liens"])
        roles = [x["role"] for x in p.get("roles", []) if not x.get("fin")]
        if roles:
            t += " ; role : " + ", ".join(roles)
        lignes.append(t)
    return "\n".join(lignes)


# ------------------------------------------------------------------------------ qui parle (les etiquettes)
def attributions():
    out = []
    try:
        with open(F_QUI, encoding="utf-8") as f:
            for ligne in f:
                try:
                    out.append(json.loads(ligne))
                except Exception:
                    pass
    except Exception:
        pass
    return out


def derniere_attribution():
    a = attributions()
    return a[-1] if a else None


def _dt(d):
    try:
        return datetime.datetime.strptime(str(d)[:16], "%Y-%m-%d %H:%M")
    except Exception:
        return None


def nouvelle_session(date_message):
    """(oui/non, raison). Les trois cas : redemarrage, changement de date, 3 heures de silence."""
    avant = derniere_attribution()
    if not avant:
        return True, "premier message"
    d_avant, d_ici = _dt(avant.get("date")), _dt(date_message)
    if d_avant is None or d_ici is None:
        return True, "date illisible"
    if str(avant.get("date"))[:16] < DEMARRAGE["le"] <= str(date_message)[:16]:
        return True, "le programme a redemarre depuis le message d'avant"
    if d_avant.date() != d_ici.date():
        return True, "la date a change depuis le message d'avant"
    if (d_ici - d_avant).total_seconds() > SILENCE_HEURES * 3600:
        return True, "plus de %d heures de silence" % SILENCE_HEURES
    return False, ""


def pour_comprendre(date_message):
    """Ce que l'etape « comprendre » doit savoir sur les personnes, en clair."""
    reg = en_texte() or "(vide : tu ne connais encore personne)"
    neuve, raison = nouvelle_session(date_message)
    avant = derniere_attribution()
    if neuve:
        suite = ("NOUVELLE SESSION (%s) : tu ne peux PAS dire « suite ». Qui parle se voit seulement si ce message "
                 "(ou la conversation juste avant lui) le dit ou le montre." % raison)
    elif not avant or avant.get("parle") in ("", "inconnu", None):
        suite = "AU MESSAGE D'AVANT : qui parlait est INCONNU. Tu ne peux pas dire « suite »."
    else:
        suite = ("AU MESSAGE D'AVANT (le %s) : c'etait %s « %s » (%s). Si rien ne montre un changement, tu peux dire "
                 "« suite »." % (avant.get("date"), avant["parle"], nom_de(avant["parle"]), avant.get("comment")))
    return reg, suite


QUESTION_SECOURS = "Pour être sûre de bien noter : qui m'écrit ?"


def question_de_qui(nom):
    """Quand plusieurs personnes du registre portent le meme nom et que rien ne les distingue : on demande.
    On ne choisit pas a sa place, et on ne fabrique pas une personne de plus."""
    return ("Il y a plusieurs « %s » dans ce que je connais : de laquelle parles-tu ?" % nom) if nom \
        else "De quelle personne parles-tu, exactement ?"


def attribuer(n, date_message, compris, vital=False):
    """LE PROGRAMME TRANCHE, a partir de ce que « comprendre » a deduit. Ecrit l'etiquette du message n et, s'il le
    faut, les personnes nouvelles. Rend {"parle", "comment", "raison", "de_qui", "question_qui", "nouvelles"}."""
    qp = compris.get("qui_parle") if isinstance(compris.get("qui_parle"), dict) else {}
    comment = _net(qp.get("comment")) or "inconnu"
    raison = str(qp.get("raison") or "")[:300]
    question = str(compris.get("question_qui") or "").strip()[:300]
    neuve, pourquoi = nouvelle_session(date_message)
    avant = derniere_attribution()
    parle, comme, nouvelles = "inconnu", "inconnu", []
    numero = str(qp.get("numero") or "").strip().lower()
    nouveau = " ".join(str(qp.get("nouveau") or "").split())
    distingue = " ".join(str(qp.get("distingue") or "").split())[:300]
    if comment == "suite":
        if neuve:
            raison = "suite refusee : %s" % pourquoi
        elif not avant or avant.get("parle") in ("", "inconnu", None):
            raison = "suite refusee : au message d'avant, qui parlait etait inconnu"
        else:
            parle, comme = avant["parle"], "deduit (suite)"
    elif comment in ("dit", "deduit"):
        if numero in personnes():
            autres = homonymes(numero)
            if autres and not distingue:
                # Deux personnes ou plus portent ce nom et rien dans la conversation ne les distingue : on demande.
                raison = ("« %s » : %d personnes portent ce nom (%s) et rien ne les distingue : je demande"
                          % (nom_de(numero), len(autres) + 1, ", ".join(sorted([numero] + autres))))
                question = question or QUESTION_SECOURS
            else:
                parle, comme = numero, comment
                if autres:
                    raison = (raison + " ; " if raison else "") + "distinguee de %s : %s" % (", ".join(autres), distingue)
        elif nouveau:
            deja = trouver(nouveau)
            if len(deja) == 1:
                # Une seule personne porte ce nom au registre : c'est elle (une parole, pas une preuve), pas un double.
                parle, comme = deja[0], comment
                raison = (raison + " ; " if raison else "") + "nom deja au registre : %s, seule personne de ce nom" % deja[0]
            elif deja:
                # Deux personnes ou plus portent ce nom : on ne fabrique pas un double et on ne choisit pas a sa place.
                raison = "« %s » colle a %s : je ne choisis pas, je demande" % (nouveau, ", ".join(deja))
                question = question or QUESTION_SECOURS
            else:
                parle, comme = ajouter_personne(nouveau, comment, message_n=n, date=date_message), comment
                nouvelles.append(parle)
    if parle == "inconnu" and vital and not question:
        question = QUESTION_SECOURS          # un geste vital ne se range pas sur une personne inconnue sans demander
    # ------------------------------------------------------------------ DE QUI ON PARLE
    # Meme comptage des homonymes que pour « qui parle » : le PROGRAMME compte, il ne choisit pas a la place
    # du sens. Une seule personne de ce nom -> c'est elle. DEUX OU PLUS et rien ne les distingue -> on NE
    # FUSIONNE PAS, on ne fabrique pas un double, et on POSE UNE QUESTION. Personne de ce nom -> une personne
    # de plus au registre (deux personnes du meme prenom = deux fiches distinctes, pour toujours).
    de_qui, ambigus = [], []
    for x in compris.get("de_qui") or []:
        if not isinstance(x, dict):
            continue
        num = str(x.get("numero") or "").strip().lower()
        nom = " ".join(str(x.get("nouveau") or "").split())
        appel = " ".join(str(x.get("appellation") or "").split())
        lien = " ".join(str(x.get("lien") or "").split())
        distingue_ici = " ".join(str(x.get("distingue") or "").split())[:300]
        if num in personnes():
            autres = homonymes(num)
            if autres and not distingue_ici:
                ambigus.append("« %s » : %d personnes portent ce nom (%s) et rien ne les distingue : je demande"
                               % (nom_de(num) or num, len(autres) + 1, ", ".join(sorted([num] + autres))))
                question = question or question_de_qui(nom_de(num) or nom)
                continue
            pid = num
            if autres:
                ambigus.append("« %s » distinguee de %s : %s" % (nom_de(num), ", ".join(autres), distingue_ici))
        elif nom:
            deja = combien_de_ce_nom(nom)
            if len(deja) == 1:
                pid = deja[0]                       # une seule personne de ce nom : c'est elle (une parole, pas une preuve)
            elif deja:
                ambigus.append("« %s » colle a %d personnes (%s) : je ne choisis pas, je demande"
                               % (nom, len(deja), ", ".join(deja)))
                question = question or question_de_qui(nom)
                continue
            else:
                pid = ajouter_personne(nom, "deduit", par=parle if parle != "inconnu" else "", message_n=n,
                                       date=date_message)
                nouvelles.append(pid)
        else:
            continue
        if pid == parle:
            continue
        if appel and _net(appel) != _net(nom_de(pid)):
            ajouter_appellation(pid, appel, parle if parle != "inconnu" else "")
        if lien:
            ajouter_lien(pid, "%s de %s" % (lien, parle) if parle != "inconnu"
                         else "%s de la personne (inconnue) qui ecrivait le message n%s" % (lien, n))
        if pid not in de_qui:
            de_qui.append(pid)
    e = {"n": int(n or 0), "date": str(date_message)[:16], "parle": parle, "comment": comme, "raison": raison,
         "de_qui": de_qui, "de_qui_ambigus": ambigus, "question_qui": question, "note_le": _maintenant()}
    with _verrou:
        with open(F_QUI, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return dict(e, nouvelles=nouvelles)
