$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$src = (Resolve-Path "$PSScriptRoot\src\board.html").Path -replace '\\', '/'
$boards = [ordered]@{
  'overview' = '00-resumen-v3'
  'context'  = '01-contexto-presentacion'
  'globo'    = '02-globo-industrial'
  'sv'       = '03-monograma-SV'
  'corp'     = '04-opciones-corporativas'
  'palette'  = '05-paleta-y-tipografia'
  'selection' = '06-seleccion-final'
  'plateV'   = '07-placa-simbolos-vertical'
  'plateH'   = '08-placa-simbolos-horizontal'
}
$only = $args
foreach ($k in $boards.Keys) {
  if ($only.Count -gt 0 -and $only -notcontains $k) { continue }
  $out = Join-Path (Resolve-Path "$PSScriptRoot\..\bocetos").Path "$($boards[$k]).png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    --window-size=1600,1000 --virtual-time-budget=8000 --allow-file-access-from-files `
    "--screenshot=$out" "file:///$src`?b=$k" 2>$null | Out-Null
  Write-Output "$k -> $out ($(Test-Path $out))"
}
