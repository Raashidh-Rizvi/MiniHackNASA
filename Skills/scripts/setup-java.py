import hashlib,json,pathlib,sys,urllib.request,xml.etree.ElementTree as ET,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
saved=ROOT/'reports/java-versions.json'
pinned=json.loads(saved.read_text()) if saved.exists() and '--update' not in sys.argv else None
if pinned and (ROOT/'backend/pom.xml').exists() and (ROOT/'tools'/('apache-maven-'+pinned['maven'])/'bin/mvn.cmd').exists():
    print('Existing pinned Java setup retained; use --update for a deliberate upgrade.')
    sys.exit(0)
base='https://repo.maven.apache.org/maven2/'
def read(url): return urllib.request.urlopen(url,timeout=180).read()
def version(path,prefix=''):
    tree=ET.fromstring(read(base+path+'/maven-metadata.xml'))
    versions=[x.text for x in tree.findall('versioning/versions/version') if x.text.startswith(prefix) and not any(c.isalpha() for c in x.text)]
    return versions[-1]
mv=pinned['maven'] if pinned else version('org/apache/maven/apache-maven','3.9.')
url=base+f'org/apache/maven/apache-maven/{mv}/apache-maven-{mv}-bin.zip'
dest=ROOT/'downloads'/f'apache-maven-{mv}-bin.zip'
if not dest.exists(): dest.write_bytes(read(url))
assert hashlib.sha512(dest.read_bytes()).hexdigest()==read(url+'.sha512').decode().split()[0]
with zipfile.ZipFile(dest) as z:z.extractall(ROOT/'tools')
deps={'junit':('org/junit/jupiter/junit-jupiter','5.'),'mockito':('org/mockito/mockito-core',''),'testcontainers':('org/testcontainers/postgresql','1.'),'restassured':('io/rest-assured/rest-assured',''),'wiremock':('org/wiremock/wiremock','3.'),'pitest':('org/pitest/pitest-maven',''),'pitjunit':('org/pitest/pitest-junit5-plugin','')}
v={k:pinned[k] if pinned else version(*p) for k,p in deps.items()}
(ROOT/'reports'/'java-versions.json').write_text(json.dumps({'maven':mv,**v},indent=2))
pom='''<project xmlns="http://maven.apache.org/POM/4.0.0"><modelVersion>4.0.0</modelVersion><groupId>local.toolkit</groupId><artifactId>backend-examples</artifactId><version>1.0.0</version><properties><maven.compiler.release>17</maven.compiler.release><project.build.sourceEncoding>UTF-8</project.build.sourceEncoding></properties><dependencies>'''
for key,(path,_) in deps.items():
    if key.startswith('pit'):continue
    parts=path.split('/');artifact=parts[-1];group='.'.join(parts[:-1])
    pom+=f'<dependency><groupId>{group}</groupId><artifactId>{artifact}</artifactId><version>{v[key]}</version><scope>test</scope></dependency>'
pom+='''<dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><version>42.7.8</version><scope>test</scope></dependency></dependencies><build><plugins><plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-compiler-plugin</artifactId><version>3.14.1</version></plugin><plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-surefire-plugin</artifactId><version>3.5.4</version></plugin>'''
pom+=f'''<plugin><groupId>org.pitest</groupId><artifactId>pitest-maven</artifactId><version>{v['pitest']}</version><configuration><targetClasses><param>toolkit.Discount</param></targetClasses><targetTests><param>toolkit.DiscountTest</param></targetTests><mutationThreshold>70</mutationThreshold></configuration><dependencies><dependency><groupId>org.pitest</groupId><artifactId>pitest-junit5-plugin</artifactId><version>{v['pitjunit']}</version></dependency></dependencies></plugin>'''
pom+='''</plugins></build><profiles><profile><id>database</id><build><plugins><plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-failsafe-plugin</artifactId><version>3.5.4</version><executions><execution><goals><goal>integration-test</goal><goal>verify</goal></goals></execution></executions></plugin></plugins></build></profile></profiles></project>'''
(ROOT/'backend'/'pom.xml').write_text(pom)
print('Maven downloaded, checksum verified; backend pom created:',v)
