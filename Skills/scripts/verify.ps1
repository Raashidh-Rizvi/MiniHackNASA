$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$rows=@()
function Check([string]$task) {
 $log=Join-Path "$root\reports" "$task.log"
 try {& "$root\scripts\run.ps1" -Task $task *> $log; $state='passed'}catch{$state='failed'; $_ | Out-String | Add-Content $log}
 $script:rows+=@{task=$task;status=$state;log=$log}
 $script:rows | ConvertTo-Json | Set-Content "$root\reports\verification.json"
 Write-Output "$task : $state"
}
Check 'unit'
Check 'java'
Check 'browser'
Check 'mutation-js'
Check 'mutation-java'
Check 'semgrep'
Check 'secrets'
Check 'trivy'
Check 'lighthouse'
$demo=Start-Process -FilePath (Get-Command node).Source -ArgumentList 'server.mjs' -WorkingDirectory "$root\frontend" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root\reports\demo.log" -RedirectStandardError "$root\reports\demo-errors.log"
try {
 $ready=$false
 for($i=0;$i -lt 20;$i++) {
  try{Invoke-WebRequest http://127.0.0.1:4173/health -TimeoutSec 1 | Out-Null;$ready=$true;break}catch{Start-Sleep -Milliseconds 500}
 }
 if($ready){Check 'api';Check 'load';Check 'zap'}
 else{$rows+=@{task='demo';status='failed';log="$root\reports\demo-errors.log"}}
}finally{if(!$demo.HasExited){Stop-Process -Id $demo.Id}}
$rows | ConvertTo-Json | Set-Content "$root\reports\verification.json"
