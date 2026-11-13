import http from 'k6/http';
import {check,sleep} from 'k6';
export const options={vus:1,duration:'5s',thresholds:{http_req_failed:['rate<0.01'],http_req_duration:['p(95)<500']}};
export default function(){ const r=http.get(`${__ENV.TARGET_URL || 'http://127.0.0.1:4173'}/health`);check(r,{'healthy':r=>r.status===200});sleep(1); }
