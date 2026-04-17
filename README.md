# ⚡ Mandacaru

> Local-first CLI agent that tracks every dollar a developer spends across their entire dev stack.

**By MacambaX AI LLC** | Apache 2.0

---

## What It Does

Mandacaru collects billing data from your AI and cloud providers — OpenAI, GCP, Vercel, Anthropic, GitHub Copilot — and gives you a single CLI dashboard showing where your money goes. Runs entirely on your machine. No cloud. No data leaves your laptop.

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai) with `llama3.2-vision` model (for Playwright-based collectors)

## Quick Start

```bash
# Clone
git clone https://github.com/macambax/macambax-mandacaru.git
cd macambax-mandacaru

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Install browser for Playwright collectors
playwright install chromium

# Verify
mandacaru
```

## Development

```bash
# Run tests
pytest

# Lint (when configured)
ruff check .
```

## Project Status

**Phase 1 — Local CLI** (in progress)

- 5 billing providers
- SQLite database at `~/.mandacaru/mandacaru.db`
- CLI commands: init, sync, report, budget, daemon

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
