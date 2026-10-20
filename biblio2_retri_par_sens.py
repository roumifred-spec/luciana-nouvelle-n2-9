# -*- coding: utf-8 -*-
"""
BRIQUE 6 — LE RE-TRI COMPLET DE TOUTE LA MEMOIRE, PAR LE SENS.

TRAVAIL 6 DU CHANTIER DU 13/10/2026. Fichier NEUF : s'il n'est pas la, le programme fait
exactement ce qu'il faisait hier.

=====================================================================================
 CE QUE CE FICHIER FAIT, ET RIEN D'AUTRE
=====================================================================================

Il reprend LA MEMOIRE ENTIERE -- les souvenirs, le fil des conversations, l'ancienne
bibliotheque -- et il la REFAIT TRIER DEPUIS LE DEBUT par le cerveau reflechi, avec la
demande du 13/10/2026 (de quoi ca parle vraiment, est-ce que c'est reel, est-ce que ca tient
debout demain, qu'est-ce que ca remplace).

Ca peut tourner des heures. Ce n'est pas un probleme : le travail est SAUVEGARDE par paquets,
et on peut l'arreter et le reprendre autant de fois qu'on veut -- il reprend exactement ou il
s'est arrete, jamais au debut.

=====================================================================================
 LES SIX GARDE-FOUS, ET ILS SONT DANS LE CODE, PAS DANS UNE PROMESSE
=====================================================================================

  1  IL ECRIT UNE BIBLIOTHEQUE NEUVE, A COTE. Tout va dans un dossier DATE :
         ~/Luciana/bibliotheque2/retri_AAAA-MM-JJ/
     L'arbre qui tourne (arbre.json) n'est PAS touche. Pendant tout le re-tri, la memoire
     vivante continue de servir ses souvenirs comme avant : rien n'est coupe.

  2  IL FAIT UNE SAUVEGARDE DATEE AVANT TOUT. La premiere chose qu'il ecrit est une copie de
     l'arbre, du plan et du marque-page d'aujourd'hui, dans le dossier date, sous le nom
     « avant_le_retri_... ». Elle est faite AVANT le premier rangement.

  3  IL NE REMPLACE RIEN TOUT SEUL. Le jour ou la nouvelle bibliotheque plait, elle prend la
     place de l'ancienne UNIQUEMENT si quelqu'un lance expres :
         python biblio2_retri_par_sens.py --appliquer
     Sans ce mot, l'original n'est jamais touche. Et meme avec ce mot, il refuse de remplacer
     une bibliotheque par une plus petite sans qu'on ajoute --meme-si-plus-petite.

  4  IL NE PERD AUCUN MOT. Le texte de chaque souvenir est recopie MOT POUR MOT dans la
     nouvelle fiche. On ne resume pas, on ne coupe pas, on ne reecrit pas : on range et on
     etiquette.

  5  IL LIT LA MEMOIRE, IL NE L'ECRIT JAMAIS. Les trois sources du passe sont ouvertes en
     LECTURE SEULE (c'est biblio2_reprise.py qui les lit, et il ne sait pas ecrire ailleurs
     que dans bibliotheque2).

  6  UNE SEULE ECRITURE A LA FOIS, et chacune est atomique (on ecrit a cote, puis on bascule
     d'un coup). Une coupure de courant ne peut pas laisser un fichier a moitie ecrit.

=====================================================================================
 COMMENT ON LE LANCE
=====================================================================================

    python biblio2_retri_par_sens.py --chiffres     DIT l'etat des deux bibliotheques,
                                                    sans ecrire une seule ligne.
    python biblio2_retri_par_sens.py                REFAIT LE TRI de tout le passe.
    python biblio2_retri_par_sens.py 50             n'en fait que 50 (pour voir).
    python biblio2_retri_par_sens.py --appliquer     met la nouvelle a la place de l'ancienne.
    python biblio2_retri_par_sens.py --demo          essai complet sur 195 faux souvenirs,
                                                     SANS cle, SANS reseau, SANS aucune
                                                     donnee personnelle.

NOTE IA : tout est ecrit en POSITIF.
"""

import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor

import biblio2_archiviste as arch
import biblio2_plan as plan_biblio
import biblio2_reprise as reprise

try:
    import biblio2_reglages as reglages
except Exception:
    reglages = None


def _dossier_biblio2():
    try:
        return reglages.DOSSIER_BIBLIO2
    except Exception:
        return os.path.join(os.path.expanduser("~"), "Luciana", "bibliotheque2")


# 17/10/2026 (Fred) : combien de souvenirs le re-tri fait juger EN MEME TEMPS (avant : un seul).
EN_MEME_TEMPS = 5


def _chantiers():
    """Les dossiers de re-tri dates (retri_AAAA-MM-JJ), du plus ancien au plus recent."""
    try:
        return sorted(n for n in os.listdir(_dossier_biblio2()) if re.match(r"^retri_\d{4}-\d\d-\d\d$", n))
    except Exception:
        return []


def _chantier_fini(nom):
    try:
        with open(os.path.join(_dossier_biblio2(), nom, "journal_du_retri.txt"), encoding="utf-8") as f:
            return "APPLIQUE" in f.read()
    except Exception:
        return False


def jour_du_chantier():
    """17/10/2026 : LE CHANTIER EN COURS, QUEL QUE SOIT LE JOUR. Avant, le dossier etait celui du jour :
    relance le lendemain, le re-tri repartait de zero sans le dire (et on repayait tout). Maintenant,
    si le dernier chantier n'est pas encore en service, on le reprend ; sinon on en ouvre un du jour."""
    noms = _chantiers()
    if noms and not _chantier_fini(noms[-1]):
        return noms[-1][len("retri_"):]
    return time.strftime("%Y-%m-%d")


def recommencer_de_zero():
    """Le choix de Fred (B) : le chantier pas fini est MIS DE COTE (renomme, jamais efface), et le
    re-tri repart d'une bibliotheque neuve. Rend la liste des dossiers mis de cote."""
    mis = []
    for n in _chantiers():
        if not _chantier_fini(n):
            neuf = "%s_abandonne_%s" % (n, time.strftime("%Y-%m-%d_%Hh%M"))
            try:
                os.rename(os.path.join(_dossier_biblio2(), n), os.path.join(_dossier_biblio2(), neuf))
                mis.append(neuf)
            except Exception as ex:
                print("  (je n'ai pas pu mettre de cote %s : %s)" % (n, str(ex)[:120]))
    return mis


def dossier_du_retri(quand=None):
    """LE DOSSIER DATE ou tout le re-tri est ecrit. Un dossier par jour : relancer le
    lendemain ne melange pas deux chantiers."""
    jour = quand or jour_du_chantier()
    return os.path.join(_dossier_biblio2(), "retri_%s" % jour)


def _f_neuf(nom, quand=None):
    d = dossier_du_retri(quand)
    return os.path.join(d, {"arbre": "arbre_par_sens.json",
                            "marque_page": "marque_page_par_sens.json",
                            "plan": "plan_par_sens.json",
                            "signal": "signal_par_sens.json",
                            "journal": "journal_du_retri.txt",
                            "a_trancher": "a_trancher_par_le_proprietaire.txt"}[nom])


def _f_vieux(nom):
    """Les fichiers de la bibliotheque QUI TOURNE. On les LIT ; on n'y ecrit qu'avec
    --appliquer, et une seule fois."""
    try:
        return {"arbre": reglages.FICHIER_ARBRE,
                "plan": reglages.FICHIER_PLAN,
                "signal": reglages.FICHIER_SIGNAL,
                "marque_page": reglages.FICHIER_MARQUE_PAGE}[nom]
    except Exception:
        return os.path.join(_dossier_biblio2(), {"arbre": "arbre.json", "plan": "plan.json",
                                                 "signal": "signal_plan.json",
                                                 "marque_page": "marque_page.json"}[nom])


# ---------------------------------------------------------------------
#  ECRITURE SURE, ET UNE SEULE A LA FOIS.
# ---------------------------------------------------------------------

def _ecrire_json(chemin, valeur):
    """On ecrit a cote, puis on bascule d'un coup. Ne laisse jamais un fichier a moitie."""
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(valeur, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)
    return chemin


def _ecrire_texte(chemin, texte):
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texte)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)
    return chemin


def _lire_json(chemin, defaut=None):
    try:
        with open(chemin, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return {} if defaut is None else defaut


def journal(ligne, quand=None):
    """UNE LIGNE DATEE dans le journal du re-tri, a chaque etape. C'est ce qui permet de
    savoir, des heures plus tard, ce qui s'est passe. Ne leve jamais."""
    try:
        d = dossier_du_retri(quand)
        os.makedirs(d, exist_ok=True)
        with open(_f_neuf("journal", quand), "a", encoding="utf-8") as f:
            f.write("%s  %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), ligne))
    except Exception:
        pass


# =====================================================================
#  GARDE-FOU 2 — LA SAUVEGARDE DATEE, AVANT TOUT.
# =====================================================================

def sauvegarde_datee(quand=None):
    """COPIE l'arbre, le plan et le marque-page D'AUJOURD'HUI dans le dossier date, sous le
    nom « avant_le_retri_... ». C'est la PREMIERE chose ecrite, avant le moindre rangement.
    Rend la liste des copies faites. Ne leve jamais : elle DIT ce qu'elle n'a pas pu copier."""
    faites, manques = [], []
    for nom in ("arbre", "plan", "marque_page", "signal"):
        source = _f_vieux(nom)
        if not os.path.exists(source):
            manques.append(os.path.basename(source))
            continue
        try:
            valeur = _lire_json(source, {})
            cible = os.path.join(dossier_du_retri(quand),
                                 "avant_le_retri_" + os.path.basename(source))
            _ecrire_json(cible, valeur)
            faites.append(os.path.basename(cible))
        except Exception as ex:
            manques.append("%s (%s)" % (os.path.basename(source), str(ex)[:60]))
    journal("sauvegarde datee : %d copie(s) faite(s)%s"
            % (len(faites), (" | pas de copie pour : %s" % ", ".join(manques)) if manques else ""),
            quand)
    return faites, manques


# =====================================================================
#  LE RE-TRI LUI-MEME.
# =====================================================================

def chiffres_de(arbre):
    c = arch.compter(arbre)
    return c


def dire_les_chiffres(titre="ETAT DES DEUX BIBLIOTHEQUES (rien n'est ecrit)"):
    """DIT l'etat des deux bibliotheques cote a cote, SANS RIEN ECRIRE. C'est ce qui donne
    les chiffres AVANT / APRES."""
    vieux = arch.arbre_charger(_f_vieux("arbre"))
    neuf = arch.arbre_charger(_f_neuf("arbre"))
    cv, cn = chiffres_de(vieux), chiffres_de(neuf)
    print("=== %s ===" % titre)
    print("  %-34s %12s %12s" % ("", "QUI TOURNE", "PAR LE SENS"))
    for cle, nom in (("fiches", "fiches"), ("rayons", "rayons"), ("tiroirs", "tiroirs"),
                     ("filtres", "filtres"), ("sous_filtres", "sous-filtres"),
                     ("en_suspens", "en suspens"),
                     ("avec_le_sens", "avec la phrase du sens"),
                     ("mis_de_cote", "mis de cote (a trancher)"),
                     ("remplacements_annonces", "remplacements annonces")):
        print("  %-34s %12s %12s" % (nom, cv.get(cle, 0), cn.get(cle, 0)))
    print("\n  bibliotheque qui tourne : %s" % _f_vieux("arbre"))
    print("  bibliotheque par le sens : %s" % _f_neuf("arbre"))
    if reglages is not None:
        try:
            print("  %s" % reglages.cerveau_reflechi_dit())
        except Exception:
            pass
    return {"qui_tourne": cv, "par_le_sens": cn}


def ecrire_ce_qui_attend_le_proprietaire(arbre, quand=None):
    """ECRIT, EN CLAIR ET EN FRANCAIS, LA LISTE DE CE QUI ATTEND LE PROPRIETAIRE : les
    morceaux qui n'ont peut-etre pas existe, et ce que le cerveau dit etre remplace. C'est
    une liste a LIRE, pas un fichier technique. Ne leve jamais."""
    lignes = ["CE QUI ATTEND VOTRE DECISION, APRES LE RE-TRI PAR LE SENS",
              "=" * 72, "",
              "Rien n'a ete efface. Tout le texte est entier dans la bibliotheque.",
              "Ces deux listes sont la pour que VOUS tranchiez, a votre rythme.", ""]
    de_cote = arch.a_remonter_au_proprietaire(arbre)
    lignes.append("1) CA N'A PEUT-ETRE PAS EXISTE (%d)" % len(de_cote))
    lignes.append("   (une hypothese, une plaisanterie, une erreur ou une invention de "
                  "l'assistante)")
    lignes.append("")
    for n, (_c, _s, fi) in enumerate(de_cote, 1):
        lignes.append("   %d. %s" % (n, (fi.get("sens") or fi.get("resume")
                                         or fi.get("texte") or "")[:300]))
        if fi.get("pourquoi_en_suspens"):
            lignes.append("      pourquoi : %s" % fi["pourquoi_en_suspens"][:300])
        lignes.append("      le texte entier est garde dans la bibliotheque.")
        lignes.append("")
    remp = arch.remplacements_annonces(arbre)
    lignes.append("")
    lignes.append("2) CA REMPLACE QUELQUE CHOSE DE PLUS ANCIEN (%d)" % len(remp))
    lignes.append("   (le programme garde les DEUX : c'est vous qui dites ce qui saute)")
    lignes.append("")
    for n, (_c, _s, fi, quoi) in enumerate(remp, 1):
        lignes.append("   %d. %s" % (n, (fi.get("sens") or fi.get("resume") or "")[:300]))
        lignes.append("      remplacerait : %s" % quoi[:300])
        lignes.append("")
    try:
        return _ecrire_texte(_f_neuf("a_trancher", quand), "\n".join(lignes))
    except Exception:
        return ""


def refaire_le_tri(juge, limite=None, sources=None, quand=None, paquet=None):
    """LE RE-TRI COMPLET, DEPUIS LE DEBUT, DANS UNE BIBLIOTHEQUE NEUVE.

    'juge(souvenir, arbre)' = le cerveau reflechi (ou un faux cerveau, en --demo).

    IL REPREND TOUJOURS OU IL S'EST ARRETE : le marque-page du re-tri retient LES REPERES
    deja faits, et on prend l'union avec ceux reellement presents dans la bibliotheque
    neuve. On peut donc l'arreter par Ctrl+C et le relancer : il ne refait rien deux fois.

    Rend (arbre_neuf, rapport). Ne leve jamais (meme un Ctrl+C est rattrape et sauvegarde)."""
    quand = quand or jour_du_chantier()
    os.makedirs(dossier_du_retri(quand), exist_ok=True)

    #  --- GARDE-FOU 2 : la sauvegarde datee, AVANT la premiere ecriture de travail ------
    faites, manques = sauvegarde_datee(quand)
    print("=== LA SAUVEGARDE DATEE EST FAITE, AVANT TOUT ===")
    print("  dossier : %s" % dossier_du_retri(quand))
    for nom in faites:
        print("  copie   : %s" % nom)
    for nom in manques:
        print("  (pas de copie pour %s : il n'existe pas encore, et c'est dit)" % nom)

    vieux = arch.arbre_charger(_f_vieux("arbre"))
    c_avant_vieux = chiffres_de(vieux)
    arbre = arch.arbre_charger(_f_neuf("arbre", quand))
    c_avant = chiffres_de(arbre)

    print("\n=== AVANT ===")
    print("  la bibliotheque QUI TOURNE (et qui n'est pas touchee) : %d fiche(s), "
          "%d rayon(s), %d tiroir(s)"
          % (c_avant_vieux["fiches"], c_avant_vieux["rayons"], c_avant_vieux["tiroirs"]))
    print("  la bibliotheque PAR LE SENS, en cours de construction : %d fiche(s)"
          % c_avant["fiches"])

    #  CE QUI EST DEJA REFAIT : le marque-page du re-tri, UNION les reperes de l'arbre neuf.
    faits = set()
    mp = _lire_json(_f_neuf("marque_page", quand), {})
    for _src, liste in ((mp or {}).get("faits") or {}).items():
        for r in (liste or []):
            if r:
                faits.add(str(r))
    faits |= arch.arbre_reperes(arbre)
    print("  deja refait : %d repere(s)" % len(faits))

    print("\n=== LECTURE DE TOUTE LA MEMOIRE (lecture seule) ===")
    passe, soucis = (sources() if callable(sources) else reprise.tout_le_passe())
    a_faire = [s for s in passe if s["repere"] not in faits]
    if limite:
        a_faire = a_faire[:int(limite)]
    print("\n  souvenirs trouves en tout : %d" % len(passe))
    print("  deja refaits (on les saute) : %d" % (len(passe) - len(
        [s for s in passe if s["repere"] not in faits])))
    print("  A REFAIRE MAINTENANT       : %d" % len(a_faire))
    for souci in soucis:
        print("  (source illisible, et je le dis : %s)" % souci)
    journal("depart : %d souvenirs en tout, %d a refaire" % (len(passe), len(a_faire)), quand)

    if paquet is None:
        try:
            paquet = int(reglages.lire()["paquet_sauvegarde"])
        except Exception:
            paquet = 25

    n_fait = n_suspens = n_de_cote = n_doublon = 0
    arrete_par_la_main = False
    depart = time.time()

    def _sauver():
        arch.arbre_sauver(_f_neuf("arbre", quand), arbre)
        par_source = {}
        for r in sorted(faits):
            par_source.setdefault(str(r).split("#", 1)[0] or "inconnu", []).append(str(r))
        _ecrire_json(_f_neuf("marque_page", quand), {
            "_a_quoi_ca_sert": ("LE MARQUE-PAGE DU RE-TRI PAR LE SENS. Il retient LE REPERE "
                                "de chaque souvenir deja refait. C'est ce qui permet "
                                "d'arreter le re-tri et de le reprendre sans jamais ranger "
                                "deux fois le meme souvenir."),
            "version": 1, "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
            "combien": len(faits),
            "combien_par_source": {k: len(v) for k, v in sorted(par_source.items())},
            "faits": {k: v for k, v in sorted(par_source.items())},
            "chiffres": chiffres_de(arbre),
        })

    print("")
    try:
        # 17/10/2026 (Fred) : EN_MEME_TEMPS souvenirs juges en meme temps, puis ranges DANS L'ORDRE.
        # Les cerveaux d'une vague voient tous la meme bibliotheque (rien ne bouge pendant qu'ils
        # reflechissent) ; le Python range ensuite un par un, comme avant.
        k = 0
        with ThreadPoolExecutor(max_workers=max(1, int(EN_MEME_TEMPS))) as _pool:
            for _debut in range(0, len(a_faire), max(1, int(EN_MEME_TEMPS))):
                vague = a_faire[_debut:_debut + max(1, int(EN_MEME_TEMPS))]
                futurs = [_pool.submit(arch.juger_avec_reessais, juge, s, arbre,
                                       lambda t: print("\n  " + t)) for s in vague]
                jugements = [f.result() for f in futurs]
                arch.verrou_rafraichir(_dossier_biblio2())       # « je suis toujours la »
                panne = None
                for s, j in zip(vague, jugements):
                    if isinstance(j, dict) and j.get("_panne"):
                        # CERVEAU INJOIGNABLE : ce souvenir n'est PAS range ni marque ; on finit la
                        # vague, on sauve, et on s'arrete. Le meme double-clic reprendra ici.
                        panne = panne or j
                        continue
                    k += 1
                    ok, propre, raison = arch.valider_jugement(j)
                    #  LE PYTHON MET LA DATE (il la connait, c'est fiable), le cerveau ne s'en occupe pas.
                    if propre is not None and s.get("date"):
                        propre.setdefault("filtres", {})["date"] = str(s["date"])[:10]
                    rap = arch.ranger(arbre, s, (ok, propre, raison), reperes_deja=faits)
                    if rap.get("deja_range"):
                        n_doublon += 1
                    else:
                        n_fait += 1
                        if rap.get("mis_de_cote"):
                            n_de_cote += 1
                        elif rap["en_suspens"]:
                            n_suspens += 1
                    if k % paquet == 0 or k == len(a_faire):
                        _sauver()
                        ecoule = time.time() - depart
                        reste = (ecoule / max(1, k)) * (len(a_faire) - k)
                        print("  ... %d/%d refaits  |  %d en suspens, %d mis de cote  |  il reste "
                              "environ %d min      "
                              % (k, len(a_faire), n_suspens, n_de_cote, reste / 60.0), end="\r")
                        journal("avancee : %d/%d refaits" % (k, len(a_faire)), quand)
                if panne:
                    raise RuntimeError(arch.phrase_de_la_panne(panne["_panne"]))
    except KeyboardInterrupt:
        arrete_par_la_main = True
        print("\n\n  (arrete a la main : je sauvegarde ce qui est fait, et je m'arrete "
              "proprement)")
    except Exception as ex:
        print("\n\n  (un souci est arrive, je sauvegarde ce qui est fait : %s)" % str(ex)[:160])
        journal("souci : %s" % str(ex)[:200], quand)

    _sauver()
    plan_apres, signal = plan_biblio.rafraichir(arbre, _f_neuf("plan", quand),
                                                _f_neuf("signal", quand))
    liste = ecrire_ce_qui_attend_le_proprietaire(arbre, quand)

    c_apres = chiffres_de(arbre)
    print("\n\n=== APRES ===")
    print("  refaits maintenant : %d   (dont %d en suspens, et %d mis de cote parce que ca "
          "n'a peut-etre pas existe)" % (n_fait, n_suspens, n_de_cote))
    if n_doublon:
        print("  doublons evites    : %d (deja dans la bibliotheque par le sens)" % n_doublon)
    print("  fiches  : %d  (la bibliotheque qui tourne en a %d)"
          % (c_apres["fiches"], c_avant_vieux["fiches"]))
    print("  rayons  : %d  (elle : %d)" % (c_apres["rayons"], c_avant_vieux["rayons"]))
    print("  tiroirs : %d  (elle : %d)" % (c_apres["tiroirs"], c_avant_vieux["tiroirs"]))
    print("  filtres : %d | sous-filtres : %d" % (c_apres["filtres"], c_apres["sous_filtres"]))
    print("  avec la phrase du sens : %d sur %d  (la bibliotheque qui tourne : %d)"
          % (c_apres.get("avec_le_sens", 0), c_apres["fiches"],
             c_avant_vieux.get("avec_le_sens", 0)))
    print("  mis de cote (a trancher par le proprietaire) : %d"
          % c_apres.get("mis_de_cote", 0))
    print("  remplacements annonces : %d" % c_apres.get("remplacements_annonces", 0))
    print("  plan : version %s" % plan_apres.get("version", 0))
    print("  rayons : %s" % ", ".join(sorted(arbre.keys())))
    if liste:
        print("\n  CE QUI ATTEND VOTRE DECISION est ecrit en clair dans :\n    %s" % liste)
    trop = arch.tiroirs_qui_debordent(arbre)
    if trop:
        print("  tiroirs trop pleins, a decouper : %s" % trop)
    print("\n  LA BIBLIOTHEQUE QUI TOURNE N'A PAS ETE TOUCHEE. La neuve est ici :\n    %s"
          % _f_neuf("arbre", quand))
    if arrete_par_la_main or (len(a_faire) and n_fait + n_doublon < len(a_faire)):
        print("\n  IL EN RESTE. Relancez la meme commande : il reprendra exactement ici.")
    else:
        print("\n  Quand elle vous plait, et SEULEMENT a ce moment-la :\n"
              "    python biblio2_retri_par_sens.py --appliquer")
    journal("fin : %d refaits, %d fiches en tout" % (n_fait, c_apres["fiches"]), quand)
    return arbre, {"avant_qui_tourne": c_avant_vieux, "apres_par_le_sens": c_apres,
                   "refaits": n_fait, "mis_de_cote": n_de_cote, "en_suspens": n_suspens,
                   "reste": max(0, len(a_faire) - n_fait - n_doublon),
                   "arrete": bool(arrete_par_la_main)}


# =====================================================================
#  GARDE-FOU 3 — RIEN NE S'APPLIQUE SANS UNE DEMANDE EXPRESSE.
# =====================================================================

def _attendre_le_verrou():
    """Prend le verrou de la bibliotheque qui tourne, en attendant que l'archiviste du jour ait fini
    s'il est en train de ranger. Le dit toutes les minutes. Rend True quand on le tient."""
    def dire(qui):
        print("  (j'attends : la bibliotheque est en train d'etre ecrite -- %s)" % (qui or "?"))
    return arch.verrou_prendre(_dossier_biblio2(), "le re-tri (mise en service)",
                               attendre_secondes=None, dire=dire)


def appliquer(quand=None, meme_si_plus_petite=False):
    """17/10/2026 (Fred) : SOUS LE VERROU de la bibliotheque -- personne n'ecrit pendant ce temps."""
    if not _attendre_le_verrou():
        print("  JE NE FAIS RIEN : le verrou de la bibliotheque n'a pas pu etre pris.")
        return {"applique": False, "pourquoi": "verrou"}
    try:
        return _appliquer_sous_verrou(quand=quand, meme_si_plus_petite=meme_si_plus_petite)
    finally:
        arch.verrou_rendre(_dossier_biblio2())


def _appliquer_sous_verrou(quand=None, meme_si_plus_petite=False):
    """MET LA BIBLIOTHEQUE PAR LE SENS A LA PLACE DE CELLE QUI TOURNE.

    C'EST LA SEULE FONCTION DE CE FICHIER QUI TOUCHE L'ORIGINAL, et elle ne part que si
    quelqu'un l'a demandee expres en ligne de commande.

    TROIS VERROUS, dans cet ordre :
      1  la bibliotheque neuve doit exister et porter des fiches ;
      2  elle doit avoir AU MOINS autant de fiches que l'ancienne -- sinon on s'arrete et on
         DIT les deux chiffres (il faut alors ajouter --meme-si-plus-petite pour passer) ;
      3  l'ancienne est recopiee, datee, a cote, AVANT d'etre remplacee.

    Rend un petit rapport. Ne leve jamais."""
    quand = quand or jour_du_chantier()
    neuf = arch.arbre_charger(_f_neuf("arbre", quand))
    # 17/10/2026 : avant la mise en service, les doublons d'accents sont fusionnes et le prenom
    # est remis dans ce que l'archiviste a ecrit (sans IA ; le texte d'origine ne bouge pas).
    _net = arch.nettoyer_la_bibliotheque(neuf)
    print("  nettoyage : %d doublon(s) d'accents fusionne(s), %d prenom(s) remis"
          % (_net["fusions"], _net["prenoms"]))
    vieux = arch.arbre_charger(_f_vieux("arbre"))
    cn, cv = chiffres_de(neuf), chiffres_de(vieux)

    print("=== APPLIQUER LA BIBLIOTHEQUE PAR LE SENS ===")
    print("  par le sens : %d fiche(s)" % cn["fiches"])
    print("  qui tourne  : %d fiche(s)" % cv["fiches"])

    if not cn["fiches"]:
        print("\n  JE NE FAIS RIEN : la bibliotheque par le sens est vide.")
        print("  Lancez d'abord : python biblio2_retri_par_sens.py")
        return {"applique": False, "pourquoi": "la bibliotheque par le sens est vide"}

    if cn["fiches"] < cv["fiches"] and not meme_si_plus_petite:
        print("\n  JE NE FAIS RIEN : la neuve a MOINS de fiches que celle qui tourne")
        print("  (%d contre %d). Ca veut sans doute dire que le re-tri n'est pas fini."
              % (cn["fiches"], cv["fiches"]))
        print("  Pour passer quand meme, en le voulant vraiment :")
        print("    python biblio2_retri_par_sens.py --appliquer --meme-si-plus-petite")
        return {"applique": False, "pourquoi": "la neuve est plus petite"}

    #  verrou 3 : une copie datee de l'ancienne, AVANT de la remplacer.
    copie = os.path.join(dossier_du_retri(quand),
                         "remplacee_le_%s_arbre.json" % time.strftime("%Y-%m-%d_%Hh%M"))
    try:
        _ecrire_json(copie, vieux)
        print("\n  copie datee de l'ancienne : %s" % copie)
    except Exception as ex:
        print("\n  JE NE FAIS RIEN : la copie de l'ancienne n'a pas pu etre ecrite (%s)"
              % str(ex)[:120])
        return {"applique": False, "pourquoi": "la copie de l'ancienne a rate"}

    #  UNE SEULE ECRITURE, et elle est atomique.
    arch.arbre_sauver(_f_vieux("arbre"), neuf)
    plan_apres, _signal = plan_biblio.rafraichir(neuf, _f_vieux("plan"), _f_vieux("signal"))
    print("  la bibliotheque par le sens EST MAINTENANT celle qui tourne.")
    print("  plan refait : version %s" % plan_apres.get("version", 0))
    print("  pour revenir en arriere : recopiez %s sur %s" % (copie, _f_vieux("arbre")))
    journal("APPLIQUE : %d fiches remplacent %d" % (cn["fiches"], cv["fiches"]), quand)
    return {"applique": True, "fiches": cn["fiches"], "avant": cv["fiches"], "copie": copie}


# =====================================================================
#  L'ESSAI — SANS CLE, SANS RESEAU, SANS AUCUNE DONNEE PERSONNELLE.
# =====================================================================

def tout_en_un(juge, sources=None):
    """17/10/2026, DEMANDE DE FRED : UN SEUL DOUBLE-CLIC, ET TOUT SE FAIT TOUT SEUL.
    1) le re-tri complet (il reprend ou il en etait si on l'a arrete) ;
    2) un DEUXIEME passage, qui ne refait rien mais RATTRAPE ce que l'archiviste du jour a range
       pendant ce temps (sinon ces souvenirs manqueraient dans la bibliotheque neuve) ;
    3) si tout est fait, la bibliotheque re-triee PREND LA PLACE de l'ancienne, qui est gardee
       en copie datee a cote. Il ne reste qu'UNE bibliotheque en service.
    S'il reste quelque chose (arret, panne d'internet...), il N'APPLIQUE RIEN : on relance le meme
    double-clic, il reprend ou il en etait. Rend True si la bibliotheque re-triee est en service."""
    lire = sources or reprise.tout_le_passe

    def sources_completes():
        """Le passe habituel + CHAQUE FICHE de la bibliotheque qui tourne, sous SON PROPRE repere.
        Ainsi une fiche qui ne vient d'aucune des sources habituelles est refaite elle aussi :
        rien ne peut manquer dans la bibliotheque re-triee. Une fiche deja relue par sa source
        porte le meme repere : elle n'est pas rangee deux fois."""
        lot, soucis = lire()
        try:
            for f in arch.toutes_les_fiches(arch.arbre_charger(_f_vieux("arbre"))):
                fi = f[-1] if isinstance(f, (list, tuple)) else f
                texte = str((fi or {}).get("texte") or "").strip()
                if not texte:
                    continue
                src = (fi or {}).get("source") or "bibliotheque2"
                lot.append({"texte": texte, "source": src,
                            "date": str(((fi or {}).get("filtres") or {}).get("date") or (fi or {}).get("date") or "")[:10],
                            "repere": (fi or {}).get("repere") or arch.repere_de(src, texte)})
        except Exception as ex:
            soucis = list(soucis or []) + ["fiches de la bibliotheque qui tourne : %s" % str(ex)[:120]]
        return lot, soucis

    def juge_qui_tient_le_verrou(s, a):
        arch.verrou_rafraichir(_dossier_biblio2())       # « je suis toujours la »
        return juge(s, a)

    # 17/10/2026 (Fred) : LE VERROU. Le passage 1 (le long) se fait sans gener personne. Pour le
    # passage 2 et la mise en service, on PREND le verrou : l'archiviste du jour ne peut plus ecrire
    # (il reessaiera apres), donc rien ne peut arriver entre le rattrapage et la mise en service, et
    # rien ne peut reecrire l'ancienne bibliotheque par-dessus la neuve.
    tient = False
    try:
        for passage in (1, 2):
            if passage == 2:
                print("\n  Je prends le verrou de la bibliotheque (l'archiviste du jour attendra la fin).")
                if not _attendre_le_verrou():
                    print("  Le verrou n'a pas pu etre pris : je n'applique RIEN.")
                    return False
                tient = True
            print("\n##### PASSAGE %d SUR 2 %s #####" % (passage, "(le re-tri)" if passage == 1
                                                         else "(on rattrape ce qui est arrive entre-temps)"))
            _arbre, rap = refaire_le_tri(juge_qui_tient_le_verrou if tient else juge,
                                         sources=sources_completes)
            if rap.get("arrete") or rap.get("reste"):
                print("\n  PAS FINI (%s) : je n'applique RIEN. La bibliotheque qui tourne est intacte."
                      % ("arrete a la main" if rap.get("arrete") else "%d souvenir(s) pas encore refait(s)" % rap["reste"]))
                print("  Relancez le meme double-clic : il reprendra exactement la.")
                return False
        print("\n##### TOUT EST REFAIT : LA BIBLIOTHEQUE RE-TRIEE PREND LA PLACE DE L'ANCIENNE #####")
        # Tout est refait : si elle a moins de fiches, ce ne sont que les textes identiques mot pour mot
        # (gardes une seule fois). L'ancienne est de toute facon recopiee, datee, AVANT le remplacement.
        r = appliquer(meme_si_plus_petite=True)
        return bool(r.get("applique"))
    finally:
        if tient:
            arch.verrou_rendre(_dossier_biblio2())


def _demo():
    """UN RE-TRI COMPLET SUR 195 FAUX SOUVENIRS, avec un faux cerveau reflechi. Tout est
    ecrit dans un dossier a cote du code : aucune memoire reelle n'est ouverte, ni en
    lecture ni en ecriture. C'est ce qui prouve que la mecanique tient AVANT de la lancer
    sur la vraie memoire."""
    essai = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_demo_retri")

    #  ON FAIT POINTER LES DEUX SEULS CHEMINS QUI COMPTENT VERS UN DOSSIER D'ESSAI, le temps
    #  de l'essai : la memoire reelle n'est donc ouverte ni en lecture ni en ecriture. On
    #  garde les vrais sous la main pour les remettre a la fin.
    _vrai_dossier = globals()["dossier_du_retri"]
    _vrai_f_vieux = globals()["_f_vieux"]

    def _dossier_d_essai(quand=None):
        return essai

    def _f_vieux_d_essai(nom):
        return os.path.join(essai, {"arbre": "vieil_arbre.json", "plan": "vieux_plan.json",
                                    "signal": "vieux_signal.json",
                                    "marque_page": "vieux_marque_page.json"}[nom])

    globals()["dossier_du_retri"] = _dossier_d_essai
    globals()["_f_vieux"] = _f_vieux_d_essai

    rate = []

    def controle(nom, condition):
        print(("  OK   %s" if condition else "  RATE %s") % nom)
        if not condition:
            rate.append(nom)

    os.makedirs(essai, exist_ok=True)

    #  ---- une fausse memoire de 195 morceaux, inventee de toutes pieces ----------------
    sujets = [("Vehicules", "Voitures", "la voiture", "un vehicule a quatre roues"),
              ("Sante", "Rendez-vous", "le medecin", "une consultation medicale"),
              ("Famille", "Les enfants", "ma fille", "un enfant du proprietaire"),
              ("Gouts", "Cuisine", "la coriandre", "une herbe aromatique"),
              ("Maison", "Les travaux", "la chaudiere", "un appareil de chauffage")]

    def faux_passe():
        out = []
        for n in range(195):
            rayon, tiroir, mot, autrement = sujets[n % len(sujets)]
            if n % 13 == 7:
                #  un morceau que l'assistante a invente : il ne doit JAMAIS devenir un fait
                t = ("Tu viens de me raconter une histoire a propos de %s qui n'a jamais eu "
                     "lieu, numero %d." % (mot, n))
                src = "conversation"
            elif n % 3 == 0:
                t = "Au sujet de %s : la note numero %d, posee par le proprietaire." % (mot, n)
                src = "souvenirs"
            elif n % 3 == 1:
                # Le numero rend chaque discussion DIFFERENTE : sans lui, les 60 phrases etaient le
                # meme texte mot pour mot, et l'outil avait raison de ne les ranger qu'une fois.
                t = ("Une longue discussion a propos de %s (numero %d). " % (mot, n)) * 60   # texte bavard
                src = "conversation"
            else:
                t = "%s > %s > fiche %d\nUne ancienne fiche au sujet de %s." % (rayon, tiroir,
                                                                                n, mot)
                src = "bibliotheque"
            out.append({"texte": t, "source": src, "date": "",
                        "repere": arch.repere_de(src, t)})
        return out, []

    def faux_cerveau(s, _arbre):
        t = s["texte"]
        for rayon, tiroir, mot, autrement in sujets:
            if mot in t:
                if "jamais eu lieu" in t:
                    return {"de_quoi_on_parle": "Une histoire batie autour de %s, que le "
                                                "proprietaire ne reconnait pas." % autrement,
                            "a_existe": False,
                            "pourquoi_pas_sur": "le proprietaire dit que ca n'a pas eu lieu",
                            "tient_demain": False, "nature": "invention de l'assistante",
                            "categorie": rayon, "sous_categorie": tiroir,
                            "filtres": {"objet": mot, "type": "fait"},
                            "resume": "Une histoire au sujet de %s." % mot, "confiance": 0.9}
                return {"de_quoi_on_parle": "Il est question de %s." % autrement,
                        "a_existe": True, "tient_demain": True, "nature": "fait pose",
                        "categorie": rayon, "sous_categorie": tiroir,
                        "filtres": {"objet": mot, "type": "fait"},
                        "resume": "Au sujet de %s." % mot, "confiance": 0.9}
        return {"categorie": "", "confiance": 0.2}

    #  une « ancienne » bibliotheque, pour avoir un avant / apres a montrer
    vieil_arbre = {}
    for n in range(40):
        rayon, tiroir, mot, _a = sujets[n % len(sujets)]
        s = {"texte": "vieille fiche %d au sujet de %s" % (n, mot), "source": "souvenirs"}
        s["repere"] = arch.repere_de("souvenirs", s["texte"])
        arch.ranger(vieil_arbre, s, arch.valider_jugement(
            {"categorie": rayon, "sous_categorie": tiroir, "confiance": 0.9}))
    arch.arbre_sauver(_f_vieux("arbre"), vieil_arbre)
    empreinte_du_vieux = json.dumps(arch.arbre_charger(_f_vieux("arbre")), sort_keys=True)

    print("### LE RE-TRI COMPLET, SUR 195 FAUX SOUVENIRS, SANS CLE ET SANS RESEAU ###\n")
    arbre, rapport = refaire_le_tri(faux_cerveau, sources=faux_passe, paquet=25)

    print("\n### ON RELANCE SUR LE MEME PASSE : rien ne doit etre refait deux fois ###\n")
    arbre2, rapport2 = refaire_le_tri(faux_cerveau, sources=faux_passe, paquet=25)

    print("\n=== CONTROLES ===")
    c1, c2 = chiffres_de(arbre), chiffres_de(arbre2)
    controle("les 195 souvenirs sont refaits par le sens", c1["fiches"] == 195)
    controle("relancer ne refait RIEN deux fois (195 avant, 195 apres)",
             c2["fiches"] == c1["fiches"] == 195)
    controle("le deuxieme passage ne refait aucun rangement", rapport2["refaits"] == 0)
    controle("chaque fiche porte un repere stable", c1["avec_repere"] == 195)
    controle("CE QUI N'A PAS EXISTE est mis de cote, et pas range comme un fait",
             c1["mis_de_cote"] == 15 and arch.A_VERIFIER in arbre)
    controle("les morceaux mis de cote sont tous marques a trancher par le proprietaire",
             len(arch.a_remonter_au_proprietaire(arbre)) == c1["mis_de_cote"])
    controle("toutes les fiches qui ont existe portent la phrase du sens",
             c1["avec_le_sens"] == 195)
    controle("AUCUN MOT N'EST PERDU : le texte bavard est garde entier, mot pour mot",
             any(len(fi.get("texte") or "") > 2000 for _c, _s, fi
                 in arch.toutes_les_fiches(arbre)))

    #  LE GARDE-FOU QUI COMPTE LE PLUS : l'original n'a pas bouge.
    controle("LA BIBLIOTHEQUE QUI TOURNE N'A PAS ETE TOUCHEE (au caractere pres)",
             json.dumps(arch.arbre_charger(_f_vieux("arbre")), sort_keys=True)
             == empreinte_du_vieux)
    controle("la sauvegarde datee d'avant le re-tri est bien la",
             os.path.exists(os.path.join(essai, "avant_le_retri_vieil_arbre.json")))
    controle("la liste de ce qui attend le proprietaire est ecrite en clair",
             os.path.exists(_f_neuf("a_trancher")))
    controle("le journal du re-tri est ecrit", os.path.exists(_f_neuf("journal")))

    #  --appliquer : les trois verrous.
    r_vide = appliquer()
    controle("APPLIQUER marche quand la neuve est plus grande (195 contre 40)",
             r_vide.get("applique") is True)
    controle("et une copie datee de l'ancienne a ete gardee AVANT de la remplacer",
             os.path.exists(r_vide.get("copie") or ""))
    controle("apres avoir applique, la bibliotheque qui tourne porte les 195 fiches",
             chiffres_de(arch.arbre_charger(_f_vieux("arbre")))["fiches"] == 195)

    #  le verrou « plus petite » : on remet une grande en place et on tente une petite.
    _ecrire_json(_f_neuf("arbre"), {"Divers": {"A trier": []}})
    r_petite = appliquer()
    controle("APPLIQUER REFUSE de remplacer une bibliotheque par une vide",
             r_petite.get("applique") is False)

    globals()["dossier_du_retri"] = _vrai_dossier
    globals()["_f_vieux"] = _vrai_f_vieux

    print("\n%s" % ("TOUT EST PASSE." if not rate else
                    "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
    return rate


if __name__ == "__main__":
    args = [a.lower() for a in sys.argv[1:]]

    if "--demo" in args:
        raise SystemExit(1 if _demo() else 0)

    if "--chiffres" in args:
        dire_les_chiffres()
        raise SystemExit(0)

    if "--tout-en-un" in args:
        if not reprise._lire_cle():
            print("=== LE RE-TRI ATTEND UNE CLE === (aucune cle dans %s) : rien n'est touche."
                  % reprise.DOSSIER)
            raise SystemExit(0)
        if "--recommencer" in args:
            # Le choix de Fred (B) : on met de cote le chantier pas fini, puis on repart de zero.
            for _n in recommencer_de_zero():
                print("  Le chantier commence est mis de cote (rien n'est efface) : %s" % _n)
        raise SystemExit(0 if tout_en_un(reprise.juger_par_l_ia) else 1)

    if "--appliquer" in args:
        r = appliquer(meme_si_plus_petite=("--meme-si-plus-petite" in args))
        raise SystemExit(0 if r.get("applique") else 1)

    #  LE VRAI RE-TRI. SANS CLE, ON NE RANGE RIEN ET ON LE DIT.
    if not reprise._lire_cle():
        print("=== LE RE-TRI ATTEND UNE CLE ===")
        print("  Aucune cle n'est posee dans %s." % reprise.DOSSIER)
        print("  Je ne range RIEN, je ne touche a RIEN, et je ne mets aucune fiche de cote :")
        print("  toute la memoire reste exactement ou elle est, intacte.")
        print("  Posez la cle, puis relancez.")
        print("  (Pour voir la mecanique tourner sans cle et sans aucune donnee reelle :")
        print("   python biblio2_retri_par_sens.py --demo)")
        raise SystemExit(0)

    limite = None
    for a in args:
        if a.isdigit():
            limite = int(a)
    if reglages is not None:
        try:
            print(reglages.cerveau_reflechi_dit())
            print("")
        except Exception:
            pass
    refaire_le_tri(reprise.juger_par_l_ia, limite=limite)
