# -*- coding: utf-8 -*-
"""
=====================================================================================
 CONTROLE DE LA PLOMBERIE — v164 (chantier du 12/10/2026)
=====================================================================================
A quoi ca sert : DIRE LA VERITE EN CHIFFRES sur les trois choses qui faisaient attendre
Fred, AVANT et APRES la reparation. Rien d'autre.

  1) le grand tiroir (la mise a jour de l'index de sens) : combien de temps par tour,
     combien par passage, et -- ce qui manquait -- quelle part etait de l'ATTENTE ;
  2) le choix du tour : combien de secondes ;
  3) l'injection de bibliotheque (BIBLIO2) : combien de caracteres par message.

IL NE TOUCHE A RIEN. Il LIT le carnet de traces ~/Luciana/controle_memoire_sens.jsonl
et il n'ecrit nulle part.

COMMENT S'EN SERVIR (dans le dossier du programme) :

    python controle_plomberie_v164.py                  -> tout le carnet, avant / apres
    python controle_plomberie_v164.py 2026-10-12       -> seulement ce jour-la
    python controle_plomberie_v164.py 2026-10-12 2026-10-13   -> deux jours compares

Les lignes ecrites par la v164 portent le marqueur "v164": true. Le script s'en sert
pour separer tout seul l'AVANT et l'APRES, sans qu'on ait rien a lui dire.
"""

import json
import os
import sys

# Le carnet est toujours a cote de la memoire de Fred, jamais dans le dossier du programme.
CARNET = os.path.join(os.path.expanduser("~"), "Luciana", "controle_memoire_sens.jsonl")

# Ce qu'on attend de la v164 (les trois promesses du chantier)
PROMESSE_TRANCHE_S = 25.0        # une tranche de grand tiroir : ~20 s, 25 avec la marge
PROMESSE_INJECTION_MIN = 10000   # l'injection doit rester utile
PROMESSE_INJECTION_MAX = 16000   # ... sans repartir vers les 30 000 de la v162


# -------------------------------------------------------------------- lecture
def lire(chemin=CARNET):
    """Le carnet, ligne par ligne, en lecture SEULE. Une ligne abimee est sautee, jamais
    une raison d'arreter : un carnet de traces n'est pas une base de donnees."""
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
        return float(x)
    except Exception:
        return defaut


def _mediane(valeurs):
    v = sorted(valeurs)
    if not v:
        return 0.0
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2.0


# ----------------------------------------------------------------- les mesures
def mesurer_grand_tiroir(evenements):
    """Ce que coute la mise a jour du grand tiroir, separee AVANT v164 / APRES v164."""
    avant, apres = [], []
    for e in evenements:
        if e.get("quoi") != "grand tiroir mis a jour":
            continue
        ligne = {"quand": e.get("quand", ""),
                 "passages": int(_n(e.get("passages_ajoutes"))),
                 "secondes": _n(e.get("secondes")),
                 "travail": _n(e.get("travail_s"), _n(e.get("secondes"))),
                 "attente": _n(e.get("attente_s"), -1.0),
                 "reste": int(_n(e.get("reste_a_faire"), -1))}
        (apres if e.get("v164") else avant).append(ligne)
    return avant, apres


def mesurer_choix_du_tour(evenements):
    avant, apres = [], []
    for e in evenements:
        if e.get("quoi") != "message":
            continue
        c = e.get("choix_du_tour_v150")
        if not isinstance(c, dict) or "secondes" not in c:
            continue
        (apres if e.get("v164") else avant).append(_n(c.get("secondes")))
    return avant, apres


def mesurer_injection(evenements):
    """L'injection BIBLIO2 par message : caracteres verses, sources servies, et -- nouveau
    en v164 -- le detail du temps passe dans chaque etape."""
    avant, apres = [], []
    for e in evenements:
        if e.get("quoi") != "biblio2" or "caracteres" not in e:
            continue
        ligne = {"quand": e.get("quand", ""),
                 "caracteres": int(_n(e.get("caracteres"))),
                 "donnes": int(_n(e.get("donnes"))),
                 "candidats": int(_n(e.get("candidats"))),
                 "cout": e.get("cout") if isinstance(e.get("cout"), dict) else {}}
        (apres if e.get("v164") else avant).append(ligne)
    return avant, apres


# ------------------------------------------------------------------ affichage
def dire_grand_tiroir(titre, lignes):
    print("\n  %s" % titre)
    if not lignes:
        print("    (aucune mesure)")
        return None
    passages = sum(l["passages"] for l in lignes)
    secondes = sum(l["secondes"] for l in lignes)
    pires = max(l["secondes"] for l in lignes)
    print("    mises a jour .................. %d" % len(lignes))
    print("    passages indexes .............. %d" % passages)
    print("    temps total ................... %.1f s" % secondes)
    print("    cout par passage .............. %.2f s" % (secondes / max(1, passages)))
    print("    duree mediane d'une tranche ... %.1f s" % _mediane([l["secondes"] for l in lignes]))
    print("    PIRE tranche .................. %.1f s   <-- c'est ca que Fred subit" % pires)
    attentes = [l["attente"] for l in lignes if l["attente"] >= 0]
    if attentes:
        print("    attente avant de travailler ... %.1f s en moyenne (mesure a part depuis la v164)"
              % (sum(attentes) / len(attentes)))
    restes = [l["reste"] for l in lignes if l["reste"] >= 0]
    if restes:
        print("    reste a faire apres la tranche  %d en moyenne (reporte, jamais abandonne)"
              % (sum(restes) / len(restes)))
    return {"pire": pires, "par_passage": secondes / max(1, passages), "lignes": len(lignes)}


def dire_choix(titre, valeurs):
    print("\n  %s" % titre)
    if not valeurs:
        print("    (aucune mesure)")
        return None
    print("    messages ...................... %d" % len(valeurs))
    print("    mediane ....................... %.2f s" % _mediane(valeurs))
    print("    le pire ....................... %.2f s" % max(valeurs))
    return {"mediane": _mediane(valeurs), "pire": max(valeurs)}


def dire_injection(titre, lignes):
    print("\n  %s" % titre)
    if not lignes:
        print("    (aucune mesure)")
        return None
    cars = [l["caracteres"] for l in lignes]
    donnes = [l["donnes"] for l in lignes]
    print("    messages ...................... %d" % len(lignes))
    print("    caracteres verses (mediane) ... %d" % _mediane(cars))
    print("    caracteres verses (le plus) ... %d" % max(cars))
    print("    sources servies (mediane) ..... %.1f" % _mediane(donnes))
    etapes = {}
    for l in lignes:
        for k, v in (l["cout"] or {}).items():
            if k.endswith("_s"):
                etapes.setdefault(k, []).append(_n(v))
    if etapes:
        print("    ou passe le temps d'un tour (mediane, secondes) :")
        for k in sorted(etapes, key=lambda k: -_mediane(etapes[k])):
            print("       %-18s %.2f s" % (k, _mediane(etapes[k])))
    return {"caracteres": _mediane(cars), "donnes": _mediane(donnes)}


# ---------------------------------------------------------------- les controles
def controler(gt, ch, inj):
    """Les trois promesses du chantier, verifiees sur les chiffres reels. On dit VERT ou
    ROUGE, jamais « ca a l'air d'aller »."""
    print("\n" + "=" * 78)
    print(" LES CONTROLES (sur l'APRES ; s'il n'y a pas encore d'APRES, on le dit)")
    print("=" * 78)
    rates = 0
    if gt is None:
        print(" [ PAS TESTABLE ] le grand tiroir : aucune mesure v164 dans le carnet.")
        print("                  -> relance Luciana en v164, echange quelques messages,")
        print("                     puis relance ce script.")
        rates += 1
    else:
        ok = gt["pire"] <= PROMESSE_TRANCHE_S
        print(" [ %s ] une tranche de grand tiroir ne depasse pas %.0f s   (pire vue : %.1f s)"
              % ("VERT " if ok else "ROUGE", PROMESSE_TRANCHE_S, gt["pire"]))
        rates += 0 if ok else 1
    if inj is None:
        print(" [ PAS TESTABLE ] l'injection : aucune mesure v164 dans le carnet.")
        rates += 1
    else:
        ok = PROMESSE_INJECTION_MIN <= inj["caracteres"] <= PROMESSE_INJECTION_MAX
        print(" [ %s ] l'injection reste entre %d et %d caracteres   (mediane : %d)"
              % ("VERT " if ok else "ROUGE", PROMESSE_INJECTION_MIN, PROMESSE_INJECTION_MAX,
                 inj["caracteres"]))
        rates += 0 if ok else 1
        ok = inj["donnes"] >= 1
        print(" [ %s ] au moins une source est servie quand il y en a   (mediane : %.1f)"
              % ("VERT " if ok else "ROUGE", inj["donnes"]))
        rates += 0 if ok else 1
    if ch is not None:
        print(" [ INFO  ] choix du tour : mediane %.2f s, pire %.2f s (depend du cerveau, pas de nous)"
              % (ch["mediane"], ch["pire"]))
    print("\n %s" % ("TOUT EST VERT." if not rates else
                     "%d controle(s) a revoir -- c'est ecrit ci-dessus, sans enjoliver." % rates))
    return rates


def main():
    jours = [a for a in sys.argv[1:] if not a.startswith("-")]
    print("=" * 78)
    print(" CONTROLE DE LA PLOMBERIE — v164")
    print(" carnet : %s" % CARNET)
    evenements = lire()
    if not evenements:
        print("\n AUCUN CARNET LISIBLE. Rien ne peut etre mesure, et on ne va pas faire semblant.")
        print(" Verifie que ce fichier existe : %s" % CARNET)
        return 2
    print(" evenements lus : %d%s" % (len(evenements),
                                      ("   jours demandes : %s" % ", ".join(jours)) if jours else ""))
    print("=" * 78)
    evenements = du_jour(evenements, jours)

    gt_avant, gt_apres = mesurer_grand_tiroir(evenements)
    ch_avant, ch_apres = mesurer_choix_du_tour(evenements)
    in_avant, in_apres = mesurer_injection(evenements)

    print("\n" + "-" * 78)
    print(" 1) LE GRAND TIROIR (la mise a jour de l'index de sens)")
    print("-" * 78)
    dire_grand_tiroir("AVANT (v162 et avant)", gt_avant)
    gt = dire_grand_tiroir("APRES (v164)", gt_apres)

    print("\n" + "-" * 78)
    print(" 2) LE CHOIX DU TOUR")
    print("-" * 78)
    dire_choix("AVANT (v162 et avant)", ch_avant)
    ch = dire_choix("APRES (v164)", ch_apres)

    print("\n" + "-" * 78)
    print(" 3) L'INJECTION DE BIBLIOTHEQUE PAR MESSAGE (BIBLIO2)")
    print("-" * 78)
    dire_injection("AVANT (v162 et avant)", in_avant)
    inj = dire_injection("APRES (v164)", in_apres)

    return 0 if controler(gt, ch, inj) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
