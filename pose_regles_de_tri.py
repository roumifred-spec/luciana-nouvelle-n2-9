# -*- coding: utf-8 -*-
# =====================================================================
#  POSE DE LA VERSION "REGLES DE TRI DE LA BIBLIOTHEQUE" dans le fichier EN SERVICE
#  Regle n22 de Fred : on SAUVEGARDE d'abord (nommee et datee), on copie ensuite, on compile.
#  Cette etape NE TOUCHE PAS a la memoire de Fred (C:\Users\Fred\Luciana) : elle n'ecrit que
#  dans les dossiers du Bureau.
# =====================================================================
import io
import os
import py_compile
import re
import shutil
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NEUF = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\luciana.py"
SERVICE = r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96\luciana.py"
SAUVE = (r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96"
         r"\SAUVEGARDE_luciana_v126_avant_regles_de_tri_2026-10-06_2015.py")


def inf(p):
    if not os.path.exists(p):
        print("   ABSENT : %s" % p)
        return
    st = os.stat(p)
    print("   %s" % p)
    print("      %d octets, ecrit le %s" % (st.st_size, time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(st.st_mtime))))


print("=== 1) LE FICHIER QUI TOURNE, AVANT TOUT ===")
inf(SERVICE)

print("")
print("=== 2) LES NUMEROS DE VERSION DANS LE FICHIER NEUF ===")
s = open(NEUF, encoding="utf-8").read()
print("   jetons trouves : %s" % sorted(set(re.findall(r"v1[0-9][0-9]", s))))
print("   taille du fichier neuf : %d octets" % os.path.getsize(NEUF))

print("")
print("=== 3) SAUVEGARDE NOMMEE ET DATEE (avant de toucher a quoi que ce soit) ===")
if not os.path.exists(SERVICE):
    print("   STOP : le fichier en service n'est PAS a cette adresse. RIEN n'a ete touche.")
    sys.exit(2)
if os.path.exists(SAUVE):
    print("   ELLE EXISTE DEJA, je ne l'ecrase pas : %s" % SAUVE)
else:
    shutil.copy2(SERVICE, SAUVE)
    print("   FAITE.")
inf(SAUVE)

print("")
print("=== 4) POSE DE LA NOUVELLE VERSION ===")
shutil.copy2(NEUF, SERVICE)
inf(SERVICE)

print("")
print("=== 5) COMPILATION DU FICHIER EN SERVICE ===")
try:
    py_compile.compile(SERVICE, doraise=True)
    print("   COMPILATION : OK (aucune erreur de syntaxe)")
except Exception as ex:
    print("   COMPILATION : ECHEC -> %s" % ex)
    print("   >>> LA SAUVEGARDE EST LA, on peut revenir en arriere : %s" % SAUVE)

print("")
print("=== 6) LA MEMOIRE DE FRED N'A PAS ETE TOUCHEE PAR CE SCRIPT ===")
print("   (ce script n'ecrit que sur le Bureau : %s / %s)" % (SERVICE, SAUVE))
