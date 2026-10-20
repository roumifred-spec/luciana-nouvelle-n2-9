@echo off
set LIVE=C:\Users\Fred\Desktop\luciana_v96\luciana_v96\luciana.py
set LOG=C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\res_reperes.txt
echo === REPERES DANS LE FICHIER EN SERVICE (06/10/2026 23h16) === > "%LOG%"
for %%S in (chien_de_garde_a_donner RAYON_A_TRANCHER _sous_luciana sous_tiroirs_de _carnets_pertinents choisir_en_filtrant sous_tiroirs_orphelins) do (
  for /f %%N in ('findstr /C:"%%S" "%LIVE%" ^| find /c /v ""') do echo %%S : %%N ligne(s) >> "%LOG%"
)
echo --- le badge de version --- >> "%LOG%"
findstr /C:"&middot; v12" "%LIVE%" >> "%LOG%"
exit
