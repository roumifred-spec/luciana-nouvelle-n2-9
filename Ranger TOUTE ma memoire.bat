@echo off
chcp 65001 >nul
title Ranger TOUTE ma memoire (archiviste)
cd /d "%~dp0"
python -c "import anthropic" >nul 2>&1 || python -m pip install anthropic
echo.
echo   L'archiviste range TOUTE ta memoire dans la nouvelle bibliotheque.
echo   Il reflechit sur chaque souvenir : ca peut prendre un moment.
echo.
echo   Ta memoire et ta Luciana ne sont PAS touchees (lecture seule).
echo   Tu peux fermer cette fenetre et la relancer : il reprend ou il s'est arrete.
echo.
python biblio2_reprise.py
echo.
echo   ----------------------------------------------------------------
echo   Fini. Quand tu veux brancher cette memoire dans Luciana :
echo   double-clique "Brancher la nouvelle memoire".
echo   ----------------------------------------------------------------
explorer "%USERPROFILE%\Luciana\bibliotheque2"
pause
