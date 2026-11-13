import argparse,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('task');p.add_argument('status');p.add_argument('log');a=p.parse_args()
dest=root/'reports/verification.json'
rows=json.loads(dest.read_text(encoding='utf-8-sig')) if dest.exists() else []
if isinstance(rows,dict):rows=[rows]
rows=[r for r in rows if r['task']!=a.task]
rows.append({'task':a.task,'status':a.status,'log':str(root/'reports'/a.log)})
dest.write_text(json.dumps(rows,indent=2))
