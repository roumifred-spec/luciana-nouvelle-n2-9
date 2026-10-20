@echo off
rem =====================================================================
rem  LE CONTROLE DU CHANTIER v146 : LE VERROU DE SURVEILLANCE ("LA NOUNOU")
rem
rem  Double-clique ce fichier. Il fait TROIS choses, dans cet ordre :
rem    1) la SAUVEGARDE datee de luciana.py (regle d'or n22 : avant de toucher a quoi que ce
rem       soit). Elle est posee a cote du programme, et elle n'ecrase JAMAIS une sauvegarde
rem       qui existe deja. Si elle rate, le script le DIT.
rem    2) le BADGE, vu dans le fichier : il doit dire v146 une seule fois, et plus v145.
rem    3) les verifications du chantier v146, une par une, avec le detail de ce qui rate.
rem       Elles font tourner le VRAI code du verrou dans un dossier temporaire jetable :
rem       rien n'est ecrit dans C:\Users\Fred\Luciana, et rien n'est envoye nulle part.
rem
rem  Tout ce qui s'affiche est AUSSI ecrit dans res_v146.txt, a cote de ce fichier :
rem  c'est ce fichier-la qu'il faut m'envoyer s'il y a du rouge.
rem =====================================================================
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_v146.txt" 2>&1"
  echo.
  echo Termine. Le resultat complet est dans : res_v146.txt
  echo.
  type "%~dp0res_v146.txt"
  pause
  exit /b
)
cd /d "%~dp0"
echo ===== 1 - LA SAUVEGARDE DATEE (avant tout) =====
python _faire_la_sauvegarde_v146_nounou.py
echo CODE_RETOUR_SAUVEGARDE=%ERRORLEVEL%
echo.
echo ===== 2 - LE BADGE, VU DANS LE FICHIER =====
findstr /N "ton amie &middot; v146" luciana.py
findstr /N "ton amie &middot; v145" luciana.py
echo (la premiere ligne doit apparaitre UNE fois ; la seconde, AUCUNE)
echo.
echo ===== 3 - LE CONTROLE DU CHANTIER v146 =====
python _verif_v146_nounou.py
echo CODE_RETOUR_VERIF=%ERRORLEVEL%
echo.
echo ===== FIN =====
