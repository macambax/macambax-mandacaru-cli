# Mandacarú — Feature Tracker

> **Methodology:** Spec Kit (`/specify` → `/plan` → `/tasks` → `/implement`)
> **Phase:** 1 — Local CLI
> **Status:** Not Started

---

## Sprint 1 — Foundation

### F-001: Project Scaffolding
- [ ] Create `mandacaru/` package with project structure per spec
- [ ] Create `pyproject.toml` with all dependencies (typer, rich, playwright, sqlalchemy, httpx, apscheduler, python-dotenv)
- [ ] Set up virtual environment
- [ ] Install Playwright browsers (`playwright install chromium`)
- [ ] Create `CLAUDE.md` in project root for AI context
- [ ] Create `.env.example` template

### F-002: Database Layer
- [ ] `mandacaru/db/__init__.py`
- [ ] `mandacaru/db/models.py` — SQLAlchemy models (Provider, Invoice, DailyUsage, SyncLog, Budget, BudgetAlert, Setting)
- [ ] `mandacaru/db/migrations.py` — Schema version management
- [ ] `mandacaru/db/queries.py` — Common query helpers (monthly_spend, provider_monthly_totals)
- [ ] Database initialization: create `~/.mandacaru/` dir, init SQLite, seed providers & settings
- [ ] WAL mode + foreign keys enabled via SQLite pragmas
- [ ] Unit tests: `tests/test_models.py`

### F-003: Configuration Management
- [ ] `mandacaru/config.py` — Settings loader from `~/.mandacaru/config.toml` + `.env`
- [ ] Support for LLM provider config (ollama/anthropic/openai)
- [ ] Load credentials from `~/.mandacaru/.env` via python-dotenv
- [ ] Default settings seeding (ollama_base_url, ollama_model, sync_hour, currency, db_version, phase)

### F-004: CLI Skeleton
- [ ] `mandacaru/cli.py` — Typer app with all command groups stubbed
- [ ] Command groups: providers, sync, report, budget, daemon, config, logs
- [ ] `mandacaru` (no args) — renders startup screen with ASCII cactus
- [ ] `mandacaru version` — show version info

### F-005: `mandacaru init`
- [ ] Check Python version ≥ 3.11
- [ ] Check Ollama running at `localhost:11434`
- [ ] Check `llama3.2-vision` model available
- [ ] Create `~/.mandacaru/` directory
- [ ] Initialize SQLite database (`~/.mandacaru/mandacaru.db`)
- [ ] Run schema migrations
- [ ] Seed default providers (5 active Phase 1 + 10 inactive Phase 2)
- [ ] Seed default settings
- [ ] Interactive credential setup wizard
- [ ] Run first sync after setup

### F-006: `mandacaru doctor`
- [ ] Re-run all prerequisite checks at any time
- [ ] Output: Python version, Ollama status, llama3.2-vision availability, DB path validation
- [ ] Rich-formatted status output (✅/❌ per check)

### F-007: Startup Screen
- [ ] `mandacaru/startup.py` — ASCII mandacaru cactus art
- [ ] Brand colors: Purple `#7C3AED`, Teal `#2ABFA3`, Orange `#E88E36`
- [ ] Show version, phase, quick command reference
- [ ] Panel and simple render modes

---

## Sprint 2 — First Collectors + Reporting

### F-008: Base Collector
- [ ] `mandacaru/collectors/base.py` — `BaseCollector` abstract class
- [ ] Define interface: `collect()` → list of usage/invoice records
- [ ] Handle sync_log entry creation (success/failed/partial + duration_ms)
- [ ] Error handling and retry logic

### F-009: OpenAI API Collector
- [ ] `mandacaru/collectors/openai_collector.py`
- [ ] Call `GET https://api.openai.com/v1/usage` with API key from `.env`
- [ ] Parse response: extract per-model daily costs, token counts, request counts
- [ ] Upsert into `daily_usage` table (UNIQUE constraint prevents duplicates)
- [ ] Store `raw_response` JSON blob
- [ ] Write `sync_log` entry

### F-010: GCP Billing Collector
- [ ] `mandacaru/collectors/gcp_collector.py`
- [ ] Use GCP Cloud Billing API with service account credentials
- [ ] Parse billing data for project `macambax-website-dev` (configurable)
- [ ] Upsert into `daily_usage` table
- [ ] Store `raw_response` JSON blob
- [ ] Write `sync_log` entry

### F-011: `mandacaru sync`
- [ ] Load all active providers from DB
- [ ] For each provider: dispatch to correct collector based on `collection_method`
- [ ] Show Rich progress bar per provider during sync
- [ ] `--provider <slug>` flag to sync a single provider
- [ ] `--dry-run` flag to show what would be synced without writing to DB
- [ ] Run budget check automatically after sync
- [ ] Summary output: X providers synced, Y failed

### F-012: Report Renderer
- [ ] `mandacaru/reports/renderer.py` — Rich table rendering
- [ ] Query `monthly_spend` view for current month
- [ ] Display: provider name, cost, budget, status (subscription/usage/infra)
- [ ] Budget progress bars with color coding (green <60%, yellow 60-80%, red >80%)
- [ ] Total row with overall budget status
- [ ] Days remaining + projected month-end spend
- [ ] Last sync timestamp + provider health summary

### F-013: `mandacaru report`
- [ ] Default: current month summary dashboard
- [ ] `--month YYYY-MM` — report for a specific month
- [ ] `--daily` — day-by-day breakdown for current month
- [ ] `--provider <slug>` — provider-specific detail report
- [ ] `--model` — breakdown by model within each provider
- [ ] Unit tests: `tests/test_reports.py`

---

## Sprint 3 — Vision Collectors

### F-014: Ollama Vision Client
- [ ] `mandacaru/vision/ollama_client.py` — wrapper for Ollama API
- [ ] Send screenshot to `llama3.2-vision` model
- [ ] Parse structured JSON from vision response
- [ ] Handle connection errors to Ollama gracefully
- [ ] Track Mandacarú's own Ollama cost (self-tracking, transparent by design)

### F-015: Vision Prompt Templates
- [ ] `mandacaru/vision/prompts.py` — extraction prompt templates per provider
- [ ] Anthropic billing page prompt → `{billing_period, amount_usd, invoice_date, invoice_ref}`
- [ ] GitHub Copilot billing page prompt → same structure
- [ ] Validate returned JSON schema before DB insert

### F-016: Anthropic Playwright Collector
- [ ] `mandacaru/collectors/anthropic_collector.py`
- [ ] Launch headless Chromium via Playwright
- [ ] Load stored session cookies for `console.anthropic.com`
- [ ] Navigate to `https://console.anthropic.com/settings/billing`
- [ ] Wait for page load, capture screenshot
- [ ] Send to Ollama vision → extract billing JSON
- [ ] Upsert into `invoices` table
- [ ] Write `sync_log` entry

### F-017: GitHub Copilot Playwright Collector
- [ ] `mandacaru/collectors/copilot_collector.py`
- [ ] Launch headless Chromium via Playwright
- [ ] Load stored session cookies for `github.com`
- [ ] Navigate to `https://github.com/settings/billing`
- [ ] Wait for page load, capture screenshot
- [ ] Send to Ollama vision → extract billing JSON
- [ ] Upsert into `invoices` table
- [ ] Write `sync_log` entry

### F-018: Vercel API Collector
- [ ] `mandacaru/collectors/vercel_collector.py`
- [ ] Call Vercel REST API with read-only token from `.env`
- [ ] Parse billing/usage data
- [ ] Upsert into `daily_usage` table
- [ ] Store `raw_response` JSON blob
- [ ] Write `sync_log` entry

### F-019: Full Sync — All 5 Providers
- [ ] `mandacaru sync` runs all 5 Phase 1 providers end-to-end
- [ ] Verify with real credentials per provider before marking done
- [ ] `sync_log` has entries for all providers
- [ ] Unit tests: `tests/test_collectors.py`

---

## Sprint 4 — Budget, Daemon & Polish

### F-020: Budget Management
- [ ] `mandacaru budget set --overall <amount>` — set overall monthly budget
- [ ] `mandacaru budget set --provider <slug> <amount>` — set per-provider budget
- [ ] `mandacaru budget set --threshold <0.0-1.0>` — set alert threshold (default 0.80)
- [ ] `mandacaru budget list` — show all budgets and current usage
- [ ] `mandacaru budget check` — manual budget check against current spend

### F-021: Budget Alerts
- [ ] Triggered automatically after every `mandacaru sync`
- [ ] Compare current period spend vs budget amount × alert_threshold
- [ ] Fire alert: write `budget_alerts` entry
- [ ] `mandacaru budget alerts` — show unacknowledged alerts
- [ ] `mandacaru budget alerts --ack-all` — mark all as acknowledged
- [ ] Terminal display: Rich panel with warning colors

### F-022: Daemon Mode
- [ ] `mandacaru/scheduler/daemon.py` — APScheduler background process
- [ ] `mandacaru daemon start` — start daily auto-sync at configured hour (default 07:00)
- [ ] `mandacaru daemon stop` — stop background daemon
- [ ] `mandacaru daemon status` — show daemon status, last run, next run
- [ ] `mandacaru daemon logs` — show recent daemon activity
- [ ] Write PID file to `~/.mandacaru/daemon.pid`
- [ ] Configurable via `mandacaru config set sync_hour <hour>`

### F-023: Provider Management
- [ ] `mandacaru providers list` — list all providers with status (active/inactive, last sync, collection method)
- [ ] `mandacaru providers enable <slug>` — activate a provider
- [ ] `mandacaru providers disable <slug>` — deactivate a provider
- [ ] `mandacaru providers add` — interactive wizard to add a custom provider

### F-024: Config Commands
- [ ] `mandacaru config show` — display current configuration
- [ ] `mandacaru config set <key> <value>` — change any setting
- [ ] Supported keys: sync_hour, ollama_model, ollama_base_url, llm_provider, currency

### F-025: Log Viewer
- [ ] `mandacaru logs` — show recent `sync_log` entries
- [ ] Rich-formatted table with status colors (green=success, red=failed, yellow=partial)

### F-026: Reset Command
- [ ] `mandacaru reset` — drop and recreate database
- [ ] Requires explicit confirmation prompt (destructive action)

### F-027: Polish & Documentation
- [ ] Polish startup screen + all help text
- [ ] Write `README.md` with setup guide and usage examples
- [ ] Verify `pipx install mandacaru` works
- [ ] Push to `github.com/macambax/mandacaru`

---

## Phase 2 Features (Future — Post Phase 1)

> These are tracked here for visibility but will not be built until Phase 1 is complete and pushed to GitHub.

### F-100: Optional Cloud LLM Support
- [ ] Switch from Ollama to Anthropic (`claude-haiku-4-5`) or OpenAI (`gpt-4o-mini`) for better vision accuracy
- [ ] Config-driven via `~/.mandacaru/config.toml`

### F-101: Additional Providers (20+)
- [ ] Mistral, Groq, Cohere, Hugging Face, Replicate, ElevenLabs
- [ ] Supabase, Cloudflare Workers, Pinecone, GitHub Actions

### F-102: Manual Entry Subscriptions
- [ ] Flat-fee tools with no billing API: Cursor, Windsurf, ChatGPT Plus, Notion, Linear, Figma, Slack, Zoom, 1Password

### F-103: Export
- [ ] `mandacaru report --export csv`
- [ ] `mandacaru report --export json`
- [ ] Export to `~/.mandacaru/exports/`

### F-104: Cost Optimization Tips
- [ ] AI-generated suggestions (e.g., "Switch from gpt-4o to gpt-4o-mini, save ~$31/month")

### F-105: Community Provider Plugins
- [ ] `BaseCollector` plugin system — extend with `providers/custom/my_provider.py`
- [ ] `CONTRIBUTING.md` with plugin development guide

### F-106: MCP Server
- [ ] `mandacaru mcp start` — MCP server for Claude Code integration
- [ ] Ask "what did I spend this week?" from VS Code

---

## Phase 3 Features (Future — SaaS)

> Tracked for roadmap visibility. Not in scope for Phase 1 or 2.

- [ ] F-200: PostgreSQL migration (one-line DATABASE_URL change + add user_id FK)
- [ ] F-201: Web dashboard (React + Vite + Recharts)
- [ ] F-202: Auth (Supabase Google OAuth)
- [ ] F-203: Multi-user / team accounts
- [ ] F-204: Stripe subscription billing (Free / Solo $9 / Team $29 / Studio $79)
- [ ] F-205: Real-time alerts (email + Slack)
- [ ] F-206: Spend forecasting (AI predicts month-end)
- [ ] F-207: Anomaly detection (flags unusual spikes)
- [ ] F-208: Cost attribution (tag by project/client/feature)
- [ ] F-209: REST API for programmatic access

---

*Mandacarú · MacambaX AI LLC · April 2026*
