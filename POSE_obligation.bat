@echo off
set CHANTIER=C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\luciana.py
set CHIEN=C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\_verif_rangement_auto.py
set DOSSIER=C:\Users\Fred\Desktop\luciana_v96\luciana_v96
set SERVICE=%DOSSIER%\luciana.py
set SAUV=%DOSSIER%\SAUVEGARDE_luciana_v125_avant_obligation_2026-10-06_2200.py
> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo ===== POSE DE LA V126 (TUYAU + OBLIGATION) =====
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo --- 1 - sauvegarde du fichier en service AVANT
copy /Y "%SERVICE%" "%SAUV%" >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt 2>&1
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo --- 2 - copie du nouveau fichier
copy /Y "%CHANTIER%" "%SERVICE%" >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt 2>&1
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo --- 3 - le chien de garde a cote du programme en service
copy /Y "%CHIEN%" "%DOSSIER%\_verif_rangement_auto.py" >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt 2>&1
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo --- 4 - compilation du fichier EN SERVICE
cd /d "%DOSSIER%"
python -m py_compile luciana.py >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt 2>&1
set CODE=%ERRORLEVEL%
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo CODE_RETOUR_COMPILE=%CODE%
if not "%CODE%"=="0" (
  copy /Y "%SAUV%" "%SERVICE%" >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt 2>&1
  >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo REMISE DE LA SAUVEGARDE : la compilation avait rate, le fichier d'avant est revenu
)
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo --- 5 - tailles et dates
dir "%SERVICE%" >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt
dir "%SAUV%" >> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt
>> C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_obligation.txt echo ===== FIN =====
