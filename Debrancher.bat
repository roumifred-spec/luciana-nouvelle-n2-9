@echo off
chcp 65001 >nul
title Debrancher la nouvelle memoire
del "%USERPROFILE%\Luciana\bibliotheque2\BRANCHE.txt" >nul 2>&1
echo.
echo   C'est fait : la nouvelle memoire est DEBRANCHEE.
echo   Luciana est revenue a son fonctionnement d'avant, tout de suite.
echo   (Rien n'est perdu : l'arbre range reste la, tu peux rebrancher quand tu veux.)
echo.
pause
