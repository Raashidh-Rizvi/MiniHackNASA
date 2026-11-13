# One-time installation for the current Windows user's Codex chats.
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$source=Join-Path $root 'skills\shared\testing-toolkit'
$userSkills=Join-Path $env:USERPROFILE '.agents\skills'
$destination=Join-Path $userSkills 'testing-toolkit'
if(!(Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))){throw "Skill source missing: $source"}
New-Item -ItemType Directory -Force -Path $userSkills | Out-Null
if(Test-Path -LiteralPath $destination){
 $existing=Get-Item -LiteralPath $destination
 if($existing.LinkType -eq 'Junction' -and [IO.Path]::GetFullPath([string]$existing.Target) -eq [IO.Path]::GetFullPath($source)){
  Write-Output "Already installed for this user: $destination"
  exit 0
 }
 throw "An existing skill occupies $destination; it was preserved."
}
New-Item -ItemType Junction -Path $destination -Target $source | Out-Null
if(!(Test-Path -LiteralPath (Join-Path $destination 'SKILL.md'))){throw 'Global discovery link could not be read'}
Write-Output "Installed for all local Codex projects of this Windows user: $destination"
Write-Output 'Use $testing-toolkit in your next turn. If it is absent, start a new chat or restart Codex.'
