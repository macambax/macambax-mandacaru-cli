# Quickstart: F-001 Project Scaffolding

## Prerequisites

- Python 3.11+
- pip (bundled with Python)

## Setup

```bash
# Clone the repo
git clone https://github.com/macambax/macambax-mandacaru.git
cd macambax-mandacaru

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install Playwright browsers
playwright install chromium
```

## Verify

```bash
# CLI entry point works
mandacaru
# Expected: ⚡ Mandacaru v0.1.0 — run 'mandacaru --help' for commands

# Help works
mandacaru --help

# Version is importable
python -c "from mandacaru import __version__; print(__version__)"
# Expected: 0.1.0

# All modules importable
python -c "import mandacaru.db.models; import mandacaru.collectors.base; import mandacaru.vision.ollama_client"

# Tests run clean
pytest
# Expected: 0 errors (0 tests collected is fine)
```

## What's Next

- **F-002**: Database Layer — fills in `mandacaru/db/models.py`
- **F-003**: Configuration Management — fills in `mandacaru/config.py`
- **F-004**: CLI Skeleton — adds command groups to `mandacaru/cli.py`
