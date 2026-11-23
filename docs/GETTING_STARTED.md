# Getting started

## Requirements
- Python 3.11 or newer.
- Git.
- Windows, Linux, or macOS.
- Internet access only to install dependencies or use the optional research feature (not implemented yet).

## Install development dependencies

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[core,admin,dev]"
```

## Run the Core

```bash
uvicorn mohsen_core.main:app --app-dir apps/mohsen-core --host 127.0.0.1 --port 8765
```

Set `MOHSEN_API_TOKEN` in your environment before exposing any API beyond localhost. The default development mode is loopback-only.

## Run the Admin

In a second terminal:

```bash
uvicorn mohsen_admin.main:app --app-dir apps/mohsen-admin --host 127.0.0.1 --port 8766
```

Open http://127.0.0.1:8766. Configure `MOHSEN_CORE_URL` and `MOHSEN_ADMIN_TOKEN` as appropriate. Admin forwards its configured Core token when calling the Core API.

## Run tests

```bash
python -m pytest
```

## Important
The chat endpoint deliberately reports that the language model is not ready. No pretrained model is included, and no claim of intelligent responses is made before training and evaluation.
