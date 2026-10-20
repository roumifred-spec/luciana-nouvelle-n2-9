# -*- coding: utf-8 -*-
"""Lecture SEULE du carnet de traces : mesures du grand tiroir et du choix du tour.

Ne modifie jamais le carnet. Sert a donner les chiffres AVANT / APRES.
"""
import json
import os
import sys

CARNET = r"C:\Users\Fred\Luciana\controle_memoire_sens.jsonl"


def lire(chemin=CARNET):
    lignes = []
    with open(chemin, "r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                lignes.append(json.loads(ligne))
            except Exception:
                continue
    return lignes


def resume(jour=None):
    evs = lire()
    tiroirs = []
    choix = []
    injections = []
    for e in evs:
        quand = e.get("quand", "")
        if jour and not quand.startswith(jour):
            continue
        quoi = e.get("quoi", "")
        if quoi == "grand tiroir mis a jour":
            tiroirs.append(e)
        elif quoi in ("choix du tour", "choix"):
            choix.append(e)
        if quoi == "message" and isinstance(e.get("bibliotheque"), dict):
            injections.append(e)
    return evs, tiroirs, choix, injections


def _nb(e, *cles):
    for c in cles:
        if c in e and isinstance(e[c], (int, float)):
            return e[c]
    return None


def main():
    jour = sys.argv[1] if len(sys.argv) > 1 else None
    evs, tiroirs, choix, injections = resume(jour)
    print("=" * 70)
    print("CARNET :", CARNET)
    print("evenements :", len(evs), "| jour :", jour or "tous")
    print("=" * 70)

    print("\n--- GRAND TIROIR (mise a jour de l'index de sens) ---")
    print("{:<21} {:>9} {:>11} {:>11}".format("quand", "passages", "secondes", "s/passage"))
    tot_p = tot_s = 0
    for e in tiroirs:
        p = _nb(e, "passages", "ajoutes", "nouveaux") or 0
        s = _nb(e, "secondes", "duree", "duree_s") or 0
        tot_p += p
        tot_s += s
        par = (s / p) if p else 0
        print("{:<21} {:>9} {:>11.1f} {:>11.2f}".format(e.get("quand", "?"), p, s, par))
    if tot_p:
        print("-> total {} passages en {:.1f} s = {:.2f} s/passage".format(tot_p, tot_s, tot_s / tot_p))
    if tiroirs:
        pires = sorted(tiroirs, key=lambda e: -(_nb(e, "secondes", "duree", "duree_s") or 0))[:3]
        print("-> pires tours :", [(e.get("quand"), _nb(e, "secondes", "duree", "duree_s")) for e in pires])

    print("\n--- CHOIX DU TOUR ---")
    for e in choix:
        print("{:<21} {}".format(e.get("quand", "?"), {k: v for k, v in e.items() if k not in ("quoi", "quand")}))

    print("\n--- INJECTION BIBLIO2 par message ---")
    print("{:<21} {:>9} {:>12}".format("quand", "passages", "caracteres"))
    cars = []
    for e in injections:
        b = e["bibliotheque"]
        c = b.get("caracteres", 0)
        cars.append(c)
        print("{:<21} {:>9} {:>12}".format(e.get("quand", "?"), b.get("passages", 0), c))
    if cars:
        cars_tries = sorted(cars)
        print("-> injection : min {} / median {} / max {} / moyenne {:.0f} caracteres".format(
            cars_tries[0], cars_tries[len(cars_tries) // 2], cars_tries[-1], sum(cars) / len(cars)))


if __name__ == "__main__":
    main()
