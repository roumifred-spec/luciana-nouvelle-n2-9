@echo off
rem =====================================================================
rem  LE CONTROLE DU CHANTIER v150 : "LE VRAI CERVEAU (DeepSeek REFLECHI)
rem  DANS TOUT LE BIBLIOTHECAIRE ET L'ARCHIVISTE"
rem
rem  Double-clique ce fichier. Il fait TROIS choses, dans cet ordre :
rem    1) la SAUVEGARDE datee du programme d'AVANT le chantier (regle d'or n22).
rem       Elle est extraite de l'historique git (commit 9a7fa4b) et PAS copiee
rem       depuis luciana.py -- luciana.py est deja la v150 a ce stade, le copier
rem       donnerait une sauvegarde qui mentirait sur son nom. Elle n'ecrase JAMAIS
rem       une sauvegarde qui existe deja, et elle se verifie sur DEUX points :
rem       la taille ET l'empreinte sha256.
rem       POUR COMPARER AUSSI AVEC LE FICHIER QUI TOURNE CHEZ FRED, lance plutot
rem       le script a la main avec les deux points releves sur le PC :
rem          python _faire_la_sauvegarde_v150_cerveau_reflechi.py <taille> <empreinte>
rem    2) le BADGE, vu dans le fichier : il doit dire v150 une seule fois, et plus v149.
rem    3) les verifications du chantier v150, une par une, avec le detail de ce qui
rem       rate : la compilation, l'option de reflexion qui ne part PLUS (requete
rem       interceptee), le rangement par le cerveau rallume, UN SEUL appel au cerveau
rem       par message (appels comptes pour de vrai), CINQ pannes simulees pour la
rem       cascade, le repli compare element par element au comportement d'avant, et
rem       Luminita qui n'a pas ete touchee.
rem
rem  ZERO APPEL PAYE : le cerveau est remplace par un faux client dans un bac a sable
rem  jetable. Rien n'est ecrit dans C:\Users\Fred\Luciana, rien dans le dossier du
rem  programme, rien chez Luminita, et aucun fichier n'est envoye nulle part.
rem
rem  Tout ce qui s'affiche est AUSSI ecrit dans res_v150.txt, a cote de ce fichier :
rem  c'est ce fichier-la qu'il faut m'envoyer s'il y a du rouge.
rem =====================================================================
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_v150.txt" 2>&1"
  echo.
  echo Termine. Le resultat complet est dans : res_v150.txt
  echo.
  type "%~dp0res_v150.txt"
  pause
  exit /b
)
cd /d "%~dp0"
echo ===== 1 - LA SAUVEGARDE DATEE DU PROGRAMME D'AVANT =====
python _faire_la_sauvegarde_v150_cerveau_reflechi.py
echo CODE_RETOUR_SAUVEGARDE=%ERRORLEVEL%
echo.
echo ===== 2 - LE BADGE, VU DANS LE FICHIER =====
findstr /N "ton amie &middot; v150" luciana.py
findstr /N "ton amie &middot; v149" luciana.py
echo (la premiere ligne doit apparaitre UNE fois ; la seconde, AUCUNE)
echo.
echo ===== 3 - LE CONTROLE DU CHANTIER v150 =====
python _verif_v150_cerveau_reflechi.py
echo CODE_RETOUR_VERIF=%ERRORLEVEL%
echo.
echo ===== FIN =====
