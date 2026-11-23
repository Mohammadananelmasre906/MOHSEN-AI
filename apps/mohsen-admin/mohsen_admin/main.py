from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

from .config import settings

app = FastAPI(title="MOHSEN ADMIN", version="0.2.0")


async def core_request(method: str, endpoint: str, payload: dict | None = None):
    token = settings.core_api_token.get_secret_value()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.request(
                method,
                f"{settings.core_url.rstrip('/')}{endpoint}",
                headers=headers,
                json=payload,
            )
        try:
            data = response.json()
        except ValueError:
            data = {"detail": "Core returned a non-JSON response"}
        return data, response.status_code
    except httpx.HTTPError:
        return {"detail": "Core is not reachable"}, 503


@app.get("/health")
async def health():
    return {"name": "MOHSEN ADMIN", "status": "online"}


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MOHSEN ADMIN</title><style>
:root{color-scheme:dark;font:15px system-ui;background:#0b1220;color:#e5edf8}
*{box-sizing:border-box}body{max-width:1050px;margin:4vh auto;padding:18px}
header,.panel{background:#121e30;border:1px solid #263750;border-radius:16px;padding:20px;margin:14px 0}
h1{margin:0;color:#8dd9ff}h2{margin-top:0}.muted{color:#9aacc3}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#e3a63a;margin-left:8px}
button{background:#176b91;color:white;border:0;border-radius:9px;padding:10px 16px;cursor:pointer}
input,textarea{width:100%;background:#0b1627;color:#e5edf8;border:1px solid #344862;border-radius:9px;padding:11px;margin:6px 0 12px;font:inherit}
textarea{min-height:90px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.item{border-bottom:1px solid #263750;padding:10px 0}.item small{display:block;color:#9aacc3;overflow-wrap:anywhere}
pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#b9d9ed}
@media(max-width:700px){.grid{grid-template-columns:1fr}}
</style></head><body>
<header><h1>MOHSEN · محسن</h1><p class="muted">لوحة التحكم المحلية للمساعد الشخصي</p>
<p><span class="dot"></span><span id="state">جارٍ الاتصال بالنواة…</span></p><button onclick="refreshAll()">تحديث البيانات</button></header>
<div class="grid">
<section class="panel"><h2>إضافة مهمة</h2><input id="taskTitle" placeholder="اكتب المهمة"><input id="taskDue" placeholder="موعد اختياري بصيغة ISO أو نص واضح"><button onclick="addTask()">حفظ المهمة</button><div id="taskMsg" class="muted"></div></section>
<section class="panel"><h2>حفظ ملاحظة</h2><input id="noteTitle" placeholder="عنوان الملاحظة"><textarea id="noteBody" placeholder="محتوى الملاحظة"></textarea><button onclick="addNote()">حفظ الملاحظة</button><div id="noteMsg" class="muted"></div></section>
</div>
<section class="panel"><h2>المهام المفتوحة</h2><div id="tasks">جارٍ التحميل…</div></section>
<section class="panel"><h2>الملاحظات</h2><input id="noteQuery" placeholder="ابحث في ملاحظاتك"><button onclick="loadNotes()">بحث</button><div id="notes"></div></section>
<section class="panel"><h2>تحدث مع محسن</h2><textarea id="assistantInput" placeholder="مثال: أضف مهمة: مراجعة المحاضرة"></textarea><button onclick="sendMessage()">إرسال</button><pre id="assistantReply"></pre></section>
<section class="panel"><h2>حالة النظام</h2><pre id="status">…</pre><p class="muted">هذه نسخة مساعد شخصي تجريبية. الأوامر المحددة تعمل محليًا؛ توليد اللغة الحرة ينتظر بناء النموذج وتدريبه.</p></section>
<script>
async function api(path,method='GET',body=null){const r=await fetch(path,{method,headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):null});const d=await r.json();if(!r.ok)throw new Error(d.detail||d.reply||'Request failed');return d}
function showError(id,e){document.getElementById(id).textContent=e.message}
async function refreshAll(){await Promise.all([loadStatus(),loadTasks(),loadNotes()])}
async function loadStatus(){try{const d=await api('/api/core/status');document.getElementById('status').textContent=JSON.stringify(d,null,2);document.getElementById('state').textContent=d.core==='online'?'النواة متصلة':'النواة غير متاحة'}catch(e){showError('status',e);document.getElementById('state').textContent='تعذر الاتصال'}}
async function loadTasks(){try{const d=await api('/api/tasks');const el=document.getElementById('tasks');el.innerHTML='';if(!d.items.length){el.textContent='لا توجد مهام مفتوحة.';return}for(const t of d.items){const row=document.createElement('div');row.className='item';const title=document.createElement('strong');title.textContent=t.title;const meta=document.createElement('small');meta.textContent=t.due_at||'بدون موعد';const btn=document.createElement('button');btn.textContent='تم الإنجاز';btn.onclick=async()=>{try{await api('/api/tasks/'+t.id+'/complete','POST',{});loadTasks()}catch(e){alert(e.message)}};row.append(title,meta,btn);el.append(row)}}catch(e){showError('tasks',e)}}
async function addTask(){try{const title=document.getElementById('taskTitle').value.trim();if(!title)throw new Error('اكتب عنوان المهمة');await api('/api/tasks','POST',{title,due_at:document.getElementById('taskDue').value.trim()||null});document.getElementById('taskTitle').value='';document.getElementById('taskDue').value='';document.getElementById('taskMsg').textContent='تم حفظ المهمة';loadTasks()}catch(e){showError('taskMsg',e)}}
async function addNote(){try{const title=document.getElementById('noteTitle').value.trim(),content=document.getElementById('noteBody').value.trim();if(!title||!content)throw new Error('أدخل العنوان والمحتوى');await api('/api/notes','POST',{title,content});document.getElementById('noteMsg').textContent='تم حفظ الملاحظة';document.getElementById('noteTitle').value='';document.getElementById('noteBody').value='';loadNotes()}catch(e){showError('noteMsg',e)}}
async function loadNotes(){try{const q=document.getElementById('noteQuery').value;const d=await api('/api/notes'+(q?'?q='+encodeURIComponent(q):''));const el=document.getElementById('notes');el.innerHTML='';if(!d.items.length){el.textContent='لا توجد ملاحظات.';return}for(const n of d.items){const row=document.createElement('div');row.className='item';const title=document.createElement('strong');title.textContent=n.title;const body=document.createElement('small');body.textContent=n.content;row.append(title,body);el.append(row)}}catch(e){showError('notes',e)}}
async function sendMessage(){try{const message=document.getElementById('assistantInput').value.trim();if(!message)throw new Error('اكتب رسالة أولاً');const d=await api('/api/assistant/message','POST',{message});document.getElementById('assistantReply').textContent=d.reply+'\n'+JSON.stringify(d.data||{},null,2)}catch(e){document.getElementById('assistantReply').textContent=e.message}}
refreshAll();setInterval(loadStatus,15000);
</script></body></html>"""


@app.get("/api/core/status")
async def core_status():
    data, code = await core_request("GET", "/api/v1/status")
    return JSONResponse(content=data, status_code=code)


@app.get("/api/tasks")
async def tasks():
    data, code = await core_request("GET", "/api/v1/tasks?status=open")
    return JSONResponse(content=data, status_code=code)


@app.post("/api/tasks")
async def create_task(payload: dict):
    data, code = await core_request("POST", "/api/v1/tasks", payload)
    return JSONResponse(content=data, status_code=code)


@app.post("/api/tasks/{task_id}/complete")
async def complete_task(task_id: str):
    data, code = await core_request("POST", f"/api/v1/tasks/{task_id}/complete", {})
    return JSONResponse(content=data, status_code=code)


@app.get("/api/notes")
async def notes(q: str | None = None):
    endpoint = "/api/v1/notes" + (f"?q={httpx.QueryParams({'q': q})['q']}" if q else "")
    data, code = await core_request("GET", endpoint)
    return JSONResponse(content=data, status_code=code)


@app.post("/api/notes")
async def create_note(payload: dict):
    data, code = await core_request("POST", "/api/v1/notes", payload)
    return JSONResponse(content=data, status_code=code)


@app.post("/api/assistant/message")
async def assistant_message(payload: dict):
    data, code = await core_request("POST", "/api/v1/assistant/message", payload)
    return JSONResponse(content=data, status_code=code)
