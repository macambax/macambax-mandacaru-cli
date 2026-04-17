# Data Model: F-001 Project Scaffolding

**Date**: 2026-04-17  
**Status**: Complete

## Overview

F-001 is a scaffolding feature — it creates files and directories, not data entities. The "model" here is the package structure itself: what files exist, what they contain, and how they relate.

## Entities

### Package Identity

| Field | Value | Source |
|-------|-------|--------|
| name | `mandacaru` | pyproject.toml `[project].name` |
| version | `0.1.0` | `mandacaru/__init__.py` → `__version__` |
| description | Local-first CLI agent that tracks every dollar a developer spends across their entire dev stack | pyproject.toml |
| license | Apache-2.0 | pyproject.toml |
| requires-python | `>=3.11` | pyproject.toml |
| entry_point | `mandacaru = "mandacaru.cli:app"` | pyproject.toml `[project.scripts]` |
| build_backend | `hatchling.build` | pyproject.toml `[build-system]` |

### Sub-Packages

| Package | Purpose | Placeholder Modules |
|---------|---------|-------------------|
| `mandacaru.db` | Database layer | `models.py` (F-002), `migrations.py` (F-002), `queries.py` (F-002) |
| `mandacaru.collectors` | Billing collectors | `base.py` (F-008), `openai_collector.py` (F-009), `gcp_collector.py` (F-010), `vercel_collector.py` (F-018), `anthropic_collector.py` (F-016), `copilot_collector.py` (F-017) |
| `mandacaru.vision` | Ollama vision | `ollama_client.py` (F-014), `prompts.py` (F-015) |
| `mandacaru.scheduler` | Daemon mode | `daemon.py` (F-022) |
| `mandacaru.reports` | Rich output | `renderer.py` (F-012) |

### Root-Level Files

| File | Purpose | Content Scope |
|------|---------|--------------|
| `pyproject.toml` | Package metadata + deps | Full — all fields per spec |
| `.env.example` | Credential template | OpenAI, GCP, Vercel placeholders |
| `.gitignore` | VCS exclusions | Python + project-specific |
| `CLAUDE.md` | AI context | Project structure, conventions, tech stack |
| `README.md` | Human readme | Project name, description, setup steps |

## Relationships

```
pyproject.toml
  ├── defines → mandacaru/ (package)
  ├── declares → entry point → mandacaru.cli:app
  └── lists → dependencies (runtime + dev)

mandacaru/__init__.py
  └── exports → __version__ = "0.1.0"

mandacaru/cli.py
  └── creates → Typer app (stub)

Each placeholder .py
  └── contains → docstring referencing future feature ID
```

## State Transitions

N/A — no runtime state in scaffolding.

## Validation Rules

- `__version__` in `__init__.py` MUST match `version` in `pyproject.toml` (both `0.1.0`)
- Every directory under `mandacaru/` MUST contain `__init__.py`
- Every `.py` file MUST be importable without errors
- `.env.example` MUST NOT contain real credentials
- `.gitignore` MUST include `.env` and `*.db`
