from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from . import store
from .config import settings
from .schemas import AssistantMessage, ChatRequest, HealthResponse, NoteCreate, TaskCreate
from .security import require_admin_token

app = FastAPI(title=settings.app_name, version=settings.version)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        name=settings.app_name,
        version=settings.version,
        status="online",
        model_ready=False,
    )


@app.get("/api/v1/status", dependencies=[Depends(require_admin_token)])
async def status():
    return {
        "core": "online",
        "assistant": "personal_assistant_beta",
        "model": "not_initialized",
        "training": "idle",
        "memory": "local_sqlite",
        "internet_research": "not_configured",
        "capabilities": ["tasks", "notes", "local_search"],
    }


@app.get("/api/v1/tasks", dependencies=[Depends(require_admin_token)])
async def get_tasks(status: str | None = Query(default=None, pattern="^(open|completed)$")):
    return {"items": store.list_tasks(status), "count": len(store.list_tasks(status))}


@app.post("/api/v1/tasks", status_code=201, dependencies=[Depends(require_admin_token)])
async def add_task(payload: TaskCreate):
    return store.create_task(payload.title, payload.due_at)


@app.post("/api/v1/tasks/{task_id}/complete", dependencies=[Depends(require_admin_token)])
async def finish_task(task_id: str):
    task = store.complete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/api/v1/tasks/{task_id}", dependencies=[Depends(require_admin_token)])
async def remove_task(task_id: str):
    if not store.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True, "id": task_id}


@app.get("/api/v1/notes", dependencies=[Depends(require_admin_token)])
async def get_notes(q: str | None = Query(default=None, max_length=200)):
    items = store.list_notes(q)
    return {"items": items, "count": len(items)}


@app.post("/api/v1/notes", status_code=201, dependencies=[Depends(require_admin_token)])
async def add_note(payload: NoteCreate):
    return store.create_note(payload.title, payload.content)


@app.post("/api/v1/assistant/message", dependencies=[Depends(require_admin_token)])
async def assistant_message(payload: AssistantMessage):
    message = payload.message.strip()
    lowered = message.casefold()

    task_prefixes = ("أضف مهمة:", "اضف مهمة:", "مهمة:", "add task:", "remind me to ")
    for prefix in task_prefixes:
        if lowered.startswith(prefix.casefold()):
            title = message[len(prefix):].strip()
            if not title:
                raise HTTPException(status_code=422, detail="Task title is required")
            task = store.create_task(title)
            return {
                "mode": "command",
                "action": "task_created",
                "reply": f"تمت إضافة المهمة: {title}" if any("\u0600" <= c <= "\u06ff" for c in message) else f"Task added: {title}",
                "data": task,
            }

    if lowered in {"اعرض مهامي", "مهامي", "قائمة المهام", "list tasks", "show my tasks"}:
        tasks = store.list_tasks("open")
        return {"mode": "command", "action": "tasks_listed", "reply": f"لديك {len(tasks)} مهام مفتوحة." if any("\u0600" <= c <= "\u06ff" for c in message) else f"You have {len(tasks)} open tasks.", "data": tasks}

    note_prefixes = ("احفظ ملاحظة:", "ملاحظة:", "save note:")
    for prefix in note_prefixes:
        if lowered.startswith(prefix.casefold()):
            raw = message[len(prefix):].strip()
            title, separator, body = raw.partition("|")
            if not separator or not title.strip() or not body.strip():
                raise HTTPException(status_code=422, detail="Use: save note: title | note content")
            note = store.create_note(title, body)
            return {"mode": "command", "action": "note_saved", "reply": "تم حفظ الملاحظة." if any("\u0600" <= c <= "\u06ff" for c in message) else "Note saved.", "data": note}

    if lowered.startswith(("ابحث في الملاحظات:", "ابحث عن ملاحظة:", "search notes:")):
        query = message.split(":", 1)[1].strip() if ":" in message else ""
        notes = store.list_notes(query)
        return {"mode": "command", "action": "notes_searched", "reply": f"وجدت {len(notes)} ملاحظات." if any("\u0600" <= c <= "\u06ff" for c in message) else f"Found {len(notes)} notes.", "data": notes}

    return JSONResponse(
        status_code=503,
        content={
            "mode": "model_unavailable",
            "status": "model_not_ready",
            "reply": "الوظائف الحالية محدودة بالأوامر المدعومة. النموذج اللغوي المستقل لم يُبنَ أو يُدرّب بعد.",
            "supported_commands": [
                "أضف مهمة: مراجعة الدرس",
                "اعرض مهامي",
                "احفظ ملاحظة: عنوان الملاحظة | محتواها",
                "ابحث في الملاحظات: كلمة البحث",
            ],
        },
    )


@app.post("/api/v1/chat", dependencies=[Depends(require_admin_token)])
async def chat(payload: ChatRequest):
    # No pretrained weights are bundled; free-form generation remains disabled.
    return JSONResponse(
        status_code=503,
        content={
            "status": "model_not_ready",
            "message": "MOHSEN has no trained language model yet.",
            "detail": "Use /api/v1/assistant/message for the supported personal-assistant commands.",
        },
    )
