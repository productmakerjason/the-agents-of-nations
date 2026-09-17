import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve, extname } from 'node:path';
import * as submit from '../api/submit/index.js';
const root = resolve('public');
const types = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.json':'application/json', '.md':'text/plain', '.txt':'text/plain', '.xml':'application/xml' };
http.createServer(async (req,res) => {
  try {
    const path = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (path === '/api/submit') {
      const request = new Request('http://localhost' + req.url, { method:req.method, headers:req.headers, ...(req.method === 'POST' ? { body:req, duplex:'half' } : {}) });
      const response = await (submit[req.method] || submit.GET)(request);
      res.writeHead(response.status, Object.fromEntries(response.headers)); res.end(await response.text()); return;
    }
    let file = resolve(root, '.' + (path === '/' ? '/index.html' : path));
    if (!file.startsWith(root + '/')) { res.writeHead(403); res.end(); return; }
    if (!extname(file)) file += '.html';
    const data = await readFile(file);
    res.writeHead(200, { 'Content-Type': (types[extname(file)] || 'application/octet-stream') + '; charset=utf-8' }); res.end(data);
  } catch { res.writeHead(404); res.end('Not found'); }
}).listen(4173, '127.0.0.1', () => console.log('AON preview: http://127.0.0.1:4173'));
