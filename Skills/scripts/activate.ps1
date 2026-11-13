# Dot-source this file: . D:\Project\Skills\scripts\activate.ps1
$env:SKILLS_TOOLKIT_ROOT = Split-Path $PSScriptRoot -Parent
$toolDirs = @(Get-ChildItem "$env:SKILLS_TOOLKIT_ROOT\tools" -Recurse -File -Filter '*.exe' | ForEach-Object DirectoryName | Sort-Object -Unique)
$mavenDirs = @(Get-ChildItem "$env:SKILLS_TOOLKIT_ROOT\tools" -Directory -Filter 'apache-maven-*' | ForEach-Object { Join-Path $_.FullName 'bin' })
$env:PATH = (@("$env:SKILLS_TOOLKIT_ROOT\.venv\Scripts","$env:SKILLS_TOOLKIT_ROOT\frontend\node_modules\.bin") + $toolDirs + $mavenDirs + @($env:PATH)) -join ';'
Write-Output "Testing toolkit active for this terminal: $env:SKILLS_TOOLKIT_ROOT"
