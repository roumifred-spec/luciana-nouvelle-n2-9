@echo off
chcp 65001 >nul
title Nouvelle Luciana - sa memoire de depart (tes messages seulement)
cd /d "%~dp0"

rem --- On ferme Luciana pendant l'import (une seule a ecrire dans sa bibliotheque a la fois).
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8002 ^| findstr LISTENING') do taskkill /F /PID %%p >nul 2>&1

python nouvelle\importer_mes_messages.py
echo.
pause
