# CLI Entry Point Contract: F-001

**Date**: 2026-04-17

## Contract

After `pip install -e ".[dev]"`, the `mandacaru` command MUST be available in the shell.

### `mandacaru` (no arguments)

```
$ mandacaru
⚡ Mandacaru v0.1.0 — run 'mandacaru --help' for commands
```

- Exit code: 0
- Output: Version stub message to stdout

### `mandacaru --help`

```
$ mandacaru --help
Usage: mandacaru [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.
```

- Exit code: 0
- Output: Typer-generated help text

### `mandacaru --version` (if Typer supports it)

Not required for F-001. Typer does not add `--version` by default — this is F-004 scope.

## Import Contract

All modules must be importable without errors:

```python
import mandacaru
assert mandacaru.__version__ == "0.1.0"

from mandacaru import cli
from mandacaru.db import models, migrations, queries
from mandacaru.collectors import base, openai_collector, gcp_collector
from mandacaru.collectors import vercel_collector, anthropic_collector, copilot_collector
from mandacaru.vision import ollama_client, prompts
from mandacaru.scheduler import daemon
from mandacaru.reports import renderer
```

All imports succeed with no `ImportError` or `SyntaxError`.
