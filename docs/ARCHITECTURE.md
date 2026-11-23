# Architecture (foundation)

## Two independently deployable applications

### MOHSEN CORE
The single original AI runtime. Owns model loading, inference, training jobs, memory, knowledge ingestion, web research, permissions, and resource monitoring. It exposes a versioned API.

### MOHSEN ADMIN
A separate owner-only control plane. It displays Core status and submits authorized control requests to that same Core instance. It does not contain a second copy of the model and must not modify Core source files at runtime.

## Trust boundaries
- Bind both services to 127.0.0.1 by default.
- Require a high-entropy bearer token for protected Core endpoints.
- Keep Admin and Core credentials separate.
- Do not expose Admin directly to the public internet.
- Remote compute must use authenticated encrypted transport and explicit per-job data selection.
- Web content is untrusted input, never executable instructions.
- Training data requires review, provenance, licensing checks, deduplication, and safety filtering.

## Learning versus retrieval
Retrieval stores source material in a searchable knowledge store. Training changes model weights. These are distinct workflows with distinct approvals, logs, and rollback plans.

## Model family
The intended family may contain multiple sizes. Model configuration, tokenizer compatibility, dataset version, training recipe, and evaluation report must be recorded for every checkpoint. No sizes or hardware targets are promised until benchmarked.

## Privacy
The owner-provided `سياسة الخصوصية.txt` remains empty. Actual technical safeguards are implemented in code and documented here; an empty policy file is not a security mechanism.
