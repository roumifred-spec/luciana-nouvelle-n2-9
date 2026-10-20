@echo off
chcp 65001 >nul
title Essai du registre des personnes
cd /d "%~dp0"

rem --- Ne ferme PAS Luciana (le port 8002 n est pas touche) et ne touche PAS a Luciana_neuve.
rem --- Tout se passe dans Luciana_neuve_essai_registre. Resultat : RESULTAT - ESSAI DU REGISTRE DES PERSONNES.txt
python nouvelle\essai_registre.py
echo.
pause
