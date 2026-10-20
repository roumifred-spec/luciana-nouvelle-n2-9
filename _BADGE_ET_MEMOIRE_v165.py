# -*- coding: utf-8 -*-
"""SUITE DU RETOUR v165 (13/10/2026, 01h03) : LE BADGE ET LA MEMOIRE 1.

Le premier passage a pose la V165 (compilation sans erreur) mais deux choses restaient :
 - le badge : introuvable avec mon premier motif -> je le cherche AUTREMENT, sur la ligne unique qui dit "ton amie" ;
 - la memoire 1 : mon premier script avait oublie d'importer json -> je la LIS pour de vrai, maintenant.

CE QU'IL FAIT, ET RIEN D'AUTRE : il lit, il corrige le badge SEULEMENT s'il trouve une ligne sure et unique, il recompile, il ecrit son rapport.
"""

import os, io, re, json, py_compile

D = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur"
P = os.path.join(D, "luciana.py")
RP = os.path.join(D, "reglage_memoire_sens.json")
R = os.path.join(D, "RESULTAT_badge_et_memoire_v165.txt")

rap = []


def dire(t):
    rap.append(t)
    print(t)


def lire(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


dire("=== 1. LA MEMOIRE 1 (le reglage, lu pour de vrai) ===")
try:
    d = json.load(io.open(RP, encoding="utf-8-sig"))
    dire("rappel_ancien (memoire 1) ....... %s" % d.get("rappel_ancien"))
    dire("le reste du reglage ............. actif=%s / seuil=%s" % (d.get("actif"), d.get("seuil")))
except Exception as ex:
    dire("reglage ILLISIBLE -> %s" % str(ex)[:200])

dire("")
dire("=== 2. LE BADGE, CHERCHE SUR LA BONNE LIGNE ===")
t = lire(P)
avant_taille = len(t)
lignes = t.splitlines()
for i, l in enumerate(lignes, 1):
    if "ton amie" in l:
        dire("ligne %d (ton amie) : %s" % (i, l.strip()[:200]))
cibles = [l for l in lignes if "ton amie" in l]

if len(cibles) == 1:
    l = cibles[0]
    m = re.search(r"v\d+", l)
    if not m:
        dire("aucun numero 'vXXX' sur cette ligne : JE N'AI PAS TOUCHE.")
    elif m.group(0) == "v165":
        dire("le badge dit DEJA v165 : JE N'AI PAS TOUCHE. C'est ce que Fred veut voir.")
    else:
        nl = l[:m.start()] + "v165" + l[m.end():]
        io.open(P, "w", encoding="utf-8").write(t.replace(l, nl, 1))
        dire("badge : '%s' -> '%s'" % (m.group(0), "v165"))
        dire("        (une seule ligne 'ton amie', remplacee telle quelle, rien d'autre touche)")
        try:
            py_compile.compile(P, doraise=True)
            dire("recompilation apres le badge ..... SANS ERREUR")
        except Exception as ex:
            dire("recompilation apres le badge ..... RATE -> %s" % str(ex)[:300])
else:
    dire("j'ai trouve %d ligne(s) 'ton amie' -> JE N'AI PAS TOUCHE (je ne devine pas)." % len(cibles))
del t

dire("")
dire("=== 3. VERIFICATION FINALE, RELUE SUR LE DISQUE ===")
f = lire(P)
taille = os.path.getsize(P)
badge = "aucun"
for l in f.splitlines():
    if "ton amie" in l:
        mm = re.search(r"v\d+", l)
        if mm:
            badge = mm.group(0)
dire("programme en service ............ %d octets (texte : %d caracteres avant, %d apres)" % (taille, avant_taille, len(f)))
dire("badge .......................... %s" % badge)
dire("le plan d'action (carnet) ...... %s" % ("OUI" if "carnet_de_mission" in f else "NON (la V165 est d'avant le carnet)"))
try:
    py_compile.compile(P, doraise=True)
    dire("compilation finale ............. SANS ERREUR")
except Exception as ex:
    dire("compilation finale ............. RATE -> %s" % str(ex)[:300])
del f

dire("")
dire("FAIT.")

io.open(R, "w", encoding="utf-8").write("\n".join(rap))
print("")
print("rapport ecrit : RESULTAT_badge_et_memoire_v165.txt")
