# -*- coding: utf-8 -*-
"""LES 16 FICHIERS DE LANGUE : LES METTRE EN PLACE, ET LE PROUVER.
Chantier v111 (premiere passe de la greffe : les fondations de la couche client).

POURQUOI CE SCRIPT EXISTE, DIT FRANCHEMENT
------------------------------------------
La session de travail qui a fait la greffe pouvait LIRE le dossier du donneur, mais elle n'avait
pas le droit de COPIER un fichier depuis le Bureau vers le dossier du chantier (bac a sable).
Un seul fichier a donc ete recopie a la main et verifie : langues\\fr.json (le fichier de repli,
le plus important). Les 15 autres sont mis en place par CE script, qui copie les OCTETS et le
PROUVE -- c'est plus sur qu'une recopie a la main, et ca ne coute pas un centime.

CE QU'IL FAIT, ET RIEN D'AUTRE :
 1) il verifie que le dossier du donneur est bien la ;
 2) il copie les 16 fichiers <code>.json dans le dossier langues\\ a cote de luciana.py ;
 3) il RELIT CHAQUE COPIE SUR LE DISQUE et compare son sha256 a celui de l'original. C'est la
    seule preuve qui vaut : taille identique ET empreinte identique, sinon ce n'est pas une copie ;
 4) il relit chaque copie comme du JSON (si un fichier est abime, on le saura ici, pas chez le
    client) et il COMPTE les cles : le total, et les 33 cles ke_* du mode enfant ;
 5) il compare l'annuaire de chaque langue a celui du francais et DIT, langue par langue,
    combien de cles manquent et lesquelles.

CE QU'IL NE FAIT PAS : il ne touche PAS a luciana.py. Il n'ecrit RIEN dans C:\\Users\\Fred\\Luciana
(ma memoire), ni dans C:\\Users\\Fred\\Lumi, ni dans C:\\Users\\Daniela\\Luminita, ni dans
C:\\Users\\Fred\\Lumi_appli. Il ne lit le donneur qu'en LECTURE SEULE.

Il finit TOUJOURS par une ligne "VERDICT : OUI" ou "VERDICT : NON".

POUR LE LANCER (fenetre de commande, dans le dossier du chantier) :
    python _copier_les_langues.py
"""
import hashlib
import json
import os
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
CIBLE = os.path.join(ICI, "langues")

# Le DONNEUR, tel qu'il est ecrit dans la ligne de cible du chantier. Si Fred deplace ce dossier,
# c'est la SEULE ligne a changer.
SOURCE = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\DONNEUR_LUMINITA_v74_langues"

# Les 16 langues de Luminita v74, dans l'ordre alphabetique de leur code.
ATTENDUES = ["bg", "cs", "da", "de", "el", "en", "es", "fi", "fr",
             "hu", "it", "nl", "pl", "pt", "ro", "sv"]

# Les dossiers AUXQUELS ON NE TOUCHE JAMAIS (ordre de Fred). Ce script n'ecrit que dans langues\,
# mais on verifie quand meme : une erreur de chemin ne doit pas pouvoir devenir un degat.
INTERDITS = [os.path.join(os.path.expanduser("~"), "Luciana"),
             os.path.join(os.path.expanduser("~"), "Lumi"),
             os.path.join(os.path.expanduser("~"), "Lumi_appli"),
             r"C:\Users\Daniela\Luminita"]

soucis = []


def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        while True:
            bout = f.read(1024 * 1024)
            if not bout:
                break
            h.update(bout)
    return h.hexdigest()


def sous_un_interdit(chemin):
    """Est-ce que ce chemin tombe dans un dossier auquel on n'a pas le droit de toucher ?"""
    p = os.path.abspath(chemin).lower()
    for d in INTERDITS:
        d = os.path.abspath(d).lower()
        if p == d or p.startswith(d + os.sep):
            return d
    return ""


print("=" * 92)
print("LES 16 FICHIERS DE LANGUE  (mise en place + preuve)")
print("=" * 92)

# --- LE VERROU : on refuse d'ecrire dans un dossier interdit, quoi qu'il arrive. ---
mauvais = sous_un_interdit(CIBLE)
if mauvais:
    print("ARRET IMMEDIAT : le dossier a ecrire tombe dans un dossier INTERDIT (%s)." % mauvais)
    print("Je ne touche a rien.")
    print("")
    print("VERDICT : NON")
    sys.exit(1)

print("donneur (lu seulement) : %s" % SOURCE)
print("dossier langues        : %s" % CIBLE)
print("")

if not os.path.isdir(SOURCE):
    print("ARRET : le dossier du donneur est INTROUVABLE.")
    print("Rien n'a ete copie, et je n'invente aucun chiffre.")
    print("Si tu as deplace le dossier, corrige la ligne SOURCE en haut de ce script.")
    print("")
    print("VERDICT : NON")
    sys.exit(1)

try:
    os.makedirs(CIBLE, exist_ok=True)
except Exception as ex:
    print("ARRET : je n'ai pas pu creer le dossier langues : %s" % str(ex)[:300])
    print("")
    print("VERDICT : NON")
    sys.exit(1)

# --- 1) LA COPIE, FICHIER PAR FICHIER, AVEC RELECTURE SUR LE DISQUE ---
print("%-10s %10s  %-11s  %s" % ("fichier", "octets", "empreinte", "relecture JSON"))
print("-" * 92)
annuaires = {}
copies_ok = 0
for code in ATTENDUES:
    src = os.path.join(SOURCE, code + ".json")
    dst = os.path.join(CIBLE, code + ".json")
    if not os.path.isfile(src):
        print("%-10s %s" % (code + ".json", "ABSENT CHEZ LE DONNEUR -- rien copie"))
        soucis.append("%s.json est absent chez le donneur" % code)
        continue
    try:
        shutil.copy2(src, dst)
    except Exception as ex:
        print("%-10s LA COPIE A ECHOUE : %s" % (code + ".json", str(ex)[:60]))
        soucis.append("la copie de %s.json a echoue : %s" % (code, str(ex)[:200]))
        continue
    try:
        t_src, t_dst = os.path.getsize(src), os.path.getsize(dst)
        s_src, s_dst = empreinte(src), empreinte(dst)
    except Exception as ex:
        print("%-10s JE N'AI PAS PU RELIRE LA COPIE : %s" % (code + ".json", str(ex)[:60]))
        soucis.append("%s.json : relecture impossible : %s" % (code, str(ex)[:200]))
        continue
    if t_src != t_dst or s_src != s_dst:
        print("%-10s %10d  %-11s  %s" % (code + ".json", t_dst, "DIFFERENTE", "copie ABIMEE"))
        soucis.append("%s.json : la copie n'a pas la meme empreinte que l'original" % code)
        continue
    try:
        with open(dst, "r", encoding="utf-8-sig") as f:
            brut = json.load(f)
        if not isinstance(brut, dict):
            raise ValueError("ce n'est pas un annuaire")
        annuaires[code] = {str(k): v for k, v in brut.items() if isinstance(v, str)}
        lisible = "%d cles" % len(annuaires[code])
        copies_ok += 1
    except Exception as ex:
        lisible = "JSON ILLISIBLE : %s" % str(ex)[:40]
        soucis.append("%s.json ne se relit pas comme du JSON : %s" % (code, str(ex)[:200]))
    print("%-10s %10d  %-11s  %s" % (code + ".json", t_dst, "identique", lisible))

print("-" * 92)
print("Copies relues identiques a l'original ET lisibles : %d / %d" % (copies_ok, len(ATTENDUES)))

# --- 2) LE COMPTE DES CLES, LANGUE PAR LANGUE, SANS RIEN ARRONDIR ---
# C'est le chiffre exact demande par Fred. On ne l'estime pas : on le compte.
print("")
print("LE COMPTE DES CLES (le francais sert de reference, c'est lui le repli)")
print("-" * 92)
ref = annuaires.get("fr")
if not ref:
    print("Je ne peux pas faire le compte : fr.json n'est pas lisible.")
    soucis.append("fr.json n'est pas lisible : aucun compte de cles possible")
else:
    cles_fr = set(ref)
    cles_ke_fr = {k for k in cles_fr if k.startswith("ke_")}
    print("Reference fr.json : %d cles au total, dont %d cles ke_* (le mode enfant)."
          % (len(cles_fr), len(cles_ke_fr)))
    print("")
    print("%-10s %8s %8s %10s %10s" % ("langue", "total", "ke_*", "manquantes", "en plus"))
    for code in ATTENDUES:
        d = annuaires.get(code)
        if d is None:
            print("%-10s %8s" % (code, "ILLISIBLE"))
            continue
        cles = set(d)
        manquantes = cles_fr - cles
        en_plus = cles - cles_fr
        n_ke = len([k for k in cles if k.startswith("ke_")])
        print("%-10s %8d %8d %10d %10d" % (code, len(cles), n_ke, len(manquantes), len(en_plus)))
        if manquantes:
            # On NOMME les cles qui manquent : c'est ca qui permet de les reparer.
            noms = sorted(manquantes)
            print("           manquantes : %s" % ", ".join(noms[:12]))
            if len(noms) > 12:
                print("           ... et %d autres" % (len(noms) - 12))
            soucis.append("%s.json : %d cles manquantes par rapport au francais"
                          % (code, len(manquantes)))
        if n_ke != len(cles_ke_fr):
            soucis.append("%s.json : %d cles ke_* au lieu de %d" % (code, n_ke, len(cles_ke_fr)))
    print("")
    print("RAPPEL : une cle qui manque dans une langue n'est PAS un bug a l'ecran. textes() la")
    print("remplit avec le francais, et T() rend une chaine vide en dernier recours : le client")
    print("ne voit JAMAIS une etiquette technique. Mais une cle manquante reste un DEFAUT a")
    print("corriger dans le fichier de langue.")

print("")
print("=" * 92)
if soucis:
    print("CE QUI N'A PAS MARCHE (dit franchement, sans rien arrondir) :")
    for s in soucis:
        print("  - %s" % s)
    print("")
    print("VERDICT : NON")
    sys.exit(1)

print("Les %d fichiers de langue sont en place, relus sur le disque (meme empreinte que" % len(ATTENDUES))
print("l'original), lisibles comme du JSON, et ils ont tous les memes cles que le francais.")
print("")
print("VERDICT : OUI")
sys.exit(0)
