$ErrorActionPreference='Continue'
$root=Split-Path $PSScriptRoot -Parent
$rows=@()
function Probe($name,$exe,$arguments) {
 try {
  $output=(& $exe @arguments 2>&1 | Out-String).Trim()
  $rows=@{name=$name;status=if($LASTEXITCODE -eq 0){'ready'}else{'failed'};output=$output}
 }catch{$rows=@{name=$name;status='missing';output=$_.Exception.Message}}
 return $rows
}
$rows+=Probe 'Node' 'node' @('--version')
$rows+=Probe 'Python' "$root\.venv\Scripts\python.exe" @('--version')
$rows+=Probe 'Java' 'java' @('-version')
$rows+=Probe 'Docker engine' 'docker' @('info','--format','{{.ServerVersion}}')
$rows+=Probe 'Schemathesis' "$root\.venv\Scripts\schemathesis.exe" @('--version')
$rows+=Probe 'Semgrep' "$root\.venv\Scripts\semgrep.exe" @('--version')
foreach($name in @('k6','gitleaks','trivy','toxiproxy','toxiproxy-cli')) {
 $exe=Get-ChildItem "$root\tools\$name" -Filter '*.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
 if($exe){$rows+=Probe $name $exe.FullName @('--version')}else{$rows+=@{name=$name;status='missing';output='Portable download not present'}}
}
$rows | ConvertTo-Json -Depth 4 | Set-Content "$root\reports\doctor.json"
$rows | ForEach-Object {Write-Output "$($_.name): $($_.status) $($_.output)"}
