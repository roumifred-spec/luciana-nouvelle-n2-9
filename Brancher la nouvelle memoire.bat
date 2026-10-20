@echo off
chcp 65001 >nul
title Brancher la nouvelle memoire
if not exist "%USERPROFILE%\Luciana\bibliotheque2" mkdir "%USERPROFILE%\Luciana\bibliotheque2"
echo branche> "%USERPROFILE%\Luciana\bibliotheque2\BRANCHE.txt"
echo.
echo   C'est fait : la nouvelle memoire (le bibliothecaire) est BRANCHEE.
echo   Des ton prochain message, Luciana recevra ses souvenirs du bibliothecaire
echo   au lieu de l'ancien tri. (Pas besoin de redemarrer.)
echo.
echo   Si quelque chose ne va pas : double-clique "Debrancher" et tu reviens
echo   a la Luciana d'avant, tout de suite.
echo.
pause
