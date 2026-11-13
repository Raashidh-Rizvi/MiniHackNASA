import concurrent.futures,importlib.util,json,pathlib,shutil,urllib.request,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ranged',ROOT/'scripts/range-download.py');ranged=importlib.util.module_from_spec(spec);spec.loader.exec_module(ranged)
def install(item):
    name,version=item
    with ranged.request(f'https://api.github.com/repos/zaproxy/zap-extensions/releases/tags/{name}-v{version}') as r:d=json.load(r)
    a=next(a for a in d['assets'] if a['name'].endswith('.zap'))
    digest=(a.get('digest') or '').removeprefix('sha256:')
    dest=ROOT/'downloads'/a['name']
    result=ranged.download(('zap-addon-'+name,a['browser_download_url'],dest,digest))
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None,'Invalid add-on archive'
    target=ROOT/'tools/zap-home/plugin'/a['name'];target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(dest,target)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p:
    results=list(p.map(install,[('commonlib','1.44.0'),('automation','0.61.0'),('network','0.31.0')]))
(ROOT/'reports/zap-addons.json').write_text(json.dumps(results,indent=2))
