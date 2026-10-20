@echo off
cd /d C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75
> res_controle_obligation2.txt echo ===== 1 - LES REPERES DU TUYAU DANS LE FICHIER DESCENDU =====
findstr /N "_verdict = chien_de_garde_a_donner" luciana.py >> res_controle_obligation2.txt
findstr /N "def chien_de_garde_a_donner" luciana.py >> res_controle_obligation2.txt
findstr /N "def _chien_de_garde_du_rangement" luciana.py >> res_controle_obligation2.txt
>> res_controle_obligation2.txt echo ===== 2 - COMPILATION DU FICHIER =====
python -m py_compile luciana.py >> res_controle_obligation2.txt 2>&1
>> res_controle_obligation2.txt echo CODE_RETOUR_COMPILE=%ERRORLEVEL%
>> res_controle_obligation2.txt echo ===== 3 - LE VRAI BANC D ESSAI DE L OBLIGATION =====
python _verif_chien_de_garde_rangement.py >> res_controle_obligation2.txt 2>&1
>> res_controle_obligation2.txt echo CODE_RETOUR_BANC=%ERRORLEVEL%
>> res_controle_obligation2.txt echo ===== FIN =====
