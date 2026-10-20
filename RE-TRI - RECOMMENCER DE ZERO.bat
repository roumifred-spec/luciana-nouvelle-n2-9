@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo RE-TRI : ON RECOMMENCE DE ZERO. Le chantier commence est mis de cote (rien n est efface),
echo puis tout est re-trie par le sens et mis en service (l ancienne bibliotheque est gardee en copie datee).
echo A ne lancer qu UNE fois. Si la fenetre se ferme, relancez RE-TRI - TOUT.bat : il reprend ou il en etait.
python biblio2_retri_par_sens.py --tout-en-un --recommencer
pause
