@echo off
chcp 65001 >nul
title Reprise memoire Luciana (essai 30)
cd /d "%~dp0"

rem Luciana utilise deja 'anthropic' ; on verifie juste au cas ou.
python -c "import anthropic" >nul 2>&1 || python -m pip install anthropic

echo.
echo   Je range un PETIT paquet (30 souvenirs) de ta memoire dans la
echo   nouvelle bibliotheque, avec ton archiviste + DeepSeek.
echo.
echo   IMPORTANT : ta memoire n'est PAS modifiee (lecture seule),
echo   et ta Luciana n'est PAS touchee. On ecrit dans un dossier neuf.
echo.
rem --- Chaque essai repart propre : on efface l'INDEX du rangement, et RIEN D'AUTRE.
rem     (On ne touche QUE a notre dossier bibliotheque2, jamais a ta memoire ni a Luciana.)
rem
rem     CORRIGE LE 11/10/2026 : avant, cette ligne supprimait TOUT le dossier
rem     bibliotheque2 d'un coup -- donc aussi curseur.txt (ton reglage a 0,35, qui
rem     repartait alors a la valeur par defaut) et BRANCHE.txt (ce qui DEBRANCHAIT la
rem     memoire sans rien dire). On n'efface plus que les fichiers du rangement :
rem     ton curseur et ton interrupteur restent exactement comme tu les as laisses.
set BIB2=%USERPROFILE%\Luciana\bibliotheque2
if exist "%BIB2%\arbre.json"       del /q "%BIB2%\arbre.json"
if exist "%BIB2%\marque_page.json" del /q "%BIB2%\marque_page.json"
if exist "%BIB2%\plan.json"        del /q "%BIB2%\plan.json"
if exist "%BIB2%\signal_plan.json" del /q "%BIB2%\signal_plan.json"
if exist "%BIB2%\plan_deja_vu.txt" del /q "%BIB2%\plan_deja_vu.txt"
python biblio2_reprise.py 30
echo.
echo   ----------------------------------------------------------------
echo   J'ouvre le dossier ou j'ai ecrit l'arbre.
echo   Envoie le fichier "arbre.json" a Claude pour qu'il regarde le tri.
echo   ----------------------------------------------------------------
explorer "%USERPROFILE%\Luciana\bibliotheque2"
pause
