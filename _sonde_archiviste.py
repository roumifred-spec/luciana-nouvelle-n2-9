# -*- coding: utf-8 -*-
"""Sonde de lecture seule : est-ce qu'on peut VRAIMENT lire les fichiers de Fred d'ici ?
Aucune ecriture. Sert uniquement a verifier le reel avant de construire l'archiviste."""
import io
import json
import os

DOSSIER = os.path.join(os.path.expanduser("~"), "Luciana")
DOSSIER_SENS = DOSSIER + "_sens"

CIBLES = [
    os.path.join(DOSSIER_SENS, "morceaux.jsonl"),
    os.path.join(DOSSIER_SENS, "etat.json"),
    os.path.join(DOSSIER, "plan_bibliotheque.json"),
    os.path.join(DOSSIER, "journal_tiroirs.jsonl"),
    os.path.join(DOSSIER, "noms_propres.json"),
    os.path.join(DOSSIER, "carnet.json"),
    os.path.join(DOSSIER, "consignes.jsonl"),
    os.path.join(DOSSIER, "souvenirs.json"),
    os.path.join(DOSSIER, "archive_outils.jsonl"),
    os.path.join(DOSSIER, "bibliotheque"),
    os.path.join(DOSSIER, "gouffre"),
]

for c in CIBLES:
    if not os.path.exists(c):
        print("ABSENT          ", c)
        continue
    if os.path.isdir(c):
        try:
            n = sum(len(fs) for _, _, fs in os.walk(c))
            print("DOSSIER %6d fichiers  %s" % (n, c))
        except Exception as e:
            print("DOSSIER ILLISIBLE", c, repr(e))
        continue
    try:
        taille = os.path.getsize(c)
        with io.open(c, "r", encoding="utf-8", errors="replace") as f:
            tete = f.readline()
        print("LU      %10d o  %s" % (taille, c))
        print("           1re ligne : %s" % tete[:160].replace("\n", " "))
    except Exception as e:
        print("ILLISIBLE       ", c, repr(e))

# combien de morceaux exactement
p = os.path.join(DOSSIER_SENS, "morceaux.jsonl")
if os.path.exists(p):
    n = 0
    sources = {}
    dates_vides = 0
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            n += 1
            try:
                x = json.loads(ligne)
            except Exception:
                continue
            sources[x.get("s")] = sources.get(x.get("s"), 0) + 1
            if not (x.get("d") or "").strip():
                dates_vides += 1
    print("")
    print("morceaux.jsonl : %d lignes, par source %s, dates vides %d" % (n, sources, dates_vides))
