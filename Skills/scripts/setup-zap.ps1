$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$zapBat=Get-ChildItem "$root\tools\zap" -Recurse -Filter zap.bat | Select-Object -First 1
if(!$zapBat){throw 'Download ZAP Core first'}
New-Item -ItemType Directory -Force "$root\tools\zap-home" | Out-Null
Push-Location $zapBat.DirectoryName
try {
 & $zapBat.FullName -cmd -dir "$root\tools\zap-home" -addoninstall automation
 if($LASTEXITCODE -ne 0){throw "ZAP add-on installation exited $LASTEXITCODE"}
}finally{Pop-Location}
