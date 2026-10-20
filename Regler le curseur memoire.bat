@echo off
chcp 65001 >nul
title Regler le curseur de la memoire
if not exist "%USERPROFILE%\Luciana\bibliotheque2" mkdir "%USERPROFILE%\Luciana\bibliotheque2"
echo.
echo   LE CURSEUR DE PERTINENCE DE TA MEMOIRE
echo   --------------------------------------
echo   Le curseur va de 0 a 1. C'est la barre a atteindre pour qu'un souvenir
echo   ressorte quand tu poses une question.
echo.
echo     0.6  = le reglage de depart (on commence par la, ensemble).
echo     plus HAUT (0.7 / 0.8) = plus severe : elle ne ressort un souvenir que
echo                             s'il est VRAIMENT proche de ta question.
echo     plus BAS  (0.5 / 0.4) = plus large : elle ressort plus facilement.
echo.
echo   Si rien n'atteint la barre, elle te repond avec ses connaissances
echo   generales, au lieu de te servir un souvenir qui n'a rien a voir.
echo.
set "c="
set /p c=  Quel curseur veux-tu (ex. 0.6) ?
if "%c%"=="" (
  echo.
  echo   Rien saisi : on ne change rien.
  echo.
  pause
  exit /b
)
(echo %c%)>"%USERPROFILE%\Luciana\bibliotheque2\curseur.txt"
echo.
echo   C'est fait : curseur = %c%
echo   Ca marche tout de suite, des ton prochain message (pas besoin de redemarrer).
echo.
pause
