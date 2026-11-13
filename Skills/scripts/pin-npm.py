"""Resolve small version manifests instead of fetching huge wildcard histories."""
import concurrent.futures,json,pathlib,urllib.request
root=pathlib.Path(__file__).resolve().parents[1]
names='vitest @vitest/coverage-v8 @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @playwright/test @axe-core/playwright axe-core @lhci/cli @stryker-mutator/core @stryker-mutator/vitest-runner react react-dom'.split()
def get(name):
    req=urllib.request.Request('https://registry.npmjs.org/'+name.replace('/','%2f')+'/latest',headers={'User-Agent':'Skills-Toolkit'})
    with urllib.request.urlopen(req,timeout=60) as r: data=json.load(r)
    return name,data['version']
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:versions=dict(pool.map(get,names))
versions['vitest']='4.1.10'
versions['@vitest/coverage-v8']='4.1.10'
versions['vite']='8.3.5'
path=root/'frontend/package.json'
data=json.loads(path.read_text());data['devDependencies']=versions
path.write_text(json.dumps(data,indent=2)+'\n')
print(versions)
