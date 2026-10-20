@echo off
cd /d "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
python _verif_biblio_trois_etages.py > res_biblio_trois_etages.txt 2>&1
echo CODE RETOUR %ERRORLEVEL% >> res_biblio_trois_etages.txt
exit
