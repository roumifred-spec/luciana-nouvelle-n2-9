@echo off
rem =====================================================================
rem  LE CONTROLE DU CHANTIER v149 : "LA REFONTE DU PANNEAU A VALIDER"
rem  (une seule ligne par chose, un seul numero visible, une vraie question en francais,
rem   et un OUI qui suffit UNE SEULE FOIS)
rem
rem  Double-clique ce fichier. Il fait TROIS choses, dans cet ordre :
rem    1) la SAUVEGARDE datee du programme d'AVANT le chantier (regle d'or n22). Elle est
rem       extraite de l'historique git (commit 01cdd3a) et PAS copiee depuis luciana.py --
rem       luciana.py est deja modifie a ce stade, le copier donnerait une sauvegarde qui
rem       mentirait sur son nom. Elle n'ecrase JAMAIS une sauvegarde qui existe deja, et elle
rem       se verifie avec DEUX points : la taille ET l'empreinte sha256. Si elle rate, le
rem       script le DIT.
rem    2) le BADGE, vu dans le fichier : il doit dire v149 une seule fois, et plus v148.
rem    3) les controles du chantier v149, un par un, avec le detail de ce qui rate :
rem       - trois mises a jour de la MEME chose ne laissent QU'UNE ligne dans la file ;
rem       - aucun numero de file dans le texte affiche a Fred ;
rem       - une chose deja en cours SANS question en recoit une, en francais (aucun .jsonl,
rem         aucun numero, ni 'etat' ni 'attente' dedans) ;
rem       - un OUI fait sortir la chose de la liste active ET la classe, UNE SEULE fois,
rem         sans doublon -- et un deuxieme clic n'ecrit rien de plus ;
rem       - le verrou de Fred bloque TOUJOURS une ecriture de Luciana (le repli) ;
rem       - rien n'est detruit, les nombres du panneau ne gonflent pas, deux choses font
rem         bien deux lignes, et chez Luminita il ne se passe rien du tout.
rem
rem  ZERO APPEL PAYE : tout tourne dans un bac a sable jetable. Rien n'est ecrit dans
rem  C:\Users\Fred\Luciana, rien dans le dossier du programme (sauf la sauvegarde datee et le
rem  compte rendu), rien chez Luminita, et aucun fichier n'est envoye nulle part.
rem
rem  Tout ce qui s'affiche est AUSSI ecrit dans res_refonte_panneau.txt, a cote de ce fichier :
rem  c'est ce fichier-la qu'il faut m'envoyer s'il y a du rouge.
rem =====================================================================
if "%~1"=="" (
  cmd /c ""%~f0" suite > "%~dp0res_refonte_panneau.txt" 2>&1"
  echo.
  echo Termine. Le resultat complet est dans : res_refonte_panneau.txt
  echo.
  type "%~dp0res_refonte_panneau.txt"
  pause
  exit /b
)
cd /d "%~dp0"
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ===== 1 - LA SAUVEGARDE DATEE DU PROGRAMME D'AVANT =====
python _faire_la_sauvegarde_v149_panneau.py
echo CODE_RETOUR_SAUVEGARDE=%ERRORLEVEL%
echo.
echo ===== 2 - LE BADGE, VU DANS LE FICHIER =====
findstr /N "ton amie &middot; v149" luciana.py
findstr /N "ton amie &middot; v148" luciana.py
echo (la premiere ligne doit apparaitre UNE fois ; la seconde, AUCUNE)
echo.
echo ===== 3 - LE CONTROLE DU CHANTIER v149 =====
python _verif_refonte_panneau.py
echo CODE_RETOUR_VERIF=%ERRORLEVEL%
echo.
echo ===== FIN =====
