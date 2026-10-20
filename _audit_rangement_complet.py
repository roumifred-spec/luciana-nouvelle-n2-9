# -*- coding: utf-8 -*-
# =====================================================================
# AUDIT COMPLET DU RANGEMENT (demande de Fred, 06/10/2026 : "tu dois tout
# regarder, pas que les 15").
# LECTURE SEULE : ce script ne fait QUE lire. Il n'ecrit rien dans
# C:\Users\Fred\Luciana. Il ecrit son rapport a cote, sur le Bureau.
# =====================================================================
import json, os, io, collections, hashlib, datetime

D = r"C:\Users\Fred\Luciana"
ICI = os.path.dirname(os.path.abspath(__file__))
RAPPORT = os.path.join(ICI, "res_audit_rangement_complet.txt")
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
                    lignes.append((i, {"__illisible__": str(e)[:90], "__brut__": l[:150]}))
    except Exception as e:
        p("   !! impossible d'ouvrir :", e)
    return lignes


def texte_de(d):
    for k in ("texte", "message", "contenu", "ligne", "phrase", "mot", "resume"):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


def action_de(d):
    for k in ("action", "statut", "type", "etat", "resultat", "quoi"):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return "?"


def tiroir_de(d):
    for k in ("tiroir", "nom_tiroir", "vers", "dossier", "rayon", "cible", "nom"):
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


INTERDITS = ("divers", "fourre", "vrac", "a trier", "à trier", "journee", "journée", "autre", "non classe")

p("=" * 78)
p("AUDIT COMPLET DU RANGEMENT - LUCIANA")
p("Ecrit le", datetime.datetime.now().strftime("%d/%m/%Y a %Hh%M"))
p("LECTURE SEULE - rien n'a ete modifie.")
p("=" * 78)

# ---------------------------------------------------------------- 1
p("")
p("### 1) LE JOURNAL DU RANGEMENT : rangement_journee.jsonl ###")
j = os.path.join(D, "rangement_journee.jsonl")
lignes = lire_jsonl(j)
p("lignes lues :", len(lignes))
if lignes:
    p("cles de la 1re ligne :", sorted(lignes[0][1].keys()))
    p("cles de la 2e ligne  :", sorted(lignes[1][1].keys()) if len(lignes) > 1 else "-")

    actions = collections.Counter(action_de(d) for _, d in lignes)
    p("")
    p("--- les actions vues (comptees) ---")
    for a, n in actions.most_common():
        p("   %5d  %s" % (n, a))

    p("")
    p("--- les tiroirs utilises (tous, pas seulement 15) ---")
    tiroirs = collections.Counter(tiroir_de(d) for _, d in lignes if tiroir_de(d))
    p("nombre de tiroirs differents :", len(tiroirs))
    for t, n in tiroirs.most_common():
        p("   %5d  %s" % (n, t))

    p("")
    p("--- les lignes SANS tiroir ---")
    sans = [(i, d) for i, d in lignes if not tiroir_de(d)]
    p("nombre :", len(sans), "sur", len(lignes))
    for i, d in sans[:25]:
        p("   ligne %d : %s" % (i, json.dumps(d, ensure_ascii=False)[:180]))

    p("")
    p("--- un nom de tiroir INTERDIT est-il apparu ? ---")
    troubles = [(i, tiroir_de(d)) for i, d in lignes if any(x in tiroir_de(d).lower() for x in INTERDITS)]
    p("nombre :", len(troubles))
    for i, t in troubles[:25]:
        p("   ligne %d : %s" % (i, t))

    p("")
    p("--- DOUBLONS : le meme texte range deux fois ---")
    vus = {}
    doublons = []
    for i, d in lignes:
        t = texte_de(d)
        if not t:
            continue
        h = hashlib.sha1(t.encode("utf-8", "replace")).hexdigest()
        if h in vus:
            doublons.append((vus[h], i, t[:110]))
        else:
            vus[h] = i
    p("doublons exacts :", len(doublons))
    for a, b, t in doublons[:40]:
        p("   ligne %d <-> ligne %d : %s" % (a, b, t))

    p("")
    p("--- 5 dernieres lignes, en clair (pour voir la forme) ---")
    for i, d in lignes[-5:]:
        p("   %s" % json.dumps(d, ensure_ascii=False)[:400])

# ---------------------------------------------------------------- 2
p("")
p("### 2) LE JOURNAL DES TIROIRS : journal_tiroirs.jsonl ###")
j2 = os.path.join(D, "journal_tiroirs.jsonl")
l2 = lire_jsonl(j2)
p("lignes lues :", len(l2))
if l2:
    p("cles de la 1re ligne :", sorted(l2[0][1].keys()))
    a2 = collections.Counter(action_de(d) for _, d in l2)
    p("--- actions ---")
    for a, n in a2.most_common():
        p("   %5d  %s" % (n, a))
    t2 = collections.Counter(tiroir_de(d) for _, d in l2 if tiroir_de(d))
    p("--- tiroirs (%d differents) ---" % len(t2))
    for t, n in t2.most_common():
        p("   %5d  %s" % (n, t))
    p("--- 5 dernieres lignes ---")
    for i, d in l2[-5:]:
        p("   %s" % json.dumps(d, ensure_ascii=False)[:400])

# ---------------------------------------------------------------- 3
p("")
p("### 3) LA JOURNEE RANGEE : journee_rangee.json ###")
j3 = os.path.join(D, "journee_rangee.json")
try:
    with io.open(j3, encoding="utf-8", errors="replace") as f:
        jr = json.load(f)
    p("type a la racine :", type(jr).__name__)
    if isinstance(jr, dict):
        for k, v in jr.items():
            if isinstance(v, (list, dict)):
                p("   %s : %s, %d element(s)" % (k, type(v).__name__, len(v)))
            else:
                p("   %s : %r" % (k, v))
        listes = [(k, v) for k, v in jr.items() if isinstance(v, list)]
        for k, v in listes:
            p("")
            p("   --- la liste '%s' : %d elements ---" % (k, len(v)))
            if v and isinstance(v[0], dict):
                p("   cles d'un element :", sorted(v[0].keys()))
            textes = collections.Counter()
            for e in v:
                if isinstance(e, dict):
                    t = texte_de(e)
                    if t:
                        textes[t] += 1
            dup = [(t, n) for t, n in textes.items() if n > 1]
            p("   textes repetes a l'identique :", len(dup))
            for t, n in sorted(dup, key=lambda x: -x[1])[:25]:
                p("      %dx : %s" % (n, t[:150]))
    elif isinstance(jr, list):
        p("elements :", len(jr))
        p("cles d'un element :", sorted(jr[0].keys()) if jr and isinstance(jr[0], dict) else "-")
except Exception as e:
    p("   !! erreur :", e)

# ---------------------------------------------------------------- 4
p("")
p("### 4) LE PLAN DE LA BIBLIOTHEQUE : les 42 tiroirs ###")
j4 = os.path.join(D, "plan_bibliotheque.json")
try:
    with io.open(j4, encoding="utf-8", errors="replace") as f:
        pl = json.load(f)
    tiroirs = pl.get("tiroirs") if isinstance(pl, dict) else None
    if isinstance(pl, dict):
        p("cles a la racine :", sorted(pl.keys()))
    if isinstance(tiroirs, list):
        p("nombre de tiroirs :", len(tiroirs))
        p("cles d'un tiroir :", sorted(tiroirs[0].keys()) if tiroirs else "-")
        p("")
        p("--- CHAQUE TIROIR, avec ses champs ---")
        for t in tiroirs:
            nom = t.get("nom", "?")
            etat = t.get("etat", "?")
            mots = t.get("mots") or t.get("mots_cles") or t.get("motscles") or []
            parent = t.get("parent") or t.get("sujet") or t.get("categorie") or ""
            contient = (t.get("contient") or "")[:60]
            p("   - %s  [%s]  parent=%r  mots=%d  contient=%r" % (nom, etat, parent, len(mots) if isinstance(mots, list) else -1, contient))
    else:
        p("structure inattendue :", type(tiroirs).__name__)
        p(json.dumps(pl, ensure_ascii=False)[:1500])
except Exception as e:
    p("   !! erreur :", e)

# ---------------------------------------------------------------- 5
p("")
p("### 5) LE COMPTE FINAL (les chiffres a retenir) ###")
p("lignes du journal du rangement :", len(lignes))
if lignes:
    a = collections.Counter(action_de(d) for _, d in lignes)
    for k, n in a.most_common():
        p("   %s : %d" % (k, n))
    p("lignes sans tiroir :", len([1 for _, d in lignes if not tiroir_de(d)]))
    p("lignes a nom interdit :", len([1 for _, d in lignes if any(x in tiroir_de(d).lower() for x in INTERDITS)]))
    p("doublons exacts :", len(doublons) if lignes else 0)

p("")
p("=" * 78)
p("FIN DE L'AUDIT.")
p("=" * 78)

with io.open(RAPPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))

print("RAPPORT ECRIT :", RAPPORT)
print("lignes du rapport :", len(OUT))
