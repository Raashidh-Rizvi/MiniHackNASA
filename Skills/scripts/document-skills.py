import pathlib,re
root=pathlib.Path(__file__).resolve().parents[1]
rows=['# Every skill: purpose and activation','',
'Run skills in an AI chat, not PowerShell. Codex uses `$name`; Claude generally uses `/name`. If unavailable, ask the assistant to read the exact SKILL.md. Supporting files remain alongside it. Optional tools, services, credentials, and workflow requirements are described in each full skill.','',
'| Skill | Purpose | Codex chat | Claude chat | Complete instructions |','|---|---|---|---|---|']
for p in sorted((root/'skills/shared').glob('*/SKILL.md')):
    content=p.read_text(encoding='utf-8-sig'); name=p.parent.name
    match=re.search(r'description:\s*(.*)',content)
    description=re.sub(r'\s+',' ',match.group(1)).replace('|','/').strip('"') if match else 'Read the linked skill instructions.'
    if description in ['>','>-','|','|-'] and match:
        continuation=re.match(r'((?:\r?\n[ \t]+[^\n]*)+)',content[match.end():])
        if continuation:description=re.sub(r'\s+',' ',continuation.group(1)).strip().replace('|','/')
    rows.append(f'| {name} | {description} | `${name} <task>` | `/{name} <task>` | [SKILL.md](../skills/shared/{name}/SKILL.md) |')
rows+=['','Graphify has a preserved [Claude-specific variant](../skills/claude/graphify/SKILL.md).','',
'Supply the target project, desired outcome, and constraints with every invocation. A direct prompt also works: `Read D:/Project/Skills/skills/shared/<name>/SKILL.md and follow it for this task.`','',
'The testing-toolkit skill coordinates the executable testing tools. The other skills guide planning, implementation, design, debugging, review, and delivery. VibeWise is a separately activated Claude plugin; see the root README.']
(root/'docs/SKILLS.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(f'Documented {len(list((root/"skills/shared").glob("*/SKILL.md")))} skills')
