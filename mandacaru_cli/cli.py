"""Mandacaru — CLI entry point."""

import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo("⚡ Mandacaru v0.1.0 — run 'mandacaru --help' for commands")


if __name__ == "__main__":
    app()
