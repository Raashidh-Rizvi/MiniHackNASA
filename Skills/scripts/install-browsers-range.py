"""Install the exact official browser archives listed by the installed Playwright CLI."""
import argparse,concurrent.futures,importlib.util,json,os,pathlib,re,subprocess,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ranged',ROOT/'scripts/range-download.py');ranged=importlib.util.module_from_spec(spec);spec.loader.exec_module(ranged)
parser=argparse.ArgumentParser();parser.add_argument('--browsers',nargs='+',default=['chromium','firefox','webkit']);args=parser.parse_args()
listing=subprocess.check_output(['node',str(ROOT/'frontend/node_modules/playwright/cli.js'),'install','--dry-run',*args.browsers],text=True)
(ROOT/'reports/browser-download-plan.txt').write_text(listing)
jobs=[]
for block in listing.strip().split('\n\n'):
    location=re.search(r'Install location:\s+(.+)',block)
    url=re.search(r'Download url:\s+(.+)',block)
    if not location or not url:continue
    dest=pathlib.Path(location.group(1).strip());link=url.group(1).strip()
    if (dest/'INSTALLATION_COMPLETE').exists():continue
    jobs.append((dest.name,link,ROOT/'downloads'/('browser-'+link.rsplit('/',1)[1]),'',dest))
def install(job):
    name,link,archive,sha,dest=job
    result=ranged.download((name,link,archive,sha))
    with zipfile.ZipFile(archive) as z:
        bad=z.testzip()
        if bad:raise RuntimeError('Corrupt browser archive: '+bad)
        dest.mkdir(parents=True,exist_ok=True);z.extractall(dest)
    (dest/'INSTALLATION_COMPLETE').touch()
    result['installationPath']=str(dest)
    return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(install,jobs):
        results.append(result)
        (ROOT/'reports/browser-downloads.json').write_text(json.dumps(results,indent=2))
subprocess.run(['node',str(ROOT/'frontend/node_modules/playwright/cli.js'),'install',*args.browsers],check=True,env={**os.environ,'PLAYWRIGHT_SKIP_BROWSER_GC':'1'})
