# Implementation Plan: F-001 Project Scaffolding

**Branch**: `001-project-scaffolding` | **Date**: 2026-04-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `dev/specs/F-001/spec.md`

## Summary

Create the complete `mandacaru/` Python package structure with pyproject.toml, all sub-packages (db, collectors, vision, scheduler, reports), placeholder modules, CLI entry point via Typer, test infrastructure, credential templates, and documentation files. After this feature, `pip install -e ".[dev]"` works and `mandacaru` is a callable command.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: typer[all]>=0.9, rich>=13.0, sqlalchemy>=2.0, httpx>=0.27, playwright>=1.40, apscheduler>=3.10, python-dotenv>=1.0, ollama>=0.4  
**Storage**: N/A (F-001 is scaffolding only; SQLite introduced in F-002)  
**Testing**: pytest>=8.0, pytest-asyncio>=0.23  
**Target Platform**: macOS (dev), Linux (production), Python 3.11+  
**Project Type**: CLI application  
**Performance Goals**: N/A (scaffolding feature — no runtime behavior)  
**Constraints**: Offline-capable after initial install; `pip install -e ".[dev]"` must complete in <60s on broadband  
**Scale/Scope**: Single developer, ~20 source files created as placeholders

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Local-First | PASS | F-001 creates no network calls; all files are local to the repo |
| II. CLI-First with Rich | PASS | CLI entry point via Typer stub; Rich is a dependency |
| III. Collector Architecture | PASS | Placeholder files follow one-file-per-provider pattern |
| IV. Data Integrity | N/A | No data operations in scaffolding |
| V. Self-Tracking | N/A | No Ollama calls in scaffolding |
| VI. Phase-Gated Scope | PASS | Only Phase 1 providers have placeholder files; no Phase 2/3 features |
| VII. Simplicity & YAGNI | PASS | Placeholders contain only docstrings; no premature abstractions |
| Security | PASS | .env.example has no real credentials; .gitignore covers .env and .db |

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
mandacaru/                     ← Python package root
├── __init__.py                ← __version__ = "0.1.0"
├── cli.py                     ← Typer app stub (entry point)
├── startup.py                 ← placeholder (F-007)
├── config.py                  ← placeholder (F-003)
├── db/
│   ├── __init__.py
│   ├── models.py              ← placeholder (F-002)
│   ├── migrations.py          ← placeholder (F-002)
│   └── queries.py             ← placeholder (F-002)
├── collectors/
│   ├── __init__.py
│   ├── base.py                ← placeholder (F-008)
│   ├── openai_collector.py    ← placeholder (F-009)
│   ├── gcp_collector.py       ← placeholder (F-010)
│   ├── vercel_collector.py    ← placeholder (F-018)
│   ├── anthropic_collector.py ← placeholder (F-016)
│   └── copilot_collector.py   ← placeholder (F-017)
├── vision/
│   ├── __init__.py
│   ├── ollama_client.py       ← placeholder (F-014)
│   └── prompts.py             ← placeholder (F-015)
├── scheduler/
│   ├── __init__.py
│   └── daemon.py              ← placeholder (F-022)
└── reports/
    ├── __init__.py
    └── renderer.py            ← placeholder (F-012)

tests/
├── __init__.py
├── test_collectors.py         ← placeholder
├── test_models.py             ← placeholder
└── test_reports.py            ← placeholder
```

**Structure Decision**: Single-project layout matching the constitution's Project Structure section. The `mandacaru/` package lives at the repo root (alongside `dev/`, `zzz_context_docs/`, `.specify/`). No monorepo, no frontend — pure Python CLI.

## Complexity Tracking

No constitution violations. F-001 is pure scaffolding with zero runtime logic.

## Post-Design Constitution Re-Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Local-First | PASS | No network calls, no external data transmission |
| II. CLI-First with Rich | PASS | Typer entry point with Rich as dependency |
| III. Collector Architecture | PASS | One-file-per-provider pattern in `collectors/` |
| IV. Data Integrity | N/A | No data operations |
| V. Self-Tracking | N/A | No Ollama calls |
| VI. Phase-Gated Scope | PASS | Only Phase 1 provider placeholders created |
| VII. Simplicity & YAGNI | PASS | Docstring-only placeholders, minimal CLI stub |
| Security | PASS | `.env.example` has no real credentials; `.gitignore` covers secrets |

**Result**: All gates PASS. No violations. Proceed to `/speckit.tasks`.

## Generated Artifacts

| Artifact | Path |
|----------|------|
| Plan | `dev/specs/F-001/plan.md` |
| Research | `dev/specs/F-001/research.md` |
| Data Model | `dev/specs/F-001/data-model.md` |
| Contracts | `dev/specs/F-001/contracts/cli-entry-point.md` |
| Quickstart | `dev/specs/F-001/quickstart.md` |
