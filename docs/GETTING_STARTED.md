# Getting started

## Requirements
- Python 3.11 or newer.
- Git.
- Windows, Linux, or macOS.

## Install

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[core,admin,dev]"
Copy-Item .env.example .env
```

Generate a strong random value for `MOHSEN_API_TOKEN` in `.env`. Keep `.env` private and never commit it. The Core stores personal data in the local SQLite file configured by `MOHSEN_DATABASE_PATH`; by default it uses the current user's home directory under `.mohsen/data`.

## Run Core

In the first terminal:

```powershell
uvicorn mohsen_core.main:app --app-dir apps/mohsen-core --host 127.0.0.1 --port 8765
```

## Run Admin

In a second terminal:

```powershell
uvicorn mohsen_admin.main:app --app-dir apps/mohsen-admin --host 127.0.0.1 --port 8766
```

Open http://127.0.0.1:8766. Keep both services on `127.0.0.1`; this first beta is a local owner tool and is not hardened for LAN or public exposure.

## Available beta features
- Create, list, complete, and delete tasks through the Core API.
- Save notes and search their title/content.
- Use the Admin dashboard to create tasks and notes and view open tasks.
- Send supported Arabic/English commands to `/api/v1/assistant/message`.

Examples:
- `أضف مهمة: مراجعة المحاضرة`
- `اعرض مهامي`
- `احفظ ملاحظة: فكرة المشروع | مساعد شخصي ثنائي اللغة`
- `ابحث في الملاحظات: المشروع`
- `add task: review lecture`
- `list tasks`

The task due-date field currently stores the supplied date/time text; it does not yet run a background notification scheduler.

## Run tests

```powershell
python -m pytest
```

## Honest capability boundary
This beta is a functional personal organizer, not yet a trained conversational language model. It does not include pretrained weights. Supported commands are handled by explicit application logic; free-form generation returns `503 model_not_ready` rather than inventing an AI answer. Internet research, desktop packaging, mobile access, and model training are not included in this beta yet.
