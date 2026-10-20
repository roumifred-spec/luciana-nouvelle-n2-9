@echo off
rem =====================================================================
rem  LE CONTROLE DU CHANTIER v148 : "LE LECTEUR DE SENS"
rem  (un petit modele lit la phrase de Fred et rend les NUMEROS des consignes
rem   qui la concernent, avec retour immediat au tri par les mots si ca rate)
rem
rem  Double-clique ce fichier. Il fait TROIS choses, dans cet ordre :
rem    1) la SAUVEGARDE datee du programme d'AVANT le chantier (regle d'or n22). Elle est
rem       extraite de l'historique git (commit 3ea7dab) et PAS copiee depuis luciana.py --
rem       luciana.py est deja modifie a ce stade, le copier donnerait une sauvegarde qui
rem       mentirait sur son nom. Elle n'ecrase JAMAIS une sauvegarde qui existe deja, et elle
rem       se verifie avec DEUX points : la taille ET l'empreinte sha256. Si elle rate, le
rem       script le DIT.
rem    2) le BADGE, vu dans le fichier : il doit dire v148 une seule fois, et plus v147.
rem    3) les verifications du chantier v148, une par une, avec le detail de ce qui rate :
rem       la compilation, le tri par les mots compare caractere pour caractere a celui
rem       d'avant (git), les trois positions de l'interrupteur, CINQ pannes du modele
rem       SIMULEES pour prouver le repli, le noyau servi en entier, les 39 lignes d'index
rem       toujours la, et ce qui part vraiment au modele.
rem
rem  ZERO APPEL PAYE : le petit modele est remplace par un faux client dans un bac a sable
rem  jetable. Rien n'est ecrit dans C:\Users\Fred\Luciana, rien dans le dossier du programme,
rem  rien chez Luminita, et aucun fichier n'est envoye nulle part.
rem
rem  Tout ce qui s'affiche est AUSSI ecrit dans res_v148.txt, a cote de ce fichier :
rem  c'est ce fichier-la qu'il faut m'envoyer s'il y a du rouge.
rem =====================================================================
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_v148.txt" 2>&1"
  echo.
  echo Termine. Le resultat complet est dans : res_v148.txt
  echo.
  type "%~dp0res_v148.txt"
  pause
  exit /b
)
cd /d "%~dp0"
echo ===== 1 - LA SAUVEGARDE DATEE DU PROGRAMME D'AVANT =====
python _faire_la_sauvegarde_v148_lecteur_de_sens.py
echo CODE_RETOUR_SAUVEGARDE=%ERRORLEVEL%
echo.
echo ===== 2 - LE BADGE, VU DANS LE FICHIER =====
findstr /N "ton amie &middot; v148" luciana.py
findstr /N "ton amie &middot; v147" luciana.py
echo (la premiere ligne doit apparaitre UNE fois ; la seconde, AUCUNE)
echo.
echo ===== 3 - LE CONTROLE DU CHANTIER v148 =====
python _verif_v148_lecteur_de_sens.py
echo CODE_RETOUR_VERIF=%ERRORLEVEL%
echo.
echo ===== FIN =====
