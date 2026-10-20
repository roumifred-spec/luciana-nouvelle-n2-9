@echo off
chcp 65001 >nul
cd /d "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
echo === BANC D'ESSAI DU CHIEN DE GARDE === > res_chien_de_garde.txt
python _verif_chien_de_garde_rangement.py >> res_chien_de_garde.txt 2>&1
echo. >> res_chien_de_garde.txt
echo === FIN === >> res_chien_de_garde.txt
echo === OU EST BRANCHE LE CHIEN DE GARDE DANS LE VRAI luciana.py === > res_branchement.txt
python _montre_branchement.py >> res_branchement.txt 2>&1
echo. >> res_branchement.txt
echo === FIN === >> res_branchement.txt
exit
