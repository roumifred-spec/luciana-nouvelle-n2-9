@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================================================
echo   LE PERSONNAGE ANIME DE LUCIANA - les trois etapes, dans l'ordre
echo ==========================================================================
echo.
echo   1) on remet la BASE v100 (celle qui tourne chez toi, SANS la dictee Whisper)
echo   2) on pose le PERSONNAGE
echo   3) on CONTROLE le resultat
echo.
echo   Si une etape echoue, on s'arrete : rien n'est ecrit a moitie.
echo.
pause

echo.
echo --- 1) LA BASE v100 -------------------------------------------------------
python _poser_la_base_v100.py
if errorlevel 1 goto rate

echo.
echo --- 2) LE PERSONNAGE ------------------------------------------------------
python _poser_le_personnage_luciana.py
if errorlevel 1 goto rate

echo.
echo --- 3) LE CONTROLE --------------------------------------------------------
python _verif_personnage_luciana.py

echo.
echo ==========================================================================
echo   FINI. Lis le controle ci-dessus : ce qui est [RATE] est un vrai probleme,
echo   ce qui est [ ? ] n'a pas pu etre verifie et n'est PAS suppose bon.
echo.
echo   IL RESTE A DEPOSER LES HUIT VIDEOS dans le dossier "apparence" :
echo     personnage_1_marche.webm  personnage_2_parle.webm  personnage_3_regarde.webm
echo     activite_01.webm  activite_02.webm  activite_03.webm  activite_04.webm
echo     activite_05.webm
echo ==========================================================================
pause
exit /b 0

:rate
echo.
echo ==========================================================================
echo   ARRETE : l'etape ci-dessus a echoue. Rien n'a ete ecrit a moitie.
echo   Lis le message juste au-dessus : il dit ce qui bloque.
echo ==========================================================================
pause
exit /b 1
