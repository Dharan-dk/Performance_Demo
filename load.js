import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '2m',

  thresholds: {
    'http_req_duration{endpoint:products}': ['p(95)<50'],
    'http_req_duration{endpoint:heavy}': ['p(95)<100'],
    'http_req_failed': ['rate<0.01'],
  },
};

export default function () {
  if (Math.random() < 0.7) {
    http.get('http://localhost/products', {
      tags: { endpoint: 'products' }
    });
  } else {
    http.get('http://localhost/heavy-process', {
      tags: { endpoint: 'heavy' }
    });
  }
  sleep(1);
}