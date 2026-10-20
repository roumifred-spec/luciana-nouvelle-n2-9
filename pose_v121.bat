@echo off
cd /d "C:\Users\Fred\Desktop\luciana_v96\luciana_v96"
set SORTIE="C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_pose_v121.txt"
echo === POSE DE LA v121 DANS LE DOSSIER EN SERVICE === > %SORTIE%
echo dossier : %CD% >> %SORTIE%
echo. >> %SORTIE%
echo --- 1) SAUVEGARDE de la version en service (avant de toucher) --- >> %SORTIE%
copy /Y luciana.py SAUVEGARDE_luciana_v118_avant_v121_2026-10-06.py >> %SORTIE% 2>&1
echo. >> %SORTIE%
echo --- 2) COPIE de la v121 a la place de la version en service --- >> %SORTIE%
copy /Y "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\luciana.py" luciana.py >> %SORTIE% 2>&1
echo. >> %SORTIE%
echo --- 3) COMPILATION de la version posee --- >> %SORTIE%
echo DEBUT_DU_CONTROLE >> %SORTIE%
python -m py_compile luciana.py >> %SORTIE% 2>&1
echo py_compile code retour : %ERRORLEVEL% >> %SORTIE%
echo FIN_DU_CONTROLE >> %SORTIE%
echo. >> %SORTIE%
echo --- 4) LE BADGE dans le fichier pose --- >> %SORTIE%
python -c "d=open('luciana.py','rb').read(); print('v121 :', d.count(b'v121'), '| v120 :', d.count(b'v120'), '| v118 :', d.count(b'v118'))" >> %SORTIE% 2>&1
echo. >> %SORTIE%
echo --- 5) TAILLE ET EMPREINTE --- >> %SORTIE%
for %%F in (luciana.py) do echo taille : %%~zF octets >> %SORTIE%
certutil -hashfile luciana.py SHA256 >> %SORTIE% 2>&1
echo === TERMINE === >> %SORTIE%
