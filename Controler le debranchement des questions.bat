@echo off
chcp 65001 >nul
title Controler le debranchement des questions de l'archiviste
cd /d "%~dp0"
set RAPPORT=%~dp0RESULTAT_controle_debranchement_des_questions.txt

echo ================================================================ > "%RAPPORT%"
echo  CONTROLE DU DEBRANCHEMENT DU BLOC DE QUESTIONS  -  %DATE% %TIME% >> "%RAPPORT%"
echo. >> "%RAPPORT%"
echo  CE QU'ON PROUVE ICI, EN UNE PHRASE : >> "%RAPPORT%"
echo    REGLAGE ETEINT + UN VIEUX DRAPEAU QUESTIONS.txt ENCORE PRESENT >> "%RAPPORT%"
echo    SUR LE DISQUE  =  AUCUN BLOC DE QUESTIONS INJECTE. >> "%RAPPORT%"
echo. >> "%RAPPORT%"
echo  RIEN N'EST ECRIT DANS TA MEMOIRE : tout va dans les dossiers d'essai >> "%RAPPORT%"
echo  _demo_pont_questions et _demo_chaine_des_questions, a cote du code. >> "%RAPPORT%"
echo  Ce controle ne MODIFIE PAS le reglage : il le LIT. >> "%RAPPORT%"
echo ================================================================ >> "%RAPPORT%"

echo.
echo   Controle en cours... (quelques secondes)
echo.

set RATES=0

echo. >> "%RAPPORT%"
echo ### 1) L'ETAT DU REGLAGE, TEL QU'IL EST SUR LE DISQUE >> "%RAPPORT%"
python biblio2_reglages.py --etat-des-questions >> "%RAPPORT%" 2>&1
if errorlevel 1 set RATES=1

echo. >> "%RAPPORT%"
echo ### 2) LES CONTROLES DE L'INTERRUPTEUR (biblio2_reglages.py) >> "%RAPPORT%"
python biblio2_reglages.py >> "%RAPPORT%" 2>&1
if errorlevel 1 (
  set RATES=1
  echo   [1/3] RATE : des controles de l'interrupteur ratent.
) else (
  echo   [1/3] OK   : l'interrupteur est eteint d'origine et ne s'allume pas par accident.
)

echo. >> "%RAPPORT%"
echo ### 3) LA PREUVE SUR DU REEL : REGLAGE ETEINT + VIEUX DRAPEAU PRESENT >> "%RAPPORT%"
echo      (c'est le bloc "CONTROLE DU DEBRANCHEMENT DEFINITIF" du rapport) >> "%RAPPORT%"
python biblio2_pont.py >> "%RAPPORT%" 2>&1
if errorlevel 1 (
  set RATES=1
  echo   [2/3] RATE : des controles du pont ratent.
) else (
  echo   [2/3] OK   : reglage eteint + vieux drapeau present = aucun bloc injecte.
)

echo. >> "%RAPPORT%"
echo ### 4) LUCIANA COMPILE-T-ELLE TOUJOURS ? >> "%RAPPORT%"
python -m py_compile luciana.py >> "%RAPPORT%" 2>&1
if errorlevel 1 (
  set RATES=1
  echo   [3/3] RATE : luciana.py ne compile pas.
) else (
  echo   [3/3] OK   : luciana.py compile.
)

echo.
if "%RATES%"=="1" (
  echo   ============================================================
  echo     QUELQUE CHOSE RATE. Envoie-moi le fichier
  echo     RESULTAT_controle_debranchement_des_questions.txt
  echo     qui vient d'etre ecrit a cote du programme.
  echo   ============================================================
) else (
  echo   ============================================================
  echo     TOUT EST VERT. Le bloc de questions de l'archiviste est
  echo     DEBRANCHE, et il ne peut pas se rebrancher tout seul :
  echo       - seul le reglage decide, et il est ETEINT ;
  echo       - un vieux QUESTIONS.txt sur le disque ne fait plus rien ;
  echo       - le programme ne recree jamais ce fichier.
  echo     Le detail est dans
  echo     RESULTAT_controle_debranchement_des_questions.txt
  echo   ============================================================
)
echo.
pause
