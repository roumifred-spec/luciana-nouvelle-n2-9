@echo off
cd /d C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75
set OUT=res_pose_tuyau.txt
set SERVICE=C:\Users\Fred\Desktop\luciana_v96\luciana_v96
set SAUV=%SERVICE%\SAUVEGARDE_luciana_v126_avant_tuyau_2026-10-06_2117.py

echo ===== 1 - LE NOUVEAU CODE DU TUYAU EST-IL DANS LE DEPOT ? ===== > %OUT%
findstr /n /c:"chien_de_garde_a_donner" luciana.py >> %OUT% 2>&1
findstr /n /c:"DIS-LE A FRED" luciana.py >> %OUT% 2>&1
findstr /n /c:"_chien_de_garde_du_rangement" luciana.py >> %OUT% 2>&1

findstr /c:"chien_de_garde_a_donner" luciana.py > nul 2>&1
if errorlevel 1 (
  echo STOP - LE NOUVEAU CODE N'EST PAS DANS LE FICHIER - JE NE POSE RIEN >> %OUT%
  goto fin
)
echo ===== 2 - LE NOUVEAU CODE EST LA, JE SAUVEGARDE ET JE POSE ===== >> %OUT%

copy /y "%SERVICE%\luciana.py" "%SAUV%" >> %OUT% 2>&1
copy /y luciana.py "%SERVICE%\luciana.py" >> %OUT% 2>&1
copy /y _verif_rangement_auto.py "%SERVICE%\_verif_rangement_auto.py" >> %OUT% 2>&1

echo ===== 3 - COMPILATION DU FICHIER EN SERVICE ===== >> %OUT%
python -m py_compile "%SERVICE%\luciana.py" >> %OUT% 2>&1
if errorlevel 1 (
  echo COMPILATION RATEE - JE REMETS LA SAUVEGARDE TOUT DE SUITE >> %OUT%
  copy /y "%SAUV%" "%SERVICE%\luciana.py" >> %OUT% 2>&1
  goto fin
)
echo COMPILATION DU FICHIER EN SERVICE : OK, code retour 0 >> %OUT%

echo ===== 4 - ETAT DU FICHIER EN SERVICE MAINTENANT ===== >> %OUT%
dir "%SERVICE%\luciana.py" >> %OUT% 2>&1
dir "%SAUV%" >> %OUT% 2>&1

:fin
echo FINI >> %OUT%
