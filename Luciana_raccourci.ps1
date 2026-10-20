# Cree le raccourci "Luciana" (version v75) avec le portrait de Luciana comme icone.
# Ecrit par Luciana le 01/10/2026.
$ErrorActionPreference = 'Stop'

$portrait = 'C:\Users\Fred\Desktop\Luciana_portrait_2.jpg'
$ico      = 'C:\Users\Fred\Desktop\luciana_v75\Luciana.ico'
$lnk      = 'C:\Users\Fred\Desktop\Luciana.lnk'
$cible    = 'C:\Users\Fred\Desktop\Lancer_Luciana_v75.bat'
$dossier  = 'C:\Users\Fred\Desktop\luciana_v75\luciana_v74'

if (-not (Test-Path $portrait)) { Write-Host 'PORTRAIT_INTROUVABLE'; exit 1 }
if (-not (Test-Path $cible))    { Write-Host 'LANCER_V75_INTROUVABLE'; exit 1 }

# 1) Fabriquer l'icone (.ico) a partir du portrait
Add-Type -AssemblyName System.Drawing
$img  = [System.Drawing.Image]::FromFile($portrait)
$cote = [Math]::Min($img.Width, $img.Height)
$srcX = [int](($img.Width  - $cote) / 2)
$srcY = [int](($img.Height - $cote) / 2)

$bmp = New-Object System.Drawing.Bitmap 256, 256
$g   = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$dstRect = New-Object System.Drawing.Rectangle 0, 0, 256, 256
$srcRect = New-Object System.Drawing.Rectangle $srcX, $srcY, $cote, $cote
$g.DrawImage($img, $dstRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
$g.Dispose()

$hicon = $bmp.GetHicon()
$icon  = [System.Drawing.Icon]::FromHandle($hicon)
$fs    = [System.IO.File]::Create($ico)
$icon.Save($fs)
$fs.Close()
$icon.Dispose()
$bmp.Dispose()
$img.Dispose()

# 2) Creer le raccourci avec cette icone
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($lnk)
$sc.TargetPath       = $cible
$sc.WorkingDirectory = $dossier
$sc.IconLocation     = "$ico,0"
$sc.Description      = 'Luciana v75 (derniere version)'
$sc.Save()

if (Test-Path $ico) { Write-Host 'ICO_OK' }
if (Test-Path $lnk) { Write-Host 'LNK_OK' }
Write-Host 'TERMINE'
