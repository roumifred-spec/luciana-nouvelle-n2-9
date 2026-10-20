@echo off
chcp 65001 >nul
title Essai de comprendre la situation
cd /d "%~dp0"

rem --- N ecrit rien et ne touche pas a sa vraie bibliotheque.
python nouvelle\essai_comprendre.py
echo.
pause
