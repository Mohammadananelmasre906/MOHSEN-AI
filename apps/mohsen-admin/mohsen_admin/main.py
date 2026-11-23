from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

from .config import settings

app = FastAPI(title="MOHSEN ADMIN", version="0.1.0")


@app.get("/health")
async def health():
    return {"name": "MOHSEN ADMIN", "status": "online"}


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MOHSEN ADMIN</title><style>
:root{color-scheme:dark;font:15px system-ui;background:#0b1220;color:#e5edf8}
body{max-width:900px;margin:8vh auto;padding:24px}header,.panel{background:#121e30;border:1px solid #263750;border-radius:16px;padding:22px;margin:16px 0}
h1{margin:0;color:#8dd9ff}.muted{color:#9aacc3}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#e3a63a;margin-right:8px}
button{background:#176b91;color:white;border:0;border-radius:9px;padding:10px 16px;cursor:pointer}
pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#b9d9ed}
</style></head><body>
<header><h1>MOHSEN ADMIN</h1><p class="muted">Local owner control panel · connected to the original Core</p>
<p><span class="dot"></span><span id="state">Checking Core…</span></p></header>
<section class="panel"><h2>Core status</h2><button onclick="refresh()">Refresh status</button><pre id="status">Waiting…</pre>
<p class="muted">The language model is not trained yet. This dashboard does not simulate AI responses.</p></section>
<script>
async function refresh(){const out=document.getElementById('status'),state=document.getElementById('state');
try{const r=await fetch('/api/core/status');const d=await r.json();out.textContent=JSON.stringify(d,null,2);state.textContent=d.core==='online'?'Core connected':'Core unavailable'}
catch(e){out.textContent='Unable to reach Admin API';state.textContent='Admin error'}}
refresh();setInterval(refresh,10000);
</script></body></html>"""


@app.get("/api/core/status")
async def core_status():
    token = settings.core_api_token.get_secret_value()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(
                f"{settings.core_url.rstrip('/')}/api/v1/status",
                headers=headers,
            )
        return response.json() if response.status_code == 200 else {
            "core": "unavailable",
            "reason": f"Core returned HTTP {response.status_code}",
        }
    except httpx.HTTPError:
        return {"core": "unavailable", "reason": "Core is not reachable"}
