# -*- coding: utf-8 -*-
"""LE PLAN DE LA BIBLIOTHEQUE (le catalogue) -- piece 1 de la bibliotheque rangee (decidee avec Fred le 20/10/2026).

CE QUE C'EST : la memoire de l'archiviste, ecrite sur le disque. Les catégories et sous-catégories (ici : des
« tiroirs »), la phrase de sens de chacune, et dans quel tiroir est rangee chaque fiche.

CE QUE CE FICHIER NE FAIT PAS : il ne decide de RIEN. Il ne cree aucun tiroir tout seul, il ne range rien tout
seul. C'est l'archiviste (piece 2) qui decide, par le sens. Ici, seulement ce que le PROGRAMME tient :
  - le catalogue (plan.json), ecrit sans jamais rien perdre ;
  - les comptes (combien de fiches dans chaque tiroir) et les dates (du ... au ...), calcules, jamais devines ;
  - les tiroirs qui approchent la limite (pour que l'archiviste les divise) ;
  - le plan lisible au Bloc-notes : « MON PLAN (catalogue).txt ».

Les regles de Fred tenues ici : aucune categorie fixee d'avance ; les textes des fiches ne sont JAMAIS reecrits
(seules les etiquettes bougent : ranger une fiche ne touche pas a bibliotheque.jsonl) ; rien n'est efface.
"""
import os, json, time, threading, unicodedata, shutil

F_PLAN = ""
F_PLAN_LISIBLE = ""
F_TRACE = ""
_verrou = threading.RLock()
_CACHE = {"plan": None, "mtime": None, "illisible": "", "refus": ""}
REPARER = ("POUR REPARER : ferme Luciana, puis, dans le dossier de Luciana, lance : python nouvelle\\reparer_le_plan.py "
           "(il demande OUI avant de toucher quoi que ce soit). Il remet la derniere bonne copie (plan.json.copie) ; "
           "le fichier abime est garde a cote, rien n'est efface.")


class PlanProtege(Exception):
    """Le programme refuse d'ecrire : il ecraserait un plan qui existe (rien n'est perdu, et c'est dit)."""


def poser_le_dossier(d):
    global F_PLAN, F_PLAN_LISIBLE, F_TRACE
    F_PLAN = os.path.join(d, "plan.json")
    F_PLAN_LISIBLE = os.path.join(d, "MON PLAN (catalogue).txt")
    F_TRACE = os.path.join(d, "trace_des_messages.jsonl")
    _CACHE["plan"] = None
    _CACHE["mtime"] = None
    _CACHE["illisible"] = ""
    _CACHE["refus"] = ""


def _dire(phrase):
    """Un refus n'est jamais silencieux : la fenetre noire, la trace, et le panneau d'etat (_CACHE["refus"]),
    toujours avec ce qu'il faut faire pour reparer."""
    phrase = phrase + " " + REPARER
    _CACHE["refus"] = time.strftime("%d/%m %H:%M ") + phrase
    try:
        print("PLAN : " + phrase)
    except Exception:
        pass
    try:
        with open(F_TRACE, "a", encoding="utf-8") as f:
            f.write(json.dumps({"date": time.strftime("%Y-%m-%d %H:%M"), "panne": "plan",
                                "detail": phrase}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _a_du_contenu(d):
    return isinstance(d, dict) and bool(d.get("tiroirs") or d.get("rangement"))


def _lire_un_plan(chemin):
    """Le plan d'un fichier, ou une exception s'il est illisible ou si ce n'est pas un plan."""
    with open(chemin, encoding="utf-8") as f:
        d = json.load(f)
    if not isinstance(d, dict) or not isinstance(d.get("tiroirs", {}), dict) \
            or not isinstance(d.get("rangement", {}), dict):
        raise ValueError("ce n'est pas un plan")
    return d


def _vide():
    return {"version": 1, "tiroirs": {}, "rangement": {}, "vital": {}, "aussi": {}, "liens": {},
            "neuf_a_partir_de": 0, "maj": ""}


def _mtime():
    try:
        return os.path.getmtime(F_PLAN)
    except Exception:
        return None


def charger():
    """Le plan. Relu tout seul si le fichier a change sur le disque (un autre programme a pu l'ecrire)."""
    with _verrou:
        m = _mtime()
        if _CACHE["plan"] is None or m != _CACHE["mtime"]:
            p = _vide()
            illisible = ""
            if m is not None:                       # pas de fichier = plan neuf, vide : c'est normal
                try:
                    d = _lire_un_plan(F_PLAN)
                    for k in ("tiroirs", "rangement", "vital", "aussi", "liens"):
                        if isinstance(d.get(k), dict):
                            p[k] = d[k]
                    p["maj"] = str(d.get("maj") or "")
                    p["neuf_a_partir_de"] = int(d.get("neuf_a_partir_de") or 0)
                except Exception as ex:
                    # ABIME : on ne fait PAS comme s'il etait vide. Il est garde tel quel, et plus rien n'y est
                    # ecrit tant qu'il n'est pas repare (ex. remettre « plan.json.copie » a sa place).
                    illisible = str(ex)[:200]
                    _dire("plan.json est ABIME (%s) : je n'y ecris plus rien, pour ne pas perdre le rangement."
                          % illisible)
            _CACHE["plan"], _CACHE["mtime"], _CACHE["illisible"] = p, m, illisible
        return _CACHE["plan"]


def sauver(p):
    with _verrou:
        if _CACHE.get("illisible"):
            raise PlanProtege("plan.json est illisible : rien n'est ecrit (%s)" % _CACHE["illisible"])
        if os.path.exists(F_PLAN):
            try:
                sur_le_disque = _lire_un_plan(F_PLAN)
            except Exception as ex:
                # ABIME : on ne le copie PAS (la bonne copie d'avant reste telle quelle), on n'ecrit rien.
                _CACHE["illisible"] = str(ex)[:200]
                _dire("plan.json est ABIME (%s) : rien n'est ecrit, la copie de secours n'est pas touchee."
                      % str(ex)[:200])
                raise PlanProtege("plan.json abime : rien n'est ecrit")
            if _a_du_contenu(sur_le_disque) and not _a_du_contenu(p):
                _dire("refus : le plan a ecrire est VIDE alors que plan.json ne l'est pas. Rien n'est ecrit, "
                      "le plan sur le disque est garde tel quel.")
                raise PlanProtege("plan vide refuse : il ecraserait le plan existant")
            # La version d'avant, gardee avant chaque ecriture. Seulement ici : le fichier vient d'etre LU SANS
            # ERREUR et c'est bien un plan. Un plan abime ne remplace jamais une copie saine.
            shutil.copy2(F_PLAN, F_PLAN + ".copie")
        p["maj"] = time.strftime("%Y-%m-%d %H:%M")
        tmp = F_PLAN + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=1)
        os.replace(tmp, F_PLAN)
        _CACHE["plan"], _CACHE["mtime"] = p, _mtime()


# ------------------------------------------------------------------------------ les tiroirs
def _nom_propre(nom):
    return " ".join(str(nom or "").split())[:120]


def _pareil(a, b):
    """Deux noms de tiroir sont le meme s'ils ne different que par les accents, les majuscules ou les espaces."""
    def net(t):
        t = unicodedata.normalize("NFD", _nom_propre(t).lower())
        return "".join(c for c in t if unicodedata.category(c) != "Mn")
    return net(a) == net(b)


def nouveau_tiroir(nom, parent=None, sens=""):
    """Cree un tiroir (une categorie, ou une sous-categorie si parent est donne). S'il existe deja un tiroir de ce
    nom au meme endroit, rend celui-la (jamais deux fois le meme). Rend son identifiant (ex. « t7 »)."""
    nom = _nom_propre(nom)
    if not nom:
        raise ValueError("un tiroir a besoin d'un nom")
    with _verrou:
        p = charger()
        if parent and parent not in p["tiroirs"]:
            raise ValueError("le tiroir parent %s n'existe pas" % parent)
        for tid, t in p["tiroirs"].items():
            if t.get("parent") == parent and _pareil(t["nom"], nom):
                if sens and not t.get("sens"):
                    t["sens"] = str(sens)
                    sauver(p)
                return tid
        n = 1 + max([int(k[1:]) for k in p["tiroirs"] if k[1:].isdigit()] or [0])
        tid = "t%d" % n
        p["tiroirs"][tid] = {"nom": nom, "parent": parent, "sens": str(sens or ""),
                             "cree_le": time.strftime("%Y-%m-%d %H:%M")}
        sauver(p)
        return tid


def tiroir_par_chemin(noms, sens=""):
    """[« Vie privee », « Ma fille », « Ecole »] -> l'identifiant du dernier tiroir. Les niveaux qui manquent sont
    crees (c'est l'archiviste qui a decide ce chemin) ; la phrase de sens va au dernier niveau s'il est neuf."""
    noms = [_nom_propre(x) for x in (noms or []) if _nom_propre(x)]
    if not noms:
        raise ValueError("chemin vide")
    parent = None
    for i, nom in enumerate(noms):
        parent = nouveau_tiroir(nom, parent, sens if i == len(noms) - 1 else "")
    return parent


def changer_le_sens(tid, sens):
    with _verrou:
        p = charger()
        if tid in p["tiroirs"]:
            p["tiroirs"][tid]["sens"] = str(sens or "")
            sauver(p)


def ranger(numeros, tid):
    """Range une ou plusieurs fiches dans un tiroir (ou les y deplace). Le texte des fiches n'est pas touche."""
    if not isinstance(numeros, (list, tuple, set)):
        numeros = [numeros]
    with _verrou:
        p = charger()
        if _CACHE.get("illisible"):
            raise PlanProtege("plan.json est abime : rien n'est range (%s)" % _CACHE["illisible"])
        if tid not in p["tiroirs"]:
            raise ValueError("le tiroir %s n'existe pas" % tid)
        for n in numeros:
            p["rangement"][str(int(n))] = tid
        sauver(p)


def etat_du_plan():
    """Pour le panneau : le dernier refus d'ecrire (avec quoi faire), ou « »."""
    charger()
    return _CACHE.get("refus", "")


def reparer_depuis_la_copie():
    """LA SORTIE : remet plan.json.copie a la place d'un plan.json abime. Rien n'est efface : le fichier abime
    est garde a cote (plan.json.abime-AAAA-MM-JJ_HHMM). Rend (reussi, phrase en clair)."""
    with _verrou:
        try:
            _lire_un_plan(F_PLAN)
            return False, "plan.json n'est pas abime : rien a reparer, rien n'a ete touche."
        except FileNotFoundError:
            pass
        except Exception:
            pass
        copie = F_PLAN + ".copie"
        try:
            d = _lire_un_plan(copie)
        except FileNotFoundError:
            return False, ("Il n'y a pas de copie de secours (plan.json.copie). Rien n'a ete touche. Les fiches, elles, "
                           "sont intactes : le « 4 - ... RANGER SA BIBLIOTHEQUE DANS LE PLAN.bat » peut refaire le "
                           "rangement depuis zero.")
        except Exception as ex:
            return False, ("La copie de secours est abimee elle aussi (%s). Rien n'a ete touche. Les fiches sont "
                           "intactes : le .bat 4 peut refaire le rangement depuis zero." % str(ex)[:200])
        if os.path.exists(F_PLAN):
            garde = F_PLAN + ".abime-" + time.strftime("%Y-%m-%d_%H%M")
            os.replace(F_PLAN, garde)
        else:
            garde = ""
        shutil.copy2(copie, F_PLAN)
        _CACHE["plan"], _CACHE["mtime"], _CACHE["illisible"], _CACHE["refus"] = None, None, "", ""
        return True, ("Plan repare depuis la copie du %s : %d tiroir(s), %d fiche(s) rangee(s).%s Les fiches rangees "
                      "apres cette copie redeviennent « pas encore rangees » (le .bat 4 les range)."
                      % (d.get("maj") or "?", len(d.get("tiroirs") or {}), len(d.get("rangement") or {}),
                         (" Le fichier abime est garde : %s." % os.path.basename(garde)) if garde else ""))


def tiroir_de(n):
    return charger()["rangement"].get(str(int(n)))


def chemin(tid):
    """[« Vie privee », « Ma fille », « Ecole »] : le chemin d'un tiroir, de la grande categorie jusqu'a lui."""
    p = charger()
    out, vus = [], set()
    while tid and tid in p["tiroirs"] and tid not in vus:
        vus.add(tid)
        out.insert(0, p["tiroirs"][tid]["nom"])
        tid = p["tiroirs"][tid].get("parent")
    return out


def chemin_de_la_fiche(n):
    tid = tiroir_de(n)
    return chemin(tid) if tid else []


def enfants(tid):
    p = charger()
    return sorted([k for k, t in p["tiroirs"].items() if t.get("parent") == tid], key=lambda k: p["tiroirs"][k]["nom"].lower())


def descendants(tid):
    out, pile = [], [tid]
    while pile:
        x = pile.pop()
        for e in enfants(x):
            if e not in out:
                out.append(e)
                pile.append(e)
    return out


def fiches_du_tiroir(tid, profond=True):
    """Les numeros des fiches rangees dans ce tiroir (et, si profond, dans tous ses sous-tiroirs)."""
    p = charger()
    dedans = {tid} | (set(descendants(tid)) if profond else set())
    return sorted(int(n) for n, t in p["rangement"].items() if t in dedans)


def poser_aussi(n, tids):
    """Une fiche qui parle VRAIMENT de deux sujets : ses autres tiroirs (jugement de l'archiviste)."""
    with _verrou:
        p = charger()
        tids = [t for t in tids if t in p["tiroirs"] and t != p["rangement"].get(str(int(n)))]
        if tids:
            p["aussi"][str(int(n))] = sorted(set(tids))
            sauver(p)


def aussi_de(n):
    return charger()["aussi"].get(str(int(n)), [])


def poser_lien(n, genre, vers):
    """genre : « remplace » (n rend fausse aujourd'hui la fiche « vers ») ou « reprend » (n revient a l'ancienne
    facon de faire ecrite dans « vers »). Le texte des fiches n'est pas touche."""
    with _verrou:
        p = charger()
        p["liens"].setdefault(str(int(n)), {})[genre] = int(vers)
        sauver(p)


def liens_de(n):
    return charger()["liens"].get(str(int(n)), {})


def poser_neuf_a_partir_de(n):
    with _verrou:
        p = charger()
        p["neuf_a_partir_de"] = int(n)
        sauver(p)


# ------------------------------------------------------------------------------ le vital (piece 3)
NIVEAUX = ("vital", "courant", "loisir")


def poser_le_vital(n, niveau):
    niveau = niveau if niveau in NIVEAUX else "vital"          # dans le doute : vital (decision de Fred)
    with _verrou:
        p = charger()
        p["vital"][str(int(n))] = niveau
        sauver(p)


def vital_de(n):
    return charger()["vital"].get(str(int(n)), "")


# ------------------------------------------------------------------------------ ce que le programme calcule
def _jour(date):
    d = str(date or "").replace("T", " ")
    return d[:10] if len(d) >= 10 else ""


def comptes(liste_fiches):
    """Pour chaque tiroir : combien de fiches DIRECTEMENT dedans, combien en tout (sous-tiroirs compris), et les
    dates du ... au ... Calcule a partir des fiches, jamais garde de travers."""
    p = charger()
    par_n = {int(f["n"]): f for f in liste_fiches}
    direct = {tid: [] for tid in p["tiroirs"]}
    for n, tid in p["rangement"].items():
        if tid in direct and int(n) in par_n:
            direct[tid].append(par_n[int(n)])
    out = {}
    for tid in p["tiroirs"]:
        tout = list(direct[tid])
        for d in descendants(tid):
            tout += direct.get(d, [])
        jours = sorted(j for j in (_jour(f.get("date")) for f in tout) if j)
        out[tid] = {"direct": len(direct[tid]), "total": len(tout),
                    "du": jours[0] if jours else "", "au": jours[-1] if jours else ""}
    return out


def a_diviser(liste_fiches, seuil):
    """Les tiroirs qui ont atteint le seuil (fiches rangees directement dedans) : l'archiviste doit les diviser."""
    c = comptes(liste_fiches)
    return sorted([tid for tid, x in c.items() if x["direct"] >= int(seuil)], key=lambda t: -c[t]["direct"])


def non_rangees(liste_fiches):
    """Les fiches qui n'ont encore aucun tiroir (l'archiviste les rangera)."""
    r = charger()["rangement"]
    return [f for f in liste_fiches if str(int(f["n"])) not in r]


def _date_fr(j):
    return "%s/%s/%s" % (j[8:10], j[5:7], j[0:4]) if len(j) == 10 else "?"


def catalogue(liste_fiches, avec_ids=True):
    """LE PLAN EN TEXTE, tel que l'archiviste, le moteur et le bibliothecaire le lisent : chaque tiroir sur une
    ligne, en retrait sous son parent, avec sa phrase de sens, son nombre de fiches et ses dates."""
    p = charger()
    c = comptes(liste_fiches)
    lignes = []

    def ecrire(tid, prof):
        t = p["tiroirs"][tid]
        x = c.get(tid, {"direct": 0, "total": 0, "du": "", "au": ""})
        if not x["du"]:
            dates = ""
        elif x["du"] == x["au"]:
            dates = " (le %s)" % _date_fr(x["du"])
        else:
            dates = " (du %s au %s)" % (_date_fr(x["du"]), _date_fr(x["au"]))
        nb = ("%d fiche(s)" % x["total"]) + ((", dont %d rangee(s) ici" % x["direct"]) if (enfants(tid) and x["direct"]) else "")
        lignes.append("%s%s%s -- %s%s%s" % ("    " * prof, ("[%s] " % tid) if avec_ids else "", t["nom"], nb, dates,
                                            (" -- " + t["sens"]) if t.get("sens") else ""))
        for e in enfants(tid):
            ecrire(e, prof + 1)

    for tid in enfants(None):
        ecrire(tid, 0)
    return "\n".join(lignes)


def ecrire_le_plan_lisible(liste_fiches, seuil=40):
    """« MON PLAN (catalogue).txt » : le plan, lisible au Bloc-notes par Fred."""
    try:
        reste = len(non_rangees(liste_fiches))
        pleins = a_diviser(liste_fiches, seuil)
        p = charger()
        texte = ["MON PLAN : LE CATALOGUE DE MA BIBLIOTHEQUE (ecrit par le programme, mis a jour a chaque rangement).",
                 "Les categories sont creees par l'archiviste, par le sens. Aucune n'est fixee d'avance.",
                 "Mis a jour le %s. %d tiroir(s). %d fiche(s) pas encore rangee(s)." % (p.get("maj") or "?",
                                                                                       len(p["tiroirs"]), reste),
                 ""]
        texte.append(catalogue(liste_fiches, avec_ids=False) or "(aucun tiroir pour l'instant)")
        if pleins:
            texte += ["", "A DIVISER (%d fiches ou plus rangees directement dedans) : %s"
                      % (seuil, ", ".join(" > ".join(chemin(t)) for t in pleins))]
        with open(F_PLAN_LISIBLE, "w", encoding="utf-8") as f:
            f.write("\n".join(texte) + "\n")
    except Exception:
        pass
