# -*- coding: utf-8 -*-
"""
=====================================================================================
 CONTROLE DE LA LENTEUR AVANT QUE LUCIANA REPONDE — v165 (chantier du 12/10/2026)
=====================================================================================
UN SEUL SUJET : le temps que Fred passe devant un ecran vide AVANT que Luciana
commence a repondre. Rien d'autre.

Ce temps-la, c'est la somme de deux attentes qui, jusqu'a la v164, se SUIVAIENT :

  1) LE CHOIX DU TOUR      -- le petit cerveau qui trie consignes / passages / carnets
                              (champ "choix_du_tour_v150" -> "secondes") ;
  2) LES FACETTES          -- le petit cerveau qui dit dans quels tiroirs chercher
                              (champ "cout" -> "besoin_ia_s" de la ligne biblio2).

Les trois corrections de la v165 :
  * CORRECTION 1 : les deux partent EN MEME TEMPS  -> on attend le PLUS LONG, plus la somme ;
  * CORRECTION 2 : meme sujet -> on RESERT le tri deja fait -> on attend ZERO ;
  * CORRECTION 3 : un plafond de 120 s sur les facettes -> plus de 30 minutes possibles.

IL NE TOUCHE A RIEN. Il LIT le carnet ~/Luciana/controle_memoire_sens.jsonl et
n'ecrit nulle part. Les lignes ecrites par la v165 portent le marqueur "v165": true :
le script s'en sert pour separer tout seul l'AVANT et l'APRES.

COMMENT S'EN SERVIR (dans le dossier du programme) :

    python controle_lenteur_v165.py                     -> tout le carnet
    python controle_lenteur_v165.py 2026-10-12          -> seulement ce jour-la
    python controle_lenteur_v165.py 2026-10-12 2026-10-13
    python controle_lenteur_v165.py --derniers 30       -> les 30 derniers tours seulement
"""

import json
import os
import sys

CARNET = os.path.join(os.path.expanduser("~"), "Luciana", "controle_memoire_sens.jsonl")

# LES PROMESSES DE LA v165, ecrites ici pour qu'on puisse les contredire avec des chiffres.
PROMESSE_FACETTES_MAX_S = 130.0     # le plafond de 120 s, plus une marge de mesure
PROMESSE_ATTENTE_MEDIANE_S = 30.0   # la mediane de l'attente des deux tris doit passer sous ca
DERNIERS_PAR_DEFAUT = 30            # la fenetre de comparaison demandee par Fred


# -------------------------------------------------------------------- lecture
def lire(chemin=CARNET):
    """Le carnet, ligne par ligne, en lecture SEULE. Une ligne abimee est sautee : un carnet
    de traces n'est pas une base de donnees, et une ligne tronquee ne doit rien arreter."""
    lignes = []
    if not os.path.isfile(chemin):
        return lignes
    with open(chemin, "r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except Exception:
                continue
            if isinstance(d, dict):
                lignes.append(d)
    return lignes


def du_jour(evenements, jours):
    if not jours:
        return evenements
    return [e for e in evenements
            if any(str(e.get("quand", "")).startswith(j) for j in jours)]


def _n(x, defaut=0.0):
    try:
        if x is None:
            return defaut
        return float(x)
    except Exception:
        return defaut


def _mediane(valeurs):
    v = sorted(valeurs)
    if not v:
        return 0.0
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2.0


# ----------------------------------------------------------------- les tours
def les_tours(evenements):
    """UN TOUR = une ligne "message" et la ligne "biblio2" qui la precede immediatement.
    C'est l'ordre dans lequel le programme les ecrit : la bibliotheque 2 trace d'abord, la
    ligne "message" ferme le tour. On n'invente aucun appariement : on prend le dernier
    biblio2 vu avant chaque message, et rien d'autre.

    Rend une liste de dicts, un par tour :
      quand, v165, choix_s, facettes_s, attente_mesuree_s, somme_des_deux_s,
      reutilise, ressemblance, par_quoi, profondeur, fil_parti, attente_du_fil_s
    """
    tours, dernier_biblio2 = [], None
    for e in evenements:
        quoi = e.get("quoi")
        if quoi == "biblio2":
            if "caracteres" in e or isinstance(e.get("cout"), dict):
                dernier_biblio2 = e
            continue
        if quoi != "message":
            continue
        c = e.get("choix_du_tour_v150")
        if not isinstance(c, dict):
            dernier_biblio2 = None
            continue
        cout = {}
        if isinstance(dernier_biblio2, dict) and isinstance(dernier_biblio2.get("cout"), dict):
            cout = dernier_biblio2["cout"]
        tri = e.get("tri_du_tour") if isinstance(e.get("tri_du_tour"), dict) else {}
        sujet = tri.get("meme_sujet") if isinstance(tri.get("meme_sujet"), dict) else {}
        choix_s = _n(c.get("secondes"))
        facettes_s = _n(cout.get("besoin_ia_s"), -1.0)
        tours.append({
            "quand": str(e.get("quand") or ""),
            "v165": bool(e.get("v165")),
            "choix_s": choix_s,
            "facettes_s": facettes_s,
            # CE QUE FRED A VRAIMENT ATTENDU :
            #  - en v164 les deux attentes se suivaient : c'est leur SOMME ;
            #  - en v165 le programme la mesure lui-meme (attente_des_deux_tris_s).
            "somme_des_deux_s": choix_s + max(0.0, facettes_s),
            "attente_mesuree_s": _n(e.get("attente_des_deux_tris_s"), -1.0),
            "reutilise": bool(c.get("reutilise")),
            "tri_en_fond": bool(c.get("tri_en_fond")),
            "appels": int(_n(c.get("appels_au_cerveau"))),
            "profondeur": int(_n(c.get("profondeur"), 1)),
            "ressemblance": _n(sujet.get("ressemblance"), -1.0),
            "par_quoi_sujet": str(sujet.get("par_quoi") or ""),
            "fil_parti": bool(tri.get("fil_parti")),
            "attente_du_fil_s": _n(tri.get("attente_du_fil_s"), -1.0),
            "fil": str(tri.get("fil") or ""),
        })
        dernier_biblio2 = None
    return tours


# ------------------------------------------------------------------ affichage
def dire_attente(titre, tours):
    print("\n  %s" % titre)
    if not tours:
        print("    (aucune mesure)")
        return None
    choix = [t["choix_s"] for t in tours]
    facettes = [t["facettes_s"] for t in tours if t["facettes_s"] >= 0]
    mesurees = [t["attente_mesuree_s"] for t in tours if t["attente_mesuree_s"] >= 0]
    sommes = [t["somme_des_deux_s"] for t in tours]
    print("    tours mesures ................. %d" % len(tours))
    print("    1) choix du tour ... mediane %7.2f s   pire %7.2f s" % (_mediane(choix), max(choix)))
    if facettes:
        print("    2) facettes ........ mediane %7.2f s   pire %7.2f s"
              % (_mediane(facettes), max(facettes)))
    else:
        print("    2) facettes ........ (aucune mesure 'besoin_ia_s' sur ces tours)")
    print("    1+2, L'UN APRES L'AUTRE (ce que Fred attendait en v164) :")
    print("         mediane %7.2f s   pire %7.2f s" % (_mediane(sommes), max(sommes)))
    if mesurees:
        print("    ATTENTE REELLEMENT MESUREE PAR LE PROGRAMME (v165) :")
        print("         mediane %7.2f s   pire %7.2f s" % (_mediane(mesurees), max(mesurees)))
    reutilises = [t for t in tours if t["reutilise"]]
    if tours:
        print("    tris RESERVIS (zero appel) .... %d sur %d  (%.0f %%)"
              % (len(reutilises), len(tours), 100.0 * len(reutilises) / len(tours)))
    if reutilises:
        rs = [t["attente_mesuree_s"] for t in reutilises if t["attente_mesuree_s"] >= 0]
        if rs:
            print("       attente sur ces tours-la ... mediane %.2f s   pire %.2f s"
                  % (_mediane(rs), max(rs)))
    fils = [t["attente_du_fil_s"] for t in tours if t["attente_du_fil_s"] >= 0]
    if fils:
        print("    ce qu'il restait a attendre du petit fil (correction 1) :")
        print("         mediane %7.2f s   pire %7.2f s" % (_mediane(fils), max(fils)))
    bavures = [t["fil"] for t in tours if t["fil"]]
    if bavures:
        print("    le petit fil a dit quelque chose sur %d tour(s) :" % len(bavures))
        for b in sorted(set(bavures))[:6]:
            print("       - %s" % b[:140])
    return {"mediane_somme": _mediane(sommes), "pire_somme": max(sommes),
            "mediane_mesuree": (_mediane(mesurees) if mesurees else None),
            "pire_mesuree": (max(mesurees) if mesurees else None),
            "pire_facettes": (max(facettes) if facettes else None),
            "reutilises": len(reutilises), "tours": len(tours)}


def dire_meme_sujet(titre, tours):
    """LE DETECTEUR DE « MEME SUJET » : c'est ici qu'on CALIBRE le seuil sur du reel, au lieu
    d'en discuter. On montre la repartition des ressemblances mesurees et des profondeurs."""
    print("\n  %s" % titre)
    if not tours:
        print("    (aucune mesure)")
        return
    prof = {}
    for t in tours:
        prof[t["profondeur"]] = prof.get(t["profondeur"], 0) + 1
    print("    profondeur du tour : %s"
          % "  ".join("%d -> %d tour(s)" % (k, prof[k]) for k in sorted(prof)))
    mesurees = [t["ressemblance"] for t in tours if t["ressemblance"] >= 0]
    if not mesurees:
        print("    (la ressemblance n'est ecrite que depuis la v165 : rien a calibrer ici)")
        return
    par = {}
    for t in tours:
        if t["par_quoi_sujet"]:
            par[t["par_quoi_sujet"]] = par.get(t["par_quoi_sujet"], 0) + 1
    if par:
        print("    mesure par ......... %s" % "  ".join("%s : %d" % (k, v) for k, v in par.items()))
    mesurees.sort()
    print("    ressemblance mesuree : mini %.3f   mediane %.3f   maxi %.3f"
          % (mesurees[0], _mediane(mesurees), mesurees[-1]))
    print("    combien de tours passeraient tel ou tel seuil (pour choisir en connaissance) :")
    for seuil in (0.40, 0.50, 0.55, 0.60, 0.65, 0.72, 0.80, 0.90):
        combien = len([r for r in mesurees if r >= seuil])
        print("       seuil %.2f -> %3d tour(s) sur %d  (%.0f %%)"
              % (seuil, combien, len(mesurees), 100.0 * combien / len(mesurees)))


# ---------------------------------------------------------------- les controles
def controler(apres):
    """Les promesses de la v165, verifiees sur les chiffres reels. VERT ou ROUGE, jamais
    « ca a l'air d'aller ». S'il n'y a pas encore d'APRES, on le DIT."""
    print("\n" + "=" * 78)
    print(" LES CONTROLES (sur l'APRES ; s'il n'y a pas encore d'APRES, on le dit)")
    print("=" * 78)
    if apres is None:
        print(" [ PAS TESTABLE ] aucune mesure v165 dans le carnet.")
        print("                  -> lance Luciana en V165, echange quelques messages,")
        print("                     puis relance ce script. Rien n'est annonce sans preuve.")
        return 1
    rates = 0
    if apres["pire_facettes"] is None:
        print(" [ PAS TESTABLE ] le plafond des facettes : aucune mesure 'besoin_ia_s'.")
        rates += 1
    else:
        ok = apres["pire_facettes"] <= PROMESSE_FACETTES_MAX_S
        print(" [ %s ] les facettes ne depassent plus %.0f s   (pire vue : %.1f s)"
              % ("VERT " if ok else "ROUGE", PROMESSE_FACETTES_MAX_S, apres["pire_facettes"]))
        rates += 0 if ok else 1
    valeur = apres["mediane_mesuree"]
    if valeur is None:
        print(" [ PAS TESTABLE ] l'attente des deux tris n'est pas encore ecrite dans le carnet.")
        rates += 1
    else:
        ok = valeur <= PROMESSE_ATTENTE_MEDIANE_S
        print(" [ %s ] l'attente mediane des deux tris reste sous %.0f s   (mesuree : %.2f s)"
              % ("VERT " if ok else "ROUGE", PROMESSE_ATTENTE_MEDIANE_S, valeur))
        rates += 0 if ok else 1
    if apres["tours"]:
        part = 100.0 * apres["reutilises"] / apres["tours"]
        print(" [ INFO  ] tris reservis : %d sur %d (%.0f %%). Plus c'est haut, moins Fred attend."
              % (apres["reutilises"], apres["tours"], part))
    print("\n %s" % ("TOUT EST VERT." if not rates else
                     "%d controle(s) a revoir -- c'est ecrit ci-dessus, sans enjoliver." % rates))
    return rates


def main():
    args = sys.argv[1:]
    derniers = 0
    jours = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--derniers", "-d"):
            i += 1
            try:
                derniers = int(args[i])
            except Exception:
                derniers = DERNIERS_PAR_DEFAUT
        elif not a.startswith("-"):
            jours.append(a)
        i += 1

    print("=" * 78)
    print(" CONTROLE DE LA LENTEUR AVANT QUE LUCIANA REPONDE — V165")
    print(" carnet : %s   (lecture seule)" % CARNET)
    evenements = lire()
    if not evenements:
        print("\n AUCUN CARNET LISIBLE. Rien ne peut etre mesure, et on ne va pas faire semblant.")
        print(" Verifie que ce fichier existe : %s" % CARNET)
        return 2
    print(" evenements lus : %d%s" % (len(evenements),
                                      ("   jours demandes : %s" % ", ".join(jours)) if jours else ""))
    print("=" * 78)
    tours = les_tours(du_jour(evenements, jours))
    avant = [t for t in tours if not t["v165"]]
    apres = [t for t in tours if t["v165"]]
    if derniers > 0:
        avant, apres = avant[-derniers:], apres[-derniers:]
        print("\n (fenetre demandee : les %d derniers tours de chaque cote)" % derniers)

    print("\n" + "-" * 78)
    print(" 1) L'ATTENTE AVANT QUE LUCIANA COMMENCE A REPONDRE")
    print("-" * 78)
    dire_attente("AVANT (v164 et avant)", avant)
    ap = dire_attente("APRES (V165)", apres)

    print("\n" + "-" * 78)
    print(" 2) LE DETECTEUR DE « MEME SUJET » (correction 2) — ET SON CALIBRAGE")
    print("-" * 78)
    dire_meme_sujet("AVANT (v164 et avant)", avant)
    dire_meme_sujet("APRES (V165)", apres)

    return 0 if controler(ap) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
