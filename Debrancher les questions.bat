@echo off
chcp 65001 >nul
title Debrancher les questions de l'archiviste
cd /d "%~dp0"

rem =====================================================================
rem  CHANTIER DU 12/10/2026 : CE BOUTON N'EFFACE PLUS DE FICHIER.
rem =====================================================================
rem  AVANT, il supprimait ~\Luciana\bibliotheque2\QUESTIONS.txt. Ca marchait, mais ca ne
rem  tenait pas : le fichier pouvait revenir, et les questions avec.
rem
rem  MAINTENANT, il ecrit UN REGLAGE, et c'est la seule chose qui compte :
rem      reglage_biblio2.json  ->  "questions_de_l_archiviste" -> "bloc_dans_le_contexte"
rem  Un vieux QUESTIONS.txt qui traine encore dans ton dossier ne change plus rien : plus
rem  aucune ligne de code ne le lit. On le laisse donc tranquille, on ne supprime rien.
rem
rem  C'est l'etat LIVRE par defaut : ce bouton sert a y revenir si quelqu'un a branche.

python biblio2_reglages.py --eteindre-les-questions
if errorlevel 1 goto RATE

echo.
echo   C'est fait : les questions de l'archiviste sont DEBRANCHEES.
echo.
echo   Des ton prochain message, Luciana reprend exactement son chemin d'avant :
echo   plus aucune question dans le tour, plus rien au milieu de tes phrases.
echo.
echo   RIEN N'EST PERDU : les questions deja ecrites restent sur leurs fiches, les
echo   reponses deja donnees restent rangees, et les fiches en attente restent en
echo   attente. On eteint un affichage, on ne detruit aucune donnee. Si tu rebranches
echo   un jour, la chaine reprend ou elle s'etait arretee.
echo.
echo   (La nouvelle memoire, elle, reste branchee : ce bouton-ci ne touche QUE les
echo   questions. Le bibliothecaire qui te sert tes souvenirs par le sens, les consignes,
echo   les carnets et la memoire longue continuent exactement comme avant. Pour la
echo   memoire, c'est le bouton "Debrancher".)
echo.
pause
exit /b 0

:RATE
echo.
echo   RIEN N'A CHANGE : le reglage n'a pas pu etre ecrit (le message ci-dessus dit
echo   pourquoi). Pour eteindre a la main, ouvre reglage_biblio2.json et mets false a
echo   la ligne "bloc_dans_le_contexte".
echo.
pause
exit /b 1
