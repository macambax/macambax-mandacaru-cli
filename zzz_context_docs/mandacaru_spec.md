# Mandacarú — Complete Product Specification
**MacambaX AI LLC · April 2026 · Confidential**

---

## Table of Contents

1. [Product Overview](#1-product-overview)
2. [Brand & Identity](#2-brand--identity)
3. [The Problem](#3-the-problem)
4. [Competitive Landscape](#4-competitive-landscape)
5. [Architecture Overview](#5-architecture-overview)
6. [Tech Stack](#6-tech-stack)
7. [Database Schema](#7-database-schema)
8. [CLI Commands](#8-cli-commands)
9. [Providers](#9-providers)
10. [Phase 1 — Local CLI (Build Now)](#10-phase-1--local-cli-build-now)
11. [Phase 2 — Open Source Release](#11-phase-2--open-source-release)
12. [Phase 3 — SaaS Cloud](#12-phase-3--saas-cloud)
13. [Monetization](#13-monetization)
14. [Project Structure](#14-project-structure)
15. [Development Methodology — BMAD vs Spec Kit](#15-development-methodology--bmad-vs-spec-kit)
16. [Getting Started — Phase 1 Build Checklist](#16-getting-started--phase-1-build-checklist)

---

## 1. Product Overview

**Mandacarú** is a local-first CLI agent that tracks every dollar a developer spends across their entire dev stack — AI providers, cloud infrastructure, SaaS subscriptions — in one place, running entirely on their own machine.

Named after the *mandacaru* cactus (*Cereus jamacaru*) — the iconic cactus of Brazil's Caatinga biome that survives and thrives with minimal resources. The metaphor: Mandacarú helps developers survive the AI spend explosion by making every dollar visible.

### North Star Statement
> *Every dollar your dev stack costs. One place. Runs on your machine.*

### The Core Insight
Most developers running AI-powered workflows in 2026 juggle 4-8 billing dashboards across Claude Pro, GitHub Copilot, OpenAI API, GCP, Vercel, and more. There is no unified view. Bills surprise you at month-end. There is no lightweight, local-first, privacy-preserving tool for the solo developer or small AI team.

### Why It's Different
- **No proxy model** — does not intercept your API calls. Reads billing pages directly.
- **No cloud dependency** — runs entirely on your Mac Mini / Linux box.
- **No API keys required for Phase 1** — Ollama handles vision extraction locally.
- **Open source core** — developers can audit exactly what it does with their credentials.
- **Tracks itself** — Mandacarú logs the cost of the Ollama calls it makes to run. Transparent by design.

---

## 2. Brand & Identity

| Attribute | Value |
|-----------|-------|
| **Product name** | Mandacarú |
| **Accent** | Mandacarú (ú always accented) |
| **Parent brand** | MacambaX AI LLC |
| **Color** | Purple `#7C3AED` |
| **Secondary** | Teal `#2ABFA3` (MacambaX brand) |
| **Accent** | Orange `#E88E36` (MacambaX accent) |
| **GitHub org** | github.com/macambax |
| **Repo** | github.com/macambax/mandacaru |
| **Domain** | mandacaru.macambax.ai (Phase 1) / mandacaru.ai (Phase 3 TBD) |
| **License** | Apache 2.0 |
| **CLI command** | `mandacaru` |
| **Icon** | ⚡ (lightning bolt — energy cost metaphor) |

### MacambaX Product Family
- **Cajú** `#E88E36` — SaaS for independent fitness instructors
- **Mandacarú** `#7C3AED` — Dev stack cost tracker (this product)
- **Umbú** — Reserved for future product (marketplace)

---

## 3. The Problem

### For Solo Developers and Small AI Teams
- Running 4-8 AI/cloud billing dashboards simultaneously
- No aggregate view of total monthly AI spend
- Anthropic and GitHub Copilot have **no billing API** — costs only visible in the browser
- Usage-based pricing (tokens, requests, GPU minutes) creates unpredictable bills
- No alerting when approaching budget limits
- Carbon footprint of AI workloads invisible

### The Market Reality (2026)
- 78% of IT leaders report unexpected charges from AI consumption-based pricing
- Average developer using AI tools spends $80-200/month across providers
- All existing tools are either enterprise-grade ($500+/month) or require routing API calls through a third-party proxy
- **The gap:** No lightweight, local-first, privacy-preserving cost tracker for solo developers

---

## 4. Competitive Landscape

| Tool | Approach | Target | Price | Gap |
|------|----------|--------|-------|-----|
| **Helicone** | API proxy | Developers | Free-$25/mo | Requires routing calls through their servers |
| **Langfuse** | Self-hosted observability | Engineering teams | Free (self-host) | Complex setup, engineering-heavy |
| **CloudZero** | Enterprise FinOps | Enterprises | % of spend | $100K+ cloud spend minimum |
| **Vantage** | Multi-cloud cost mgmt | Teams | 1% of spend | Not AI-specific, overkill for solo |
| **Datadog LLM** | Observability platform | Enterprise | $$$$ | Enterprise only |
| **Flexprice** | Usage metering + billing | AI startups | Custom | B2B metering, not personal cost tracking |

### Mandacarú's Positioning
- **Lighter than Langfuse** — no complex self-hosted stack
- **More private than Helicone** — no proxy, no API call interception
- **Cheaper than CloudZero** — free for Phase 1 and 2
- **More honest than all of them** — open source, auditable

---

## 5. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MANDACARÚ CLI AGENT                       │
│                   (runs on Mac Mini)                         │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    COLLECTOR LAYER                           │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ API          │  │ Playwright  │  │ Manual Entry        │  │
│  │ Collectors   │  │ Collectors  │  │ (flat subscriptions)│  │
│  │             │  │             │  │                     │  │
│  │ • OpenAI    │  │ • Anthropic │  │ • Cursor            │  │
│  │ • GCP       │  │   Console   │  │ • Windsurf          │  │
│  │ • Vercel    │  │ • GitHub    │  │ • Notion            │  │
│  │ • Mistral   │  │   Copilot   │  │ • Linear            │  │
│  │ • Groq      │  │             │  │ • Figma             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                    │              │
│         │         ┌──────▼──────┐             │              │
│         │         │   OLLAMA    │             │              │
│         │         │ llama3.2-   │             │              │
│         │         │ vision      │             │              │
│         │         │ (local,free)│             │              │
│         │         └──────┬──────┘             │              │
│         │                │                    │              │
└─────────┼────────────────┼────────────────────┼──────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                             │
│              SQLite (~/.mandacaru/mandacaru.db)              │
│                                                              │
│  providers │ invoices │ daily_usage │ sync_log              │
│  budgets   │ budget_alerts          │ settings              │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLI INTERFACE                             │
│                  (Typer + Rich)                             │
│                                                              │
│  mandacaru init  │  sync  │  report  │  budget  │  daemon   │
└─────────────────────────────────────────────────────────────┘
```

### Agent Loop (Daily Sync)
```
APScheduler triggers at 07:00 daily
  │
  ├── For each active API provider:
  │     → Call billing API directly
  │     → Parse JSON response
  │     → Upsert into daily_usage
  │     → Write sync_log entry
  │
  ├── For each Playwright provider:
  │     → Launch headless browser
  │     → Navigate to billing URL
  │     → Capture screenshot
  │     → Send to Ollama llama3.2-vision
  │     → Extract structured JSON cost data
  │     → Upsert into invoices or daily_usage
  │     → Write sync_log entry
  │
  └── Run budget_check
        → Compare current spend vs budgets
        → Fire alerts if thresholds exceeded
        → Write budget_alerts entries
```

---

## 6. Tech Stack

### Phase 1 — Local CLI

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| **Language** | Python | 3.11+ | Deep familiarity from Cajú |
| **CLI framework** | Typer | latest | Built on Click, beautiful by default |
| **Terminal UI** | Rich | latest | Tables, colors, panels, progress bars |
| **Browser automation** | Playwright | latest | Already explored for Cajú testing |
| **Vision/LLM** | Ollama | latest | Free, local, no API key required |
| **Vision model** | llama3.2-vision | latest | Best local vision model for structured extraction |
| **ORM** | SQLAlchemy | 2.x | Same as Cajú; SQLite → PostgreSQL with one line change |
| **Database** | SQLite | 3.x | Zero setup, single file, ships with Python |
| **Scheduler** | APScheduler | 3.x | Background daemon mode |
| **Config** | python-dotenv | latest | .env file for credentials |
| **HTTP client** | httpx | latest | Async-ready, modern |
| **Package install** | pipx | latest | Isolated install, `pipx install mandacaru` |

### Phase 3 Additions

| Layer | Technology | Why |
|-------|-----------|-----|
| **Database** | PostgreSQL 17 | Multi-user, production-grade |
| **Auth** | Supabase | Google OAuth, free tier |
| **Frontend** | Vite + React + Recharts | Dashboard UI |
| **Payments** | Stripe | Freemium subscription management |
| **Infrastructure** | GCP Cloud Run | Already deployed for Cajú/MacambaX |
| **Secrets** | GCP Secret Manager | Encrypted provider credentials |

### LLM Configuration (Configurable)

```toml
# ~/.mandacaru/config.toml

[llm]
provider = "ollama"              # Phase 1 default — free, local
model = "llama3.2-vision"
base_url = "http://localhost:11434"

# Optional Phase 2 upgrade for better accuracy:
# provider = "anthropic"
# model = "claude-haiku-4-5"
# api_key_env = "ANTHROPIC_API_KEY"

# Alternative:
# provider = "openai"
# model = "gpt-4o-mini"
# api_key_env = "OPENAI_API_KEY"
```

---

## 7. Database Schema

### Tables

#### `providers`
Registry of all billing providers.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| slug | TEXT UNIQUE | e.g. `openai_api`, `anthropic_pro` |
| name | TEXT | e.g. `OpenAI API` |
| billing_model | TEXT | `subscription` \| `usage` \| `infra` |
| collection_method | TEXT | `api` \| `playwright` |
| website_url | TEXT | Billing page URL for Playwright |
| api_docs_url | TEXT | Billing API documentation |
| is_active | INTEGER | 0=disabled, 1=enabled |
| notes | TEXT | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

#### `invoices`
Subscription billing cycles — one row per provider per billing period.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| provider_id | FK → providers | |
| billing_period | TEXT | `YYYY-MM` format e.g. `2026-04` |
| amount_usd | REAL | |
| currency | TEXT | Default `USD` |
| invoice_date | DATE | Actual charge date |
| invoice_ref | TEXT | Provider's invoice ID |
| payment_method | TEXT | e.g. `Mercury Visa` |
| notes | TEXT | |
| created_at | TIMESTAMP | |
| **UNIQUE** | (provider_id, billing_period) | |

#### `daily_usage`
Usage-based costs per provider + model + day.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| provider_id | FK → providers | |
| usage_date | DATE | |
| model_name | TEXT | e.g. `gpt-4o`, `default` |
| input_tokens | INTEGER | Nullable for non-LLM providers |
| output_tokens | INTEGER | Nullable |
| total_tokens | INTEGER | Nullable |
| requests_count | INTEGER | API call count |
| compute_units | REAL | For GPU/infra providers |
| cost_usd | REAL | |
| raw_response | TEXT | Full JSON blob from API — never discard |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |
| **UNIQUE** | (provider_id, usage_date, model_name) | Upsert key |

#### `sync_log`
Audit trail for every sync attempt. Critical for debugging silent Playwright failures.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| provider_id | FK → providers | |
| synced_at | TIMESTAMP | |
| status | TEXT | `success` \| `failed` \| `partial` |
| records_fetched | INTEGER | |
| error_message | TEXT | Nullable on success |
| duration_ms | INTEGER | Sync duration |
| collection_method | TEXT | `api` \| `playwright` |
| notes | TEXT | |

#### `budgets`
Spending limits. `provider_id = NULL` means overall budget.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| provider_id | FK → providers | NULL = overall budget |
| label | TEXT | e.g. `Monthly AI Budget` |
| period_type | TEXT | `monthly` \| `weekly` |
| amount_usd | REAL | |
| alert_threshold | REAL | 0.0–1.0, e.g. `0.80` = alert at 80% |
| is_active | INTEGER | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |
| **UNIQUE** | (provider_id, period_type) | |

#### `budget_alerts`
History of every alert fired.

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| budget_id | FK → budgets | |
| fired_at | TIMESTAMP | |
| billing_period | TEXT | `YYYY-MM` |
| spend_at_alert | REAL | Spend when alert fired |
| budget_amount | REAL | Budget at time of firing |
| pct_used | REAL | e.g. `0.83` |
| acknowledged | INTEGER | 0=unseen, 1=seen |
| acknowledged_at | TIMESTAMP | |

#### `settings`
Key-value config store.

| Column | Type | Notes |
|--------|------|-------|
| key | TEXT PK | |
| value | TEXT | |
| description | TEXT | |
| updated_at | TIMESTAMP | |

### Default Settings
| Key | Default Value |
|-----|--------------|
| ollama_base_url | http://localhost:11434 |
| ollama_model | llama3.2-vision |
| llm_provider | ollama |
| sync_hour | 7 |
| currency | USD |
| db_version | 1 |
| phase | 1 |

### Key Design Decisions
- **raw_response on daily_usage** — always store full API JSON. Zero cost in SQLite. Enables future mining without re-syncing.
- **sync_log** — without this, silent Playwright failures are invisible.
- **provider_id NULL in budgets** — elegantly handles both per-provider and overall limits in one table.
- **UNIQUE constraint on daily_usage** — enables safe upsert: re-running sync never duplicates data.
- **Phase 3 migration** — add `user_id` FK to every table + `users` table. SQLAlchemy handles SQLite → PostgreSQL with one line change.

---

## 8. CLI Commands

### Full Command Reference

```bash
# ── Setup ────────────────────────────────────────────────────
mandacaru
# Shows startup screen with ASCII mandacaru cactus + command list

mandacaru init
# First-time setup wizard:
#   - Checks prerequisites (Python, Ollama, llama3.2-vision)
#   - Creates ~/.mandacaru/ directory
#   - Initializes SQLite database
#   - Seeds default providers and settings
#   - Guides credential setup

mandacaru doctor
# Re-runs prerequisite checks at any time
#   ✅ Python 3.11.4
#   ✅ Ollama running on localhost:11434
#   ✅ llama3.2-vision model found
#   ✅ SQLite database at ~/.mandacaru/mandacaru.db

# ── Providers ────────────────────────────────────────────────
mandacaru providers list
# Lists all providers with status (active/inactive, last sync, collection method)

mandacaru providers enable <slug>
# Activates a provider e.g. `mandacaru providers enable groq`

mandacaru providers disable <slug>
# Deactivates a provider

mandacaru providers add
# Interactive wizard to add a custom provider

# ── Sync ─────────────────────────────────────────────────────
mandacaru sync
# Syncs all active providers
# Shows progress bar per provider
# Reports success/failure per provider
# Runs budget check after sync

mandacaru sync --provider openai_api
# Sync a single provider

mandacaru sync --dry-run
# Shows what would be synced without writing to DB

# ── Report ───────────────────────────────────────────────────
mandacaru report
# Current month summary dashboard
# Shows: cost per provider, total, budget status, trend

mandacaru report --month 2026-03
# Report for a specific month

mandacaru report --daily
# Day-by-day breakdown for current month

mandacaru report --provider openai_api
# Provider-specific detail report

mandacaru report --model
# Breakdown by model within each provider

mandacaru report --export csv
# Export current month to ~/.mandacaru/exports/

mandacaru report --export json
# Export as JSON

# ── Budget ───────────────────────────────────────────────────
mandacaru budget set --overall 150
# Set overall monthly budget to $150

mandacaru budget set --provider openai_api 50
# Set per-provider budget

mandacaru budget set --threshold 0.80
# Set alert threshold (default 80%)

mandacaru budget list
# Show all budgets and current usage

mandacaru budget check
# Manual budget check — show status of all budgets

mandacaru budget alerts
# Show unacknowledged alerts

mandacaru budget alerts --ack-all
# Mark all alerts as acknowledged

# ── Daemon ───────────────────────────────────────────────────
mandacaru daemon start
# Start background daemon — syncs daily at configured hour

mandacaru daemon stop
# Stop background daemon

mandacaru daemon status
# Show daemon status, last run, next run

mandacaru daemon logs
# Show recent daemon activity

# ── Config ───────────────────────────────────────────────────
mandacaru config show
# Show current configuration

mandacaru config set sync_hour 6
# Change any setting

mandacaru config set ollama_model llama3.2-vision
# Change vision model

mandacaru config set llm_provider anthropic
# Switch from Ollama to Anthropic API (Phase 2)

# ── Utility ──────────────────────────────────────────────────
mandacaru version
# Show version info

mandacaru logs
# Show recent sync_log entries

mandacaru reset
# ⚠️ Drops and recreates database (with confirmation prompt)
```

### Sample `mandacaru report` Output

```
╔════════════════════════════════════════════════════════╗
║     ⚡ MANDACARÚ  •  April 2026                         ║
╠════════════════════════════════════════════════════════╣
║  PROVIDER              COST      BUDGET   STATUS       ║
╠════════════════════════════════════════════════════════╣
║  Claude Pro           $20.00      —       subscription ║
║  GitHub Copilot       $39.00      —       subscription ║
║  GCP / Vertex          $7.43    $20.00   ████░░  37%   ║
║  OpenAI API           $14.20    $50.00   ███░░░  28%   ║
║  Vercel                $2.10      —       infra        ║
╠════════════════════════════════════════════════════════╣
║  TOTAL                $82.73   $150.00  █████░░  55%   ║
║  Days remaining           14                           ║
║  Projected month-end $118.19   ✅  on track             ║
╚════════════════════════════════════════════════════════╝
  Last synced: today 07:00 · All providers healthy
```

---

## 9. Providers

### Phase 1 — Your Personal Stack (Active by Default)

| Slug | Name | Billing Model | Method | Notes |
|------|------|--------------|--------|-------|
| `anthropic_pro` | Claude Pro | subscription | playwright | $20/mo flat. Ollama vision required. |
| `github_copilot` | GitHub Copilot Pro Max | subscription | playwright | $39/mo. 1500 premium req/month. |
| `openai_api` | OpenAI API | usage | api | Direct Usage API. No vision needed. |
| `gcp` | GCP / Vertex AI | infra | api | GCP Billing API. Project: macambax-website-dev |
| `vercel` | Vercel | infra | api | Frontend hosting. REST API available. |

### Phase 2 — Community Providers (Seeded Inactive)

| Slug | Name | Billing Model | Method |
|------|------|--------------|--------|
| `mistral` | Mistral AI | usage | api |
| `groq` | Groq | usage | api |
| `cohere` | Cohere | usage | api |
| `huggingface` | Hugging Face | usage | api |
| `replicate` | Replicate | usage | api |
| `elevenlabs` | ElevenLabs | usage | api |
| `supabase` | Supabase | infra | api |
| `cloudflare` | Cloudflare Workers | infra | api |
| `pinecone` | Pinecone | infra | api |
| `github_actions` | GitHub Actions | infra | api |

### Phase 2 — Manual Entry Subscriptions (Flat Fee Tools)

| Name | Typical Cost |
|------|-------------|
| Cursor Pro | $20/mo |
| Windsurf Pro | $15/mo |
| ChatGPT Plus | $20/mo |
| Linear | $8-16/seat |
| Notion | $8-16/seat |
| Figma | $12-45/seat |
| Slack | $7-12/seat |
| Zoom | $15/seat |
| 1Password | $3-8/seat |

### Collection Methods

#### Direct API (No Ollama Required)
- OpenAI: `GET https://api.openai.com/v1/usage`
- GCP: Cloud Billing API REST
- Vercel: `GET https://api.vercel.com/v2/projects`
- Mistral, Groq, Cohere: provider-specific billing APIs

#### Playwright + Ollama Vision (Local Screenshot Extraction)
```python
# Pseudocode for playwright collectors

async def collect_anthropic():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Load stored session cookies
        await page.context.add_cookies(load_cookies("anthropic"))
        await page.goto("https://console.anthropic.com/settings/billing")
        await page.wait_for_load_state("networkidle")
        screenshot = await page.screenshot()
        
        # Send to Ollama
        result = ollama.chat(
            model="llama3.2-vision",
            messages=[{
                "role": "user",
                "content": """Extract billing data from this screenshot.
                              Return ONLY valid JSON:
                              {
                                "billing_period": "YYYY-MM",
                                "amount_usd": 0.00,
                                "invoice_date": "YYYY-MM-DD",
                                "invoice_ref": "string or null"
                              }""",
                "images": [screenshot]
            }]
        )
        return json.loads(result["message"]["content"])
```

---

## 10. Phase 1 — Local CLI (Build Now)

### Goal
A working CLI agent running on your Mac Mini that shows what you spend on AI tools each month without opening five browser tabs.

### Scope
- 5 providers: Claude Pro, GitHub Copilot, OpenAI API, GCP, Vercel
- CLI commands: `init`, `sync`, `report`, `budget set/check`, `daemon start/stop`
- Ollama + llama3.2-vision for Playwright providers
- SQLite storage
- No auth, no cloud, no multi-user

### Prerequisites for Users
```bash
# 1. Install Ollama
brew install ollama          # macOS
# or: curl -fsSL https://ollama.ai/install.sh | sh  # Linux

# 2. Pull vision model (~5GB download, one-time)
ollama pull llama3.2-vision

# 3. Start Ollama service
ollama serve

# 4. Install Mandacarú
pipx install mandacaru

# 5. Initialize
mandacaru init
```

### Credentials Setup (Phase 1)
Credentials live in `~/.mandacaru/.env` — never committed to Git.

```bash
# ~/.mandacaru/.env

# OpenAI — Usage API key (read-only billing access)
OPENAI_API_KEY=sk-...

# GCP — Service account JSON path (billing.viewer role only)
GOOGLE_APPLICATION_CREDENTIALS=~/.mandacaru/gcp-billing-sa.json
GCP_PROJECT_ID=macambax-website-dev

# Vercel — Read-only token
VERCEL_TOKEN=...

# Anthropic Console — stored session cookies (managed by mandacaru init)
# GitHub — stored session cookies (managed by mandacaru init)
```

### Phase 1 Features — Detailed

#### `mandacaru init`
1. Check Python version ≥ 3.11
2. Check Ollama running at `localhost:11434`
3. Check `llama3.2-vision` model available
4. Create `~/.mandacaru/` directory
5. Create `~/.mandacaru/mandacaru.db` (SQLite)
6. Run schema migrations
7. Seed default providers
8. Seed default settings
9. Interactive credential setup wizard
10. Run first sync

#### `mandacaru sync`
1. Load active providers from DB
2. For API providers: call billing API, parse response, upsert `daily_usage`
3. For Playwright providers: screenshot → Ollama vision → parse JSON → upsert `invoices`
4. Write `sync_log` entry for each provider (success or failure)
5. Run budget check
6. Show summary: X providers synced, Y failed

#### `mandacaru report`
1. Query `monthly_spend` view for current month
2. Query `budgets` for active limits
3. Calculate projected month-end spend
4. Render Rich table with colors:
   - Green: under 60% of budget
   - Yellow: 60-80% of budget
   - Red: over 80% of budget
5. Show unacknowledged alerts if any

#### Budget Alerts
- Triggered automatically after every sync
- Threshold default: 80% of budget
- Terminal: Rich panel with warning color
- Phase 3: email + Slack

#### Daemon Mode
- APScheduler background process
- Default: daily at 07:00
- Configurable via `mandacaru config set sync_hour 6`
- Writes PID to `~/.mandacaru/daemon.pid`

### Phase 1 Non-Goals
- No web UI
- No auth
- No cloud
- No Stripe
- No multi-user
- No email/Slack alerts
- No export
- No optimization recommendations

---

## 11. Phase 2 — Open Source Release

### Goal
Public GitHub release. Community adoption. More providers. Better accuracy. MCP integration.

### New Features

#### Optional Cloud LLM
```toml
# Switch from Ollama to cloud LLM for better accuracy
[llm]
provider = "anthropic"
model = "claude-haiku-4-5"
api_key_env = "ANTHROPIC_API_KEY"
```

#### More Providers (20+)
Mistral, Groq, Cohere, Hugging Face, Perplexity, Together AI, Replicate, ElevenLabs, xAI, Supabase, Cloudflare Workers, MongoDB Atlas, Pinecone, Twilio, SendGrid, GitHub Actions

#### Subscription Tracker
Manual entry for flat-fee tools with no billing API (Cursor, Windsurf, Notion, Linear, Figma, Slack)

#### Export
```bash
mandacaru report --export csv
mandacaru report --export json
```

#### Cost Optimization Tips
AI-generated suggestions: "Switch this workload from gpt-4o to gpt-4o-mini and save ~$31/month"

#### Community Provider Plugins
```python
# providers/custom/my_provider.py
class MyProviderCollector(BaseCollector):
    slug = "my_provider"
    name = "My Provider"
    billing_model = "usage"
    collection_method = "api"

    async def collect(self) -> list[DailyUsageRecord]:
        # implement collection logic
        pass
```

#### MCP Server
Ask Claude Code "what did I spend this week?" from inside VS Code:
```bash
mandacaru mcp start
# Starts MCP server on localhost
# Add to VS Code Claude Code config
```

### Open Source Launch Plan
1. Clean up Phase 1 code
2. Write comprehensive README with setup guide
3. Add CONTRIBUTING.md with plugin development guide
4. Push to `github.com/macambax/mandacaru`
5. Post on Hacker News: *"Show HN: Local CLI agent that reads AI billing pages because Anthropic has no billing API"*
6. Cross-post on X (@macambax_ai), Indie Hackers, Reddit r/selfhosted

---

## 12. Phase 3 — SaaS Cloud

### Goal
Monetize. Serve non-technical users. Team plans.

### New Infrastructure
- GCP Cloud Run (same as Cajú)
- PostgreSQL 17 (migrate from SQLite — one line change)
- Supabase (Google OAuth)
- Stripe (subscription billing)
- React + Vite web dashboard

### New Features
- Web dashboard (full React UI — see mockup)
- Multi-user / team accounts
- Real-time alerts (email + Slack)
- Spend forecasting (AI predicts month-end)
- Anomaly detection (flags unusual spikes)
- Cost attribution (tag costs by project/client/feature)
- REST API for programmatic access
- All Phase 2 providers

### Pricing

| Tier | Price | Providers | History | Seats | Alerts |
|------|-------|-----------|---------|-------|--------|
| **Free** | $0 | 3 | 30 days | 1 | Terminal only |
| **Solo** | $9/mo | Unlimited | 1 year | 1 | Email |
| **Team** | $29/mo | Unlimited | 2 years | 5 | Email + Slack |
| **Studio** | $79/mo | Unlimited | Forever | 20 | Email + Slack + API |

### Phase 3 Migration Path
```python
# SQLite → PostgreSQL: one line
DATABASE_URL = "postgresql://user:pass@host/mandacaru"

# Add to every table:
user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

---

## 13. Monetization

### Phase 1
- $0 — build for yourself, validate the concept

### Phase 2
- $0 — grow community, earn GitHub stars
- Potential: GitHub Sponsors once repo gains traction

### Phase 3
- **Primary:** Freemium SaaS subscriptions (Solo $9, Team $29, Studio $79)
- **Secondary:** Optimization recommendations as paid feature
- **Tertiary:** Provider affiliate/referral programs (Anthropic, OpenAI, GCP all have programs)
- **Long-term:** "State of AI API Costs" monthly data report — audience builder

### Revenue Target
- Phase 3 launch: $500 MRR within 6 months
- 56 Solo users OR 18 Team users OR 7 Studio users

---

## 14. Project Structure

```
mandacaru/
│
├── mandacaru/                    # Main package
│   ├── __init__.py
│   ├── cli.py                    # Typer app — all commands
│   ├── startup.py                # ASCII cactus + welcome screen
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py             # SQLAlchemy models (provided)
│   │   ├── migrations.py         # Schema version management
│   │   └── queries.py            # Common query helpers
│   │
│   ├── collectors/               # One file per provider
│   │   ├── __init__.py
│   │   ├── base.py               # BaseCollector abstract class
│   │   ├── openai_collector.py   # Direct API
│   │   ├── gcp_collector.py      # Direct API
│   │   ├── vercel_collector.py   # Direct API
│   │   ├── anthropic_collector.py # Playwright + Ollama
│   │   └── copilot_collector.py  # Playwright + Ollama
│   │
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── ollama_client.py      # Ollama vision wrapper
│   │   └── prompts.py            # Extraction prompt templates
│   │
│   ├── scheduler/
│   │   ├── __init__.py
│   │   └── daemon.py             # APScheduler daemon
│   │
│   ├── reports/
│   │   ├── __init__.py
│   │   └── renderer.py           # Rich table rendering
│   │
│   └── config.py                 # Settings management
│
├── tests/
│   ├── test_collectors.py
│   ├── test_models.py
│   └── test_reports.py
│
├── .env.example                  # Template — never commit .env
├── pyproject.toml                # Dependencies + pipx config
├── README.md
├── CONTRIBUTING.md
└── CLAUDE.md                     # Context for Claude Code sessions
```

### `CLAUDE.md` (for VS Code / Claude Code context)
```markdown
# Mandacarú — Claude Code Context

## What this is
Local CLI agent tracking developer AI and infra costs.
Python + Typer + Rich + SQLAlchemy + SQLite + Playwright + Ollama.

## Database
SQLite at ~/.mandacaru/mandacaru.db
Models in mandacaru/db/models.py
Run `python -m mandacaru.db.models` to init DB

## Key patterns
- BaseCollector in collectors/base.py — extend for new providers
- All DB access via SQLAlchemy sessions from get_session()
- Ollama client in vision/ollama_client.py — wraps llama3.2-vision
- Rich console in reports/renderer.py — all terminal output goes here

## Phase 1 scope
Providers: anthropic_pro, github_copilot, openai_api, gcp, vercel
Commands: init, sync, report, budget, daemon
No auth, no cloud, no multi-user — this runs locally only.

## Testing
pytest tests/ — run before every commit
No mocking of Ollama in unit tests — use fixtures in tests/fixtures/
```

---

## 15. Development Methodology — BMAD vs Spec Kit

### The Question
You've explored both BMAD and Spec Kit at Cotality and for MacambaX. Which is better for building Mandacarú?

### Quick Recap

**Spec Kit** — Spec-first, command-driven (`/specify`, `/plan`, `/tasks`, `/implement`)
- You write the spec, AI implements from it
- Linear flow: spec → plan → tasks → code
- Best for: locked scope, clear requirements, translational work

**BMAD (Breakthrough Method of Agile AI Development)** — Agent-driven, role-based
- Multiple AI agents (Architect, Developer, QA) collaborate
- More generative — AI helps discover requirements too
- Best for: greenfield products, evolving scope, complex systems

### For Mandacarú Specifically

**Use Spec Kit. Here's why:**

**1. You already have the spec — this document.**
The whole point of Spec Kit is to give AI a locked specification and have it implement faithfully. You now have a 15-section spec covering every table, every command, every provider, every phase. That's your `/specify` input. Spec Kit was designed for exactly this situation.

**2. Phase 1 is translational, not generative.**
You know what you want to build. The schema is designed. The commands are defined. The tech stack is chosen. You're not discovering requirements — you're implementing known requirements. Spec Kit's strength is translational work. BMAD's strength is generative discovery. You need translation right now.

**3. Solo founder — you ARE all the BMAD roles.**
BMAD's multi-agent architecture (Architect, Developer, QA) maps well to a team. As a solo founder you'd be orchestrating all three roles yourself, which adds overhead without the benefit of actual role separation.

**4. Spec Kit's `/tasks` command gives you a sprint board immediately.**
Run `/tasks` against this spec and you get a prioritized implementation checklist. That's exactly what you need to stay focused across weekend build sessions.

**5. BMAD is better for Cajú's next major feature cycle.**
When Cajú needs a major new feature where requirements are fuzzy — multi-location scheduling, payment integration, Stripe — BMAD's generative discovery is the right tool. Mandacarú Phase 1 is not that.

### Recommended Workflow

```
1. Open VS Code with GitHub Copilot + Claude Opus 4.6

2. Create project: mandacaru/

3. Add context files to workspace:
   - mandacaru_spec.md       (this file)
   - mandacaru_schema.sql    (provided)
   - mandacaru_models.py     (provided)
   - mandacaru_startup.py    (provided)

4. Create CLAUDE.md in project root (template above)

5. Start Spec Kit session:
   /specify  →  paste this document
   /plan     →  review architecture plan
   /tasks    →  get prioritized task list
   /implement → implement task by task

6. Build order (recommended):
   Week 1: DB init + models + `mandacaru init`
   Week 2: OpenAI + GCP collectors (API-based, no Ollama)
           `mandacaru sync` + `mandacaru report` working
   Week 3: Ollama vision setup + Anthropic + Copilot collectors
   Week 4: Budget system + daemon + polish
           Push to GitHub

7. Test each collector with real credentials before moving on.
   The sync_log table will tell you exactly what worked.
```

### One Important Spec Kit Gap to Know
Spec Kit has no official command to sync ad-hoc changes back to spec. When you deviate from the spec during implementation (and you will), manually update this document. Keep it as the source of truth — it's your context for every future Copilot and Claude Code session.

---

## 16. Getting Started — Phase 1 Build Checklist

### Environment Setup
- [ ] Create `mandacaru/` project directory in VS Code
- [ ] Copy `mandacaru_models.py` → `mandacaru/db/models.py`
- [ ] Copy `mandacaru_schema.sql` → `mandacaru/db/schema.sql`
- [ ] Copy `mandacaru_startup.py` → `mandacaru/startup.py`
- [ ] Create `CLAUDE.md` in project root
- [ ] Create `pyproject.toml` with dependencies
- [ ] Set up virtual environment: `python -m venv .venv`
- [ ] Install deps: `pip install typer rich playwright sqlalchemy httpx apscheduler python-dotenv`
- [ ] Install Playwright browsers: `playwright install chromium`
- [ ] Verify Ollama running: `ollama list`
- [ ] Verify llama3.2-vision: `ollama pull llama3.2-vision`

### Build Order — Phase 1

**Sprint 1 — Foundation (Weekend 1)**
- [ ] `mandacaru/db/models.py` — SQLAlchemy models (provided, test it)
- [ ] `mandacaru/config.py` — Settings loader from `~/.mandacaru/config.toml` + `.env`
- [ ] `mandacaru/cli.py` — Typer app skeleton with all commands stubbed
- [ ] `mandacaru init` — Prerequisites check + DB init + credential wizard
- [ ] `mandacaru doctor` — Re-check prerequisites
- [ ] `mandacaru version` — Show version

**Sprint 2 — First Collectors (Weekend 2)**
- [ ] `mandacaru/collectors/base.py` — `BaseCollector` abstract class
- [ ] `mandacaru/collectors/openai_collector.py` — OpenAI Usage API
- [ ] `mandacaru/collectors/gcp_collector.py` — GCP Billing API
- [ ] `mandacaru sync --provider openai_api` — working end-to-end
- [ ] `mandacaru/reports/renderer.py` — Rich table rendering
- [ ] `mandacaru report` — basic working report

**Sprint 3 — Vision Collectors (Weekend 3)**
- [ ] `mandacaru/vision/ollama_client.py` — Ollama wrapper
- [ ] `mandacaru/vision/prompts.py` — extraction prompt templates
- [ ] `mandacaru/collectors/anthropic_collector.py` — Playwright + Ollama
- [ ] `mandacaru/collectors/copilot_collector.py` — Playwright + Ollama
- [ ] `mandacaru/collectors/vercel_collector.py` — Vercel API
- [ ] `mandacaru sync` — all 5 providers working

**Sprint 4 — Budget + Daemon + Polish (Weekend 4)**
- [ ] `mandacaru budget set` / `budget check` / `budget list`
- [ ] `mandacaru/scheduler/daemon.py` — APScheduler daemon
- [ ] `mandacaru daemon start/stop/status`
- [ ] `mandacaru report --daily` — day-by-day breakdown
- [ ] `mandacaru logs` — sync_log viewer
- [ ] Polish startup screen + help text
- [ ] Write README.md
- [ ] Push to `github.com/macambax/mandacaru`
- [ ] Post on X (@macambax_ai)

---

## Appendix — Key Files Provided

| File | Description |
|------|-------------|
| `mandacaru_spec.md` | This document — full product specification |
| `mandacaru_schema.sql` | Raw SQL schema — all tables, indexes, views, seed data |
| `mandacaru_models.py` | SQLAlchemy ORM models — drop into `mandacaru/db/models.py` |
| `mandacaru_startup.py` | CLI startup screen with ASCII cactus — drop into `mandacaru/startup.py` |

---

*Mandacarú · MacambaX AI LLC · April 2026*
*"Every dollar your dev stack costs. One place. Runs on your machine."*
