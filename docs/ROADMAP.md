# Roadmap

## Milestone 0 — Repository foundation (current)
- [x] Monorepo layout for Core and Admin
- [x] API boundary and local-first defaults
- [x] Empty owner privacy-policy file
- [ ] Verify installation and tests on the owner's Windows machine

## Milestone 1 — Runtime and security
- [ ] Configuration validation and secret handling
- [ ] Owner authentication and session controls
- [ ] Task lifecycle, cancellation, and audit events
- [ ] Resource monitor and safe shutdown

## Milestone 2 — Model research prototype
- [ ] Tokenizer/data format decisions
- [ ] Small randomly initialized decoder-only Transformer
- [ ] CPU/GPU capability detection
- [ ] Reproducible tiny-corpus overfit test
- [ ] Checkpoint save/resume and evaluation

## Milestone 3 — Data and learning pipeline
- [ ] User-provided dataset import
- [ ] Source provenance, licensing, quality and deduplication checks
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
