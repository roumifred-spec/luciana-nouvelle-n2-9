@echo off
cd /d C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75
echo ================ LE BANC D'ESSAI DU CHIEN DE GARDE ================
python _verif_chien_de_garde_rangement.py > res_banc_obligation.txt 2>&1
echo CODE_RETOUR_BANC=%errorlevel% >> res_banc_obligation.txt
echo ================ LA COMPILATION DU FICHIER DU DEPOT =================
python -m py_compile luciana.py > res_compile_obligation.txt 2>&1
echo CODE_RETOUR_COMPILE=%errorlevel% >> res_compile_obligation.txt
echo FINI - les deux resultats sont ecrits dans le dossier.
