# -*- coding: utf-8 -*-
"""Pose de la correction du rangement (verrou + paquets + verite au bandeau).
Sauvegarde datee AVANT de toucher, copie, compilation, puis le script de controle.
Ecrit tout dans res_pose_v114.txt."""
import os, re, shutil, subprocess, sys

ATELIER = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
SERVICE = r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96"
src = os.path.join(ATELIER, "luciana.py")
dst = os.path.join(SERVICE, "luciana.py")

L = []
L.append("=== 0) CONTEXTE ===")
L.append("atelier : " + ATELIER)
L.append("service : " + SERVICE)

L.append("")
L.append("=== 1) LES DEUX FICHIERS AVANT ===")
L.append("source (atelier, corrige) : %d octets" % os.path.getsize(src))
L.append("cible (en service)        : %d octets" % os.path.getsize(dst))

# --- sauvegarde datee du fichier qui marche ---
sauv = os.path.join(SERVICE, "2026-10-06_02h15_luciana_v113_sauvegarde_AVANT_v114.py")
if os.path.exists(sauv):
    L.append("SAUVEGARDE : elle existait deja, je n'y touche pas -> " + sauv)
else:
    shutil.copy2(dst, sauv)
    L.append("SAUVEGARDE faite : %s (%d octets)" % (sauv, os.path.getsize(sauv)))
ok_sauv = os.path.exists(sauv) and os.path.getsize(sauv) == os.path.getsize(dst)
L.append("SAUVEGARDE verifiee (meme taille que l'original) : %s" % ("OUI" if ok_sauv else "NON"))
if not ok_sauv:
    L.append("!!! Je m'arrete la : pas de sauvegarde, on ne touche a rien.")
    open(os.path.join(ATELIER, "res_pose_v114.txt"), "w", encoding="utf-8").write("\n".join(L))
    sys.exit(0)

# --- copie par-dessus ---
shutil.copy2(src, dst)
taille = os.path.getsize(dst)
L.append("")
L.append("=== 2) COPIE PAR-DESSUS ===")
L.append("COPIER : OK")
L.append("cible apres copie : %d octets" % taille)
L.append("identique a la source : %s" % ("OUI" if taille == os.path.getsize(src) else "NON"))

# --- le badge ---
t = open(dst, encoding="utf-8", errors="replace").read()
L.append("")
L.append("=== 3) LE BADGE ===")
for chaine in ("ton amie &middot; v113", "ton amie . v113", "ton amie &middot; v114"):
    L.append("  '%s' : %d fois" % (chaine, t.count(chaine)))
avant = t.count("ton amie &middot; v113")
if avant == 1:
    t = t.replace("ton amie &middot; v113", "ton amie &middot; v114")
    open(dst, "w", encoding="utf-8", newline="").write(t)
    t2 = open(dst, encoding="utf-8", errors="replace").read()
    L.append("BADGE : v113 -> v114, ecrit. Verif : %d fois 'v114', %d fois 'v113'"
             % (t2.count("ton amie &middot; v114"), t2.count("ton amie &middot; v113")))
else:
    L.append("BADGE : pas touche (chaine trouvee %d fois, je ne devine pas)." % avant)

# --- compilation du fichier pose ---
L.append("")
L.append("=== 4) COMPILATION DU FICHIER EN SERVICE ===")
r = subprocess.run([sys.executable, "-m", "py_compile", dst], capture_output=True, text=True)
L.append("py_compile code retour : %d" % r.returncode)
L.append("(0 = compile. Autre = CASSE.)")
if r.stdout:
    L.append(r.stdout[-1500:])
if r.stderr:
    L.append(r.stderr[-1500:])

# --- les controles du rangement ---
L.append("")
L.append("=== 5) LE SCRIPT DE CONTROLE DU RANGEMENT ===")
cands = [os.path.join(SERVICE, "_verif_rangement_journee.py"),
         os.path.join(ATELIER, "_verif_rangement_journee.py")]
verif = None
for c in cands:
    L.append("  %s : %s" % (c, "existe" if os.path.exists(c) else "absent"))
    if os.path.exists(c) and verif is None:
        verif = c
if verif:
    r2 = subprocess.run([sys.executable, verif], capture_output=True, text=True,
                        cwd=os.path.dirname(verif))
    L.append("script lance : %s" % verif)
    L.append("code retour : %d" % r2.returncode)
    sortie = (r2.stdout or "")
    L.append("--- fin de la sortie ---")
    L.append(sortie[-7000:])
    if r2.stderr:
        L.append("--- erreurs ---")
        L.append(r2.stderr[-2500:])
else:
    L.append("AUCUN script de controle trouve. Je le dis, je n'invente rien.")

open(os.path.join(ATELIER, "res_pose_v114.txt"), "w", encoding="utf-8").write("\n".join(L))
print("OK -> res_pose_v114.txt")
