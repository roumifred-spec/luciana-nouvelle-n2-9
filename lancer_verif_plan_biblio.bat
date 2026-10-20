@echo off
cd /d "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
python _verif_plan_bibliotheque.py > res_verif_plan_biblio_2026-10-06.txt 2>&1
echo CODE RETOUR = %errorlevel% >> res_verif_plan_biblio_2026-10-06.txt
