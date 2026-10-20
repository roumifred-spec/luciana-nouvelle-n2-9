@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo RE-TRI DE TOUTE LA MEMOIRE PAR LE SENS, PUIS MISE EN SERVICE (l ancienne est gardee en copie datee).
echo On peut fermer et relancer : il reprend ou il en etait.
python biblio2_retri_par_sens.py --tout-en-un
pause
