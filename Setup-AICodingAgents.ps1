# Run from Windows PowerShell 5.1 or PowerShell 7.
# Configures D:\Project for Claude Code, Codex, Antigravity, OpenCode, and Freebuff.
# It only installs skill bundles and Playwright MCP. It does not disable approval prompts.
param([string]$ProjectRoot = 'D:\Project')

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "Project directory not found: $ProjectRoot"
}
if (-not (Get-Command node.exe -ErrorAction SilentlyContinue)) {
    throw 'Node.js is not on PATH. Install Node.js 22+ first.'
}
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw 'npm.cmd is not on PATH. Reinstall Node.js/npm.'
}
if (-not (Get-Command npx.cmd -ErrorAction SilentlyContinue)) {
    throw 'npx.cmd is not on PATH. Reinstall Node.js/npm.'
}

Set-Location -LiteralPath $ProjectRoot
Write-Host "Configuring AI agents at: $ProjectRoot" -ForegroundColor Cyan
Write-Host "Node version: $(& node.exe --version)"

# 1. Install portable skills into the agent-specific, project-local locations.
# --copy avoids Windows junction/symlink permission issues.
$agents = @('claude-code', 'antigravity', 'codex', 'opencode')
function Add-SkillsFromRepo {
    param([string]$Repo, [string]$Skill = '')
    $params = @('-y', 'skills', 'add', $Repo, '-y', '--copy')
    if ($Skill) { $params += @('--skill', $Skill) }
    foreach ($agent in $agents) { $params += @('-a', $agent) }
    Write-Host "Installing skills: $Repo $(if ($Skill) { ' / ' + $Skill })" -ForegroundColor Yellow
    & npx.cmd @params
    if ($LASTEXITCODE -ne 0) { Write-Warning "Skill installation failed: $Repo" }
}

Add-SkillsFromRepo 'Leonxlnx/taste-skill'
Add-SkillsFromRepo 'vercel-labs/agent-skills' 'web-design-guidelines'
Add-SkillsFromRepo 'addyosmani/agent-skills'
Add-SkillsFromRepo 'pbakaus/impeccable'
Add-SkillsFromRepo 'DietrichGebert/ponytail' 'ponytail'

# 2. Install Playwright MCP outside the application's own node_modules.
# Launching the JS entrypoint with node.exe works around native Windows npx/cmd stdio issues.
$toolRoot = Join-Path $ProjectRoot '.agent-tools'
New-Item -ItemType Directory -Force -Path $toolRoot | Out-Null
Write-Host 'Installing local Playwright MCP runtime...' -ForegroundColor Yellow
& npm.cmd install --prefix $toolRoot --no-audit --no-fund '@playwright/mcp@latest'
if ($LASTEXITCODE -ne 0) { throw 'Playwright MCP npm installation failed.' }
$cli = Join-Path $toolRoot 'node_modules\@playwright\mcp\cli.js'
if (-not (Test-Path -LiteralPath $cli)) { throw "Missing Playwright MCP entrypoint: $cli" }
$cli = (Resolve-Path -LiteralPath $cli).Path

# 3. Safely merge each tool's JSON MCP config, creating backups when editing.
function Add-JsonMcp {
    param([string]$Path, [string]$Section, [object]$Server)
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    if (Test-Path -LiteralPath $Path) {
        try {
            $doc = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
        } catch {
            Write-Warning "Could not parse $Path as JSON; leaving it unchanged. Edit it manually if it contains JSONC comments."
            return
        }
        Copy-Item -LiteralPath $Path -Destination ($Path + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    } else {
        $doc = [pscustomobject]@{}
    }
    if (-not $doc.PSObject.Properties[$Section]) {
        $doc | Add-Member -NotePropertyName $Section -NotePropertyValue ([pscustomobject]@{})
    }
    if ($doc.$Section.PSObject.Properties['playwright']) {
        Write-Host "Existing Playwright MCP preserved: $Path" -ForegroundColor DarkYellow
        return
    }
    $doc.$Section | Add-Member -NotePropertyName 'playwright' -NotePropertyValue $Server
    $json = $doc | ConvertTo-Json -Depth 80
    [System.IO.File]::WriteAllText($Path, $json + [Environment]::NewLine, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "Added Playwright MCP: $Path" -ForegroundColor Green
}

$commonServer = [pscustomobject]@{ command = 'node'; args = @($cli) }
Add-JsonMcp (Join-Path $ProjectRoot '.mcp.json') 'mcpServers' $commonServer
Add-JsonMcp (Join-Path $ProjectRoot '.agents\mcp_config.json') 'mcpServers' $commonServer
Add-JsonMcp (Join-Path $ProjectRoot '.agents\mcp.json') 'mcpServers' $commonServer
$openCodeServer = [pscustomobject]@{ type = 'local'; command = @('node', $cli); enabled = $true; timeout = 15000 }
Add-JsonMcp (Join-Path $ProjectRoot 'opencode.json') 'mcp' $openCodeServer

# 4. Codex uses TOML rather than JSON. This config is project-scoped.
$codexConfig = Join-Path $ProjectRoot '.codex\config.toml'
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $codexConfig) | Out-Null
$toml = if (Test-Path -LiteralPath $codexConfig) { Get-Content -LiteralPath $codexConfig -Raw } else { '' }
if ($toml -notmatch '(?m)^\s*\[mcp_servers\.(?:"playwright"|playwright)\]\s*$') {
    if (Test-Path -LiteralPath $codexConfig) {
        Copy-Item -LiteralPath $codexConfig -Destination ($codexConfig + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    }
    # TOML single-quoted strings treat backslashes as literal characters.
    $tomlPath = $cli.Replace("'", "")
    $block = "`r`n[mcp_servers.playwright]`r`ncommand = 'node'`r`nargs = ['$tomlPath']`r`nstartup_timeout_sec = 20`r`n"
    [System.IO.File]::WriteAllText($codexConfig, $toml + $block, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "Added Playwright MCP: $codexConfig" -ForegroundColor Green
} else {
    Write-Host "Existing Codex Playwright MCP preserved: $codexConfig" -ForegroundColor DarkYellow
}

# 5. Add Graphify project-local skill if the Graphify CLI is already installed.
if (Get-Command graphify -ErrorAction SilentlyContinue) {
    Write-Host 'Installing Graphify into project-local Agent Skills directories...' -ForegroundColor Yellow
    & graphify install --project --platform agents
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Graphify cross-agent install failed; inspect graphify --help.' }
    # Also install the Claude Code Windows integration, where hooks may be supported.
    & graphify install --project --platform windows
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Graphify Claude Code Windows install failed.' }
} else {
    Write-Warning 'Graphify CLI not found. Official package: uv tool install graphifyy'
}

# 6. Do not accidentally commit Playwright MCP dependencies to Git.
$ignorePath = Join-Path $ProjectRoot '.gitignore'
$ignore = if (Test-Path -LiteralPath $ignorePath) { Get-Content -LiteralPath $ignorePath -Raw } else { '' }
if ($ignore -notmatch '(?m)^\s*\.agent-tools/\s*$') {
    [System.IO.File]::AppendAllText($ignorePath, "`r`n# Local AI agent tooling`r`n.agent-tools/`r`n", (New-Object System.Text.UTF8Encoding($false)))
}

# 7. Verify project-level artifacts and available CLIs.
Write-Host "`nInstalled SKILL.md files:" -ForegroundColor Cyan