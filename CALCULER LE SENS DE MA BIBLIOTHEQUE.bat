@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo CALCUL DU SENS DE TA BIBLIOTHEQUE PAR LE MOTEUR DE GOOGLE (V196), UNE SEULE FOIS.
echo Luciana peut rester ouverte. On peut fermer et relancer : il reprend ou il en etait.
python biblio2_moteur_google.py --tout
pause
