"""Download official sources and portable Windows tools; retain versions and failures."""
import concurrent.futures, hashlib, json, pathlib, re, subprocess, sys, tarfile, urllib.request, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
_report = ROOT/'reports/downloads.json'
PREVIOUS_DOWNLOADS = json.loads(_report.read_text()) if _report.exists() else []
REPOS = {
 'vitest':'vitest-dev/vitest','testing-library':'testing-library/react-testing-library',
 'playwright':'microsoft/playwright','axe-core':'dequelabs/axe-core',
 'junit':'junit-team/junit-framework','mockito':'mockito/mockito',
 'testcontainers-java':'testcontainers/testcontainers-java','rest-assured':'rest-assured/rest-assured',
 'schemathesis':'schemathesis/schemathesis','wiremock':'wiremock/wiremock',
 'lighthouse-ci':'GoogleChrome/lighthouse-ci','k6':'grafana/k6','semgrep':'semgrep/semgrep',
 'gitleaks':'gitleaks/gitleaks','trivy':'aquasecurity/trivy','zap':'zaproxy/zaproxy',
 'toxiproxy':'Shopify/toxiproxy','pitest':'hcoles/pitest','stryker-js':'stryker-mutator/stryker-js',
 'vibe-wise':'nykooi1/vibe-wise'}

def fetch(url, dest=None):
    req=urllib.request.Request(url, headers={'User-Agent':'Skills-Toolkit-Setup','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'})
    with urllib.request.urlopen(req,timeout=180) as r:
        data=r.read()
    if dest:
        pathlib.Path(dest).write_bytes(data)
    return data

def clone(item):
    name, repo=item
    dest=ROOT/'repositories'/name
    try:
        if not (dest/'.git').exists():
            subprocess.run(['git','clone','--depth','1','https://github.com/'+repo+'.git',str(dest)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=900)
        rev=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
        return {'name':name,'repository':repo,'status':'downloaded','commit':rev,'path':str(dest)}
    except Exception as e:
        return {'name':name,'repository':repo,'status':'failed','error':str(e)}

def portable(name,repo,pattern):
    try:
        if '--update' not in sys.argv:
            old=next((r for r in PREVIOUS_DOWNLOADS if r['name']==name and 'repository' not in r and r['status']=='downloaded'),None)
            present=list((ROOT/'tools'/name).rglob('*.exe'))+list((ROOT/'tools'/name).rglob('zap.bat'))
            if old and present:return old
        release=json.loads(fetch('https://api.github.com/repos/'+repo+'/releases/latest'))
        assets=release['assets']
        asset=next(a for a in assets if re.search(pattern,a['name'],re.I))
        dest=ROOT/'downloads'/asset['name']
        if not dest.exists(): fetch(asset['browser_download_url'],dest)
        sha=hashlib.sha256(dest.read_bytes()).hexdigest()
        verified=False
        digest=asset.get('digest')
        if digest and digest.startswith('sha256:'):
            if sha!=digest.split(':')[1]: raise RuntimeError('SHA256 mismatch')
            verified=True
        else:
            checks=next((a for a in assets if re.search(r'checksums.*\.txt$|_checksums\.txt$',a['name'],re.I)),None)
            if checks:
                content=fetch(checks['browser_download_url']).decode()
                line=next(l for l in content.splitlines() if asset['name'] in l)
                if sha != line.split()[0]: raise RuntimeError('Release checksum mismatch')
                verified=True
        out=ROOT/'tools'/name
        out.mkdir(exist_ok=True)
        if dest.suffix=='.zip':
            with zipfile.ZipFile(dest) as z: z.extractall(out)
        elif dest.name.endswith('.tar.gz'):
            with tarfile.open(dest) as t: t.extractall(out,filter='data')
        elif dest.suffix=='.exe': (out/dest.name).write_bytes(dest.read_bytes())
        return {'name':name,'version':release['tag_name'],'status':'downloaded','asset':asset['name'],'url':asset['browser_download_url'],'sha256':sha,'verifiedReleaseChecksum':verified}
    except Exception as e: return {'name':name,'status':'failed','error':str(e)}

if __name__=='__main__':
    jobs=[('k6','grafana/k6',r'windows-amd64\.zip$'),('gitleaks','gitleaks/gitleaks',r'windows_x64\.zip$'),('trivy','aquasecurity/trivy',r'windows-64bit\.zip$'),('toxiproxy','Shopify/toxiproxy',r'toxiproxy-server-windows-amd64\.exe$'),('toxiproxy-cli','Shopify/toxiproxy',r'toxiproxy-cli-windows-amd64\.exe$'),('zap','zaproxy/zaproxy',r'Core\.zip$')]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(clone,x) for x in REPOS.items()]+[pool.submit(portable,*x) for x in jobs]
        for f in concurrent.futures.as_completed(futures):
            row=f.result();results.append(row)
            print(row['name']+': '+row['status'],flush=True)
            (ROOT/'reports'/'downloads.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    sys.exit(1 if any(r['status']=='failed' for r in results) else 0)
