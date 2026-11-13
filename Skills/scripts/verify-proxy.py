"""Exercise a temporary, isolated localhost fault proxy against the demo server."""
import json,pathlib,subprocess,time,urllib.request
root=pathlib.Path(__file__).resolve().parents[1]
exe=next((root/'tools/toxiproxy').glob('*.exe'))
def request(path,data=None,method=None):
    req=urllib.request.Request('http://127.0.0.1:18474'+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'},method=method)
    with urllib.request.urlopen(req,timeout=10) as response:return response.read()
log=(root/'reports/toxiproxy-server.log').open('w')
proc=subprocess.Popen([str(exe),'-host','127.0.0.1','-port','18474'],stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
try:
    for i in range(40):
        try:request('/version');break
        except OSError:time.sleep(.1)
    request('/proxies',{'name':'toolkit-demo','listen':'127.0.0.1:18666','upstream':'127.0.0.1:4173','enabled':True})
    with urllib.request.urlopen('http://127.0.0.1:18666/health') as r:assert json.load(r)['status']=='ok'
    request('/proxies/toolkit-demo/toxics',{'name':'demo-latency','type':'latency','stream':'downstream','toxicity':1.0,'attributes':{'latency':250,'jitter':0}})
    start=time.monotonic()
    with urllib.request.urlopen('http://127.0.0.1:18666/health') as r:assert r.status==200
    elapsed=time.monotonic()-start
    assert elapsed>=.2,elapsed
    request('/proxies/toolkit-demo',method='DELETE')
    (root/'reports/toxiproxy-smoke.json').write_text(json.dumps({'status':'passed','injectedLatencyMs':250,'observedSeconds':elapsed,'target':'local bundled fixture'},indent=2))
    print('Proxy forwarding and injected latency verified:',round(elapsed,3),'seconds')
finally:
    proc.terminate();proc.wait(timeout=10);log.close()
