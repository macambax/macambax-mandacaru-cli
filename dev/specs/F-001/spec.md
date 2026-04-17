# Feature Specification: Project Scaffolding

**Feature Branch**: `001-project-scaffolding`  
**Created**: 2026-04-17  
**Status**: Draft  
**Input**: User description: "F-001: Project Scaffolding — Create the complete project directory structure, pyproject.toml with all dependencies, virtual environment, Playwright browser install, CLAUDE.md for AI context, .env.example credential template, and all __init__.py files so that every subsequent feature has a working Python package to build in."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install and Run the CLI (Priority: P1)

A developer clones the `macambax-mandacaru` repository and wants to get started immediately. They create a virtual environment, run `pip install -e ".[dev]"`, and then type `mandacaru` in their terminal. The CLI responds with a stub message confirming the tool is installed and the entry point works. This proves the package is correctly structured and installable.

**Why this priority**: Without a working installable package and CLI entry point, no other feature can be developed or tested. This is the foundation everything else depends on.

**Independent Test**: Run `pip install -e ".[dev]"` in a fresh virtual environment, then execute `mandacaru` and confirm it produces output without errors.

**Acceptance Scenarios**:

1. **Given** a freshly cloned repository with no virtual environment, **When** the developer creates a venv and runs `pip install -e ".[dev]"`, **Then** the installation completes successfully with zero errors and all dependencies are resolved.
2. **Given** the package is installed in the virtual environment, **When** the developer runs `mandacaru` from the command line, **Then** a Typer-based CLI stub responds with a message (e.g., version or placeholder text) and exits with code 0.
3. **Given** the package is installed, **When** the developer runs `mandacaru --help`, **Then** Typer displays a help message showing the available commands.

---

### User Story 2 - Complete Project Structure for Feature Development (Priority: P2)

A developer who will work on a subsequent feature (e.g., F-002: Database Layer) opens the project and navigates to the `mandacaru/` package. They find all expected sub-packages (`db/`, `collectors/`, `vision/`, `scheduler/`, `reports/`) already created with `__init__.py` files and placeholder modules. Each placeholder contains a docstring referencing which future feature will fill it in, so the developer knows exactly where to write code.

**Why this priority**: The directory structure and placeholder files set clear boundaries for every subsequent feature. Without them, developers would need to create structure ad hoc, leading to inconsistency.

**Independent Test**: After installation, verify every expected directory and file exists, each `__init__.py` is present, and each placeholder module contains a docstring.

**Acceptance Scenarios**:

1. **Given** the project has been scaffolded, **When** a developer lists the `mandacaru/` package contents, **Then** all sub-packages (`db/`, `collectors/`, `vision/`, `scheduler/`, `reports/`) exist with `__init__.py` files.
2. **Given** the project has been scaffolded, **When** a developer opens any placeholder module (e.g., `mandacaru/db/models.py`), **Then** the file contains a docstring referencing the future feature that will implement it (e.g., "Placeholder for F-002: Database Layer").
3. **Given** the project has been scaffolded, **When** the developer inspects `mandacaru/__init__.py`, **Then** it contains `__version__ = "0.1.0"`.

---

### User Story 3 - Test Suite Runs Clean (Priority: P3)

A developer wants to verify the project health by running the test suite. They execute `pytest` and it discovers the `tests/` directory with placeholder test files. All tests pass (or are skipped cleanly) with zero errors, proving that the testing infrastructure is correctly configured.

**Why this priority**: A working test runner is essential for all future features to validate their implementations. It must work from day one.

**Independent Test**: Run `pytest` from the project root and confirm it exits with code 0 and discovers the test directory.

**Acceptance Scenarios**:

1. **Given** the project is installed with dev dependencies, **When** the developer runs `pytest`, **Then** it exits with code 0, discovers the `tests/` directory, and reports no errors.
2. **Given** the `tests/` directory exists, **When** the developer inspects its contents, **Then** placeholder test files exist for collectors, models, and reports.

---

### User Story 4 - Configuration Templates Ready (Priority: P4)

A developer needs to know what credentials and environment variables the project requires. They find `.env.example` in the project root listing all required credential placeholders with comments explaining each one. They copy it to `.env` and fill in their keys.

**Why this priority**: Credential templates prevent developers from guessing what environment variables are needed and reduce onboarding friction.

**Independent Test**: Verify `.env.example` exists and contains documented placeholders for all known credential requirements.

**Acceptance Scenarios**:

1. **Given** the project has been scaffolded, **When** a developer opens `.env.example`, **Then** it contains placeholder entries for all expected credentials (API keys for cloud providers, Ollama configuration) with descriptive comments.
2. **Given** the project has been scaffolded, **When** a developer opens `CLAUDE.md`, **Then** it provides AI-friendly context about the project structure, purpose, and conventions.

---

### User Story 5 - Playwright Browser Available (Priority: P5)

A developer working on future Playwright-based collector features needs the Chromium browser already installed. After running the setup steps, `playwright install chromium` has been executed and the browser binary is available for automation tasks.

**Why this priority**: Playwright browser installation can be slow and is a prerequisite for several collector features. Having it done during scaffolding removes a blocker for those features.

**Independent Test**: After setup, run a Playwright script that launches Chromium and confirm it starts without errors.

**Acceptance Scenarios**:

1. **Given** the virtual environment is active and Playwright is installed, **When** the developer runs `playwright install chromium`, **Then** the Chromium browser binary is downloaded and available.
2. **Given** Chromium is installed, **When** a Playwright script attempts to launch a browser, **Then** it launches successfully without missing-browser errors.

---

### Edge Cases

- What happens when Python version is below 3.11? The `requires-python >= 3.11` constraint in `pyproject.toml` causes `pip install` to fail with a clear version mismatch error.
- What happens when `pip install -e ".[dev]"` is run outside a virtual environment? Installation proceeds but may conflict with system packages. The README should recommend using a virtual environment.
- What happens when Playwright browser install fails due to missing system dependencies? Playwright outputs diagnostic messages indicating which OS-level libraries are needed. The scaffolding documentation should note this as a potential issue on minimal Linux installations.
- What happens when the developer has no internet connection during setup? Dependency installation and Playwright browser download will fail. These steps require network access and the project should document this requirement.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST contain a `mandacaru/` Python package at the repository root with an `__init__.py` that exports `__version__ = "0.1.0"`.
- **FR-002**: The project MUST include a `pyproject.toml` with build system set to `hatchling`, package name `mandacaru`, version `0.1.0`, license `Apache-2.0`, and `requires-python >= 3.11`.
- **FR-003**: The `pyproject.toml` MUST declare these runtime dependencies: `typer[all]>=0.9`, `rich>=13.0`, `sqlalchemy>=2.0`, `httpx>=0.27`, `playwright>=1.40`, `apscheduler>=3.10`, `python-dotenv>=1.0`, `ollama>=0.4`.
- **FR-004**: The `pyproject.toml` MUST declare dev dependencies: `pytest>=8.0`, `pytest-asyncio>=0.23`.
- **FR-005**: The `pyproject.toml` MUST define a CLI entry point `mandacaru = "mandacaru.cli:app"` so that after editable install the `mandacaru` command is available.
- **FR-006**: The `mandacaru/cli.py` file MUST contain a minimal Typer application stub that responds to invocation without errors.
- **FR-007**: The project MUST contain the following sub-packages inside `mandacaru/`, each with an `__init__.py`: `db/`, `collectors/`, `vision/`, `scheduler/`, `reports/`.
- **FR-008**: Each sub-package MUST contain placeholder module files with docstrings referencing the future feature that will implement them (e.g., `models.py` references F-002, `base.py` references F-008).
- **FR-009**: The project MUST include a `tests/` directory with an `__init__.py` and placeholder test files (`test_collectors.py`, `test_models.py`, `test_reports.py`).
- **FR-010**: The project MUST include a `.env.example` file with commented placeholder entries for all credentials the project will need.
- **FR-011**: The project MUST include a `.gitignore` appropriate for Python projects (covering `__pycache__/`, `*.pyc`, `.env`, `*.egg-info/`, `.venv/`, etc.).
- **FR-012**: The project MUST include a `CLAUDE.md` file providing AI-context about the project structure, purpose, conventions, and technology stack.
- **FR-013**: The project MUST include a `README.md` file with setup instructions, project description, and quick-start steps.
- **FR-014**: All placeholder files MUST be valid Python (importable without syntax errors).
- **FR-015**: After `pip install -e ".[dev]"`, running `pytest` MUST exit with code 0 and report zero errors.
- **FR-016**: The project MUST support Playwright browser installation via `playwright install chromium` after the virtual environment is set up.

### Key Entities

- **Python Package (`mandacaru/`)**: The main installable package containing all source code organized into sub-packages by functional area (database, collectors, vision, scheduler, reports).
- **Project Metadata (`pyproject.toml`)**: Central configuration declaring package identity, dependencies, build system, and CLI entry points.
- **Placeholder Modules**: Python files with docstrings only, serving as reserved locations for future feature implementations. Each references the feature ID that will fill it in.
- **Credential Template (`.env.example`)**: A documented list of all environment variables the project will require, with placeholder values and comments.
- **AI Context File (`CLAUDE.md`)**: A markdown document providing project context for AI assistants working on the codebase.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can go from a fresh clone to a working `mandacaru` CLI command in under 5 minutes (clone, create venv, install, run).
- **SC-002**: Running `pip install -e ".[dev]"` resolves and installs all 10 declared dependencies without conflicts or errors.
- **SC-003**: The `mandacaru` command executes and exits with code 0 after editable install.
- **SC-004**: `pytest` discovers the test directory and exits with code 0, reporting zero failures and zero errors.
- **SC-005**: All 5 sub-packages (`db`, `collectors`, `vision`, `scheduler`, `reports`) are importable as `mandacaru.<subpackage>` without errors.
- **SC-006**: Every placeholder module file is importable without syntax errors.
- **SC-007**: `.env.example` contains documented entries for all credential placeholders needed by the project.
- **SC-008**: `CLAUDE.md` and `README.md` are present and contain meaningful project context (not empty or boilerplate-only).

## Assumptions

- The developer has Python 3.11 or later installed on their system.
- The developer has network access for downloading dependencies and Playwright browser binaries.
- The repository root is `macambax-mandacaru/` and the Python package lives directly inside it as `mandacaru/`.
- The developer uses a Unix-like environment (macOS or Linux) or Windows with appropriate tooling for virtual environments.
- Playwright browser installation (`playwright install chromium`) is a one-time setup step and may require OS-level dependencies on some Linux distributions.
- The `mandacaru` CLI stub at this stage only needs to respond to invocation (e.g., print a message or show help); full command implementations come in later features.
- The `.env.example` includes placeholders for known providers (OpenAI, GCP, Anthropic, Vercel) even though their collectors are implemented in later sprints.
- The `CLAUDE.md` content is tailored to the Mandacaru project specifically, not a generic template.
