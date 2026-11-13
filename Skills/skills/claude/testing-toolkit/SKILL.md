---
name: testing-toolkit
description: Select and run suitable tests and quality checks for the current project using the local Windows toolkit. Use for requests to test changes, validate an application, or choose testing tools; distinguish target-project evidence from bundled demos.
---

# Testing toolkit

The toolkit lives at `D:/Project/Skills`. Resolve every toolkit document and command against this absolute root, regardless of the current project's working directory. It is a local Windows installation, not a cloud service.

1. Use the user's named project, or the current working project when none is named. Inspect its stack, changes, instructions, and existing tests. If the current folder is the toolkit itself and the intended application is unclear, resolve the target before testing.
2. Read `D:/Project/Skills/docs/TOOLS.md` for available tools and `D:/Project/Skills/reports/SETUP-STATUS.md` for known blockers. Read `D:/Project/Skills/README.md` only when activation or installation details are needed. For complementary agent skills, consult `D:/Project/Skills/docs/SKILLS.md` and load only relevant instructions.
3. Choose the smallest useful set of checks for the actual task. Prefer the target's existing test commands. React/Vite may need Vitest and Testing Library; Java may need JUnit/Mockito/API tests; other stacks should retain their native tests. Browser journeys, axe, source scans, provider simulation, load, and mutation tools supplement those tests when relevant. Do not run every tool merely because it is installed.
4. State briefly which checks you selected and why, then perform the authorized work. Use `D:/Project/Skills/scripts/run.ps1 -Task <task>` for suitable toolkit operations, with explicit target paths/URLs. No separate terminal activation is needed for this launcher. Use target-project commands for its native unit/integration tests.
5. The included unit, Java, mutation, and default browser suites test bundled examples only. To test a real application's behavior, use its own code, accounts, endpoints, schemas, fixtures, and assertions. Never substitute passing demos for target-project verification.
6. For browser checks against another app use `-TargetUrl`; replace the demo journey with actual flows. `-UseInstalledChromium` uses the working cached browser explicitly. Review new visual baselines; run browser invocations sequentially because they share report/trace folders.
7. Use disposable data for database/property tests and route only test clients through Toxiproxy. Require explicit target scope before production stress or active security scans. A known Docker, database-download, or browser-download blocker must remain visible; report it rather than repeatedly reinstalling or silently skipping a required check.
8. Report the selected checks, actual target, results, report paths, and remaining gaps. Preserve existing application behavior and unrelated work.

When the user asks to use this skill throughout a chat, keep selecting appropriate checks for related follow-up changes until they change that preference. A global installation makes the skill available in new chats; it does not create a background process, schedule, or guarantee invocation on every message.

Invoke in Codex: `$testing-toolkit Test D:\Project\MyApp and prioritize authorization and critical forms.`

One reusable prompt: `Use $testing-toolkit throughout this chat. For the current project, choose and run only the checks relevant to my task and changes. Use existing project tests, report actual results and blockers, and do not treat bundled examples as application coverage.`

Invoke in Claude Code: `/testing-toolkit` followed by the target and testing goal. If the client does not expose slash skills, ask it to read this SKILL.md and follow it.
