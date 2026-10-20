@echo off
cd /d C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75
echo === POSE DE LA v123 DANS LE DOSSIER EN SERVICE === > res_pose_v123.txt
set DEST=C:\Users\Fred\Desktop\luciana_v96\luciana_v96
echo dossier : %DEST% >> res_pose_v123.txt
echo --- 1) SAUVEGARDE de la version en service (avant de toucher) --- >> res_pose_v123.txt
copy /Y "%DEST%\luciana.py" "%DEST%\SAUVEGARDE_luciana_v121_avant_v123_2026-10-06.py" >> res_pose_v123.txt 2>&1
echo --- 2) COPIE de la v123 a la place de la version en service --- >> res_pose_v123.txt
copy /Y "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\luciana.py" "%DEST%\luciana.py" >> res_pose_v123.txt 2>&1
echo --- 3) COMPILATION de la version posee --- >> res_pose_v123.txt
python -m py_compile "%DEST%\luciana.py" >> res_pose_v123.txt 2>&1
echo code retour compile : %errorlevel% >> res_pose_v123.txt
echo --- 4) BADGE --- >> res_pose_v123.txt
findstr /C:"v123" "%DEST%\luciana.py" > nul && echo BADGE v123 TROUVE >> res_pose_v123.txt || echo BADGE v123 ABSENT >> res_pose_v123.txt
findstr /C:"v121" "%DEST%\luciana.py" > nul && echo ATTENTION v121 ENCORE LA >> res_pose_v123.txt || echo plus aucun v121 >> res_pose_v123.txt
echo --- 5) TAILLE ET EMPREINTE --- >> res_pose_v123.txt
for %%A in ("%DEST%\luciana.py") do echo taille : %%~zA octets >> res_pose_v123.txt
certutil -hashfile "%DEST%\luciana.py" SHA256 >> res_pose_v123.txt 2>&1
