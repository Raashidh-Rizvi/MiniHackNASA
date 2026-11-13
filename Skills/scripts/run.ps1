param(
 [Parameter(Mandatory)][ValidateSet('unit','browser','visual-update','browser-ui','mutation-js','java','database','mutation-java','serve','api','load','semgrep','secrets','trivy','lighthouse','zap','toxiproxy','toxiproxy-cli')][string]$Task,
 [string]$TargetPath, [string]$TargetUrl, [string]$SchemaUrl, [switch]$UseInstalledChromium,
 [Parameter(ValueFromRemainingArguments)][string[]]$ExtraArgs
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
function Run-Native([string]$exe,[string[]]$arguments) {
 & $exe @arguments
 if ($LASTEXITCODE -ne 0) {throw "$Task exited with code $LASTEXITCODE"}
}
function Find-Tool([string]$folder,[string]$pattern) {
 $found=Get-ChildItem "$root\tools\$folder" -Recurse -Filter $pattern -File | Select-Object -First 1
 if (!$found) {throw "Missing $folder; see reports\downloads.json and README.md"}; return $found.FullName
}
Push-Location $root
$oldTarget=$env:TARGET_URL
$oldPythonUtf8=$env:PYTHONUTF8
$oldBrowser=$env:TOOLKIT_CHROMIUM_EXECUTABLE
$env:PYTHONUTF8='1'
try {
 if($UseInstalledChromium) {
  if($Task -notin @('browser','visual-update','browser-ui')){throw '-UseInstalledChromium applies to browser tasks only'}
  $existing=Get-ChildItem "$env:LOCALAPPDATA\ms-playwright\chromium-*\chrome-win*\chrome.exe" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if(!$existing){throw 'No existing Playwright Chromium found'}
  $env:TOOLKIT_CHROMIUM_EXECUTABLE=$existing.FullName
  $ExtraArgs=@('--project=chromium-local')+$ExtraArgs
  Write-Output "Explicit local Chromium mode: $($existing.FullName); Firefox and WebKit are not selected."
 }
 if ($Task -in @('unit','browser','visual-update','browser-ui','mutation-js','lighthouse','serve')) {
  Set-Location "$root\frontend"
  if($TargetUrl){$env:TARGET_URL=$TargetUrl}else{Remove-Item Env:TARGET_URL -ErrorAction SilentlyContinue}
  $commands=@{unit='test';browser='e2e';'visual-update'='e2e:update';'browser-ui'='e2e:ui';'mutation-js'='mutation';lighthouse='lighthouse';serve='serve'}
  if($Task -eq 'lighthouse') {
   $chrome=Get-ChildItem "$env:LOCALAPPDATA\ms-playwright\chromium-*\chrome-win*\chrome.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
   if($chrome){$env:CHROME_PATH=$chrome.FullName}
  }
  Run-Native 'npm.cmd' (@('run',$commands[$Task],'--') + $ExtraArgs)
 } elseif($Task -in @('java','database','mutation-java')) {
  $mvn=Get-ChildItem "$root\tools\apache-maven-*\bin\mvn.cmd" | Select-Object -First 1
  if(!$mvn){throw 'Maven not installed; run python scripts/setup-java.py'}
  $goals=@{java=@('test');database=@('verify','-Pdatabase');'mutation-java'=@('test-compile','org.pitest:pitest-maven:mutationCoverage')}
  Run-Native $mvn.FullName (@('-B','-f',"$root\backend\pom.xml") + $goals[$Task] + $ExtraArgs)
 } elseif($Task -eq 'api') {
  if(!$SchemaUrl){$SchemaUrl='http://127.0.0.1:4173/openapi.json'}
  Run-Native "$root\.venv\Scripts\schemathesis.exe" (@('run',$SchemaUrl,'--max-examples','20','--report','junit','--report-junit-path',"$root\reports\schemathesis.xml")+$ExtraArgs)
 } elseif($Task -eq 'load') {
  if(!$TargetUrl){$TargetUrl='http://127.0.0.1:4173'}
  Run-Native (Find-Tool 'k6' 'k6.exe') (@('run','-e',"TARGET_URL=$TargetUrl","$root\load\smoke.js")+$ExtraArgs)
 } elseif($Task -eq 'semgrep') {
  if(!$TargetPath){$TargetPath="$root\frontend\src"}
  Run-Native "$root\.venv\Scripts\semgrep.exe" (@('scan','--config',"$root\security\rules.yml",'--metrics=off','--error',$TargetPath)+$ExtraArgs)
 } elseif($Task -eq 'secrets') {
  if(!$TargetPath){$TargetPath="$root\frontend\src"}
  Run-Native (Find-Tool 'gitleaks' 'gitleaks.exe') (@('dir',$TargetPath,'--redact','--report-format','json','--report-path',"$root\reports\gitleaks.json")+$ExtraArgs)
 } elseif($Task -eq 'trivy') {
  if(!$TargetPath){$TargetPath="$root\frontend"}
  Run-Native (Find-Tool 'trivy' 'trivy.exe') (@('fs','--scanners','vuln,misconfig','--skip-dirs','node_modules','--exit-code','1','--severity','HIGH,CRITICAL','--format','json','--output',"$root\reports\trivy.json",$TargetPath)+$ExtraArgs)
 } elseif($Task -eq 'toxiproxy') {
  Run-Native (Find-Tool 'toxiproxy' '*.exe') (@('-host','127.0.0.1')+$ExtraArgs)
 } elseif($Task -eq 'toxiproxy-cli') {
  Run-Native (Find-Tool 'toxiproxy-cli' '*.exe') $ExtraArgs
 } elseif($Task -eq 'zap') {
  if(!$TargetUrl){$TargetUrl='http://127.0.0.1:4173'}
  $quoted=ConvertTo-Json $TargetUrl -Compress
  $out=ConvertTo-Json "$root\reports" -Compress
  @"
env:
  contexts:
    - name: target
      urls: [$quoted]
jobs:
  - type: spider
    parameters:
      context: target
      maxDuration: 1
  - type: passiveScan-wait
    parameters:
      maxDuration: 2
  - type: report
    parameters:
      template: traditional-html
      reportDir: $out
      reportFile: zap-passive.html
"@ | Set-Content "$root\reports\zap-plan.yaml"
  $zapBat=Find-Tool 'zap' 'zap.bat'
  Push-Location (Split-Path $zapBat -Parent)
  try {Run-Native $zapBat @('-cmd','-silent','-dir',"$root\tools\zap-home",'-config','autoupdate.checkOnStart=false','-autorun',"$root\reports\zap-plan.yaml")}finally{Pop-Location}
 }
} finally { $env:TARGET_URL=$oldTarget; $env:PYTHONUTF8=$oldPythonUtf8; $env:TOOLKIT_CHROMIUM_EXECUTABLE=$oldBrowser; Pop-Location }
