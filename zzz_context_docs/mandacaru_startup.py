import sys

# pip install rich
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich import print as rprint
import time

console = Console()

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#A78BFA"
GREEN = "#4ADE80"
ORANGE = "#E88E36"
TEAL = "#2ABFA3"
MUTED = "#6B7280"
WHITE = "#F9FAFB"

MANDACARU = r"""
                                 [#7C3AED]║[/#7C3AED]
                                 [#7C3AED]║[/#7C3AED]
              [#7C3AED]╔══════╗[/#7C3AED]          [#7C3AED]║[/#7C3AED]          [#7C3AED]╔══════╗[/#7C3AED]
              [#7C3AED]║[/#7C3AED]      [#7C3AED]║[/#7C3AED]          [#7C3AED]║[/#7C3AED]          [#7C3AED]║[/#7C3AED]      [#7C3AED]║[/#7C3AED]
    [#A78BFA]╔═══╗[/#A78BFA]     [#7C3AED]║[/#7C3AED]      [#7C3AED]╚══╦═══╗[/#7C3AED]   [#7C3AED]╔═══╦══╝[/#7C3AED]      [#7C3AED]║[/#7C3AED]     [#A78BFA]╔═══╗[/#A78BFA]
    [#A78BFA]║[/#A78BFA]   [#A78BFA]║[/#A78BFA]     [#7C3AED]╚══════╗[/#7C3AED]     [#7C3AED]║[/#7C3AED]   [#7C3AED]║[/#7C3AED]   [#7C3AED]╔═════╝[/#7C3AED]     [#A78BFA]║[/#A78BFA]   [#A78BFA]║[/#A78BFA]
    [#A78BFA]║[/#A78BFA]   [#A78BFA]╚═════════╗[/#A78BFA]      [#7C3AED]║[/#7C3AED]   [#7C3AED]║[/#7C3AED]      [#7C3AED]╔═════════╝[/#7C3AED]   [#A78BFA]║[/#A78BFA]
    [#A78BFA]╚════════════╬══════╝[/#A78BFA]   [#7C3AED]║[/#7C3AED]   [#7C3AED]╚══════╗[/#7C3AED]   [#A78BFA]╚════════════╝[/#A78BFA]
                 [#A78BFA]║[/#A78BFA]          [#7C3AED]║[/#7C3AED]          [#A78BFA]║[/#A78BFA]
                 [#A78BFA]╚══════════╗[/#A78BFA]   [#7C3AED]║[/#7C3AED]   [#7C3AED]╔══════════╝[/#7C3AED]
                           [#7C3AED]║[/#7C3AED]   [#7C3AED]║[/#7C3AED]   [#7C3AED]║[/#7C3AED]
                           [#7C3AED]╚═══╬═══╝[/#7C3AED]
                               [#7C3AED]║[/#7C3AED]
                               [#7C3AED]║[/#7C3AED]
                   [#4ADE80]╔══╗[/#4ADE80]        [#7C3AED]║[/#7C3AED]        [#4ADE80]╔══╗[/#4ADE80]
                   [#4ADE80]║[/#4ADE80]  [#4ADE80]╚════════╬════════╝[/#4ADE80]  [#4ADE80]║[/#4ADE80]
                   [#4ADE80]╚═══════════╬═══════════╝[/#4ADE80]
                               [#7C3AED]║[/#7C3AED]
                               [#7C3AED]║[/#7C3AED]
                               [#7C3AED]║[/#7C3AED]
                    [#2ABFA3]▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[/#2ABFA3]
                    [#2ABFA3]▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[/#2ABFA3]
"""

MANDACARU_SIMPLE = """
[#7C3AED]                    │[/#7C3AED]
[#7C3AED]         ┌──────┐   │   ┌──────┐[/#7C3AED]
[#7C3AED]         │      │   │   │      │[/#7C3AED]
[#A78BFA]  ┌───┐  │      └───┼───┘      │  ┌───┐[/#A78BFA]
[#A78BFA]  │   └──┘          │          └──┘   │[/#A78BFA]
[#A78BFA]  └────────────┐    │    ┌────────────┘[/#A78BFA]
[#7C3AED]               └────┼────┘[/#7C3AED]
[#7C3AED]                    │[/#7C3AED]
[#7C3AED]                    │[/#7C3AED]
[#4ADE80]        ┌───────────┴───────────┐[/#4ADE80]
[#4ADE80]        └───────────────────────┘[/#4ADE80]
[#7C3AED]                    │[/#7C3AED]
[#7C3AED]                    │[/#7C3AED]
[#2ABFA3]          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓[/#2ABFA3]
"""

def render_startup():
    console.clear()

    # ── cactus ───────────────────────────────────────────────────────────────
    console.print()
    console.print(Align.center(MANDACARU_SIMPLE))

    # ── logo ─────────────────────────────────────────────────────────────────
    logo = Text()
    logo.append("  ⚡ MANDACARÚ  ", style=f"bold {PURPLE}")
    logo.append("by ", style=f"dim {MUTED}")
    logo.append("MacambaX AI", style=f"bold {TEAL}")
    console.print(Align.center(logo))
    console.print()

    # ── tagline ───────────────────────────────────────────────────────────────
    tagline = Text(
        "Every dollar your dev stack costs. One place. Runs on your machine.",
        style=f"italic {MUTED}"
    )
    console.print(Align.center(tagline))
    console.print()

    # ── version + status bar ─────────────────────────────────────────────────
    version_text = Text()
    version_text.append(" v0.1.0 ", style=f"bold {PURPLE}")
    version_text.append("│", style=f"dim {MUTED}")
    version_text.append(" Phase 1 — Local CLI ", style=f"{MUTED}")
    version_text.append("│", style=f"dim {MUTED}")
    version_text.append(" 100% Free ", style=f"bold {GREEN}")
    version_text.append("│", style=f"dim {MUTED}")
    version_text.append(" Powered by Ollama ", style=f"{LIGHT_PURPLE}")
    console.print(Align.center(version_text))
    console.print()

    # ── divider ───────────────────────────────────────────────────────────────
    console.print(Align.center(Text("─" * 58, style=f"dim {PURPLE}")))
    console.print()

    # ── quick commands ────────────────────────────────────────────────────────
    commands = [
        ("mandacaru init", "First time setup"),
        ("mandacaru sync", "Pull costs from all providers"),
        ("mandacaru report", "Show current month dashboard"),
        ("mandacaru budget set", "Set monthly spending limits"),
        ("mandacaru daemon start", "Auto-sync every morning at 7am"),
    ]

    cmd_text = Text()
    for cmd, desc in commands:
        cmd_text.append(f"  {cmd:<28}", style=f"bold {LIGHT_PURPLE}")
        cmd_text.append(f"{desc}\n", style=f"{MUTED}")

    console.print(Align.center(cmd_text))

    # ── divider ───────────────────────────────────────────────────────────────
    console.print(Align.center(Text("─" * 58, style=f"dim {PURPLE}")))
    console.print()

    # ── footer ────────────────────────────────────────────────────────────────
    footer = Text()
    footer.append("github.com/macambax/mandacaru", style=f"dim {TEAL}")
    footer.append("  •  ", style=f"dim {MUTED}")
    footer.append("macambax.ai", style=f"dim {ORANGE}")
    console.print(Align.center(footer))
    console.print()

def render_startup_panel():
    """Alternative: wrapped in a panel."""
    console.clear()
    console.print()

    content = Text()

    # cactus lines
    cactus_lines = [
        ("                    │                    ", PURPLE),
        ("         ┌──────┐   │   ┌──────┐         ", PURPLE),
        ("         │      │   │   │      │         ", PURPLE),
        ("  ┌───┐  │      └───┼───┘      │  ┌───┐  ", LIGHT_PURPLE),
        ("  │   └──┘          │          └──┘   │  ", LIGHT_PURPLE),
        ("  └────────────┐    │    ┌────────────┘  ", LIGHT_PURPLE),
        ("               └────┼────┘               ", PURPLE),
        ("                    │                    ", PURPLE),
        ("       ┌────────────┴────────────┐       ", GREEN),
        ("       └─────────────────────────┘       ", GREEN),
        ("                    │                    ", PURPLE),
        ("         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           ", TEAL),
    ]

    for line, color in cactus_lines:
        content.append(line + "\n", style=color)

    content.append("\n")
    content.append("        ⚡ MANDACARÚ  ", style=f"bold {PURPLE}")
    content.append("by MacambaX AI\n", style=f"bold {TEAL}")
    content.append("\n")
    content.append(
        "  Every dollar your dev stack costs.\n"
        "  One place. Runs on your machine.\n",
        style=f"italic {MUTED}"
    )
    content.append("\n")
    content.append("  mandacaru init", style=f"bold {LIGHT_PURPLE}")
    content.append("          First time setup\n", style=MUTED)
    content.append("  mandacaru sync", style=f"bold {LIGHT_PURPLE}")
    content.append("          Pull costs from all providers\n", style=MUTED)
    content.append("  mandacaru report", style=f"bold {LIGHT_PURPLE}")
    content.append("        Show current month\n", style=MUTED)
    content.append("  mandacaru daemon start", style=f"bold {LIGHT_PURPLE}")
    content.append("   Auto-sync at 7am daily\n", style=MUTED)
    content.append("\n")
    content.append("  github.com/macambax/mandacaru", style=f"dim {TEAL}")
    content.append("  •  ", style=f"dim {MUTED}")
    content.append("v0.1.0", style=f"dim {PURPLE}")

    panel = Panel(
        content,
        border_style=PURPLE,
        padding=(1, 3),
        width=60,
    )

    console.print(Align.center(panel))
    console.print()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "panel"
    if mode == "simple":
        render_startup()
    else:
        render_startup_panel()
