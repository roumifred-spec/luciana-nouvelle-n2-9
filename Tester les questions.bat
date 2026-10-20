@echo off
chcp 65001 >nul
title Tester la chaine des questions
cd /d "%~dp0"
set RAPPORT=%~dp0RESULTAT_test_des_questions.txt
echo ================================================================ > "%RAPPORT%"
echo  TEST DE LA CHAINE DES QUESTIONS  -  %DATE% %TIME% >> "%RAPPORT%"
echo  Rien n'est ecrit dans ta memoire : tout va dans les dossiers >> "%RAPPORT%"
echo  _demo_chaine_des_questions et _demo_pont_questions, a cote du code. >> "%RAPPORT%"
echo ================================================================ >> "%RAPPORT%"
echo.
echo   Test en cours... (quelques secondes)
echo.

set RATES=0

echo. >> "%RAPPORT%"
echo ### 1) LUCIANA COMPILE-T-ELLE ENCORE ?  (le plus important) >> "%RAPPORT%"
python -m py_compile luciana.py >> "%RAPPORT%" 2>&1
if errorlevel 1 (
  echo    RATE : luciana.py NE COMPILE PAS. >> "%RAPPORT%"
  set RATES=1
  echo   [1/3] RATE : luciana.py ne compile pas.
) else (
  echo    OK : luciana.py compile. >> "%RAPPORT%"
  echo   [1/3] OK   : luciana.py compile.
)

echo. >> "%RAPPORT%"
echo ### 2) LA BRIQUE : biblio2_questions.py >> "%RAPPORT%"
python biblio2_questions.py >> "%RAPPORT%" 2>&1
if errorlevel 1 (
  set RATES=1
  echo   [2/3] RATE : des controles de la brique ratent.
) else (
  echo   [2/3] OK   : la brique passe tous ses controles.
)

echo. >> "%RAPPORT%"
echo ### 3) LE PONT : biblio2_pont.py  (les chiffres sont ici) >> "%RAPPORT%"
python biblio2_pont.py >> "%RAPPORT%" 2>&1
if errorlevel 1 (
  set RATES=1
  echo   [3/3] RATE : des controles du pont ratent.
) else (
  echo   [3/3] OK   : le pont passe tous ses controles.
)

echo.
if "%RATES%"=="1" (
  echo   ============================================================
  echo     QUELQUE CHOSE RATE. N'ALLUME PAS LES QUESTIONS.
  echo     Envoie-moi le fichier RESULTAT_test_des_questions.txt
  echo     qui vient d'etre ecrit a cote du programme.
  echo   ============================================================
) else (
  echo   ============================================================
  echo     TOUT EST VERT. Tu peux allumer quand tu veux avec
  echo     le bouton "Brancher les questions".
  echo     Le detail et les chiffres sont dans le fichier
  echo     RESULTAT_test_des_questions.txt, a cote du programme.
  echo   ============================================================
)
echo.
pause
