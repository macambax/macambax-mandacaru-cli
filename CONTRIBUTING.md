# Contributing to Mandacaru

Thanks for your interest in Mandacaru! This project is in **Phase 1 — Local CLI** and is being built by MacambaX AI LLC.

## Status

Phase 1 is not accepting external contributions yet. The community plugin system (custom `BaseCollector` extensions) arrives in **Phase 2 (F-105)**.

## Reporting Issues

Open an issue at <https://github.com/macambax/macambax-mandacaru-cli/issues> with:

- What you tried
- What you expected
- What happened (include `mandacaru doctor` output when relevant)

## Development Setup

See [README.md](README.md) for setup instructions.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium
pytest
```

## Conventions

- Python 3.11+
- All DB access through SQLAlchemy sessions (no raw SQL)
- Collectors extend `BaseCollector` ABC
- Credentials via `~/.mandacaru/.env` — never committed
- Spec Kit SDD: `/specify` → `/plan` → `/tasks` → `/implement`

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
