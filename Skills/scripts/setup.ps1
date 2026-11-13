param([switch]$SkipSources)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
function Check-Exit {if($LASTEXITCODE -ne 0){throw "Installation command failed with code $LASTEXITCODE"}}
Push-Location $root
try {
 if(!$SkipSources){python scripts/download-toolkit.py; Check-Exit}
 python scripts/setup-java.py; Check-Exit
 .\scripts\setup-zap.ps1
 if(!(Test-Path .venv\Scripts\python.exe)){python -m venv .venv; Check-Exit}
 if(Test-Path requirements-lock.txt){.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt}else{.\.venv\Scripts\python.exe -m pip install schemathesis semgrep}; Check-Exit
 Push-Location frontend
 try {npm.cmd ci; Check-Exit; npx.cmd playwright install chromium firefox webkit; Check-Exit}finally{Pop-Location}
 .\scripts\run.ps1 java
}finally{Pop-Location}
