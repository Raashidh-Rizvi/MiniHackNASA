import pathlib,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
with zipfile.ZipFile(root/'downloads/project-skills-before.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,src in [('agents',pathlib.Path('D:/Project/.agents/skills')),('claude',pathlib.Path('D:/Project/.claude/skills'))]:
        for p in src.rglob('*'):
            if p.is_file():z.write(p,name+'/'+p.relative_to(src).as_posix())
