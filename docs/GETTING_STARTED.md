# Getting started

## Requirements
- Python 3.11 or newer.
- Git.
- Windows, Linux, or macOS.

## Install

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[core,admin,dev]"
```

Copy `.env.example` to `.env` and set a long random `MOHSEN_API_TOKEN`. Never commit `.env`. The Core and Admin must receive the same Core API token through their environment. Keep both services bound to 127.0.0.1.

## Run the Core

```bash
uvicorn mohsen_core.main:app --app-dir apps/mohsen-core --host 127.0.0.1 --port 8765
```

## Run the Admin

In a second terminal:

```bash
uvicorn mohsen_admin.main:app --app-dir apps/mohsen-admin --host 127.0.0.1 --port 8766
```

Open http://127.0.0.1:8766. The Admin dashboard reads status from the original Core via its authenticated API. The initial dashboard is a local development shell, not yet a hardened multi-user control panel. Do not expose it to a LAN or public network.

## Run tests

```bash
python -m pytest
```

## Important
The chat endpoint deliberately reports that the language model is not ready. No pretrained model is included, and no claim of intelligent responses is made before training and evaluation.
