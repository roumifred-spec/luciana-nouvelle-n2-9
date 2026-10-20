# -*- coding: utf-8 -*-
"""ORDRE DE FRED (13/10/2026, 00h53) : REMETTRE LA v166 (celle d'avant le debranchement du
rappel) ET REBRANCHER LA MEMOIRE 1.

CE QU'IL FAIT, DANS CET ORDRE, ET RIEN D'AUTRE :
 1) il MONTRE l'etat avant (tailles, et si l'interrupteur est la) ;
 2) il SAUVEGARDE DATE ce qui sort (le programme actuel + le reglage) AVANT d'ecrire ;
 3) il remet en service la v166 d'avant le 12/10 22h40 ;
 4) il compile (la seule preuve qui compte pour la syntaxe) ;
 5) il REBRANCHE la memoire 1 : rappel_ancien = true dans le reglage du sens ;
 6) il ecrit son rapport. Si un fichier manque, il ne touche a RIEN.
"""

import os, io, json, shutil, py_compile, datetime

D = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur"
P = os.path.join(D, "luciana.py")
SRC = os.path.join(D, "SAUVEGARDE_luciana_AVANT_debranchement_rappel_ancien_2026-10-12_22h40.py")
RP = os.path.join(D, "reglage_memoire_sens.json")
R = os.path.join(D, "RESULTAT_retour_v166_et_memoire1.txt")
h = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")

rap = []


def dire(t):
    rap.append(t)
    print(t)


for f in (P, SRC, RP):
    if not os.path.exists(f):
        dire("ARRET : il manque %s -- JE N'AI RIEN TOUCHE." % f)
        io.open(R, "w", encoding="utf-8").write("\n".join(rap))
        raise SystemExit(1)

dire("=== 1. ETAT AVANT (rien n'a encore ete touche) ===")
a = os.path.getsize(P)
b = os.path.getsize(SRC)
dire("le programme en service .......... %d octets" % a)
dire("la v166 d'avant, a remettre ...... %d octets" % b)
avant = io.open(P, encoding="utf-8", errors="replace").read()
dire("en service : l'interrupteur _rappel_ancien_actif ? %s" % ("OUI" if "_rappel_ancien_actif" in avant else "NON"))
del avant

dire("")
dire("=== 2. SAUVEGARDES DATEES, AVANT D'ECRIRE ===")
s1 = os.path.join(D, "%s_luciana_v166_modifiee_RETIREE.py" % h)
shutil.copy2(P, s1)
dire("le programme sortant est garde ... %s  (%d octets)" % (os.path.basename(s1), os.path.getsize(s1)))
s2 = os.path.join(D, "%s_SAUVEGARDE_reglage_memoire_sens_AVANT_rappel_ON.json" % h)
shutil.copy2(RP, s2)
dire("le reglage est garde ............. %s" % os.path.basename(s2))

dire("")
dire("=== 3. LE PROGRAMME : RETOUR A LA v166 D'AVANT ===")
shutil.copy2(SRC, P)
c = os.path.getsize(P)
dire("le programme en service .......... %d octets  (etait %d)" % (c, a))
neuf = io.open(P, encoding="utf-8", errors="replace").read()
dire("le PLAN D'ACTION (carnet de mission) est dedans ? ... %s" % ("OUI" if "carnet_de_mission" in neuf else "NON"))
dire("l'interrupteur _rappel_ancien_actif dedans ? ........ %s" % ("OUI" if "_rappel_ancien_actif" in neuf else "NON"))
del neuf
try:
    py_compile.compile(P, doraise=True)
    dire("compilation ...................... SANS ERREUR")
except Exception as ex:
    dire("compilation ...................... RATE -> %s" % str(ex)[:300])

dire("")
dire("=== 4. LE BADGE (regle de Fred : le numero doit evoluer) ===")
t = io.open(P, encoding="utf-8", errors="replace").read()
trouve = None
for n in ("166", "165", "164", "163"):
    m = "&middot; v" + n
    if t.count(m) == 1:
        trouve = m
        break
if trouve:
    t2 = t.replace(trouve, "&middot; v167", 1)
    io.open(P, "w", encoding="utf-8").write(t2)
    dire("badge : '%s' -> '&middot; v167' (1 seule occurrence, remplacee)" % trouve)
    try:
        py_compile.compile(P, doraise=True)
        dire("recompilation apres le badge ..... SANS ERREUR")
    except Exception as ex:
        dire("recompilation apres le badge ..... RATE -> %s" % str(ex)[:300])
else:
    dire("badge : je n'ai trouve AUCUNE ligne sure (0 ou plusieurs occurrences) : JE N'AI PAS TOUCHE.")
    dire("        le badge restera donc celui de la v166.")
del t

dire("")
dire("=== 5. LA MEMOIRE 1 : REBRANCHEE ===")
try:
    d = json.load(io.open(RP, encoding="utf-8-sig"))
    av = d.get("rappel_ancien", "(absent)")
    d["rappel_ancien"] = True
    io.open(RP, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    d2 = json.load(io.open(RP, encoding="utf-8-sig"))
    dire("rappel_ancien : avant = %s  /  apres = %s" % (av, d2.get("rappel_ancien")))
    dire("le reste du reglage intact ? ...... actif=%s / seuil=%s" % (d2.get("actif"), d2.get("seuil")))
except Exception as ex:
    dire("le reglage : RATE -> %s" % str(ex)[:300])

dire("")
dire("=== 6. VERIFICATION FINALE, RELUE SUR LE DISQUE ===")
dire("programme en service ............ %d octets" % os.path.getsize(P))
d3 = json.load(io.open(RP, encoding="utf-8-sig"))
dire("rappel_ancien (memoire 1) ....... %s" % d3.get("rappel_ancien"))
dire("")
dire("FAIT. Fred redemarre Luciana par le raccourci du Bureau pour voir le nouveau programme.")
dire("(la memoire 1, elle, est deja rebranchee : ce reglage est relu a chaque message)")

io.open(R, "w", encoding="utf-8").write("\n".join(rap))
print("")
print("rapport ecrit : RESULTAT_retour_v166_et_memoire1.txt")
