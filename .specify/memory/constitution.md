# Mandacaru Constitution

> *Every dollar your dev stack costs. One place. Runs on your machine.*

## Core Principles

### I. Local-First, Privacy-Preserving
Mandacaru runs entirely on the user's machine. No data leaves the local environment in Phase 1. No cloud dependency, no proxy model, no API call interception. The user's credentials and billing data stay in `~/.mandacaru/` and are never transmitted externally. SQLite is the sole data store. This principle is non-negotiable for Phase 1 and Phase 2.

### II. CLI-First with Rich Output
All functionality is exposed via the `mandacaru` CLI built with Typer. Output uses Rich for tables, progress bars, panels, and color-coded status. Every command must be usable non-interactively (scriptable) while also providing beautiful terminal output for humans. No web UI in Phase 1.

### III. Collector Architecture
Each billing provider has its own collector module extending `BaseCollector`. Two collection methods exist: direct API (OpenAI, GCP, Vercel) and Playwright + Ollama vision (Anthropic, GitHub Copilot). New providers are added by creating a single file — never by modifying existing collectors. The collector interface is the primary extension point.

### IV. Data Integrity & Auditability
- Every sync attempt is logged in `sync_log` — success, failure, or partial. Silent failures are unacceptable.
- `daily_usage` uses a UNIQUE constraint on `(provider_id, usage_date, model_name)` enabling safe upserts. Re-running sync never duplicates data.
- `raw_response` on `daily_usage` always stores the full API JSON. Zero cost in SQLite. Never discard raw data.
- Budget alerts are persisted in `budget_alerts` with acknowledgment tracking.

### V. Self-Tracking Transparency
Mandacaru tracks the cost of its own Ollama calls used for vision extraction. The tool must be honest about its own resource consumption. This is a brand value — "more honest than all of them."

### VI. Phase-Gated Scope
Development follows three strict phases. Do not build Phase 2 or Phase 3 features during Phase 1:
- **Phase 1 — Local CLI:** 5 providers, CLI commands, SQLite, Ollama, no auth, no cloud, no multi-user.
- **Phase 2 — Open Source:** 20+ providers, optional cloud LLM, manual subscriptions, export, MCP server, plugin system.
- **Phase 3 — SaaS Cloud:** PostgreSQL, Supabase auth, Stripe billing, React dashboard, multi-user teams.

### VII. Simplicity & YAGNI
Start simple. No over-engineering. No abstractions for one-time operations. No features beyond what the current phase requires. If a decision can be deferred, defer it. SQLAlchemy enables the SQLite → PostgreSQL migration with a one-line change when the time comes — not before.

## Technology Stack

| Layer | Technology | Constraint |
|-------|-----------|------------|
| Language | Python 3.11+ | Required — team familiarity from Cajú |
| CLI | Typer + Rich | No alternatives — this is the interface |
| ORM | SQLAlchemy 2.x | Required for SQLite → PostgreSQL path |
| Database | SQLite 3.x | Phase 1 only. File at `~/.mandacaru/mandacaru.db` |
| Browser | Playwright | Headless Chromium for Playwright collectors |
| Vision | Ollama + llama3.2-vision | Local, free, no API key. Configurable in Phase 2 |
| Scheduler | APScheduler 3.x | Daemon mode for daily auto-sync |
| HTTP | httpx | Async-ready for API collectors |
| Config | python-dotenv | Credentials in `~/.mandacaru/.env` |
| Package | Hatchling build, pipx install | `pipx install mandacaru` is the target UX |

No additional dependencies without justification. Every dependency added must serve a Phase 1 requirement.

## Security Requirements

- **No credentials in code.** All secrets in `~/.mandacaru/.env`, loaded via python-dotenv. `.env` is always in `.gitignore`.
- **Playwright cookies** for Anthropic/GitHub stored locally, never in the repo.
- **GCP service account** uses `billing.viewer` role only — read-only, least privilege.
- **OpenAI/Vercel tokens** should be scoped to read-only billing access where the provider supports it.
- **`mandacaru reset`** requires explicit confirmation — it is destructive.
- No `eval()`, no `exec()`, no dynamic code execution on user input or API responses.

## Development Workflow

- **Methodology:** Spec Kit — `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`
- **Build order:** Features implemented sequentially per sprint (Sprint 1 → 4). No skipping ahead.
- **Testing:** `pytest` before every commit. Fixtures for Ollama responses — no live Ollama calls in unit tests.
- **Feature tracking:** `dev/FEATURES.md` is the source of truth for implementation status.
- **Spec source:** `zzz_context_docs/mandacaru_spec.md` is the canonical product specification. Update it when deviating from the spec.
- **DB access:** All database operations go through SQLAlchemy sessions via `get_session()`. No raw SQL in application code.

## Project Structure

```
mandacaru/                     ← Python package root
├── __init__.py                ← __version__ = "0.1.0"
├── cli.py                     ← Typer app — all commands
├── startup.py                 ← ASCII cactus welcome screen
├── config.py                  ← Settings management
├── db/                        ← Database layer
│   ├── models.py              ← SQLAlchemy models
│   ├── migrations.py          ← Schema versioning
│   └── queries.py             ← Query helpers
├── collectors/                ← One file per provider
│   ├── base.py                ← BaseCollector ABC
│   ├── openai_collector.py
│   ├── gcp_collector.py
│   ├── vercel_collector.py
│   ├── anthropic_collector.py
│   └── copilot_collector.py
├── vision/                    ← Ollama vision layer
│   ├── ollama_client.py
│   └── prompts.py
├── scheduler/
│   └── daemon.py              ← APScheduler daemon
└── reports/
    └── renderer.py            ← Rich table rendering
```

## Brand Identity

| Attribute | Value |
|-----------|-------|
| Product name | Mandacaru |
| Parent brand | MacambaX AI LLC |
| Primary color | Purple `#7C3AED` |
| Secondary | Teal `#2ABFA3` |
| Accent | Orange `#E88E36` |
| CLI command | `mandacaru` |
| Icon | ⚡ |
| License | Apache 2.0 |
| Repo | github.com/macambax/mandacaru |

## Governance

This constitution supersedes all other development practices for Mandacaru. Any deviation must be documented in the spec and approved before implementation. Phase boundaries are hard gates — no Phase 2/3 work until the prior phase is complete and pushed to GitHub.

**Version**: 1.0.0 | **Ratified**: 2026-04-17 | **Last Amended**: 2026-04-17
