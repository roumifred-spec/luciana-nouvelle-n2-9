# -*- coding: utf-8 -*-
# =====================================================================
# AUDIT COMPLET DU RANGEMENT - version 2 (corrigee)
# La v1 cherchait le champ "tiroir" alors que le vrai nom est "tiroirs"
# (une liste). Corrige ici. LECTURE SEULE : rien n'est modifie.
# =====================================================================
import json, os, io, collections, hashlib, datetime

D = r"C:\Users\Fred\Luciana"
ICI = os.path.dirname(os.path.abspath(__file__))
RAPPORT = os.path.join(ICI, "res_audit_rangement_v2.txt")
OUT = []


def p(*a):
    OUT.append(" ".join(str(x) for x in a))


def lire_jsonl(chemin):
    lignes = []
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as f:
            for i, l in enumerate(f, 1):
                l = l.strip()
                if not l:
                    continue
                try:
                    lignes.append((i, json.loads(l)))
                except Exception as e:
                    lignes.append((i, {"__illisible__": str(e)[:90]}))
    except Exception as e:
        p("  !! impossible d'ouvrir :", e)
    return lignes


p("=" * 78)
p("AUDIT DU RANGEMENT - VERSION 2 (champ 'tiroirs' corrige)")
p("Ecrit le", datetime.datetime.now().strftime("%d/%m/%Y a %Hh%M"), "- LECTURE SEULE")
p("=" * 78)

lignes = lire_jsonl(os.path.join(D, "rangement_journee.jsonl"))
p("lignes du journal :", len(lignes))

# ---------------- A) toutes les tentatives, par jour et par resultat
p("")
p("### A) TOUTES LES TENTATIVES (166 lignes, pas seulement 15) ###")
par_jour = collections.Counter(d.get("date", "?")[:10] for _, d in lignes)
for j, n in sorted(par_jour.items()):
    res = collections.Counter(d.get("resultat", "?") for _, d in lignes if d.get("date", "").startswith(j))
    p("   %s : %d tentative(s) -> %s" % (j, n, dict(res)))

# ---------------- B) les echecs, tous, regroupes par raison
p("")
p("### B) LES ECHECS - TOUS, REGROUPES PAR RAISON ###")
echecs = [(i, d) for i, d in lignes if str(d.get("resultat", "")) != "range"]
p("nombre total d'echecs :", len(echecs), "sur", len(lignes), "tentatives")
raisons = collections.Counter(str(d.get("raison", "?"))[:95] for _, d in echecs)
for r, n in raisons.most_common():
    p("   %4d x  %s" % (n, r))
cerveaux = collections.Counter(str(d.get("cerveau", "?")) for _, d in echecs)
p("   --- par cerveau ---")
for c, n in cerveaux.most_common():
    p("   %4d x  %s" % (n, c))

# ---------------- C) les tiroirs VRAIMENT utilises
p("")
p("### C) TOUS LES TIROIRS UTILISES PAR LE RANGEMENT ###")
compte = collections.Counter()
pour_les_ranges = 0
for i, d in lignes:
    for t in (d.get("tiroirs") or []):
        compte[str(t)] += 1
    if d.get("resultat") == "range":
        pour_les_ranges += 1
p("rangements reussis :", pour_les_ranges)
p("tiroirs differents utilises :", len(compte))
for t, n in compte.most_common(60):
    p("   %4d x  %s" % (n, t))

# ---------------- D) les tiroirs CREES sans rien demander
p("")
p("### D) LES TIROIRS CREES PAR LE PROGRAMME (champ 'crees') ###")
crees = collections.Counter()
nb_creations = 0
for i, d in lignes:
    c = d.get("crees") or []
    if c:
        nb_creations += 1
        for t in c:
            crees[str(t)] += 1
p("tentatives qui ont cree au moins un tiroir :", nb_creations)
p("tiroirs neufs crees (noms exacts) :", len(crees))
for t, n in crees.most_common(60):
    p("   %4d x  %s" % (n, t))

# ---------------- E) la journee rangee : les doublons
p("")
p("### E) LA JOURNEE RANGEE : journee_rangee.json ###")
try:
    with io.open(os.path.join(D, "journee_rangee.json"), encoding="utf-8", errors="replace") as f:
        jr = json.load(f)
    msgs = jr.get("messages") or []
    p("dernier :", jr.get("dernier"), "| morceaux :", jr.get("morceaux"), "| entrees :", len(msgs))
    if msgs:
        p("cles d'une entree :", sorted(msgs[0].keys()))
        p("dates presentes :", dict(collections.Counter(str(m.get("date", "?"))[:10] for m in msgs)))
        par_q = collections.Counter(str(m.get("qui", "?")) for m in msgs)
        p("qui :", dict(par_q))
        # doublons par numero de ligne
        pareils = collections.Counter()
        for m in msgs:
            texte = str(m.get("fiche") or m.get("ligne") or "")
            cle = (str(m.get("ligne")), hashlib.sha1(texte.encode("utf-8", "replace")).hexdigest())
            pareils[cle] += 1
        dup = [(k, n) for k, n in pareils.items() if n > 1]
        p("")
        p("--- entrees IDENTIQUES (meme numero de ligne ET meme texte) ---")
        p("nombre de groupes en double :", len(dup))
        p("nombre d'entrees en trop (doublons a retirer) :", sum(n - 1 for _, n in dup))
        for (lig, _h), n in sorted(dup, key=lambda x: -x[1])[:15]:
            p("   %4d fois la ligne n° %s" % (n, lig))
        p("")
        p("--- 8 exemples de textes repetes dans la journee ---")
        textes = collections.Counter(str(m.get("fiche") or "") for m in msgs if m.get("fiche"))
        for t, n in textes.most_common(8):
            p("   %3d x  %s" % (n, t[:150]))
except Exception as e:
    p("   !! erreur :", e)

# ---------------- F) le plan : la hierarchie
p("")
p("### F) LE PLAN : LA HIERARCHIE (la ou on en est) ###")
try:
    with io.open(os.path.join(D, "plan_bibliotheque.json"), encoding="utf-8", errors="replace") as f:
        pl = json.load(f)
    ts = pl.get("tiroirs") or []
    sans_parent = [t for t in ts if not (t.get("parent") or t.get("sujet") or t.get("categorie"))]
    petits = [t for t in ts if len(t.get("mots") or []) <= 2]
    par_etat = collections.Counter(str(t.get("etat", "?")) for t in ts)
    p("tiroirs :", len(ts))
    p("etats :", dict(par_etat))
    p("tiroirs SANS categorie parente :", len(sans_parent), "sur", len(ts))
    p("tiroirs avec 2 mots-cles ou moins :", len(petits))
    for t in petits:
        p("   - %s" % t.get("nom"))
except Exception as e:
    p("   !! erreur :", e)

p("")
p("=" * 78)
p("FIN.")
p("=" * 78)

with io.open(RAPPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("RAPPORT ECRIT :", RAPPORT)
