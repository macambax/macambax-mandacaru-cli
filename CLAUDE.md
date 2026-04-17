# CLAUDE.md — AI Assistant Context

## Project

**Mandacaru** by MacambaX AI LLC — a local-first CLI agent that tracks every dollar a developer spends across their entire dev stack (AI APIs, cloud services, SaaS subscriptions).

## Tech Stack

- **Language**: Python 3.11+
- **CLI**: Typer + Rich
- **ORM**: SQLAlchemy 2.x
- **Database**: SQLite 3.x (`~/.mandacaru/mandacaru.db`)
- **Browser automation**: Playwright (headless Chromium)
- **Vision LLM**: Ollama + llama3.2-vision (local)
- **HTTP**: httpx
- **Scheduler**: APScheduler 3.x
- **Config**: python-dotenv

## Package Structure

```
mandacaru/              ← Python package
├── cli.py              ← Typer entry point
├── config.py           ← Settings management
├── startup.py          ← ASCII startup screen
├── db/                 ← SQLAlchemy models, migrations, queries
├── collectors/         ← One file per billing provider (BaseCollector pattern)
├── vision/             ← Ollama client + extraction prompts
├── scheduler/          ← APScheduler daemon
└── reports/            ← Rich table rendering
tests/                  ← pytest test suite
```

## Conventions

- **Entry point**: `mandacaru = "mandacaru.cli:app"` (Typer)
- **DB access**: All through SQLAlchemy sessions via `get_session()`. No raw SQL.
- **Collectors**: Each extends `BaseCollector` ABC. Two types: API (httpx) and Playwright+Vision.
- **Credentials**: `~/.mandacaru/.env` loaded via python-dotenv. Never in code.
- **Testing**: `pytest`. Fixtures for Ollama responses — no live Ollama calls in tests.
- **Phase 1 scope**: 5 providers (OpenAI, GCP, Vercel, Anthropic, GitHub Copilot). No auth, no cloud, no multi-user.

## Key Patterns

- Version in `mandacaru/__init__.py`: `__version__ = "0.1.0"`
- Build system: Hatchling
- License: Apache 2.0
- All sync attempts logged in `sync_log` table
- `daily_usage` uses UNIQUE constraint on `(provider_id, usage_date, model_name)` for safe upserts
