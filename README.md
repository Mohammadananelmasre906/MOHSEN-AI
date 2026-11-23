# MOHSEN AI

MOHSEN is an independent Arabic/English AI project with a dedicated local personal-assistant interface.

> **Current version:** Personal Assistant Beta 0.2. The beta provides working local tasks, notes, search, a small command-based assistant, and an Arabic Admin dashboard. The independent language model has not yet been implemented or trained.

## Repository layout

- `apps/mohsen-core` — the original runtime, authenticated API, and authoritative local data store.
- `apps/mohsen-admin` — a separate local administration app that controls the original Core through its API.
- `packages` — shared contracts and utilities.
- `docs` — architecture, setup, and roadmap.
- `tests` — automated tests.

## Personal Assistant Beta features

- Create, list, complete, and delete tasks.
- Store notes locally in SQLite and search their contents.
- Submit supported Arabic and English commands.
- Use the local Admin dashboard to manage tasks and notes.
- Keep personal data on the local machine by default.

## Principles

1. No pretrained model weights or hidden external AI provider.
2. Arabic and English are first-class targets.
3. Web research, knowledge retrieval, and weight training are separate capabilities.
4. New training data must be reviewed before it changes model weights.
5. Admin controls the single original Core instance; it is not a second AI runtime.
6. Local-first by default. Remote compute is optional and explicit.
7. Never commit credentials, private datasets, user memory, or model checkpoints.

## Quick start

Follow [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

## Privacy policy

The file `سياسة الخصوصية.txt` is intentionally empty, as requested by the project owner. Technical privacy controls are documented separately and do not depend on that file.

## Important limitations

This is a usable personal organizer beta, not yet a general conversational AI. Supported commands use explicit application logic. Free-form language generation remains disabled until the independently initialized model is implemented, trained, and evaluated. Reminder notifications, internet research, desktop/mobile packaging, remote compute, and multi-user Admin authentication are not part of this beta. Run both services on `127.0.0.1` only.
