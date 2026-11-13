# Tool-by-tool run guide

All commands below run from **PowerShell in `D:\Project\Skills`**. Use `. .\scripts\activate.ps1` for short tool names. `scripts/run.ps1` also works without activation. Results for the current machine are in `reports/SETUP-STATUS.md`.

| Area and tool | What is installed / benefit | Run command | Focus and prerequisites |
|---|---|---|---|
| Frontend: Vitest | Local npm dependency; fast business-rule and state checks | `.\scripts\run.ps1 unit` | Bundled demo tests; real project tests must import that project's code |
| Components: Testing Library | React, user-event, jest-dom, jsdom; tests the UI as a user | `.\scripts\run.ps1 unit` | `frontend/tests/toolkit.test.jsx` demonstrates invalid then corrected form input |
| Browser: Playwright | Test runner plus Chromium, Firefox, WebKit downloads | `.\scripts\run.ps1 browser` | Screenshots, traces, three browsers; `browser-ui` opens test UI |
| Visual: Playwright snapshots | Baselines saved per browser/platform in `frontend/e2e` | `.\scripts\run.ps1 visual-update` | Review new screenshots; then run `browser` without updating |
| Accessibility: axe-core | axe-core and Playwright integration | `.\scripts\run.ps1 browser` | Automated violations fail tests; manually test keyboard/focus/assistive tech too |
| Java unit: JUnit | Maven test dependency | `.\scripts\run.ps1 java` | JDK 17+; example compiles to Java 17, installed JDK is used at runtime |
| Java doubles: Mockito | Maven test dependency, subclass mock maker | `.\scripts\run.ps1 java` | Example interface mock avoids dynamic Java-agent setup; final/static mocking needs project-specific inline configuration |
| Real database: Testcontainers Java | Maven dependency and PostgreSQL example | `.\scripts\run.ps1 database` | Running Docker Linux engine, network/image pull, available disk/RAM; fails rather than silently skipping when Docker is unavailable |
| HTTP API: REST Assured | Maven dependency | `.\scripts\run.ps1 java` | Uses WireMock health/503/401 fixtures; add actual user/role/tenant cases in target project |
| API generation: Schemathesis | Isolated `.venv` CLI | `.\scripts\run.ps1 api -SchemaUrl http://127.0.0.1:4173/openapi.json` | Demo must be running; use a disposable environment with your real schema |
| Providers: WireMock | Embedded Maven dependency; no permanent server | `.\scripts\run.ps1 java` | Simulates provider unavailable/delay and unauthorized responses; extend for timeouts/retries/idempotency |
| Browser audits: Lighthouse CI | Local `@lhci/cli`; uses installed Chrome/Playwright Chromium | `.\scripts\run.ps1 lighthouse` | Three local audit runs; writes `reports/lighthouse`; budgets are starter values, not measured production goals |
| Load/capacity: k6 | Portable Windows executable | `.\scripts\run.ps1 load -TargetUrl http://127.0.0.1:4173` | Starter is 1 virtual user for 5 seconds against `/health`; change `load/smoke.js` for real load models |
| Static security: Semgrep CE | Native Windows Python package | `.\scripts\run.ps1 semgrep -TargetPath D:\Project\MyApp` | Bundled local rule only detects `eval`; this is a smoke rule, not a comprehensive security ruleset |
| Secrets: Gitleaks | Portable Windows executable | `.\scripts\run.ps1 secrets -TargetPath D:\Project\MyApp` | Scans current files, redacts findings. For full Git history run `gitleaks git D:\Project\MyApp --redact` |
| Packages/config/images: Trivy | Portable Windows executable | `.\scripts\run.ps1 trivy -TargetPath D:\Project\MyApp` | First run needs vulnerability DB network access; HIGH/CRITICAL findings return nonzero; image scan: `trivy image your-image:tag` |
| Running app: ZAP | Portable cross-platform Java distribution | `.\scripts\run.ps1 zap -TargetUrl http://127.0.0.1:4173` | Java runtime; bundled plan spiders and passively scans, writes `reports/zap-passive.html`; this is not an active penetration test |
| Network faults: Toxiproxy | Portable server + CLI | `.\scripts\run.ps1 toxiproxy` | Runs foreground bound to localhost; Ctrl+C stops it; configure a proxy and route test clients through it |
| Java effectiveness: PIT | Maven plugin with JUnit 5 adapter | `.\scripts\run.ps1 mutation-java` | Mutates only demo `Discount`; report in `backend/target/pit-reports`; add important domain classes deliberately |
| JS effectiveness: Stryker | Local core + Vitest runner | `.\scripts\run.ps1 mutation-js` | Mutates only demo `src/discount.js`; report in `frontend/reports/mutation`; surviving mutants indicate missing assertions or equivalent cases |
| Learning: VibeWise | Upstream repository and optional Claude plugin registration | Claude Code: `/vibe-wise:learn` | First install marketplace/plugin, restart Claude; requires Python; see README |

## Use browser checks against your app

```powershell
.\scripts\run.ps1 browser -UseInstalledChromium -TargetUrl http://localhost:3000
```

The generic axe check and snapshot test run on that app; the demo-specific signup journey is explicitly skipped. Existing demo snapshots will differ. Add app-specific journeys and baselines in a separate suite before treating this as application coverage. Do not update away an unexpected visual change without review.

Local Chromium mode runs only that browser. Full three-engine tests require the matching browser downloads; omit `-UseInstalledChromium` after installation succeeds. To create a baseline in local mode use `scripts/run.ps1 visual-update -UseInstalledChromium` and review the resulting image.

## More static analysis rules

After reviewing the selected pack's license and scope:

```powershell
.\.venv\Scripts\semgrep.exe scan --config auto --metrics=off D:\Project\MyApp
```

This fetches registry rules; rules, hosted services, and proprietary capabilities may have separate terms. The bundled smoke rule needs no account. Tool source licenses remain in each repository; downstream packages may have their own licenses.

## Toxiproxy example

In one terminal run `scripts/run.ps1 toxiproxy`. In a second activated terminal:

```powershell
toxiproxy-cli-windows-amd64.exe create demo -l 127.0.0.1:8666 -u 127.0.0.1:4173
toxiproxy-cli-windows-amd64.exe toxic add -t latency -a latency=250 demo
Invoke-WebRequest http://127.0.0.1:8666/health
toxiproxy-cli-windows-amd64.exe toxic remove -n latency_downstream demo
toxiproxy-cli-windows-amd64.exe delete demo
```

Only clients using port 8666 see the fault; this does not alter the original application. Real database faults require a separate proxy to the test database, never the production connection string.

## Reports and exit codes

The launcher propagates failures. A scanner returning findings is different from an installer failing; inspect its saved report. Playwright's HTML report is `frontend/playwright-report/index.html`; traces are under `frontend/test-results`. Java reports are under `backend/target/surefire-reports` and `failsafe-reports`. The setup status records what was actually run, including failures, rather than treating a download as verification.

ZAP uses the smaller official Core distribution plus the automation add-on and required commonlib/network updates. Its settings and downloaded add-ons are isolated in `tools/zap-home`. To repeat add-on installation run `scripts/setup-zap.ps1`. The demo passive scan produced 2 medium, 1 low, and 1 informational alert; review `reports/zap-passive.html`.

The Trivy executable and offline configuration checks work. If its vulnerability database cannot download, the vulnerability scan fails explicitly. The current attempt timed out; see the setup report. A configuration-only check without the vulnerability DB is:

```powershell
trivy config --skip-check-update D:\Project\MyApp
```

Large downloads can be resumed with `python scripts/range-download.py` (Semgrep, Trivy, ZAP Core), or `python scripts/install-browsers-range.py --browsers firefox` for a single browser. These use official asset URLs and retain completed byte ranges. Their final archives are checked before installation; GitHub/PyPI assets use the release SHA256 when provided. Browser archives use TLS, ZIP integrity, and a recorded local SHA256; Playwright does not provide a release checksum in its browser plan.

## Official references

- [Playwright install and browser support](https://playwright.dev/docs/intro)
- [Schemathesis CLI and options](https://schemathesis.readthedocs.io/en/stable/reference/cli/)
- [Semgrep CE native Windows installation](https://semgrep.dev/products/community-edition/)
- [Trivy installation](https://trivy.dev/docs/latest/getting-started/installation/)
- [Stryker Vitest runner](https://stryker-mutator.io/docs/stryker-js/vitest-runner/)
- [ZAP CLI](https://www.zaproxy.org/docs/desktop/cmdline/)
- [VibeWise activation](https://github.com/nykooi1/vibe-wise)
