import datetime,json,os,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
def read(name,default):
    p=root/'reports'/name
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
downloads=read('downloads.json',[])
checks=read('verification.json',[])
if isinstance(checks,dict):checks=[checks]
sources={r['name']:r for r in downloads if 'repository' in r}
portable=[r for r in downloads if 'repository' not in r]
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).isoformat(timespec='minutes')
lines=['# Setup status',f'','Updated: '+now+' (Asia/Colombo).','',
'## Skills and learning plugin','',
'- 43 existing shared skill names relocated; new testing-toolkit skill added (44 total).',
'- All 298 original source files verified byte-for-byte against the backup: see skills-integrity.json.',
'- Claude Graphify variant retained; original project discovery paths remain junctions.',
'- VibeWise 0.1.44 registered at project scope in this folder; activation still requires restarting Claude Code and invoking `/vibe-wise:learn`.',
'- Other projects require their own plugin scope/activation. Codex does not run Claude hooks automatically.','',
'## Source downloads','',f'{len([r for r in sources.values() if r["status"]=="downloaded"])}/20 source checkouts recorded as successful. Shallow history; upstream dependencies were not all built.','',
'| Source | State | Revision |','|---|---|---|']
for name,r in sorted(sources.items()):lines.append(f'| {name} | {r["status"]} | {r.get("commit",r.get("error",""))} |')
lines+=['','## Portable tools','', '| Tool | Release | State | Release SHA256 verified |','|---|---|---|---|']
for r in portable:lines.append(f'| {r["name"]} | {r.get("version","-")} | {r["status"]} | {r.get("verifiedReleaseChecksum",False)} |')
lines+=['','Maven version and Java dependency versions are in [java-versions.json](java-versions.json). Maven ZIP was verified against its official SHA512. JavaScript installation is reproducible once frontend/package-lock.json exists; Python is pinned once requirements-lock.txt exists. Runtime availability is recorded in [doctor.json](doctor.json) when generated.','',
'## Executed checks','', '| Check | Result | Evidence |','|---|---|---|']
for r in checks:
    log=pathlib.Path(r.get('log','')).name
    lines.append(f'| {r["task"]} | {r["status"]} | [{log}]({log}) |')
if not checks:lines.append('| Installation / checks | In progress | See individual installation logs |')
lines+=['','## Browser archive installation','', '| Matching Playwright engine | State |','|---|---|']
browser_manifest=root/'frontend/node_modules/playwright-core/browsers.json'
if browser_manifest.exists():
    for b in json.loads(browser_manifest.read_text())['browsers']:
        if b['name'] not in ['chromium','chromium-headless-shell','firefox','webkit','ffmpeg']:continue
        cache=pathlib.Path(os.environ['LOCALAPPDATA'])/'ms-playwright'/(b['name'].replace('-','_')+'-'+b['revision'])
        lines.append(f'| {b["name"]} {b["revision"]} | '+('Installed' if (cache/'INSTALLATION_COMPLETE').exists() else 'Download incomplete; see browser download logs')+' |')
lines+=['','Existing Chromium 1247 was explicitly selected for the verified chromium-local tests. Browser archives were fetched from the exact official URLs printed by the installed Playwright CLI. See browser-download-plan.txt and browser-range-install.log; resumable chunks remain in downloads/.','',
'ZAP passive scanning completed with demo findings: 0 high, 2 medium, 1 low, and 1 informational. This means the scan ran successfully; it does not mean the demo or a target application has no security issues. See [the actual HTML report](zap-passive.html).','',
'Semgrep distribution metadata is 1.182.1; its CLI reports 1.179.0 on this machine. Both are retained in the installation/version evidence. The local smoke rule scanned two example source files with no findings.']
lines+=['','## Blockers and practical limits','',
'- Docker executable exists, but the Linux engine was unavailable at initial inspection and after launching Docker Desktop. Database integration requires a running engine; no successful database test is claimed unless explicitly recorded above.',
'- The initial npm attempt failed with ETARGET for rolldown due to stale cached metadata. Refreshing metadata resolved installation. The mutation runner showed incompatibility with Vitest 5, so Vitest and coverage are pinned to 4.1.10 (the Stryker 10 runner\'s own tested development version), alongside Vite 8.3.5. See npm-compatibility.log and npm-versions.txt.',
'- Network downloads were slow. A failed source/binary download is recorded in downloads.json; rerunning scripts/download-toolkit.py retries missing items.',
'- Trivy itself is installed and its configuration scan succeeded with embedded checks. Its vulnerability scan was blocked by downloading the 129 MiB vulnerability database: the default mirror stalled, and the explicit GHCR retry ended with context deadline exceeded. Retry scripts/run.ps1 trivy when database access is reliable.',
'- The standard browser download repeatedly timed out. Resumable archive attempts retained partial downloads. Matching-browser availability is listed above; the successfully tested older Chromium and current WebKit remain usable.',
'- An earlier Firefox baseline run overlapped another Playwright run and collided in the shared trace folder. The final browser verification was run alone; use browser-three-engines-verified.log and the final HTML report as the authoritative result.',
'- Security findings (for example from Trivy) are different from installation failures. Review scanner reports before suppressing findings.',
'- Older agent skills can require optional MCP servers, external APIs, models, or accounts. Their instructions and support files were preserved; this setup does not provision every optional service.',
'- Bundled tests demonstrate tool operation only. Real project business logic, auth, tenancy, external services, and production performance still need targeted tests.',
'- Maven dependencies use the normal user .m2 cache; Playwright uses the normal LOCALAPPDATA/ms-playwright browser cache. Their project configuration and tool launchers are kept here.',
'- No target application or CI configuration was modified. The claude-mem observer remains signed out; work-state records are separate from durable observation capture.','',
'## Next commands','', 'See [README](../README.md), [every tool](../docs/TOOLS.md), and [every skill](../docs/SKILLS.md). Start with unit, Java, browser, then the specific risk you want to test.']
(root/'reports/SETUP-STATUS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Status report updated')
