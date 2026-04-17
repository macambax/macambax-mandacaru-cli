# F-001: Project Scaffolding — Spec Kit Specification

**Feature:** F-001
**Sprint:** 1 — Foundation
**Status:** Not Started
**Depends on:** Nothing (first feature)
**Blocks:** F-002, F-003, F-004, F-005, F-006, F-007 (all Sprint 1)

---

## 1. Objective

Create the complete project directory structure, `pyproject.toml` with all dependencies, virtual environment, Playwright browser install, `CLAUDE.md` for AI context, `.env.example` credential template, and all `__init__.py` files so that every subsequent feature has a working Python package to build in.

After this feature is done, `pip install -e .` works and `mandacaru` is a callable entry point (even if it only prints "not implemented yet").

---

## 2. Directory Structure

```
mandacaru/                        ← root of project (inside macambax-mandacaru/)
│
├── mandacaru/                    ← Python package
│   ├── __init__.py               ← version string: __version__ = "0.1.0"
│   ├── cli.py                    ← empty Typer app stub
│   ├── startup.py                ← placeholder (F-007 fills this in)
│   ├── config.py                 ← placeholder (F-003 fills this in)
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py             ← placeholder (F-002 fills this in)
│   │   ├── migrations.py         ← placeholder
│   │   └── queries.py            ← placeholder
│   │
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py               ← placeholder (F-008)
│   │   ├── openai_collector.py   ← placeholder (F-009)
│   │   ├── gcp_collector.py      ← placeholder (F-010)
│   │   ├── vercel_collector.py   ← placeholder (F-018)
│   │   ├── anthropic_collector.py ← placeholder (F-016)
│   │   └── copilot_collector.py  ← placeholder (F-017)
│   │
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── ollama_client.py      ← placeholder (F-014)
│   │   └── prompts.py            ← placeholder (F-015)
│   │
│   ├── scheduler/
│   │   ├── __init__.py
│   │   └── daemon.py             ← placeholder (F-022)
│   │
│   └── reports/
│       ├── __init__.py
│       └── renderer.py           ← placeholder (F-012)
│
├── tests/
│   ├── __init__.py
│   ├── test_collectors.py        ← placeholder
│   ├── test_models.py            ← placeholder
│   └── test_reports.py           ← placeholder
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

---

## 3. pyproject.toml

### Metadata
- **name:** `mandacaru`
- **version:** `0.1.0`
- **description:** "Local-first CLI agent that tracks every dollar a developer spends across their entire dev stack."
- **license:** Apache-2.0
- **requires-python:** `>=3.11`
- **authors:** MacambaX AI LLC

### Dependencies
| Package | Purpose |
|---------|---------|
| `typer[all]>=0.9` | CLI framework (includes Rich + shellingham) |
| `rich>=13.0` | Terminal UI: tables, colors, panels, progress bars |
| `sqlalchemy>=2.0` | ORM — SQLite now, PostgreSQL later |
| `httpx>=0.27` | Async HTTP client for API collectors |
| `playwright>=1.40` | Browser automation for Playwright collectors |
| `apscheduler>=3.10` | Background scheduler for daemon mode |
| `python-dotenv>=1.0` | Load `.env` credentials |
| `ollama>=0.4` | Python client for Ollama vision |

### Dev Dependencies
| Package | Purpose |
|---------|---------|
| `pytest>=8.0` | Test runner |
| `pytest-asyncio>=0.23` | Async test support |

### Entry Point
```toml
[project.scripts]
mandacaru = "mandacaru.cli:app"
```

### Build System
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## 4. CLAUDE.md

Provide AI coding assistants with project context. Content per the product spec section 14.

---

## 5. .env.example

```bash
# Mandacarú — Credentials Template
# Copy to ~/.mandacaru/.env and fill in your values
# NEVER commit real credentials

# OpenAI — Usage API key (read-only billing access)
OPENAI_API_KEY=sk-...

# GCP — Service account JSON path (billing.viewer role only)
GOOGLE_APPLICATION_CREDENTIALS=~/.mandacaru/gcp-billing-sa.json
GCP_PROJECT_ID=your-project-id

# Vercel — Read-only token
VERCEL_TOKEN=...
```

---

## 6. .gitignore

Must ignore:
- `.env`, `*.db`, `__pycache__/`, `.venv/`, `dist/`, `*.egg-info/`
- `~/.mandacaru/` is outside the repo but document it
- Playwright state: no browser binaries committed

---

## 7. CLI Stub (cli.py)

Minimal Typer app so the `mandacaru` entry point is callable after `pip install -e .`:

```python
import typer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo("⚡ Mandacarú v0.1.0 — run 'mandacaru --help' for commands")

if __name__ == "__main__":
    app()
```

---

## 8. Placeholder Files

All placeholder module files contain only a docstring describing what will go there and which feature fills it in. Example:

```python
"""
Mandacarú — OpenAI Collector
Implements billing data collection from OpenAI Usage API.
See F-009 for implementation.
"""
```

---

## 9. Tasks (Implementation Order)

| # | Task | Output |
|---|------|--------|
| 1 | Create `mandacaru/` project root inside `macambax-mandacaru/` | Directory exists |
| 2 | Create `pyproject.toml` | Valid TOML, parseable |
| 3 | Create all directories + `__init__.py` files | Package structure exists |
| 4 | Create placeholder `.py` files with docstrings | All modules importable |
| 5 | Create `mandacaru/cli.py` with Typer stub | Entry point defined |
| 6 | Create `mandacaru/__init__.py` with `__version__` | Version importable |
| 7 | Create `.env.example` | Template in repo root |
| 8 | Create `.gitignore` | Standard Python + project-specific ignores |
| 9 | Create `CLAUDE.md` | AI context file in repo root |
| 10 | Create `README.md` | Minimal placeholder with project name + description |
| 11 | Create virtual environment + install deps | `pip install -e ".[dev]"` succeeds |
| 12 | Install Playwright browsers | `playwright install chromium` succeeds |
| 13 | Verify: `mandacaru` command runs | Entry point works |
| 14 | Verify: `pytest` runs (0 tests, no errors) | Test framework works |

---

## 10. Acceptance Criteria

- [ ] `cd mandacaru && pip install -e ".[dev]"` completes without errors
- [ ] `mandacaru` prints the version stub message
- [ ] `mandacaru --help` shows Typer help output
- [ ] `python -c "from mandacaru import __version__; print(__version__)"` prints `0.1.0`
- [ ] `python -c "import mandacaru.db.models"` imports without error
- [ ] `python -c "import mandacaru.collectors.base"` imports without error
- [ ] `pytest` runs and reports 0 errors (0 tests collected is fine)
- [ ] `.gitignore` covers `.env`, `*.db`, `__pycache__/`, `.venv/`, `dist/`
- [ ] No real credentials anywhere in the committed files
