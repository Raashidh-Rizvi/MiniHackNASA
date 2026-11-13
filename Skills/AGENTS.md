# Working in this toolkit

Read README.md and reports/SETUP-STATUS.md first. Sources in repositories/ are vendor references with their own licenses and instructions; do not edit or build all of them when maintaining this toolkit. Runtime packages live in frontend/node_modules, .venv, tools, and the normal Maven/browser caches. Keep downloaded sources separate from installed runtime evidence.

Canonical shared skills live in skills/shared; skills/claude contains junctions plus a preserved Graphify variant. Preserve the original D:/Project/.agents/skills and .claude/skills discovery links. docs/SKILLS.md documents every skill. Update it with python scripts/document-skills.py after adding a skill.

Use scripts/run.ps1 for individual checks. Example success does not prove target-application coverage. Do not blanket-update snapshots to clear failures. Do not automatically run live stress, active security, or destructive schema tests against production.
