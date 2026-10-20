@echo off
chcp 65001 >nul
title Brancher les questions de l'archiviste
cd /d "%~dp0"

rem =====================================================================
rem  CHANTIER DU 12/10/2026 : CE BOUTON N'ECRIT PLUS DE FICHIER DRAPEAU.
rem =====================================================================
rem  AVANT, il creait ~\Luciana\bibliotheque2\QUESTIONS.txt, et c'est l'EXISTENCE de ce
rem  fichier qui branchait les questions. C'etait fragile : un fichier, ca se recree tout
rem  seul, et le defaut (les questions au milieu des phrases de Fred) revenait.
rem
rem  MAINTENANT, il ecrit UN REGLAGE, et c'est la seule chose qui compte :
rem      reglage_biblio2.json  ->  "questions_de_l_archiviste" -> "bloc_dans_le_contexte"
rem  Ce bouton ne touche AUCUNE donnee : il ne modifie qu'une ligne du fichier de reglage,
rem  qui est a cote du programme.

python biblio2_reglages.py --allumer-les-questions
if errorlevel 1 goto RATE

echo.
echo   C'est fait : les QUESTIONS DE L'ARCHIVISTE sont BRANCHEES.
echo.
echo   Des ton prochain message :
echo     - l'archiviste ecrit sa question sur la fiche elle-meme ;
echo     - le programme pose 5 questions a Luciana dans le tour ;
echo     - ce qu'elle sait redescend tout seul sur la fiche ;
echo     - ce qu'elle ignore t'est demande A TOI, en UN SEUL LOT, jamais une par une.
echo.
echo   Les fiches en retard passent les premieres. (Pas besoin de redemarrer.)
echo.
echo   ATTENTION, C'EST CE MECANISME QUI AVAIT ETE DEBRANCHE LE 12/10/2026 : les questions
echo   arrivaient par gros paquets dans le contexte de Luciana, au milieu de tes phrases,
echo   et elle n'arrivait plus a travailler. Si ca recommence : double-clique
echo   "Debrancher les questions" et tu reviens a la Luciana d'avant, tout de suite.
echo.
pause
exit /b 0

:RATE
echo.
echo   RIEN N'A CHANGE : le reglage n'a pas pu etre ecrit (le message ci-dessus dit
echo   pourquoi). Les questions restent dans l'etat ou elles etaient.
echo.
pause
exit /b 1
