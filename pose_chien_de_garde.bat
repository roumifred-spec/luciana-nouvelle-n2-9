@echo off
chcp 65001 >nul
cd /d "C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
python pose_chien_de_garde.py > res_pose_chien_de_garde.txt 2>&1
echo. >> res_pose_chien_de_garde.txt
echo === FIN === >> res_pose_chien_de_garde.txt
exit
