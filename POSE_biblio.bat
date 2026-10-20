@echo off
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_pose_biblio.txt" 2>&1"
  exit /b
)
set DEPOT=C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75
set SERVICE=C:\Users\Fred\Desktop\luciana_v96\luciana_v96
set SAUV=%SERVICE%\SAUVEGARDE_luciana_v126_avant_biblio_2026-10-06_2225.py

echo ===== POSE DE LA v127 (BIBLIOTHEQUE A ETAGES) =====
echo --- 1 - sauvegarde du fichier EN SERVICE avant de toucher ---
copy /Y "%SERVICE%\luciana.py" "%SAUV%"
echo.
echo --- 2 - copie du nouveau fichier ---
copy /Y "%DEPOT%\luciana.py" "%SERVICE%\luciana.py"
echo.
echo --- 3 - les bancs d'essai a cote du programme en service ---
copy /Y "%DEPOT%\_verif_rangement_auto.py" "%SERVICE%\_verif_rangement_auto.py"
copy /Y "%DEPOT%\_verif_plan_bibliotheque.py" "%SERVICE%\_verif_plan_bibliotheque.py"
echo.
echo --- 4 - COMPILATION du fichier en service ---
cd /d "%SERVICE%"
python -m py_compile luciana.py
echo CODE_RETOUR_COMPILE=%ERRORLEVEL%
if not "%ERRORLEVEL%"=="0" (
  echo *** COMPILATION RATEE : on remet la sauvegarde ***
  copy /Y "%SAUV%" "%SERVICE%\luciana.py"
  echo SAUVEGARDE REMISE
  exit /b
)
echo.
echo --- 5 - TAILLES ---
for %%F in ("%SAUV%") do echo SAUVEGARDE : %%~zF octets
for %%F in ("%SERVICE%\luciana.py") do echo EN SERVICE : %%~zF octets
echo.
echo --- 6 - LES REPERES DANS LE FICHIER EN SERVICE ---
findstr /N "chien_de_garde_a_donner RAYON_A_TRANCHER L'OBLIGATION" "%SERVICE%\luciana.py"
echo.
echo ===== FIN =====
