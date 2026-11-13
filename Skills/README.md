# Local skills and testing toolkit

This folder combines **agent skills**, **installed test tools**, **runnable examples**, and **20 upstream source repositories**. These are different things: a skill guides an assistant; a tool executes checks; a source checkout is for reference and is not itself a ready-to-run installation.

Start with [the actual setup results](reports/SETUP-STATUS.md), [every tool and its command](docs/TOOLS.md), and [every skill and how to invoke it](docs/SKILLS.md). Exact downloaded source revisions and portable tool versions/checksums are in [downloads.json](reports/downloads.json). Java versions are in [java-versions.json](reports/java-versions.json); JavaScript versions are pinned in `frontend/package-lock.json`; Python versions are in `requirements-lock.txt` once installation succeeds.

## One entry point in every local Codex project

The `testing-toolkit` skill is linked into this Windows user's global skill folder, `C:\Users\user\.agents\skills\testing-toolkit`. Its instructions remain maintained here. This makes it available across local Codex projects for this user; another computer or cloud environment needs its own installation and access to the tools.

Paste this into a **Codex chat**, not PowerShell:

```text
Use $testing-toolkit throughout this chat. For the current project, choose and run only the checks relevant to my task and changes. Use existing project tests, report actual results and blockers, and do not treat bundled examples as application coverage.
```

Then describe the work normally. The agent selects suitable checks for related follow-ups in that chat. Installation is one-time; this instruction is reusable in each new chat. Automatic skill selection is enabled for matching testing requests, but explicitly mentioning `$testing-toolkit` is the reliable way to request it.

Type `$` and look for **Testing Toolkit**. Codex CLI/IDE also support `/skills` to browse skills. A custom `/testing-toolkit` command is not required in Codex; that slash form belongs to clients such as Claude Code. If the new skill is absent on the next turn, open a new chat or restart Codex. See [OpenAI's skill instructions](https://learn.chatgpt.com/docs/build-skills).

To register this skill for another Windows user on this machine, run this once in PowerShell:

```powershell
& 'D:\Project\Skills\scripts\install-global-skill.ps1'
```

This links the instructions; it does not start tests, run continuously, or activate VibeWise. VibeWise remains a separate Claude Code plugin.

## Run individual tools in Windows PowerShell

```powershell
Set-Location D:\Project\Skills
. .\scripts\activate.ps1
.\scripts\run.ps1 -Task unit
.\scripts\run.ps1 -Task java
.\scripts\run.ps1 -Task browser -UseInstalledChromium
```

Activation changes PATH in the current terminal only. No permanent system PATH change is needed. If your own terminal blocks local scripts, use `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, then retry; this affects that process only.

`-UseInstalledChromium` explicitly selects the existing Playwright Chromium build on this machine and runs the `chromium-local` project only. It has its own reviewed screenshot baseline. To run Chromium, Firefox, and WebKit together, first complete `npx.cmd playwright install chromium firefox webkit` from `frontend`, then run `scripts/run.ps1 browser` without that switch. See the status report for browser download failures.

To use the already installed Chromium together with downloaded Firefox and WebKit:

```powershell
.\scripts\run.ps1 browser -UseInstalledChromium -ExtraArgs @('--project=firefox','--project=webkit')
```

This selects all three engines while keeping the existing Chromium version explicit. A missing browser fails visibly.

To run API/load/ZAP checks on the included demo, open another PowerShell terminal and run:

```powershell
Set-Location D:\Project\Skills
.\scripts\run.ps1 -Task serve
```

Keep that terminal open while running `api`, `load`, or `zap` in your first terminal. Ctrl+C stops the demo. The browser suite and Lighthouse start the demo themselves; don't start a second copy on the same port.

## Agent skills

The 43 existing shared skills were moved from `D:\Project\.agents\skills` and `D:\Project\.claude\skills` into this folder. Their original locations are Windows directory junctions, so parent-project discovery still works. Identical Claude skills link to the canonical copy in `skills/shared`. Graphify's differing Claude instructions are preserved in `skills/claude/graphify`. A pre-migration backup is in `downloads/project-skills-before.zip`.

A new `testing-toolkit` skill brings the collection to **44 shared skill names**. In Codex, ask:

```text
$testing-toolkit Test D:\Project\MyApp and focus on forms, permissions, and API errors.
```

In Claude Code, use `/testing-toolkit` and provide the project and task. Skill naming differs by client. If a skill is not listed on the next turn, start a new chat in your target project or ask the assistant to read the exact `SKILL.md` path from [SKILLS.md](docs/SKILLS.md). Skills are instructions, not terminal commands. Optional browser/design/media services named inside older skills need their own credentials or plugins; moving instructions does not install those services. This setup leaves QuicMov/EduFlow-specific skills inside those projects.

## VibeWise

The selected repository is [nykooi1/vibe-wise](https://github.com/nykooi1/vibe-wise), a Claude Code learning plugin. Its source is in `repositories/vibe-wise`. Check the status report for whether registration succeeded. A source download alone does not activate hooks.

For manual installation, run these in **Claude Code** (not PowerShell):

```text
/plugin marketplace add nykooi1/vibe-wise
/plugin install vibe-wise@vibe-wise
```

Then restart Claude Code in the project you want to learn and run `/vibe-wise:learn`. Use `/vibe-wise:reset` only when you intend to reset that project's learning profile. Learning notes live under that project's `.vibe-wise/`. This upstream plugin targets Claude Code; Codex does not execute its Claude hooks automatically. See the repository's README for current supported clients and updates.

## What to focus on first

1. Start with unit/component tests for important validation and business rules, then API tests for permissions and tenant boundaries.
2. Add a few browser journeys for login, a critical transaction, and error recovery; run axe alongside them. Automated axe checks need manual keyboard and screen-reader follow-up.
3. Use Testcontainers for real database behavior, WireMock for provider errors, and schema-driven tests for unexpected API inputs. The bundled REST Assured authorization example tests a simulated server, not your application's access controls.
4. Use Gitleaks, Semgrep, and Trivy regularly. Review findings and licensing; a tool being open source does not imply every hosted rule pack is unrestricted.
5. Establish performance baselines before choosing budgets. Increase k6 traffic gradually on an agreed test environment. Run mutation tests on critical logic, not your whole codebase by default.

Passing these demo checks proves the toolkit runs. Testing QuicMov, EduFlow, or another application still requires its own endpoints, accounts, fixtures, schema, and business assertions. No application dependencies or CI pipelines were changed by this setup.

## Reinstall and maintain

```powershell
Set-Location D:\Project\Skills
.\scripts\setup.ps1 -SkipSources
# To also fetch any missing source repositories / portable tools:
.\scripts\setup.ps1
```

Source clones use shallow Git history, preserve upstream licenses, and are not automatically updated on rerun. Use `git -C repositories\<name> pull --ff-only` deliberately, after checking local changes. Portable tools and Java retain the recorded versions on rerun. For deliberate upgrades use `python scripts/download-toolkit.py --update` or `python scripts/setup-java.py --update`; save the current reports and review compatibility before doing so. Java's saved POM pins its test dependencies. Use `npm ci` and Python's lock file to reproduce installed package versions. Downloads/caches require network access; the first Trivy vulnerability scan downloads a separate database.

For complete installation status, failed attempts, verification evidence, and remaining actions, read [SETUP-STATUS.md](reports/SETUP-STATUS.md).
