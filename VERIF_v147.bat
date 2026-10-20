@echo off
rem =====================================================================
rem  LE CONTROLE DU CHANTIER v147 : "DEUX POINTS DE COMPARAISON DE NATURE
rem  DIFFERENTE AVANT D'AFFIRMER UN FAIT, UNE ORIGINE, UNE DATE OU UNE CAUSE"
rem
rem  Double-clique ce fichier. Il fait TROIS choses, dans cet ordre :
rem    1) la SAUVEGARDE datee du programme d'AVANT le chantier (regle d'or n22). Elle est
rem       extraite de l'historique git (commit 8f8b7b5) et PAS copiee depuis luciana.py --
rem       luciana.py est deja modifie a ce stade, le copier donnerait une sauvegarde qui
rem       mentirait sur son nom. Elle n'ecrase JAMAIS une sauvegarde qui existe deja, et elle
rem       se verifie avec DEUX points : la taille ET l'empreinte sha256. Si elle rate, le
rem       script le DIT.
rem    2) le BADGE, vu dans le fichier : il doit dire v147 une seule fois, et plus v146.
rem    3) les verifications du chantier v147, une par une, avec le detail de ce qui rate.
rem       Elles font tourner le VRAI code des verrous dans un dossier temporaire jetable :
rem       rien n'est ecrit dans C:\Users\Fred\Luciana, rien n'est envoye nulle part, et aucun
rem       fichier de Luminita n'est touche. Zero appel paye.
rem
rem  Tout ce qui s'affiche est AUSSI ecrit dans res_v147.txt, a cote de ce fichier :
rem  c'est ce fichier-la qu'il faut m'envoyer s'il y a du rouge.
rem =====================================================================
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_v147.txt" 2>&1"
  echo.
  echo Termine. Le resultat complet est dans : res_v147.txt
  echo.
  type "%~dp0res_v147.txt"
  pause
  exit /b
)
cd /d "%~dp0"
echo ===== 1 - LA SAUVEGARDE DATEE DU PROGRAMME D'AVANT =====
python _faire_la_sauvegarde_v147_deux_points.py
echo CODE_RETOUR_SAUVEGARDE=%ERRORLEVEL%
echo.
echo ===== 2 - LE BADGE, VU DANS LE FICHIER =====
findstr /N "ton amie &middot; v147" luciana.py
findstr /N "ton amie &middot; v146" luciana.py
echo (la premiere ligne doit apparaitre UNE fois ; la seconde, AUCUNE)
echo.
echo ===== 3 - LE CONTROLE DU CHANTIER v147 =====
python _verif_v147_deux_points.py
echo CODE_RETOUR_VERIF=%ERRORLEVEL%
echo.
echo ===== FIN =====
