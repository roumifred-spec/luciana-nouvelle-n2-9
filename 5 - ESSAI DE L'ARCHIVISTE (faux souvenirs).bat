@echo off
chcp 65001 >nul
title Essai de l archiviste (faux souvenirs, dossier a part)
cd /d "%~dp0"

rem --- Ne touche PAS a sa vraie bibliotheque : tout se passe dans Luciana_neuve_essai_archiviste.
python nouvelle\essai_archiviste.py
echo.
pause
