$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Set-Location $PSScriptRoot
$bocetos = (Resolve-Path "..\..\bocetos").Path
node generate.mjs

New-Item -ItemType Directory -Force -Path png | Out-Null
Get-ChildItem svg\*.svg | ForEach-Object {
  $src = $_.FullName -replace '\\', '/'
  $out = Join-Path $PSScriptRoot "png\$($_.BaseName).png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    --window-size=500,500 "--screenshot=$out" "file:///$src" 2>$null | Out-Null
}

$board = (Resolve-Path "..\src\globo.html").Path -replace '\\', '/'
$boards = [ordered]@{ 'grid' = '09-globo-america-venezuela'; 'detail' = '10-globo-detalle-venezuela'; 'final' = '11-globo-finalistas' }
foreach ($k in $boards.Keys) {
  $out = Join-Path $bocetos "$($boards[$k]).png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    --window-size=1600,1000 --virtual-time-budget=8000 --allow-file-access-from-files `
    "--screenshot=$out" "file:///$board`?b=$k" 2>$null | Out-Null
  Write-Output "$k -> $out"
}

$wm = (Resolve-Path "..\src\wordmarks.html").Path -replace '\\', '/'
$out = Join-Path $bocetos "12-globo-finalistas-logotipos.png"
& $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
  --window-size=2000,1400 --virtual-time-budget=10000 --allow-file-access-from-files `
  "--screenshot=$out" "file:///$wm" 2>$null | Out-Null
Write-Output "wordmarks -> $out"

$solo = [ordered]@{ 'logos' = @('13-simbolos-finalistas', 900); 'words' = @('14-logotipos-sadaco', 1250) }
foreach ($k in $solo.Keys) {
  $out = Join-Path $bocetos "$($solo[$k][0]).png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    "--window-size=2000,$($solo[$k][1])" --virtual-time-budget=10000 --allow-file-access-from-files `
    "--screenshot=$out" "file:///$wm`?b=$k" 2>$null | Out-Null
  Write-Output "$k -> $out"
}

$presDir = Join-Path (Resolve-Path "..\..").Path "entregables\presentacion"
New-Item -ItemType Directory -Force -Path $presDir | Out-Null
$clean = [ordered]@{ 'logos' = @('01-simbolos-finalistas', 620); 'words' = @('02-logotipos-sadaco', 1250) }
foreach ($k in $clean.Keys) {
  $out = Join-Path $presDir "$($clean[$k][0]).png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    "--window-size=2000,$($clean[$k][1])" --virtual-time-budget=10000 --allow-file-access-from-files `
    "--screenshot=$out" "file:///$wm`?b=$k&clean=1" 2>$null | Out-Null
  Write-Output "clean $k -> $out"
}
