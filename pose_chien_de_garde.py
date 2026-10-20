# -*- coding: utf-8 -*-
# =====================================================================
# POSER LE CHIEN DE GARDE DANS LA VERSION QUI TOURNE CHEZ FRED
# avec SAUVEGARDE NOMMEE ET DATEE avant de toucher (regle d'or n22).
# =====================================================================
import os, hashlib, shutil, time, py_compile

DEPOT   = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
SERVICE = r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96"

src_py  = os.path.join(DEPOT,   "luciana.py")
dst_py  = os.path.join(SERVICE, "luciana.py")
src_cg  = os.path.join(DEPOT,   "_verif_rangement_auto.py")
dst_cg  = os.path.join(SERVICE, "_verif_rangement_auto.py")

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

print("=" * 78)
print("1) LE FICHIER QUI TOURNE, AVANT TOUT")
print("=" * 78)
print("EN SERVICE :", dst_py)
print("   ", os.path.getsize(dst_py), "octets, ecrit le", time.ctime(os.path.getmtime(dst_py)))
print("   sha256 :", sha(dst_py))
print("SOURCE (depot) :", src_py)
print("   ", os.path.getsize(src_py), "octets, ecrit le", time.ctime(os.path.getmtime(src_py)))
print("   sha256 :", sha(src_py))
print()

print("=" * 78)
print("2) LA SOURCE CONTIENT-ELLE BIEN TOUT ? (rien ne doit manquer)")
print("=" * 78)
s = open(src_py, encoding="utf-8").read()
for mot in ("CONSIGNE_DE_RANGEMENT_PLAN", "_chien_de_garde_du_rangement",
            "FICHIER_CHIEN_DE_GARDE", "HIERARCHIQUE", "voyant_memoire",
            "COMPTEUR DEPENSE", "reflexion"):
    print("   %-32s : %d fois" % (mot, s.count(mot)))
print()

print("=" * 78)
print("3) SAUVEGARDE NOMMEE ET DATEE (on ne touche a rien sans ca)")
print("=" * 78)
horodate = time.strftime("%Y-%m-%d_%H%M")
sauv = os.path.join(SERVICE, "SAUVEGARDE_luciana_v125_avant_chien_de_garde_%s.py" % horodate)
shutil.copy2(dst_py, sauv)
print("   copie faite :", sauv)
print("   taille :", os.path.getsize(sauv), "octets")
print("   sha256 :", sha(sauv))
ok = sha(sauv) == sha(dst_py)
print("   la copie est IDENTIQUE a l'original :", "OUI" if ok else "NON")
if not ok:
    print("   >>> ON ARRETE TOUT : la sauvegarde n'est pas fiable.")
    raise SystemExit(1)
print()

print("=" * 78)
print("4) POSE DU FICHIER EN SERVICE")
print("=" * 78)
shutil.copy2(src_py, dst_py)
print("   luciana.py copie ->", os.path.getsize(dst_py), "octets")
shutil.copy2(src_cg, dst_cg)
print("   _verif_rangement_auto.py copie ->", os.path.getsize(dst_cg), "octets")
print("   (le chien de garde a besoin de SON fichier a cote du programme,")
print("    sinon il ne trouve rien et il se tait.)")
print()

print("=" * 78)
print("5) COMPILATION DU FICHIER EN SERVICE")
print("=" * 78)
try:
    py_compile.compile(dst_py, doraise=True)
    print("   luciana.py en service : COMPILE (code retour 0)")
except Exception as e:
    print("   >>> ERREUR DE COMPILATION :", e)
    raise SystemExit(1)
try:
    py_compile.compile(dst_cg, doraise=True)
    print("   _verif_rangement_auto.py : COMPILE")
except Exception as e:
    print("   >>> ERREUR :", e)

print()
print("=" * 78)
print("6) VERIFICATION FINALE")
print("=" * 78)
sv = open(dst_py, encoding="utf-8").read()
print("   le fichier en service contient le chien de garde :",
      sv.count("_chien_de_garde_du_rangement"), "fois")
print("   il contient les 5 regles de tri :",
      sv.count("CONSIGNE_DE_RANGEMENT_PLAN"), "fois")
print("   taille en service apres pose :", len(sv), "caracteres")
print()
print("   A FAIRE PAR FRED : REDEMARRER Luciana.")
print("   Le chien de garde ne se voit PAS sur la page : il parle dans la")
print("   fenetre noire, et SEULEMENT s'il a quelque chose a dire.")
