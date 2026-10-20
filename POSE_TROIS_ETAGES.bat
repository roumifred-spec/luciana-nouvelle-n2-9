@echo off
set LIVE=C:\Users\Fred\Desktop\luciana_v96\luciana_v96\luciana.py
set SRC=C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\luciana.py
set SAUV=C:\Users\Fred\Desktop\luciana_v96\luciana_v96\SAUVEGARDE_luciana_v127_avant_trois_etages_2026-10-06_2315.py
set LOG=C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_trois_etages.txt

echo === POSE : LA BIBLIOTHEQUE A TROIS ETAGES + LES FILTRES (06/10/2026 23h15) === > "%LOG%"

if not exist "%LIVE%" (echo ERREUR : le fichier EN SERVICE n'existe pas : %LIVE% >> "%LOG%" & exit /b 1)
if not exist "%SRC%"  (echo ERREUR : le fichier DU CHANTIER n'existe pas : %SRC% >> "%LOG%" & exit /b 1)

for %%A in ("%LIVE%") do echo AVANT, fichier en service : %%~zA octets >> "%LOG%"
for %%A in ("%SRC%")  do echo CHANTIER, fichier a poser  : %%~zA octets >> "%LOG%"

copy /Y "%LIVE%" "%SAUV%" >> "%LOG%"
if errorlevel 1 (echo ERREUR : la sauvegarde a echoue, JE NE POSE RIEN >> "%LOG%" & exit /b 1)
for %%A in ("%SAUV%") do echo SAUVEGARDE gardee : %%~zA octets >> "%LOG%"

copy /Y "%SRC%" "%LIVE%" >> "%LOG%"
for %%A in ("%LIVE%") do echo APRES, fichier en service : %%~zA octets >> "%LOG%"

python -m py_compile "%LIVE%"
echo COMPILATION du fichier en service, code retour %ERRORLEVEL% >> "%LOG%"

findstr /C:"v127" /C:"_sous_luciana" "%LIVE%" >nul
echo REPERES (v127 + verrou du dossier) presents, code retour %ERRORLEVEL% >> "%LOG%"
exit
