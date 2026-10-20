@echo off
cd /d "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
echo ==== SIMULATION DU RE-TRI DE LA BIBLIOTHEQUE 06/10/2026 ==== > res_simu_retri.txt
echo --- 0) SAUVEGARDE DU PLAN AVANT TOUTE CHOSE --- >> res_simu_retri.txt
copy /Y "C:\Users\Fred\Luciana\plan_bibliotheque.json" "SAUVEGARDE_plan_bibliotheque_avant_simu_2026-10-06.json" >> res_simu_retri.txt 2>&1
echo --- 1) LA SIMULATION (lecture seule) --- >> res_simu_retri.txt
python _simu_retri.py >> res_simu_retri.txt 2>&1
echo ==== FIN ==== >> res_simu_retri.txt
exit
