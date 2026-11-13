$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$sources = @('D:\Project\.agents\skills','D:\Project\.claude\skills')
if ((Get-Item -LiteralPath $sources[0]).LinkType) { Write-Output 'Already relocated'; exit 0 }
python "$root\scripts\backup-skills.py"
if ($LASTEXITCODE -ne 0) { throw 'Skill backup failed' }
Move-Item -LiteralPath $sources[0] -Destination "$root\skills\shared"
Move-Item -LiteralPath $sources[1] -Destination "$root\skills\claude"
$records = @()
foreach ($dir in Get-ChildItem "$root\skills\claude" -Directory) {
    $canonical = Join-Path "$root\skills\shared" $dir.Name
    $left = @(Get-ChildItem $dir.FullName -Recurse -File | ForEach-Object { ($_.FullName.Substring($dir.FullName.Length)) + ':' + (Get-FileHash -LiteralPath $_.FullName).Hash } | Sort-Object)
    $right = @(Get-ChildItem $canonical -Recurse -File | ForEach-Object { ($_.FullName.Substring($canonical.Length)) + ':' + (Get-FileHash -LiteralPath $_.FullName).Hash } | Sort-Object)
    $same = ($left -join "`n") -ceq ($right -join "`n")
    if ($same) {
        $resolved = [IO.Path]::GetFullPath($dir.FullName)
        $boundary = [IO.Path]::GetFullPath("$root\skills\claude\")
        if (-not $resolved.StartsWith($boundary, [StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe relocation target' }
        Remove-Item -LiteralPath $resolved -Recurse -Force
        New-Item -ItemType Junction -Path $resolved -Target $canonical | Out-Null
    }
    $records += @{name=$dir.Name;canonical=$canonical;claude=$dir.FullName;identical=$same}
}
New-Item -ItemType Junction -Path $sources[0] -Target "$root\skills\shared" | Out-Null
New-Item -ItemType Junction -Path $sources[1] -Target "$root\skills\claude" | Out-Null
$records | ConvertTo-Json -Depth 4 | Set-Content "$root\reports\skills-migration.json"
Write-Output "Relocated $($records.Count) skills; preserved differing Claude variants; old discovery paths remain linked."
