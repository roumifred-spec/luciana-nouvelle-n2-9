# -*- coding: utf-8 -*-
import os, re, shutil, subprocess, sys, datetime

ATELIER = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
SERVICE = r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96"
SRC = os.path.join(ATELIER, "luciana.py")
DST = os.path.join(SERVICE, "luciana.py")
SORTIE = os.path.join(SERVICE, "res_v115.txt")

L = []
def dire(x=""):
    L.append(str(x))

def sauve():
    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

dire("=== 1) LES DEUX FICHIERS AVANT ===")
dire("source (atelier) : %d octets" % os.path.getsize(SRC))
dire("cible (service) : %d octets" % os.path.getsize(DST))
sauve()

dire("")
dire("=== 2) COMPILATION DU SOURCE (atelier) ===")
r = subprocess.run([sys.executable, "-m", "py_compile", SRC], capture_output=True, text=True)
dire("py_compile atelier, code retour : %s (0 = compile)" % r.returncode)
if r.returncode:
    dire(r.stderr[:2000])
sauve()

dire("")
dire("=== 3) LE CONTROLE _verif_rangement_journee.py ===")
try:
    r3 = subprocess.run([sys.executable, "_verif_rangement_journee.py"], cwd=ATELIER, capture_output=True, text=True, timeout=900)
    dire("code retour : %s" % r3.returncode)
    dire("---- sortie ----")
    dire(r3.stdout[-7000:])
    if r3.stderr:
        dire("---- erreurs ----")
        dire(r3.stderr[-2000:])
except Exception as e:
    dire("EXCEPTION au lancement du controle : %r" % e)
sauve()

dire("")
dire("=== 4) SAUVEGARDE DATEE DU FICHIER EN SERVICE ===")
quand = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")
sauv = os.path.join(SERVICE, "%s_luciana_v114_sauvegarde_AVANT_v115.py" % quand)
shutil.copy2(DST, sauv)
dire("sauvegarde ecrite : %s" % sauv)
dire("taille sauvegarde : %d octets" % os.path.getsize(sauv))
sauve()

dire("")
dire("=== 5) COPIE DU SOURCE PAR-DESSUS ===")
shutil.copy2(SRC, DST)
dire("cible apres copie : %d octets" % os.path.getsize(DST))
sauve()

dire("")
dire("=== 6) LE BADGE (ecriture binaire) ===")
with open(DST, "rb") as f:
    data = f.read()
trouves = sorted(set(re.findall(rb"ton amie &middot; v\d+", data)))
dire("badges trouves avant : %s" % [t.decode() for t in trouves])
data2 = re.sub(rb"ton amie &middot; v\d+", b"ton amie &middot; v115", data)
with open(DST, "wb") as f:
    f.write(data2)
dire("taille apres ecriture badge : %d octets" % os.path.getsize(DST))
with open(DST, "rb") as f:
    data3 = f.read()
dire("verif 'ton amie v115' : %d fois" % data3.count(b"ton amie &middot; v115"))
dire("anciens badges restants (v110 a v114) : %d fois" % len(re.findall(rb"ton amie &middot; v11[0-4]", data3)))
sauve()

dire("")
dire("=== 7) py_compile SUR LE FICHIER EN SERVICE ===")
r7 = subprocess.run([sys.executable, "-m", "py_compile", DST], capture_output=True, text=True)
dire("code retour : %s (0 = compile)" % r7.returncode)
if r7.returncode:
    dire(r7.stderr[:2000])
sauve()

dire("")
dire("=== 8) LES REPERES DU CHANTIER DANS LE FICHIER EN SERVICE ===")
for motif in [b"RANGEMENT_REVEIL_SECONDES", b"RANGEMENT_PAUSE_APRES_ECHECS", b"_boucle_rangement_journee", b"_rangement_pause_restante", b"RANGEMENT_ECHECS_MAX", b"RANGEMENT_PAQUET_MAX = 25000", b"SEUIL_JOURNEE = 80000", b"RANGEMENT_PAQUET_MAX = 60000"]:
    dire("%s : %d fois" % (motif.decode(), data3.count(motif)))
sauve()
dire("")
dire("FINI")
sauve()
print("OK -> " + SORTIE)
