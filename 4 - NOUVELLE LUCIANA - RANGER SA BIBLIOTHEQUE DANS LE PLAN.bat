@echo off
chcp 65001 >nul
title Nouvelle Luciana - ranger sa bibliotheque dans le plan
cd /d "%~dp0"

rem --- On ferme Luciana pendant le rangement (une seule a ecrire dans le plan a la fois).
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8002 ^| findstr LISTENING') do taskkill /F /PID %%p >nul 2>&1

python nouvelle\ranger_ma_bibliotheque.py
echo.
pause
