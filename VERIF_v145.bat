@echo off
rem =====================================================================
rem  LE CONTROLE DU CHANTIER v145 : "JE TE FAIS DIRE CE QUE TU N'AS PAS DIT"
rem
rem  Double-clique ce fichier. Il fait DEUX choses, dans cet ordre :
rem    1) la SAUVEGARDE datee de luciana.py (regle d'or n22 : avant de toucher a quoi que ce
rem       soit). Elle est posee a cote du programme, et le script tente aussi de la poser a
rem       cote du fichier en service. S'il ne peut pas, il le DIT.
rem    2) les verifications du chantier v145, une par une, avec le detail de ce qui rate.
rem
rem  Tout ce qui s'affiche est AUSSI ecrit dans res_v145.txt, a cote de ce fichier :
rem  c'est ce fichier-la qu'il faut m'envoyer s'il y a du rouge.
rem =====================================================================
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_v145.txt" 2>&1"
  echo.
  echo Termine. Le resultat complet est dans : res_v145.txt
  echo.
  type "%~dp0res_v145.txt"
  pause
  exit /b
)
cd /d "%~dp0"
echo ===== 1 - LA SAUVEGARDE DATEE (avant tout) =====
python _sauvegarde_v145.py
echo CODE_RETOUR_SAUVEGARDE=%ERRORLEVEL%
echo.
echo ===== 2 - LE BADGE, VU DANS LE FICHIER =====
findstr /N "ton amie &middot; v145" luciana.py
findstr /N "ton amie &middot; v144" luciana.py
echo (la premiere ligne doit apparaitre UNE fois ; la seconde, AUCUNE)
echo.
echo ===== 3 - LE CONTROLE DU CHANTIER v145 =====
python _verif_v145_dire_ou_nuance.py
echo CODE_RETOUR_VERIF=%ERRORLEVEL%
echo.
echo ===== FIN =====
