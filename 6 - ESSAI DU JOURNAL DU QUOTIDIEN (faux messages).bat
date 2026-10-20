@echo off
chcp 65001 >nul
title Essai du journal du quotidien (faux messages, dossier a part)
cd /d "%~dp0"

rem --- Ne touche PAS a sa vraie bibliotheque ni a son vrai journal : tout se passe dans Luciana_neuve_essai_vital.
python nouvelle\essai_vital.py
echo.
pause
