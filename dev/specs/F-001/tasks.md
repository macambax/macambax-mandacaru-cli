# Tasks: F-001 Project Scaffolding

**Input**: Design documents from `dev/specs/F-001/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Not requested in the feature specification. No test tasks generated.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Package root**: `mandacaru/` at repository root
- **Tests**: `tests/` at repository root
- **Config files**: Repository root (pyproject.toml, .env.example, etc.)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create the project metadata and build configuration

- [x] T001 Create `pyproject.toml` at repository root with package name `mandacaru`, version `0.1.0`, license `Apache-2.0`, `requires-python >= "3.11"`, hatchling build system, runtime dependencies (typer[all]>=0.9, rich>=13.0, sqlalchemy>=2.0, httpx>=0.27, playwright>=1.40, apscheduler>=3.10, python-dotenv>=1.0, ollama>=0.4), dev dependencies (pytest>=8.0, pytest-asyncio>=0.23), and entry point `mandacaru = "mandacaru.cli:app"`
- [x] T002 [P] Update `.gitignore` at repository root to include Python-specific entries: `__pycache__/`, `*.pyc`, `.env`, `*.egg-info/`, `.venv/`, `dist/`, `build/`, `*.db`, `.playwright/`

---

## Phase 2: Foundational (Package Structure)

**Purpose**: Create the complete package directory tree with all `__init__.py` files — MUST complete before user story work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create `mandacaru/__init__.py` with `__version__ = "0.1.0"` and package docstring
- [x] T004 [P] Create `mandacaru/db/__init__.py` (empty, package marker)
- [x] T005 [P] Create `mandacaru/collectors/__init__.py` (empty, package marker)
- [x] T006 [P] Create `mandacaru/vision/__init__.py` (empty, package marker)
- [x] T007 [P] Create `mandacaru/scheduler/__init__.py` (empty, package marker)
- [x] T008 [P] Create `mandacaru/reports/__init__.py` (empty, package marker)
- [x] T009 [P] Create `tests/__init__.py` (empty, package marker)

**Checkpoint**: All packages exist and are importable as `mandacaru.<subpackage>`

---

## Phase 3: User Story 1 — Install and Run the CLI (Priority: P1) 🎯 MVP

**Goal**: A developer can `pip install -e ".[dev]"` and run `mandacaru` successfully

**Independent Test**: Run `pip install -e ".[dev]"` in a fresh venv, then `mandacaru` exits with code 0

### Implementation for User Story 1

- [x] T010 [US1] Create `mandacaru/cli.py` with minimal Typer app: `app = typer.Typer()`, a `callback(invoke_without_command=True)` that prints `"⚡ Mandacaru v0.1.0 — run 'mandacaru --help' for commands"`, and `if __name__ == "__main__": app()` guard
- [x] T011 [US1] Create virtual environment (`python3 -m venv .venv`), activate it, run `pip install -e ".[dev]"`, and verify `mandacaru` command responds with the stub message
- [x] T012 [US1] Verify `mandacaru --help` displays Typer-generated help text and exits with code 0

**Checkpoint**: `mandacaru` CLI is installable and callable — MVP delivered

---

## Phase 4: User Story 2 — Complete Project Structure (Priority: P2)

**Goal**: All sub-packages contain placeholder modules with docstrings referencing future features

**Independent Test**: Every placeholder module is importable; docstrings contain feature IDs

### Implementation for User Story 2

- [x] T013 [P] [US2] Create `mandacaru/db/models.py` with docstring `"""Mandacaru — SQLAlchemy ORM models. Placeholder for F-002: Database Layer."""`
- [x] T014 [P] [US2] Create `mandacaru/db/migrations.py` with docstring `"""Mandacaru — Schema version management. Placeholder for F-002: Database Layer."""`
- [x] T015 [P] [US2] Create `mandacaru/db/queries.py` with docstring `"""Mandacaru — Common query helpers. Placeholder for F-002: Database Layer."""`
- [x] T016 [P] [US2] Create `mandacaru/collectors/base.py` with docstring `"""Mandacaru — BaseCollector ABC. Placeholder for F-008: Base Collector."""`
- [x] T017 [P] [US2] Create `mandacaru/collectors/openai_collector.py` with docstring `"""Mandacaru — OpenAI billing collector. Placeholder for F-009: OpenAI Collector."""`
- [x] T018 [P] [US2] Create `mandacaru/collectors/gcp_collector.py` with docstring `"""Mandacaru — GCP billing collector. Placeholder for F-010: GCP Collector."""`
- [x] T019 [P] [US2] Create `mandacaru/collectors/vercel_collector.py` with docstring `"""Mandacaru — Vercel billing collector. Placeholder for F-018: Vercel Collector."""`
- [x] T020 [P] [US2] Create `mandacaru/collectors/anthropic_collector.py` with docstring `"""Mandacaru — Anthropic billing collector (Playwright+Vision). Placeholder for F-016: Anthropic Collector."""`
- [x] T021 [P] [US2] Create `mandacaru/collectors/copilot_collector.py` with docstring `"""Mandacaru — GitHub Copilot billing collector (Playwright+Vision). Placeholder for F-017: Copilot Collector."""`
- [x] T022 [P] [US2] Create `mandacaru/vision/ollama_client.py` with docstring `"""Mandacaru — Ollama vision client. Placeholder for F-014: Ollama Integration."""`
- [x] T023 [P] [US2] Create `mandacaru/vision/prompts.py` with docstring `"""Mandacaru — Vision extraction prompts. Placeholder for F-015: Vision Prompts."""`
- [x] T024 [P] [US2] Create `mandacaru/scheduler/daemon.py` with docstring `"""Mandacaru — APScheduler daemon for daily auto-sync. Placeholder for F-022: Daemon Mode."""`
- [x] T025 [P] [US2] Create `mandacaru/reports/renderer.py` with docstring `"""Mandacaru — Rich table rendering for reports. Placeholder for F-012: Report Renderer."""`
- [x] T026 [P] [US2] Create `mandacaru/startup.py` with docstring `"""Mandacaru — ASCII cactus startup screen. Placeholder for F-007: Startup Screen."""`
- [x] T027 [P] [US2] Create `mandacaru/config.py` with docstring `"""Mandacaru — Settings management. Placeholder for F-003: Configuration Management."""`
- [x] T028 [US2] Verify all placeholder modules are importable: `python -c "from mandacaru.db import models, migrations, queries; from mandacaru.collectors import base, openai_collector, gcp_collector, vercel_collector, anthropic_collector, copilot_collector; from mandacaru.vision import ollama_client, prompts; from mandacaru.scheduler import daemon; from mandacaru.reports import renderer"`

**Checkpoint**: All placeholder modules exist, importable, with feature-referencing docstrings

---

## Phase 5: User Story 3 — Test Suite Runs Clean (Priority: P3)

**Goal**: `pytest` discovers `tests/` directory and exits with code 0, zero errors

**Independent Test**: Run `pytest` and confirm exit code 0

### Implementation for User Story 3

- [x] T029 [P] [US3] Create `tests/test_models.py` with docstring `"""Placeholder tests for database models. See F-002."""`
- [x] T030 [P] [US3] Create `tests/test_collectors.py` with docstring `"""Placeholder tests for billing collectors. See F-008+."""`
- [x] T031 [P] [US3] Create `tests/test_reports.py` with docstring `"""Placeholder tests for report rendering. See F-012."""`
- [x] T032 [US3] Run `pytest` and verify it exits with code 0, discovers `tests/` directory, reports zero errors

**Checkpoint**: Test infrastructure works — future features can add real tests immediately

---

## Phase 6: User Story 4 — Configuration Templates Ready (Priority: P4)

**Goal**: `.env.example` and `CLAUDE.md` provide onboarding context for developers and AI assistants

**Independent Test**: Verify both files exist with meaningful content (not empty)

### Implementation for User Story 4

- [x] T033 [P] [US4] Create `.env.example` at repository root with commented placeholder entries for: `OPENAI_API_KEY`, `GOOGLE_APPLICATION_CREDENTIALS`, `GCP_PROJECT_ID`, `VERCEL_TOKEN`, and header comments explaining the file's purpose and that it should be copied to `~/.mandacaru/.env`
- [x] T034 [P] [US4] Create `CLAUDE.md` at repository root with project context: project name (Mandacaru), purpose (AI/dev cost tracker), tech stack (Python 3.11+, Typer, Rich, SQLAlchemy, Playwright, Ollama), package structure overview, development conventions from constitution, Phase 1 scope
- [x] T035 [P] [US4] Create `README.md` at repository root with: project name and description, prerequisites (Python 3.11+), setup instructions (clone, venv, pip install, playwright install), quick-start commands, license (Apache 2.0), brand (MacambaX AI LLC)

**Checkpoint**: All documentation files present with actionable content

---

## Phase 7: User Story 5 — Playwright Browser Available (Priority: P5)

**Goal**: Chromium browser binary installed and available for Playwright automation

**Independent Test**: `playwright install chromium` succeeds; a Playwright launch does not error

### Implementation for User Story 5

- [x] T036 [US5] Run `playwright install chromium` in the active virtual environment and verify the browser binary is downloaded
- [x] T037 [US5] Verify Playwright can launch Chromium: `python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(); b.close(); p.stop(); print('OK')"`

**Checkpoint**: Playwright ready — vision collector features (F-016, F-017) unblocked

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [x] T038 Run quickstart.md validation: execute all commands from `dev/specs/F-001/quickstart.md` end-to-end and verify expected outputs
- [x] T039 Run full import contract validation per `dev/specs/F-001/contracts/cli-entry-point.md`
- [x] T040 Verify `.gitignore` covers all required patterns: `.env`, `*.db`, `__pycache__/`, `.venv/`, `dist/`, `*.egg-info/`, `.playwright/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on T001 (pyproject.toml must exist for package identity)
- **User Story 1 (Phase 3)**: Depends on Phase 2 (package structure must exist for cli.py)
- **User Story 2 (Phase 4)**: Depends on Phase 2 (sub-packages must exist for placeholders)
- **User Story 3 (Phase 5)**: Depends on Phase 2 (tests/ must exist) + Phase 3 (pip install for pytest)
- **User Story 4 (Phase 6)**: Depends on Phase 1 only (just creates root-level files)
- **User Story 5 (Phase 7)**: Depends on Phase 3 (pip install for playwright)
- **Polish (Phase 8)**: Depends on all previous phases

### User Story Dependencies

- **US1 (P1)**: Phase 2 → T010 → T011 → T012
- **US2 (P2)**: Phase 2 → T013–T027 (all parallel) → T028
- **US3 (P3)**: Phase 2 + US1 (pip install) → T029–T031 (parallel) → T032
- **US4 (P4)**: Phase 1 only → T033–T035 (all parallel)
- **US5 (P5)**: US1 (pip install) → T036 → T037

### Parallel Opportunities

- T002 can run parallel with T001 (different files)
- T004–T009 can all run in parallel (independent `__init__.py` files)
- T013–T027 can all run in parallel (independent placeholder files)
- T029–T031 can all run in parallel (independent test files)
- T033–T035 can all run in parallel (independent root-level files)
- US4 can start as soon as Phase 1 completes (no Phase 2 dependency)

---

## Parallel Example: User Story 2

```bash
# All placeholder modules can be created simultaneously:
T013: mandacaru/db/models.py
T014: mandacaru/db/migrations.py
T015: mandacaru/db/queries.py
T016: mandacaru/collectors/base.py
T017: mandacaru/collectors/openai_collector.py
T018: mandacaru/collectors/gcp_collector.py
T019: mandacaru/collectors/vercel_collector.py
T020: mandacaru/collectors/anthropic_collector.py
T021: mandacaru/collectors/copilot_collector.py
T022: mandacaru/vision/ollama_client.py
T023: mandacaru/vision/prompts.py
T024: mandacaru/scheduler/daemon.py
T025: mandacaru/reports/renderer.py
T026: mandacaru/startup.py
T027: mandacaru/config.py
# Then verify all at once:
T028: import validation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T009)
3. Complete Phase 3: User Story 1 (T010–T012)
4. **STOP and VALIDATE**: `mandacaru` command works
5. This alone proves the package is installable and callable

### Incremental Delivery

1. Setup + Foundational → Package structure ready
2. Add US1 → CLI works → MVP!
3. Add US2 → All placeholders exist → Structure complete
4. Add US3 → Tests run clean → Quality gate works
5. Add US4 → Docs ready → Onboarding complete
6. Add US5 → Playwright ready → Vision collectors unblocked
7. Polish → Full contract validation → Feature done
