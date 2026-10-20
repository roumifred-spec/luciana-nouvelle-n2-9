@echo off
chcp 65001 >nul
title Luciana (nouvelle)
cd /d "%~dp0"

rem --- LA NOUVELLE LUCIANA : l'ecran et les outils de la V198, des coulisses neuves.
rem     Meme adresse que d'habitude (port 8002) : on ferme d'abord une Luciana deja ouverte
rem     (une seule a la fois : elles partagent tes cles, Gmail et la voix dans ~\Luciana).
rem     Sa memoire a elle est dans ~\Luciana_neuve. L'ancienne memoire n'est pas touchee.
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%p >nul 2>&1
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8002 ^| findstr LISTENING') do taskkill /F /PID %%p >nul 2>&1

python -c "import anthropic, requests, PIL" >nul 2>&1
if errorlevel 1 (
  echo   Premiere fois : j'installe ce qui manque...
  python -m pip install anthropic edge-tts requests PILLOW
)

python nouvelle\luciana_neuve.py
echo.
echo Si une erreur apparait ci-dessus, envoie une photo de cette fenetre.
pause
