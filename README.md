# MOHSEN AI

An independent, multilingual, self-evolving AI system with a dedicated local administration platform.

> **Status:** Foundation phase. The repository intentionally starts without pretrained weights, pretrained models, or bundled training corpora. A randomly initialized language model is not useful until it has been trained; this project will make that distinction explicit.

## Repository layout

- `apps/mohsen-core` — the original AI runtime and its API.
- `apps/mohsen-admin` — a separate local administration application that controls the original Core through an authenticated API.
- `packages` — shared contracts and utilities.
- `docs` — architecture and engineering decisions.
- `tests` — automated tests.

## Principles

1. No pretrained model weights or hidden external AI provider.
2. Arabic and English are first-class training targets.
3. Web research, knowledge retrieval, and weight training are separate capabilities.
4. New training data must be reviewed before it changes model weights.
5. Admin controls the single original Core instance; it is not a second AI runtime.
6. Local-first by default. Remote compute is optional and explicit.
7. Never commit credentials, private datasets, user memory, or model checkpoints.

## Quick start

See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

## Privacy policy

The file `سياسة الخصوصية.txt` is intentionally empty, as requested by the project owner. Technical privacy controls are documented separately and do not depend on that file.

## Current limitations

The first foundation release provides the service boundary, health/status API, local admin shell, and tests. It does **not** claim that an untrained model can chat intelligently. The model/training implementation will be added and validated in subsequent milestones.
