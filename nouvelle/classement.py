# -*- coding: utf-8 -*-
"""L'ARCHIVISTE QUI RANGE ET DIVISE -- piece 2 de la bibliotheque rangee (decidee le 20/10/2026).

ON FABRIQUE UN FABRICANT, PAS DES CATEGORIES. Ce fichier ne contient AUCUNE categorie : il donne a
l'archiviste des REGLES DE FONCTIONNEMENT (celles d'un cerveau humain qui range sa memoire), et c'est lui qui
cree les categories et sous-categories, par le sens, comme un psychologue.

CE QU'IL FAIT :
  1. RANGER : chaque fiche pas encore rangee recoit son tiroir (categorie > sous-categorie > ...), qu'il choisit
     ou qu'il cree. Le moteur Google lui montre d'abord les tiroirs et les fiches les plus proches par le sens
     : il ne relit jamais toute la bibliotheque, seulement le plan + les fiches neuves.
  2. CE QUI CHANGE : si une fiche neuve rend fausse aujourd'hui une fiche deja rangee (nouveau traitement, nouvelle
     methode, nouvelle adresse...), l'ancienne est marquee « remplacee », jamais effacee. S'il revient a l'ancienne
     facon, la nouvelle passe aux archives et l'ancienne est reliee (elle peut la rouvrir en entier).
  3. LE VITAL : il dit pour chaque fiche si c'est vital, de la vie courante ou de l'amusement (dans le doute : vital).
  4. DIVISER : quand un tiroir atteint le seuil (40 par defaut, avant 50), il le divise lui-meme en sous-tiroirs,
     avec le critere de sens qui convient a CE sujet, en pensant aux questions qu'on posera.

Le PROGRAMME, lui : ne range jamais rien seul, ne coupe jamais une fiche, n'efface rien, tient les comptes et les
dates, et garde le travail sur le disque (plan.json). Un seul rangement a la fois, meme entre deux programmes.
"""
import os, json, time, threading
import plan as P

_verrou = threading.Lock()
_RATES = {}                      # numero de fiche -> nombre d'essais rates (cette session) : pas de boucle payante
_DIVISIONS_RATEES = {}           # tiroir -> nombre de fiches quand la division a rate : on ne reessaie qu'apres +10
LOT_FICHES = 20                  # fiches neuves par appel a l'archiviste
LOT_CARACTERES = 60000           # texte des fiches neuves par appel (une fiche plus grosse passe seule, EN ENTIER)
CATALOGUE_ENTIER_JUSQU_A = 60000  # au-dela, il recoit les tiroirs proches + les grandes categories
DIVISION_EN_ENTIER_JUSQU_A = 150000
SANS_AUTO_AU_DELA = 200          # une grosse reserve ancienne (un import) se range par le .bat, pas en douce
LOTS_PAR_TOUR = 3


def oublier_la_session():
    """Nouvelle bibliotheque (autre dossier) : les essais rates d'avant ne la concernent pas."""
    _RATES.clear()
    _DIVISIONS_RATEES.clear()


def C():
    import coeur
    return coeur


# ------------------------------------------------------------------------------ un seul rangement a la fois
def _f_verrou():
    return os.path.join(C().DOSSIER, "rangement_du_plan_en_cours.lock")


def _prendre():
    f = _f_verrou()
    for _ in range(2):
        try:
            fd = os.open(f, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, ("%s %s" % (os.getpid(), time.time())).encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(f) > 1800:      # verrou oublie par un programme arrete
                    os.remove(f)
                    continue
            except Exception:
                pass
            return False
        except Exception:
            return False
    return False


def _rendre():
    try:
        os.remove(_f_verrou())
    except Exception:
        pass


# ------------------------------------------------------------------------------ les regles de fonctionnement
REGLES = (
    "TES REGLES DE FONCTIONNEMENT (celles d'une personne qui range sa propre memoire) :\n"
    "1. Tu ranges chaque fiche par son SUJET DE SENS : de quoi parle vraiment ce moment, comme un psychologue, "
    "jamais d'apres les mots qu'elle contient.\n"
    "2. LES GRANDES CATEGORIES : chaque grand domaine de la vie de {proprietaire} a la sienne (par exemple sa vie privee, son "
    "travail, sa sante, ses projets... c'est toi qui les nommes). Si une fiche releve d'un AUTRE DOMAINE de la vie "
    "qu'aucune grande categorie existante, tu CREES cette grande categorie tout de suite, avec une phrase de sens "
    "(jamais le travail range dans la vie privee, ni l'inverse). Jamais de fourre-tout (« Divers », « Autres »).\n"
    "   LES SOUS-TIROIRS : tu ranges dans le tiroir QUI EXISTE DEJA le plus precis, avec son chemin EXACT, la ou on "
    "la chercherait dans 10 ans. Tu ne crees PAS de sous-tiroir pour mieux ranger : si tu ecris un sous-tiroir qui "
    "n'existe pas, le programme range la fiche dans le tiroir juste au-dessus ; les sous-tiroirs naissent a la "
    "division, quand un tiroir approche du plafond.\n"
    "3. LE TRI DEVIENT FIN AVEC LE TEMPS, PAS AVANT : un tiroir de quelques fiches n'a pas besoin "
    "d'etre decoupe ; on decoupe seulement quand le plafond approche, et alors en pensant aux sujets qui vont "
    "ENSEMBLE (sa fille + l'ecole + ses cheveux).\n"
    "4. CE QUI CHANGE : si une fiche neuve rend FAUSSE AUJOURD'HUI une fiche deja rangee (nouveau traitement, "
    "nouvelle methode, nouvelle adresse, nouveau prix...), donne le numero de l'ancienne dans \"remplace\". Si "
    "la fiche neuve dit qu'on REVIENT a une ancienne facon de faire, donne le numero de l'ancienne dans "
    "\"reprend\" (c'est souvent une fiche ARCHIVEE : regarde les fiches proches marquees ARCHIVEE ; on peut "
    "donner a la fois \"remplace\" (la facon qu'on abandonne) et \"reprend\" (l'ancienne qu'on retrouve)). Une fiche qui ne fait que completer ou raconter : ni l'un ni l'autre. Rien n'est jamais efface.\n"
    "5. LE VITAL : pour chaque fiche, \"vital\" (sante, medicaments, soins, securite, rendez-vous importants, "
    "argent important, ce qui ne doit jamais etre oublie), \"courant\" (la vie de tous les jours, le travail) ou "
    "\"loisir\" (l'amusement). Dans le doute : vital.\n"
    "6. Une fiche qui parle VRAIMENT de deux sujets peut avoir d'autres tiroirs EXISTANTS dans \"aussi\".\n"
    "7. Tu ne coupes, ne resumes et ne reecris jamais une fiche : tu ranges seulement.\n"
    "8. Tu nommes les categories et ecris leurs phrases de sens dans la langue des fiches, quelle "
    "qu'elle soit ; les mots \"vital\", \"courant\", \"loisir\" du JSON restent ces mots-la.\n")


def _chemin_txt(tid):
    return " > ".join(P.chemin(tid))


def _trouver(noms):
    """Le tiroir qui a exactement ce chemin (sans le creer), ou None."""
    tid = None
    for nom in noms or []:
        suivant = None
        for e in P.enfants(tid):
            if P._pareil(P.charger()["tiroirs"][e]["nom"], nom):
                suivant = e
                break
        if suivant is None:
            return None
        tid = suivant
    return tid


def _tiroir_pour_ranger(noms, sens=""):
    """LA REGLE TENUE PAR LE PROGRAMME : « le tri devient fin avec le temps, pas avant ».
    L'archiviste choisit librement le chemin. On descend dans les tiroirs QUI EXISTENT ; si le niveau suivant n'existe
    pas, la fiche reste dans le tiroir existant juste au-dessus (il sera divise quand il approchera du plafond, en
    voyant TOUTES ses fiches ensemble). Un sujet vraiment nouveau cree sa grande categorie, et rien d'autre."""
    tid = None
    for nom in noms:
        suivant = None
        for e in P.enfants(tid):
            if P._pareil(P.charger()["tiroirs"][e]["nom"], nom):
                suivant = e
                break
        if suivant is not None:
            tid = suivant
            continue
        if tid is None:
            return P.nouveau_tiroir(nom, None, sens)
        return tid
    return tid


def _noms(x):
    if isinstance(x, str):
        x = [y for y in x.split(">")]
    return [str(y).strip() for y in (x or []) if str(y).strip()]


# ------------------------------------------------------------------------------ le moteur Google aide l'archiviste
def _tiroirs_proches(lot, combien=8):
    """Pour chaque fiche du lot, les tiroirs les plus proches par le sens (ou {} si le moteur est en panne)."""
    m = C().MOTEUR
    tiroirs = list(P.charger()["tiroirs"].keys())
    if not tiroirs:
        return {}
    textes = ["Tiroir : %s -- %s" % (_chemin_txt(t), P.charger()["tiroirs"][t].get("sens", "")) for t in tiroirs]
    vt = m.vecteurs(textes)
    vq = m.vecteurs([(f.get("sujet", "") + "\n" + f.get("texte", "")) for f in lot], "RETRIEVAL_QUERY")
    if any(v is None for v in vt) or any(v is None for v in vq):
        return {}
    out = {}
    for f, q in zip(lot, vq):
        sc = [sum(a * b for a, b in zip(q, v)) for v in vt]
        ordre = sorted(range(len(tiroirs)), key=lambda i: -sc[i])
        out[int(f["n"])] = [tiroirs[i] for i in ordre[:combien]]
    return out


def _fiches_proches(f, deja, combien=5):
    """Les fiches deja rangees les plus proches par le sens (pour voir si la neuve remplace une ancienne)."""
    co = C()
    try:
        co.MOTEUR.indexer(deja)
        sc = co.MOTEUR.scores(f.get("sujet", "") + "\n" + f.get("texte", ""))
    except Exception:
        sc = None
    if not sc:
        return []
    ordre = sorted((x for x in deja if int(x["n"]) != int(f["n"])), key=lambda x: -sc.get(x["n"], -9))
    return ordre[:combien]


# ------------------------------------------------------------------------------ 1. RANGER
def _lots(neuves):
    lots, lot, t = [], [], 0
    for f in neuves:
        n = len(f.get("texte", ""))
        if lot and (len(lot) >= LOT_FICHES or t + n > LOT_CARACTERES):
            lots.append(lot)
            lot, t = [], 0
        lot.append(f)
        t += n
    if lot:
        lots.append(lot)
    return lots


def _consigne_ranger(lot, toutes):
    co = C()
    proches = _tiroirs_proches(lot)
    cat = P.catalogue(toutes, avec_ids=False)
    if len(cat) > CATALOGUE_ENTIER_JUSQU_A:
        vus = set()
        for tids in proches.values():
            vus.update(tids)
        lignes = sorted({_chemin_txt(t) for t in P.enfants(None)} | {_chemin_txt(t) for t in vus})
        cat = ("(Le plan est trop grand pour etre donne en entier : voici les grandes categories et les tiroirs "
               "les plus proches de ces fiches.)\n" + "\n".join(lignes))
    # TOUTES les fiches deja rangees, ARCHIVEES COMPRISES : pour « on revient a l'ancienne facon », l'ancienne est
    # justement archivee (essai reel du 20/10 : sans elle, l'archiviste ne pouvait pas la reprendre).
    deja = [f for f in co.fiches(toutes=True) if P.tiroir_de(f["n"])]
    blocs = []
    for f in lot:
        b = "=== FICHE n%d ===\n%s" % (f["n"], co.fiche_en_entier(f))
        if proches.get(int(f["n"])):
            b += "\n(Tiroirs les plus proches par le sens : %s)" % " | ".join(_chemin_txt(t) for t in proches[int(f["n"])])
        voisines = _fiches_proches(f, deja) if deja else []
        if voisines:
            b += "\n(Fiches deja rangees les plus proches par le sens : %s)" % " | ".join(
                co.titre(v) + ((" [ARCHIVEE : remplacee par la n%s]" % v.get("remplacee_par"))
                               if v.get("etat", "active") != "active" else "")
                + ((" : " + v["texte"]) if (v.get("nature") != "souvenir" and len(v.get("texte", "")) <= 1500) else "")
                for v in voisines)
        blocs.append(b)
    return (
        "TU ES L'ARCHIVISTE DE CETTE BIBLIOTHEQUE. Tu ranges des fiches neuves dans son plan.\n\n" + REGLES +
        "\nLE PLAN ACTUEL (chaque tiroir : son chemin, son nombre de fiches, ses dates, sa phrase de sens) :\n" +
        (cat or "(vide : c'est toi qui crees les premieres categories. Exemples de grandes categories possibles, "
                "pas obligatoires : Professionnel, Projets, Vie privee, Regles pour l'assistante, Ordinateur et outils.)") +
        "\n\nLES FICHES A RANGER (en entier) :\n\n" + "\n\n".join(blocs) + "\n\n"
        "Reponds UNIQUEMENT en JSON strict, une entree par fiche :\n"
        "{\"fiches\": [{\"n\": <numero>, \"chemin\": [\"Grande categorie\", \"Sous-categorie\", \"...\"], "
        "\"sens_si_nouveau\": \"<si la PREMIERE categorie de ton chemin est neuve : ce qu'elle contiendra>\", \"aussi\": [[\"...\"]], "
        "\"vital\": \"vital|courant|loisir\", \"remplace\": 0, \"reprend\": 0}]}")


def _appliquer_rangement(lot, d):
    co = C()
    stats = {"rangees": 0, "remplacees": 0, "reprises": 0}
    par_n = {int(f["n"]): f for f in lot}
    toutes = {int(f["n"]): f for f in co.fiches(toutes=True)}
    for x in (d.get("fiches") or []) if isinstance(d, dict) else []:
        try:
            n = int(str(x.get("n")).lstrip("nN"))
        except Exception:
            continue
        noms = _noms(x.get("chemin"))
        if n not in par_n or not noms:
            continue
        try:
            tid = _tiroir_pour_ranger(noms, str(x.get("sens_si_nouveau") or ""))
        except Exception:
            continue
        P.ranger(n, tid)
        stats["rangees"] += 1
        if x.get("vital"):
            P.poser_le_vital(n, str(x.get("vital")).strip().lower())
        aussi = [t for t in (_trouver(_noms(a)) for a in (x.get("aussi") or []) if a) if t]
        if aussi:
            P.poser_aussi(n, aussi)
        for genre in ("remplace", "reprend"):
            try:
                k = int(str(x.get(genre) or 0).lstrip("nN") or 0)
            except Exception:
                k = 0
            if not k or k == n or k not in toutes:
                continue
            if genre == "remplace":
                co.marquer_remplacee(k, n)
                P.poser_lien(n, "remplace", k)
                stats["remplacees"] += 1
            else:
                j = toutes[k].get("remplacee_par")
                if j and int(j) in toutes and toutes[int(j)].get("etat", "active") == "active" and int(j) != n:
                    co.marquer_remplacee(int(j), n)            # la nouvelle facon passe aux archives
                P.poser_lien(n, "reprend", k)
                stats["reprises"] += 1
    for n in par_n:
        if not P.tiroir_de(n):
            _RATES[n] = _RATES.get(n, 0) + 1
    return stats


# ------------------------------------------------------------------------------ 4. DIVISER
def _consigne_diviser(tid, toutes):
    co = C()
    p = P.charger()
    nums = set(int(n) for n, t in p["rangement"].items() if t == tid)
    dedans = [f for f in toutes if int(f["n"]) in nums]
    total = sum(len(co.fiche_en_entier(f)) for f in dedans)
    if total <= DIVISION_EN_ENTIER_JUSQU_A:
        corps = "\n\n".join(co.fiche_en_entier(f) for f in dedans)
    else:
        corps = ("(Trop de texte pour tout donner d'un coup : voici le titre, la date et l'heure de chaque fiche ; "
                 "les titres ont ete ecrits pour dire de quoi parle la fiche.)\n" + "\n".join(co.titre(f) for f in dedans))
    t = p["tiroirs"][tid]
    return dedans, (
        "TU ES L'ARCHIVISTE DE CETTE BIBLIOTHEQUE. Un tiroir est devenu trop gros : tu le DIVISES.\n\n" + REGLES +
        "\nLE TIROIR A DIVISER : %s -- %d fiches rangees directement dedans -- sens : %s\n"
        "SES SOUS-TIROIRS DEJA EXISTANTS : %s\n\n"
        "SES FICHES :\n%s\n\n"
        "TON TRAVAIL : repartis ces fiches dans QUELQUES GRANDS SOUS-TIROIRS de ce tiroir (en general 2 a 5), par "
        "le sens : juste ce qu'il faut pour que chacun reste nettement sous %d fiches, et pas plus. Chaque sous-tiroir "
        "regroupe PLUSIEURS fiches (jamais une seule) ; le tri plus fin viendra plus tard, quand un de ces "
        "sous-tiroirs se remplira a son tour (le tri devient fin avec le temps). Choisis le critere qui convient a CE sujet (une periode, un lieu, une personne, un "
        "theme, les bons et les mauvais moments...) : pense aux questions qu'on posera un jour, et a ce qu'on "
        "demandera ENSEMBLE. Tu peux reprendre un sous-tiroir existant (meme nom). Chaque fiche va dans un "
        "sous-tiroir ; une fiche vraiment generale peut rester ou elle est (ne la cite pas).\n"
        "Reponds UNIQUEMENT en JSON strict : {\"sous_tiroirs\": [{\"nom\": \"...\", \"sens\": \"...\", "
        "\"fiches\": [<numeros>]}]}"
        % (_chemin_txt(tid), len(dedans), t.get("sens") or "(pas encore de phrase)",
           ", ".join(p["tiroirs"][e]["nom"] for e in P.enfants(tid)) or "(aucun)", corps,
           int(C().reglages()["diviser_a_partir_de"])))


def diviser(tid):
    co = C()
    toutes = co.fiches(toutes=True)
    dedans, consigne = _consigne_diviser(tid, toutes)
    nums = {int(f["n"]) for f in dedans}
    brut, panne = co.appel_simple(co.reglages()["cerveau_archiviste"], "Tu es l'archiviste de cette memoire. JSON strict.",
                                  consigne, "archiviste_division", reflechir=True, max_tokens=8000)
    d = co.json_dans(brut)
    sous = (d or {}).get("sous_tiroirs") if isinstance(d, dict) else None
    existants = [P.charger()["tiroirs"][e]["nom"] for e in P.enfants(tid)]
    pleins = [s for s in (sous or []) if isinstance(s, dict) and s.get("fiches")] if isinstance(sous, list) else []
    vers_existant = any(any(P._pareil(s.get("nom"), e) for e in existants) for s in pleins)
    if len(pleins) < 2 and not vers_existant:
        return 0, panne or "division illisible ou en un seul morceau"
    bouge = 0
    for s in sous:
        if not isinstance(s, dict) or not str(s.get("nom") or "").strip():
            continue
        a_ranger = []
        for x in s.get("fiches") or []:
            try:
                n = int(str(x).lstrip("nN"))
            except Exception:
                continue
            if n in nums:
                a_ranger.append(n)
        neuf = not any(P._pareil(s["nom"], e) for e in existants)
        if a_ranger and (len(a_ranger) >= 2 or not neuf):     # jamais un tiroir neuf pour une seule fiche
            st = P.nouveau_tiroir(s["nom"], tid, str(s.get("sens") or ""))
            P.ranger(a_ranger, st)
            bouge += len(a_ranger)
            nums -= set(a_ranger)
    return bouge, ""


# ------------------------------------------------------------------------------ LE TOUR DE L'ARCHIVISTE
def a_ranger(tout=False):
    co = C()
    p = P.charger()
    neuves = [f for f in P.non_rangees(co.fiches()) if _RATES.get(int(f["n"]), 0) < 2]
    if not tout:
        neuves = [f for f in neuves if int(f["n"]) > int(p.get("neuf_a_partir_de") or 0)]
    return neuves


def ranger_le_neuf(tout=False, lots_max=LOTS_PAR_TOUR, dire=None):
    """Le tour de l'archiviste : il range les fiches neuves (par lots), puis divise les tiroirs trop pleins.
    tout=True : aussi la reserve ancienne (le premier rangement, lance par le .bat). Rend les chiffres du tour."""
    co = C()
    stats = {"rangees": 0, "remplacees": 0, "reprises": 0, "lots": 0, "divisions": 0, "pannes": [], "reste": 0}
    if not _verrou.acquire(blocking=False):
        stats["pannes"].append("un rangement tourne deja")
        return stats
    try:
        if not _prendre():
            stats["pannes"].append("un autre programme range deja le plan")
            return stats
        try:
            p = P.charger()
            if not tout and not p["tiroirs"] and not p.get("neuf_a_partir_de"):
                reserve = P.non_rangees(co.fiches())
                if len(reserve) > SANS_AUTO_AU_DELA:
                    # Une grosse reserve ancienne (ex. un import) : elle ne part pas en douce, a chaque message.
                    P.poser_neuf_a_partir_de(max(int(f["n"]) for f in reserve))
            neuves = a_ranger(tout)
            for i, lot in enumerate(_lots(neuves)):
                if lots_max and i >= lots_max:
                    break
                brut, panne = co.appel_simple(co.reglages()["cerveau_archiviste"],
                                              "Tu es l'archiviste de cette memoire. JSON strict.",
                                              _consigne_ranger(lot, co.fiches(toutes=True)), "archiviste_plan",
                                              reflechir=False, max_tokens=8000)
                d = co.json_dans(brut)
                if d is None:
                    stats["pannes"].append(panne or "reponse illisible")
                    for f in lot:
                        _RATES[int(f["n"])] = _RATES.get(int(f["n"]), 0) + 1
                    continue
                s = _appliquer_rangement(lot, d)
                for k in ("rangees", "remplacees", "reprises"):
                    stats[k] += s[k]
                stats["lots"] += 1
                if dire:
                    dire("lot %d : %d fiche(s) rangee(s)" % (i + 1, s["rangees"]))
            seuil = int(co.reglages()["diviser_a_partir_de"])
            for _passe in range(3):
                pleins = P.a_diviser(co.fiches(toutes=True), seuil)
                if not pleins:
                    break
                c = P.comptes(co.fiches(toutes=True))
                pleins = [t for t in pleins if c[t]["direct"] >= _DIVISIONS_RATEES.get(t, 0) + 10]
                if not pleins:
                    break
                for tid in pleins:
                    bouge, panne = diviser(tid)
                    if not bouge:
                        _DIVISIONS_RATEES[tid] = c[tid]["direct"]
                    if bouge:
                        stats["divisions"] += 1
                        if dire:
                            dire("tiroir divise : %s (%d fiche(s) deplacee(s))" % (_chemin_txt(tid), bouge))
                    else:
                        stats["pannes"].append("division de %s : %s" % (_chemin_txt(tid), panne))
            stats["reste"] = len(a_ranger(tout))
        finally:
            _rendre()
        co.ecrire_lisible()
        if stats["rangees"] or stats["divisions"] or stats["pannes"]:
            co.ajouter_ligne(co.F_TRACE, {"date": co.maintenant(), "classement": stats})
            co.compter("fiches_classees", stats["rangees"])
            co.compter("tiroirs_divises", stats["divisions"])
        return stats
    except Exception as ex:
        stats["pannes"].append(str(ex)[:200])
        return stats
    finally:
        _verrou.release()
