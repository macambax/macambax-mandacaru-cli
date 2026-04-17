# Research: F-001 Project Scaffolding

**Date**: 2026-04-17  
**Status**: Complete — no NEEDS CLARIFICATION items

## R-001: Build System Choice

**Decision**: Hatchling  
**Rationale**: Hatchling is the default build backend for modern Python projects using `pyproject.toml`. It requires zero configuration beyond the standard `[build-system]` table. The constitution specifies `pipx install mandacaru` as the target UX — Hatchling supports this natively.  
**Alternatives considered**:
- setuptools: More widespread but requires `setup.cfg` or `setup.py` alongside `pyproject.toml`. Unnecessary complexity.
- flit: Simpler than setuptools but less flexible for CLI entry points.
- poetry: Would introduce its own lock file and dependency resolver. Over-engineered for Phase 1.

## R-002: Dependency Version Pinning Strategy

**Decision**: Minimum version constraints in `pyproject.toml` (e.g., `>=0.9`), no upper bounds, no lock file  
**Rationale**: For a CLI tool distributed via pipx, minimum versions ensure compatibility without breaking on new releases. Lock files (`poetry.lock`, `uv.lock`) are for applications with reproducible deployments — not needed for Phase 1 local-only dev. If reproducibility becomes important in Phase 2 (open source), add `uv.lock` then.  
**Alternatives considered**:
- Exact pinning (`==`): Too restrictive for a CLI tool that users install into isolated environments.
- Upper bounds (`<2.0`): Creates unnecessary dependency conflicts. SQLAlchemy 2.x and Typer are stable — no need to cap.

## R-003: Dev Dependencies Location

**Decision**: `[project.optional-dependencies]` under `dev` key in `pyproject.toml`  
**Rationale**: Standard pattern for Hatchling. Install via `pip install -e ".[dev]"`. Keeps test dependencies separate from runtime.  
**Alternatives considered**:
- Hatch environments: Over-engineered for a single-developer project.
- Separate `requirements-dev.txt`: Non-standard when using `pyproject.toml`.

## R-004: Placeholder File Content Pattern

**Decision**: Each placeholder `.py` file contains only a module-level docstring referencing its future feature ID  
**Rationale**: Makes every module importable without errors (satisfying FR-014). Docstrings serve as breadcrumbs for developers navigating the codebase. No dummy code, no `pass` statements, no imports — maximum simplicity per Constitution Principle VII.  
**Alternatives considered**:
- Empty files: Importable but provide no guidance to developers.
- Stub implementations with `raise NotImplementedError`: Adds complexity with no Phase 1 value.

## R-005: CLI Stub Implementation

**Decision**: Minimal Typer app with a `callback(invoke_without_command=True)` that prints a version message  
**Rationale**: Proves the entry point works (`FR-005`, `FR-006`). `invoke_without_command=True` means running `mandacaru` with no args triggers the callback instead of showing help — matching the spec's startup screen behavior (F-007 will replace this).  
**Alternatives considered**:
- Empty app with only `--help`: Less useful for quick validation.
- Full command group stubs: That's F-004's scope — violates Phase-Gated Scope.

## R-006: .gitignore Scope

**Decision**: Standard Python .gitignore + project-specific entries (.env, *.db, Playwright state)  
**Rationale**: GitHub's Python .gitignore template covers `__pycache__/`, `*.pyc`, `.venv/`, `dist/`, `*.egg-info/`. Add `.env` (credentials), `*.db` (SQLite files), and `.playwright/` (browser cache if local).  
**Alternatives considered**:
- Minimal .gitignore: Risks accidentally committing credentials or build artifacts.

## R-007: CLAUDE.md vs Copilot Agent Context

**Decision**: Create `CLAUDE.md` in repo root for general AI context; Spec Kit's `.github/agents/` handles Copilot-specific context  
**Rationale**: The spec calls for `CLAUDE.md` as the AI context file. Spec Kit has already initialized `.github/agents/copilot.md` for Copilot. Both can coexist — `CLAUDE.md` is broader project context, the agent file is Copilot-specific instructions.  
**Alternatives considered**:
- Only Copilot agent file: Wouldn't serve Claude or other AI tools.
- Only CLAUDE.md: Would miss Copilot-specific integration features.
