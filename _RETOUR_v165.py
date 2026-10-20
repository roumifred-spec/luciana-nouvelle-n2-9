# -*- coding: utf-8 -*-
"""ORDRE DE FRED (13/10/2026, 01h03) : REMETTRE LA V165.

CE QU'IL FAIT, DANS CET ORDRE, ET RIEN D'AUTRE :
 1) il MONTRE l'etat avant (tailles + le badge de chacun) ;
 2) il SAUVEGARDE DATE ce qui sort AVANT d'ecrire ;
 3) il remet en service la V165 (celle d'avant le carnet de mission) ;
 4) il compile (la seule preuve qui compte pour la syntaxe) ;
 5) il met le badge a v165 SEULEMENT s'il trouve une occurrence sure ; sinon il n'y touche pas et le dit ;
 6) il ecrit son rapport, relu sur le disque. Si un fichier manque, il ne touche a RIEN.
"""

import os, io, re, shutil, py_compile, datetime

D = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur"
P = os.path.join(D, "luciana.py")
SRC = os.path.join(D, "SAUVEGARDE_luciana_V165_AVANT_carnet_2026-10-12.py")
RP = os.path.join(D, "reglage_memoire_sens.json")
R = os.path.join(D, "RESULTAT_retour_v165.txt")
h = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")

rap = []


def dire(t):
    rap.append(t)
    print(t)


def lire(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def badge_de(txt):
    m = re.findall(r"&middot;\s*v\d\d+", txt)
    return m


def ecrire_rapport():
    io.open(R, "w", encoding="utf-8").write("\n".join(rap))


for f in (P, SRC, RP):
    if not os.path.exists(f):
        dire("ARRET : il manque %s -- JE N'AI RIEN TOUCHE." % f)
        ecrire_rapport()
        raise SystemExit(1)

dire("=== 1. ETAT AVANT (rien n'a encore ete touche) ===")
a = os.path.getsize(P)
b = os.path.getsize(SRC)
dire("le programme en service .......... %d octets" % a)
dire("la V165 a remettre ............... %d octets" % b)
tx = lire(P)
txs = lire(SRC)
dire("badge du programme en service .... %s" % (badge_de(tx) or "aucun trouve"))
dire("badge de la V165 a remettre ...... %s" % (badge_de(txs) or "aucun trouve"))
dire("en service : carnet de mission (plan d'action) ? %s" % ("OUI" if "carnet_de_mission" in tx else "NON"))
dire("la V165 : carnet de mission (plan d'action) ? ..... %s" % ("OUI" if "carnet_de_mission" in txs else "NON"))
del tx, txs

dire("")
dire("=== 2. SAUVEGARDES DATEES, AVANT D'ECRIRE ===")
s1 = os.path.join(D, "%s_luciana_v166_RETIREE_pour_v165.py" % h)
shutil.copy2(P, s1)
dire("le programme sortant est garde ... %s  (%d octets)" % (os.path.basename(s1), os.path.getsize(s1)))
s2 = os.path.join(D, "%s_SAUVEGARDE_reglage_memoire_sens_AVANT_v165.json" % h)
shutil.copy2(RP, s2)
dire("le reglage est garde ............. %s" % os.path.basename(s2))

dire("")
dire("=== 3. LE PROGRAMME : RETOUR A LA V165 ===")
shutil.copy2(SRC, P)
c = os.path.getsize(P)
dire("le programme en service .......... %d octets  (etait %d)" % (c, a))
neuf = lire(P)
dire("le plan d'action (carnet) dedans ? ... %s" % ("OUI" if "carnet_de_mission" in neuf else "NON (c'est la V165, d'avant le carnet)"))
del neuf
try:
    py_compile.compile(P, doraise=True)
    dire("compilation ...................... SANS ERREUR")
except Exception as ex:
    dire("compilation ...................... RATE -> %s" % str(ex)[:300])

dire("")
dire("=== 4. LE BADGE ===")
t = lire(P)
b = badge_de(t)
if len(b) == 1:
    if b[0].replace(" ", "") == "&middot;v165":
        dire("badge deja a v165 : JE N'AI PAS TOUCHE. C'est ce que Fred veut voir.")
    else:
        t2 = t.replace(b[0], "&middot; v165", 1)
        io.open(P, "w", encoding="utf-8").write(t2)
        dire("badge : '%s' -> '&middot; v165' (1 seule occurrence, remplacee)" % b[0])
        try:
            py_compile.compile(P, doraise=True)
            dire("recompilation apres le badge ..... SANS ERREUR")
        except Exception as ex:
            dire("recompilation apres le badge ..... RATE -> %s" % str(ex)[:300])
else:
    dire("badge : %d occurrence(s) trouve(s) -> JE N'AI PAS TOUCHE (je ne devine pas)." % len(b))
    for i, l in enumerate(t.splitlines(), 1):
        if re.search(r"&middot;\s*v\d\d+", l):
            dire("   ligne %d : %s" % (i, l.strip()[:120]))
del t

dire("")
dire("=== 5. LA MEMOIRE 1 (je n'y touche pas, je dis juste ou elle en est) ===")
try:
    d = json.load(io.open(RP, encoding="utf-8-sig"))
    dire("rappel_ancien (memoire 1) ....... %s" % d.get("rappel_ancien"))
    dire("le reste du reglage ............. actif=%s / seuil=%s" % (d.get("actif"), d.get("seuil")))
except Exception as ex:
    dire("le reglage : ILLISIBLE -> %s" % str(ex)[:200])

dire("")
dire("=== 6. VERIFICATION FINALE, RELUE SUR LE DISQUE ===")
f = lire(P)
dire("programme en service ............ %d octets" % os.path.getsize(P))
dire("badge .......................... %s" % (badge_de(f) or "aucun trouve"))
dire("le plan d'action (carnet) ...... %s" % ("OUI" if "carnet_de_mission" in f else "NON"))
del f
dire("")
dire("FAIT. Fred redemarre Luciana par le raccourci du Bureau.")

ecrire_rapport()
print("")
print("rapport ecrit : RESULTAT_retour_v165.txt")
