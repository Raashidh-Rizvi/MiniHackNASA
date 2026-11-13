# Setup status

Updated: 2026-10-23T11:01+05:30 (Asia/Colombo).

## Skills and learning plugin

- 43 existing shared skill names relocated; new testing-toolkit skill added (44 total).
- All 298 original source files verified byte-for-byte against the backup: see skills-integrity.json.
- Claude Graphify variant retained; original project discovery paths remain junctions.
- VibeWise 0.1.44 registered at project scope in this folder; activation still requires restarting Claude Code and invoking `/vibe-wise:learn`.
- Other projects require their own plugin scope/activation. Codex does not run Claude hooks automatically.

## Source downloads

20/20 source checkouts recorded as successful. Shallow history; upstream dependencies were not all built.

| Source | State | Revision |
|---|---|---|
| axe-core | downloaded | 6b52b841461bd23345970b91ec75fdaff6bad31a |
| gitleaks | downloaded | b58d3f102cf3a2c84cb7f923d05c25c9b1aed84b |
| junit | downloaded | 576f546b1620c1689a3744351ce66a512e6531fb |
| k6 | downloaded | bae5899a2e048b28401cb2cf73a5f190950ffefc |
| lighthouse-ci | downloaded | 44c608c465f7b285976ce0b37786391cedc3d2f4 |
| mockito | downloaded | 220c594adceebf92a0d06e2fb1e4398b25344d46 |
| pitest | downloaded | f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6 |
| playwright | downloaded | 20a2087ea43412b90c172c88faef80786ee18b8b |
| rest-assured | downloaded | 9078ee01430e0024cc4538ee58819558d810acec |
| schemathesis | downloaded | 376156eafddc6f88b47c640f758078b2175ad957 |
| semgrep | downloaded | 087e93b3a1fdf44f97bc92b5b9c2ba221cb2488b |
| stryker-js | downloaded | c931a93237816901f1e9f48da411170beeb3dfca |
| testcontainers-java | downloaded | 10b31599694f3c49b4d7455cf1a375f30f150d11 |
| testing-library | downloaded | 20ce75f2907ca0e5c5a8ae595c0e9a4e368c7800 |
| toxiproxy | downloaded | 49299d8838525126e09c85ebe0ba89940a3261e5 |
| trivy | downloaded | 0231990f702f626e6981afaafcb0c97d43be28c7 |
| vibe-wise | downloaded | eefb53df406ab89e31444684ff32c1df205221f8 |
| vitest | downloaded | a5022655de04ec3581026dac16b11251e4b6d40d |
| wiremock | downloaded | a41e0f1f2f0d2f5b4cdca5fed43d93870b42bf07 |
| zap | downloaded | beb2c3502c39b80b281348f6349ea0df46ae61df |

## Portable tools

| Tool | Release | State | Release SHA256 verified |
|---|---|---|---|
| gitleaks | v8.30.1 | downloaded | True |
| k6 | v2.3.0 | downloaded | True |
| toxiproxy | v2.13.0 | downloaded | True |
| toxiproxy-cli | v2.13.0 | downloaded | True |
| zap | v2.17.0 | downloaded | True |
| trivy | v0.76.1 | downloaded | True |

Maven version and Java dependency versions are in [java-versions.json](java-versions.json). Maven ZIP was verified against its official SHA512. JavaScript installation is reproducible once frontend/package-lock.json exists; Python is pinned once requirements-lock.txt exists. Runtime availability is recorded in [doctor.json](doctor.json) when generated.

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| unit | passed | [unit-final.log](unit-final.log) |
| java | passed | [java-test-retry.log](java-test-retry.log) |
| browser-chromium-local | passed | [browser-launcher.log](browser-launcher.log) |
| mutation-js | passed | [mutation-js-retry.log](mutation-js-retry.log) |
| mutation-java | passed | [mutation-java.log](mutation-java.log) |
| lighthouse | passed | [lighthouse-retry.log](lighthouse-retry.log) |
| load | passed | [load.log](load.log) |
| secrets | passed | [secrets.log](secrets.log) |
| toxiproxy | passed | [toxiproxy-smoke.json](toxiproxy-smoke.json) |
| database | blocked-Docker | [database.log](database.log) |
| trivy-vulnerability-scan | blocked-database-download | [trivy-retry.log](trivy-retry.log) |
| semgrep | passed | [semgrep.log](semgrep.log) |
| trivy-configuration | passed | [trivy-config-retry.log](trivy-config-retry.log) |
| browser-chromium-and-webkit | passed | [browser-two-engines.log](browser-two-engines.log) |
| zap-passive | completed-with-findings | [zap-final.log](zap-final.log) |
| api | passed | [api-after-install.log](api-after-install.log) |
| chromium-matching-version-download | incomplete-network-timeouts | [browser-install.log](browser-install.log) |
| browser-three-engines | passed | [browser-three-engines-verified.log](browser-three-engines-verified.log) |

## Browser archive installation

| Matching Playwright engine | State |
|---|---|
| chromium 1248 | Download incomplete; see browser download logs |
| chromium-headless-shell 1248 | Download incomplete; see browser download logs |
| firefox 1555 | Installed |
| webkit 2370 | Installed |
| ffmpeg 1013 | Installed |

Existing Chromium 1247 was explicitly selected for the verified chromium-local tests. Browser archives were fetched from the exact official URLs printed by the installed Playwright CLI. See browser-download-plan.txt and browser-range-install.log; resumable chunks remain in downloads/.

ZAP passive scanning completed with demo findings: 0 high, 2 medium, 1 low, and 1 informational. This means the scan ran successfully; it does not mean the demo or a target application has no security issues. See [the actual HTML report](zap-passive.html).

Semgrep distribution metadata is 1.182.1; its CLI reports 1.179.0 on this machine. Both are retained in the installation/version evidence. The local smoke rule scanned two example source files with no findings.

## Blockers and practical limits

- Docker executable exists, but the Linux engine was unavailable at initial inspection and after launching Docker Desktop. Database integration requires a running engine; no successful database test is claimed unless explicitly recorded above.
- The initial npm attempt failed with ETARGET for rolldown due to stale cached metadata. Refreshing metadata resolved installation. The mutation runner showed incompatibility with Vitest 5, so Vitest and coverage are pinned to 4.1.10 (the Stryker 10 runner's own tested development version), alongside Vite 8.3.5. See npm-compatibility.log and npm-versions.txt.
- Network downloads were slow. A failed source/binary download is recorded in downloads.json; rerunning scripts/download-toolkit.py retries missing items.
- Trivy itself is installed and its configuration scan succeeded with embedded checks. Its vulnerability scan was blocked by downloading the 129 MiB vulnerability database: the default mirror stalled, and the explicit GHCR retry ended with context deadline exceeded. Retry scripts/run.ps1 trivy when database access is reliable.
- The standard browser download repeatedly timed out. Resumable archive attempts retained partial downloads. Matching-browser availability is listed above; the successfully tested older Chromium and current WebKit remain usable.
- An earlier Firefox baseline run overlapped another Playwright run and collided in the shared trace folder. The final browser verification was run alone; use browser-three-engines-verified.log and the final HTML report as the authoritative result.
- Security findings (for example from Trivy) are different from installation failures. Review scanner reports before suppressing findings.
- Older agent skills can require optional MCP servers, external APIs, models, or accounts. Their instructions and support files were preserved; this setup does not provision every optional service.
- Bundled tests demonstrate tool operation only. Real project business logic, auth, tenancy, external services, and production performance still need targeted tests.
- Maven dependencies use the normal user .m2 cache; Playwright uses the normal LOCALAPPDATA/ms-playwright browser cache. Their project configuration and tool launchers are kept here.
- No target application or CI configuration was modified. The claude-mem observer remains signed out; work-state records are separate from durable observation capture.

## Next commands

See [README](../README.md), [every tool](../docs/TOOLS.md), and [every skill](../docs/SKILLS.md). Start with unit, Java, browser, then the specific risk you want to test.
