# Roadmap

## Beta 0.2 — Personal assistant foundation
- [x] Separate Core and Admin applications
- [x] Authenticated Core API boundary
- [x] Local SQLite persistence for tasks and notes
- [x] Task create/list/complete/delete API
- [x] Note create/list/search API
- [x] Small explicit Arabic/English command router
- [x] Arabic local Admin dashboard
- [x] Tests for task, notes, command routing, and auth
- [ ] Confirm GitHub Actions run and owner-machine installation
- [ ] Background reminder scheduler and notification delivery
- [ ] Admin authentication/session protection before any non-loopback use

## Milestone 1 — Runtime hardening
- [ ] Task lifecycle, cancellation, audit events, and safe shutdown
- [ ] Resource monitor and background job indicator
- [ ] Database backup/restore and retention controls
- [ ] Configuration validation and security review

## Milestone 2 — Model research prototype
- [ ] Tokenizer/data format decisions
- [ ] Small randomly initialized decoder-only Transformer
- [ ] CPU/GPU capability detection
- [ ] Reproducible tiny-corpus overfit test
- [ ] Checkpoint save/resume and evaluation

## Milestone 3 — Data and learning pipeline
- [ ] User-provided dataset import
- [ ] Source provenance, licensing, quality, and deduplication checks
- [ ] Human approval queue
- [ ] Arabic/English balanced data evaluation
- [ ] Training job orchestration and rollback

## Milestone 4 — Memory and web research
- [ ] Local knowledge retrieval
- [ ] Source citations and freshness
- [ ] Sandboxed fetcher with SSRF protections
- [ ] Clear separation of retrieval and weight updates

## Milestone 5 — Admin applications
- [ ] Desktop shell
- [ ] Responsive web interface
- [ ] Model/training/memory/system dashboards
- [ ] Authenticated control of the original Core

## Milestone 6 — Hybrid compute
- [ ] Remote worker protocol
- [ ] Explicit job and dataset transfer approval
- [ ] Encrypted transport and signed artifacts
- [ ] Checkpoint synchronization

## Milestone 7 — Release hardening
- [ ] Security review
- [ ] Performance benchmarks
- [ ] Backup/restore tests
- [ ] Windows and Linux packaging
