@echo off
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_recouture.txt" 2>&1"
  exit /b
)
cd /d C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75
echo ===== 1 - LES REPERES DE LA RECOUTURE (numero de ligne + contenu) =====
findstr /N "chien_de_garde_a_donner _chien_de_garde_du_rangement _CHIEN_DE_GARDE_A_DIRE" luciana.py
echo.
echo ===== 2 - LA LIGNE D'OBLIGATION DANS LE NOYAU =====
findstr /N "OBLIGATION" luciana.py
echo.
echo ===== 3 - BANC D'ESSAI PLAN BIBLIOTHEQUE =====
python _verif_plan_bibliotheque.py
echo CODE_RETOUR_PLAN=%ERRORLEVEL%
echo.
echo ===== 4 - BANC D'ESSAI CHIEN DE GARDE / OBLIGATION =====
python _verif_chien_de_garde_rangement.py
echo CODE_RETOUR_OBLIGATION=%ERRORLEVEL%
echo.
echo ===== FIN =====
