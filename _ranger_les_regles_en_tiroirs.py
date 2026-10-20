# -*- coding: utf-8 -*-
"""v105 (PARTIE B) : LE SCRIPT QUI RANGE LES REGLES EN FICHES, DANS LES TIROIRS.

POURQUOI UN SCRIPT A PART, ET PAS LUCIANA : parce que Fred a exige que le programme en service
reste en LECTURE SEULE sur C:\\Users\\Fred\\Luciana. Ecrire les fiches, c'est un geste qui se
decide et se lance A LA MAIN. Luciana, elle, ne fait que LIRE ce que ce script a ecrit.

CE QU'IL FAIT :
  1) il LIT C:\\Users\\Fred\\Luciana\\consignes.jsonl (jamais il ne l'ecrit, jamais il ne l'efface) ;
  2) il garde les REGLES actives, et il MET DE COTE le NOYAU (les regles qui valent a chaque
     seconde : elles doivent rester sous les yeux de Luciana a chaque message, on ne les range pas) ;
  3) pour chaque autre regle, il cherche dans C:\\Users\\Fred\\Luciana\\bibliotheque le dossier
     (le "tiroir") qui parle du meme sujet, AVEC LE MEME BAREME QUE LE BRAS de Luciana :
        un mot de la regle dans le NOM du dossier : +3 ; dans le nom d'une de ses fiches : +2 ;
     et il faut au moins 3 points, ET un ecart net avec le deuxieme dossier ;
  4) si un tiroir est reconnu : il ECRIT une fiche "regle_nNN_<debut du texte>.md" dans ce dossier,
     avec le TEXTE ENTIER de la regle ;
  5) SI AUCUN TIROIR N'EST RECONNU : IL NE RANGE RIEN. La regle continue de partir en entier a
     chaque message, comme avant. C'est volontaire : mieux vaut une regle qui coute que la mauvaise
     regle dans le mauvais tiroir.

CE QU'IL NE FAIT JAMAIS :
  - il n'efface AUCUN fichier, il n'en renomme aucun, il n'en ecrase aucun (une fiche deja la est
    laissee telle quelle, et il le dit) ;
  - il ne touche PAS a consignes.jsonl, ni a memoire.jsonl, ni a aucun carnet ;
  - il ne cree AUCUN dossier : il ne range que dans des tiroirs qui existent deja.

PAR DEFAUT IL N'ECRIT RIEN. Il montre le plan, et c'est tout :
    python _ranger_les_regles_en_tiroirs.py
Pour ecrire les fiches pour de vrai, il faut le dire explicitement :
    python _ranger_les_regles_en_tiroirs.py --appliquer

LE RETOUR EN ARRIERE EST SIMPLE : efface les fiches "regle_nNN_*.md" que ce script a ecrites (il
en donne la liste), ou passe REGLES_EN_TIROIRS a False dans luciana.py. Dans les deux cas, toutes
les regles repartent en entier a chaque message, comme en v104. Aucune regle n'est jamais perdue :
leur texte est dans consignes.jsonl, qui n'est jamais reecrit.
"""
import json
import os
import re
import sys
import time
import unicodedata

HOME = os.path.expanduser("~")
DOSSIER = os.path.join(HOME, "Luciana")
FICHIER_CONSIGNES = os.path.join(DOSSIER, "consignes.jsonl")
DOSSIER_BIBLIOTHEQUE = os.path.join(DOSSIER, "bibliotheque")

# LE NOYAU : LES MEMES NUMEROS QUE DANS luciana.py (REGLES_NOYAU_NUMEROS). Si tu changes la liste
# la-bas, change-la ici aussi : ce sont les regles qu'on NE RANGE PAS.
REGLES_NOYAU_NUMEROS = (2, 5, 6, 8, 9, 13, 14, 22, 26)
REGLES_NOYAU_MARQUE = "[NOYAU]"

SCORE_MINIMUM = 3        # il faut au moins un mot dans le NOM du tiroir (+3). Un mot croise dans
                         # un nom de fiche (+2) ne suffit pas tout seul : trop facile a confondre.
ECART_MINIMUM = 2        # ... et le deuxieme tiroir doit etre nettement derriere. Sinon : on range
                         # rien. Un tiroir ambigu, c'est la mauvaise regle au mauvais endroit.

GENRE_REGLE = "regle"
GENRE_TACHE = "tache"
BIBLIO_EXTENSIONS = (".txt", ".md", ".json", ".jsonl", ".log", ".csv")
BIBLIO_DOSSIERS_IGNORES = ("anciennes_versions", "anciennes versions", "corbeille", "__pycache__")
MOTS_VIDES = set("""alors aussi autre avant avec avoir bien bon bonne cela celle celui cest cette
comme comment dans depuis donc elle elles encore entre etait etre faire fait faut fois font hein
ici juste leur leurs lui mais meme merci mieux moins mon mes notre nous parce pas peut plus pour
pourquoi quand quel quelle quelque quoi sais sans sera ses sont sous suis sur tant tes tien tiens
toi ton tous tout toute toutes tres trop une vais veux vos votre vous jamais toujours chaque tes
quand doit dois sera etre cela""".split())


def sans_accents(t):
    return "".join(c for c in unicodedata.normalize("NFD", str(t or "").lower())
                   if unicodedata.category(c) != "Mn")


def mots_cles(texte):
    vus = []
    for m in re.findall(r"[A-Za-zÀ-ÿ0-9']{4,}", str(texte or "")):
        m = sans_accents(m.strip("'"))
        if m and m not in MOTS_VIDES and m not in vus:
            vus.append(m)
    return vus


def mots_du_nom(nom):
    return re.sub(r"[^a-z0-9]+", " ", sans_accents(nom)).strip()


def genre_dit(x):
    g = sans_accents(x).strip()
    if g.startswith("regle") or g.startswith("permanent") or g.startswith("conduite"):
        return GENRE_REGLE
    if g.startswith("tache") or g.startswith("note") or g.startswith("projet"):
        return GENRE_TACHE
    return ""


def genre_deduit(importance):
    imp = sans_accents(importance).strip()
    if imp.startswith("capital"):
        return GENRE_REGLE
    if imp.startswith("normal"):
        return GENRE_TACHE
    return GENRE_REGLE


def consignes_actives():
    """LA MEME LECTURE QUE luciana.py : on rejoue le fichier ligne par ligne. Lecture seule."""
    vivantes = {}
    try:
        with open(FICHIER_CONSIGNES, "r", encoding="utf-8", errors="replace") as f:
            lignes = [l for l in f]
    except Exception as ex:
        print("   Impossible de lire %s : %s" % (FICHIER_CONSIGNES, str(ex)[:200]))
        return []
    for brut in lignes:
        brut = brut.strip()
        if not brut:
            continue
        try:
            d = json.loads(brut)
        except Exception:
            continue
        try:
            num = int(d.get("numero") or 0)
        except Exception:
            num = 0
        if not num:
            continue
        action = sans_accents(d.get("action") or "ajouter").strip()
        if action.startswith(("oubli", "retir", "suppr", "fini", "termin")):
            vivantes.pop(num, None)
            continue
        if action.startswith("class"):
            g = genre_dit(d.get("genre"))
            if vivantes.get(num) and g:
                vivantes[num]["genre"] = g
            continue
        texte = str(d.get("texte") or "").strip()
        if not texte:
            continue
        ancienne = vivantes.get(num) or {}
        g = genre_dit(d.get("genre")) or ancienne.get("genre") or genre_deduit(d.get("importance"))
        vivantes[num] = {"numero": num, "texte": texte, "genre": g,
                         "importance": str(d.get("importance") or ancienne.get("importance") or "normale"),
                         "date": ancienne.get("date") or str(d.get("date") or "")}
    return [vivantes[n] for n in sorted(vivantes)]


def est_du_noyau(c):
    if int(c.get("numero") or 0) in REGLES_NOYAU_NUMEROS:
        return True
    return REGLES_NOYAU_MARQUE.lower() in str(c.get("texte") or "").lower()


def les_tiroirs():
    """Les dossiers REELS de la bibliotheque, avec les noms de leurs fiches. Lecture seule."""
    tiroirs = []
    if not os.path.isdir(DOSSIER_BIBLIOTHEQUE):
        return tiroirs

    def parcourir(chemin, relatif, profondeur):
        if profondeur > 3:
            return
        fiches, sous = [], []
        try:
            with os.scandir(chemin) as entrees:
                for e in entrees:
                    try:
                        if e.is_dir():
                            if sans_accents(e.name) not in BIBLIO_DOSSIERS_IGNORES:
                                sous.append(e)
                        elif e.is_file() and e.name.lower().endswith(BIBLIO_EXTENSIONS):
                            fiches.append(e.name)
                    except Exception:
                        continue
        except Exception:
            return
        if fiches and relatif:
            tiroirs.append({"nom": relatif, "chemin": chemin, "fiches": fiches,
                            "cherchable": mots_du_nom(relatif),
                            "fiches_cherchables": " ".join(mots_du_nom(n) for n in fiches)})
        for e in sous:
            parcourir(e.path, (relatif + "/" + e.name) if relatif else e.name, profondeur + 1)

    parcourir(DOSSIER_BIBLIOTHEQUE, "", 1)
    return tiroirs


def le_tiroir_de(regle, tiroirs):
    """Le tiroir qui parle du meme sujet que cette regle, ou None. MEME BAREME QUE LE BRAS de
    Luciana (+3 nom du dossier, +2 nom d'une fiche), plus une exigence d'ECART : si deux tiroirs
    sont au coude a coude, on ne range pas. Mieux rien que le mauvais tiroir."""
    mots = mots_cles(regle.get("texte"))
    if not mots or not tiroirs:
        return None, 0, "aucun mot-cle utilisable dans le texte de la regle"
    notes = []
    for t in tiroirs:
        score = (sum(3 for m in mots if m in t["cherchable"])
                 + sum(2 for m in mots if m in t["fiches_cherchables"]))
        if score:
            notes.append((score, t))
    if not notes:
        return None, 0, "aucun tiroir ne parle de ce sujet"
    notes.sort(key=lambda x: (-x[0], x[1]["nom"]))
    meilleur, t = notes[0]
    if meilleur < SCORE_MINIMUM:
        return None, meilleur, "le meilleur tiroir (%s) ne marque que %d point(s), il en faut %d" % (
            t["nom"], meilleur, SCORE_MINIMUM)
    if len(notes) > 1 and (meilleur - notes[1][0]) < ECART_MINIMUM:
        return None, meilleur, "deux tiroirs se valent (%s et %s) : c'est ambigu, on ne range pas" % (
            t["nom"], notes[1][1]["nom"])
    return t, meilleur, ""


def nom_de_la_fiche(regle):
    debut = mots_du_nom(str(regle.get("texte") or "")[:70]).replace(" ", "_")
    debut = re.sub(r"_+", "_", debut).strip("_")[:50]
    return "regle_n%d_%s.md" % (int(regle["numero"]), debut or "regle")


# ===========================================================================
appliquer = "--appliquer" in sys.argv
print("=" * 88)
print("RANGER LES REGLES EN FICHES, DANS LES TIROIRS   (v105, PARTIE B)")
print("=" * 88)
print("   carnet lu      : %s  (EN LECTURE SEULE)" % FICHIER_CONSIGNES)
print("   bibliotheque   : %s" % DOSSIER_BIBLIOTHEQUE)
print("   mode           : %s" % ("J'ECRIS LES FICHES POUR DE VRAI" if appliquer else
                                  "JE MONTRE LE PLAN, JE N'ECRIS RIEN (--appliquer pour ecrire)"))
print()

if not os.path.exists(FICHIER_CONSIGNES):
    print("   ARRET : le carnet de consignes n'existe pas. Rien n'a ete ecrit.")
    sys.exit(1)
if not os.path.isdir(DOSSIER_BIBLIOTHEQUE):
    print("   ARRET : la bibliotheque n'existe pas. Je ne cree AUCUN dossier (c'est voulu).")
    print("   Cree d'abord les dossiers de sujets a la main, puis relance.")
    sys.exit(1)

actives = consignes_actives()
regles = [c for c in actives if c.get("genre") == GENRE_REGLE]
tiroirs = les_tiroirs()
print("   %d consigne(s) active(s), dont %d REGLE(s). %d tiroir(s) dans la bibliotheque."
      % (len(actives), len(regles), len(tiroirs)))
print()

noyau, a_ranger, sans_tiroir, deja_la = [], [], [], []
for c in regles:
    if est_du_noyau(c):
        noyau.append(c)
        continue
    t, score, pourquoi = le_tiroir_de(c, tiroirs)
    if t is None:
        sans_tiroir.append((c, pourquoi))
        continue
    cible = os.path.join(t["chemin"], nom_de_la_fiche(c))
    if os.path.exists(cible):
        deja_la.append((c, cible))
        continue
    a_ranger.append((c, t, score, cible))

print("-" * 88)
print("LE NOYAU — CES %d REGLES NE SERONT JAMAIS RANGEES (elles partent en entier, a chaque message) :"
      % len(noyau))
for c in noyau:
    print("   n%-4d %s" % (c["numero"], str(c["texte"])[:92]))
if not noyau:
    print("   (aucune : verifie REGLES_NOYAU_NUMEROS, en haut de ce script ET dans luciana.py)")

print()
print("-" * 88)
print("A RANGER — %d regle(s) vont avoir une fiche dans leur tiroir :" % len(a_ranger))
for c, t, score, cible in a_ranger:
    print("   n%-4d -> tiroir \"%s\" (%d points)" % (c["numero"], t["nom"], score))
    print("          %s" % os.path.basename(cible))
    print("          %s" % str(c["texte"])[:92])

print()
print("-" * 88)
print("DEJA RANGEES — %d fiche(s) existent deja, JE N'Y TOUCHE PAS :" % len(deja_la))
for c, cible in deja_la:
    print("   n%-4d %s" % (c["numero"], cible))

print()
print("-" * 88)
print("PAS RANGEES — %d regle(s) restent en entier a chaque message, et c'est VOULU :"
      % len(sans_tiroir))
for c, pourquoi in sans_tiroir:
    print("   n%-4d %s" % (c["numero"], pourquoi))
    print("          %s" % str(c["texte"])[:92])
print("   (une regle sans tiroir reconnu continue de partir EN ENTIER : elle n'est pas perdue,")
print("    elle n'est pas mise de cote, elle s'applique exactement comme avant.)")

if not appliquer:
    print()
    print("=" * 88)
    print("RIEN N'A ETE ECRIT. C'etait le plan. Pour l'executer :")
    print("    python %s --appliquer" % os.path.basename(__file__))
    sys.exit(0)

print()
print("=" * 88)
print("J'ECRIS LES FICHES...")
ecrites, soucis = [], []
for c, t, score, cible in a_ranger:
    contenu = (
        "REGLE n%d DE FRED — rangee en tiroir le %s par %s.\n"
        "TIROIR : %s\n"
        "\n"
        "CETTE LIGNE EST UNE REGLE DE CONDUITE, PAS UNE NOTE. Elle s'applique, au meme titre que\n"
        "celles qui sont dans le carnet a chaque message. Son texte entier, mot pour mot :\n"
        "\n"
        "%s\n"
        "\n"
        "(Le texte d'origine reste ecrit pour toujours dans %s, qui n'est jamais reecrit ni efface.\n"
        " Pour le relire depuis Luciana : outil 'consigne', action 'ouvrir', numero %d.)\n"
        % (c["numero"], time.strftime("%Y-%m-%d %H:%M"), os.path.basename(__file__),
           t["nom"], str(c["texte"]), FICHIER_CONSIGNES, c["numero"]))
    try:
        if os.path.exists(cible):          # ceinture et bretelles : on n'ecrase JAMAIS
            soucis.append("%s existait deja entre-temps : rien ecrit" % cible)
            continue
        with open(cible, "x", encoding="utf-8") as f:   # "x" : refuse d'ecraser, par construction
            f.write(contenu)
            f.flush()
            os.fsync(f.fileno())
        ecrites.append(cible)
    except Exception as ex:
        soucis.append("n%d : %s" % (c["numero"], str(ex)[:160]))

print()
for chemin in ecrites:
    print("   ECRITE : %s (%d octets)" % (chemin, os.path.getsize(chemin)))
print()
print("   %d fiche(s) ecrite(s) pour de vrai." % len(ecrites))
if soucis:
    print("   %d souci(s), et je les dis :" % len(soucis))
    for s in soucis:
        print("     - %s" % s)
print()
print("   consignes.jsonl n'a PAS ete touche : pas une ligne ecrite, pas une ligne effacee.")
print("   Luciana enverra desormais ces %d regle(s) seulement quand le sujet est reconnu."
      % len(ecrites))
print("   POUR TOUT ANNULER : efface les fiches listees ci-dessus, ou mets REGLES_EN_TIROIRS")
print("   a False dans luciana.py. Dans les deux cas, tout repart en entier comme en v104.")
sys.exit(0 if not soucis else 1)
