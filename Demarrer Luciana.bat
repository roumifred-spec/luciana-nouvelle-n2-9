@echo off
chcp 65001 >nul
title Luciana
cd /d "%~dp0"

rem --- On ferme tout vieux Luciana encore ouvert (port 8000 = l'ancienne, 8002 = la V180) ---
rem    UNE SEULE Luciana a la fois : les deux partagent la meme memoire (dossier ~\Luciana).
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%p >nul 2>&1
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8002 ^| findstr LISTENING') do taskkill /F /PID %%p >nul 2>&1

rem --- V180 : un raccourci "Luciana V180" sur le Bureau, refait a chaque lancement, qui pointe
rem     TOUJOURS vers CE dossier-ci (l'ancien raccourci "Luciana" pointe vers l'ancien dossier).
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Luciana V180.lnk'); $s.TargetPath='%~f0'; $s.WorkingDirectory='%~dp0'; $s.IconLocation='%SystemRoot%\System32\shell32.dll,220'; $s.Save()" >nul 2>&1

rem --- Raccourci sur le Bureau, cree une seule fois ---
set "LNK=%USERPROFILE%\Desktop\Luciana.lnk"
if not exist "%LNK%" powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Luciana.lnk'); $s.TargetPath='%~f0'; $s.WorkingDirectory='%~dp0'; $s.IconLocation='%SystemRoot%\System32\shell32.dll,220'; $s.Save()" >nul 2>&1

rem --- v76 : LA LISTE D'INSTALLATION COMPLETE, verifiee une fois a chaque demarrage ---
rem     anthropic = le cerveau ; edge-tts = la voix ; requests = internet ;
rem     PILLOW    = OBLIGATOIRE : sans lui "import pyautogui" plante
rem                 (ModuleNotFoundError: PIL) et Luciana se retrouve SANS souris
rem                 ni capture d'ecran. C'est ce qui manquait sur le PC de la cliente.
python -c "import anthropic, requests, PIL" >nul 2>&1
if errorlevel 1 (
  echo.
  echo   Premiere fois sur ce PC : j'installe ce qui manque, ca prend une minute...
  echo   ^(pip install anthropic edge-tts requests PILLOW^)
  echo.
  python -m pip install --upgrade pip >nul 2>&1
  python -m pip install anthropic edge-tts requests PILLOW
  echo.
)

python luciana.py
echo.
echo Si une erreur apparait ci-dessus, envoie une photo de cette fenetre a Fred.
echo Si tu vois "ModuleNotFoundError", tape ceci puis relance :
echo    pip install anthropic edge-tts requests PILLOW
pause
