"""Download official large assets using validated HTTP byte ranges and SHA256."""
import concurrent.futures,hashlib,json,math,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
def request(url,headers=None):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Skills-Toolkit',**(headers or {})}),timeout=90)
def download(job):
    name,url,dest,sha=job
    with request(url,{'Range':'bytes=0-0'}) as r:
        if r.status!=206:raise RuntimeError(name+': server does not support ranges')
        size=int(r.headers['Content-Range'].split('/')[1]);r.read()
    chunksize=1024*1024
    parts=ROOT/'downloads'/('parts-'+name);parts.mkdir(exist_ok=True)
    def chunk(i):
        start=i*chunksize;end=min(size-1,start+chunksize-1);p=parts/str(i)
        if p.exists() and p.stat().st_size==end-start+1:return
        for attempt in range(3):
            try:
                with request(url,{'Range':f'bytes={start}-{end}'}) as r:
                    if r.status!=206 or r.headers.get('Content-Range')!=f'bytes {start}-{end}/{size}':raise RuntimeError('Invalid range response')
                    data=r.read()
                if len(data)!=end-start+1:raise RuntimeError('Incomplete range')
                p.write_bytes(data);return
            except Exception:
                if attempt==2:raise
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        done=0
        for _ in pool.map(chunk,range(math.ceil(size/chunksize))):
            done+=1
            if done%10==0:print(f'{name}: {min(done*chunksize,size)//1048576}/{size//1048576} MiB',flush=True)
    temp=dest.with_suffix(dest.suffix+'.partial')
    with temp.open('wb') as out:
        for i in range(math.ceil(size/chunksize)):out.write((parts/str(i)).read_bytes())
    digest=hashlib.sha256(temp.read_bytes()).hexdigest()
    if sha and sha!=digest:raise RuntimeError(name+': SHA256 mismatch')
    temp.replace(dest)
    print(name+': complete, SHA256 '+digest,flush=True)
    return {'name':name,'size':size,'sha256':digest,'path':str(dest),'url':url,'expectedSHA256Verified':bool(sha)}
if __name__=='__main__':
    jobs=[]
    with request('https://pypi.org/pypi/semgrep/1.182.1/json') as r:data=json.load(r)
    a=next(a for a in data['urls'] if 'win_amd64' in a['filename'])
    jobs.append(('semgrep',a['url'],ROOT/'downloads'/a['filename'],a['digests']['sha256']))
    for name,repo,pattern in [('trivy','aquasecurity/trivy','windows-64bit.zip'),('zap-core','zaproxy/zaproxy','Core.zip')]:
        with request('https://api.github.com/repos/'+repo+'/releases/latest') as r:release=json.load(r)
        a=next(a for a in release['assets'] if a['name'].endswith(pattern))
        digest=a.get('digest') or ''
        jobs.append((name,a['browser_download_url'],ROOT/'downloads'/a['name'],digest.removeprefix('sha256:')))
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(download,jobs):
            results.append(result)
            (ROOT/'reports/range-downloads.json').write_text(json.dumps(results,indent=2))
