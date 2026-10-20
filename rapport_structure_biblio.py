# -*- coding: utf-8 -*-
# Rapport de structure de la bibliotheque (memoire 2)
# Ecrit par Luciana, 11/10/2026 - LECTURE SEULE, ne modifie RIEN.
import json, os, collections

BASE = r"C:\Users\Fred\Luciana\bibliotheque2"
SORTIE = r"C:\Users\Fred\Desktop\Structure_bibliotheque_11-10-2026.txt"

L = []
def w(t=""):
    L.append(t)

def est_fiche(x):
    return isinstance(x, dict) and ("texte" in x or "resume" in x or "filtres" in x)

def nb(noeud):
    if isinstance(noeud, list):
        return sum(1 for x in noeud if est_fiche(x))
    if isinstance(noeud, dict):
        return sum(nb(v) for k, v in noeud.items() if not str(k).startswith("_"))
    return 0

def collecter(noeud, chemin, acc):
    if isinstance(noeud, dict):
        for k, v in noeud.items():
            if str(k).startswith("_"):
                continue
            if isinstance(v, list):
                f = [x for x in v if est_fiche(x)]
                if f:
                    acc.append((chemin + [str(k)], f))
            else:
                collecter(v, chemin + [str(k)], acc)
    elif isinstance(noeud, list):
        f = [x for x in noeud if est_fiche(x)]
        if f:
            acc.append((chemin, f))

w("STRUCTURE DE LA BIBLIOTHEQUE (memoire 2)")
w("Rapport lu directement par Luciana dans le fichier de l'archiviste, le 11/10/2026.")
w("Lecture seule : rien n'a ete modifie.")
w("=" * 72)
w("")

w("1. LES FICHIERS DU DOSSIER")
try:
    for nom in sorted(os.listdir(BASE)):
        p = os.path.join(BASE, nom)
        if os.path.isfile(p):
            w("   %-30s %9.1f Ko" % (nom, os.path.getsize(p) / 1024.0))
        else:
            w("   %-30s [dossier]" % nom)
except Exception as e:
    w("   liste impossible : %r" % (e,))
w("")

try:
    with open(os.path.join(BASE, "arbre.json"), "r", encoding="utf-8") as f:
        arbre = json.load(f)
except Exception as e:
    w("LECTURE IMPOSSIBLE : %r" % (e,))
    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("ERREUR LECTURE ARBRE")
    raise SystemExit

cats = [(k, v) for k, v in arbre.items() if not str(k).startswith("_")]
acc = []
collecter(arbre, [], acc)
total = sum(len(f) for _, f in acc)

compte_champs = collections.Counter()
for _, f in acc:
    for x in f:
        for c in (x.get("filtres") or {}):
            compte_champs[c] += 1

w("2. VUE D'ENSEMBLE")
w("   Rayons (categories) ............ %d" % len(cats))
w("   Tiroirs ........................ %d" % len(acc))
w("   Fiches rangees ................. %d" % total)
w("   Champs d'etiquette ............. %s" % ", ".join("%s (%d)" % (k, v) for k, v in compte_champs.most_common()))
w("")

w("3. LA STRUCTURE, RAYON PAR RAYON")
for cat, contenu in sorted(cats, key=lambda kv: -nb(kv[1])):
    sous = []
    collecter(contenu, [str(cat)], sous)
    w("")
    w("* RAYON : %s   -- %d fiches, %d tiroirs" % (cat, nb(contenu), len(sous)))
    for chemin, fiches in sorted(sous, key=lambda x: -len(x[1])):
        w("      %-60s %4d fiches" % (" > ".join(chemin[1:]) or "(direct)", len(fiches)))
w("")

w("4. LES ETIQUETTES (les plus frequentes, rayon par rayon)")
for cat, contenu in sorted(cats, key=lambda kv: -nb(kv[1])):
    sous = []
    collecter(contenu, [str(cat)], sous)
    w("")
    w("* %s" % cat)
    for champ in ("type", "qui", "ou", "objet", "date"):
        c = collections.Counter()
        for _, fiches in sous:
            for x in fiches:
                v = (x.get("filtres") or {}).get(champ)
                if isinstance(v, list):
                    for i in v:
                        if i:
                            c[str(i)] += 1
                elif v:
                    c[str(v)] += 1
        if c:
            w("   %-6s : %s" % (champ, " | ".join("%s (%d)" % (a, b) for a, b in c.most_common(8))))
w("")

w("5. EXEMPLES DE FICHES RANGEES (le souvenir + son etiquette)")
for cat, contenu in sorted(cats, key=lambda kv: -nb(kv[1])):
    sous = []
    collecter(contenu, [str(cat)], sous)
    w("")
    w("* %s" % cat)
    pris = 0
    for chemin, fiches in sorted(sous, key=lambda x: -len(x[1])):
        for x in fiches[:2]:
            t = (x.get("texte") or x.get("resume") or "").replace("\n", " ")
            w("   [%s]" % " > ".join(chemin[1:]))
            w("      souvenir  : %s" % t[:115])
            et = []
            for k, v in (x.get("filtres") or {}).items():
                if isinstance(v, list):
                    v = ", ".join(str(i) for i in v if i)
                if v:
                    et.append("%s=%s" % (k, v))
            w("      etiquette : %s" % " ; ".join(et))
            pris += 1
        if pris >= 6:
            break
w("")
w("Fin du rapport.")

with open(SORTIE, "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("OK - rapport ecrit : %d fiches, %d tiroirs, %d rayons" % (total, len(acc), len(cats)))
