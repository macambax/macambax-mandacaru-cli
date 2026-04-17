# Mandacarú — Recommendations by Phase (Opus 4.7 Context)

**MacambaX AI LLC · April 2026**

This document consolidates phase-by-phase recommendations for building Mandacarú. Pass this as context to Claude Opus 4.7 / GitHub Copilot / VS Code sessions.

---

## Phase 1 — Local CLI (Build for Yourself)

### Strategic Recommendations
- Build it for yourself first. Do not optimize for other users yet.
- Ship something running on your Mac Mini within 4 weekends.
- Do not publish publicly until Phase 2. Keep the repo private during Phase 1.
- Use Spec Kit with VS Code + GitHub Copilot + Claude Opus 4.7 for implementation.
- Reference the full spec document (`mandacaru_spec.md`) in every AI session.
- Store credentials in `~/.mandacaru/.env` — never commit to Git.
- Hardcode your own 5 providers. Do not build plugin architecture yet.

### Technical Recommendations
- Use SQLite, not PostgreSQL. Single file, zero setup, perfect for one user.
- Use SQLAlchemy ORM so Phase 3 migration to PostgreSQL is a one-line change.
- Use Python + Typer + Rich — stay close to what you know from Cajú.
- Use Ollama + llama3.2-vision for free local vision extraction.
- Always store `raw_response` JSON in `daily_usage` table — zero cost, huge future value.
- Always write to `sync_log` — silent Playwright failures are the #1 debugging problem.
- Use polling, not proxy. Never intercept user API calls.
- Design schema with `provider_id = NULL` for overall budgets — elegant single-table pattern.
- Use `UNIQUE(provider_id, usage_date, model_name)` for safe upsert on re-sync.
- Separate collectors into one file per provider. Abstract with `BaseCollector`.

### Providers to Build (in this order)
1. **OpenAI API** — direct billing API, no vision needed, fastest validation
2. **GCP** — direct billing API, already have service account
3. **Vercel** — direct REST API, simple
4. **Anthropic Console** — Playwright + Ollama (hardest, save for last)
5. **GitHub Copilot** — Playwright + Ollama

### Phase 1 Non-Goals (Do NOT Build)
- No web UI
- No auth
- No cloud
- No Stripe
- No multi-user
- No email/Slack alerts
- No plugin architecture
- No MCP server
- No optimization AI
- No CSV/JSON export

### Phase 1 Success Criteria
- Runs daily on your Mac Mini via APScheduler daemon
- Saves you from manually checking 5 browser tabs
- You actually use it every morning with your coffee
- One month of historical data in SQLite

---

## Phase 2 — Open Source Release

### Strategic Recommendations
- Only start Phase 2 after Phase 1 has run reliably for 30 days on your Mac Mini.
- Open source under Apache 2.0 license, not MIT — better for enterprise adoption later.
- Launch with "Show HN: I built a local CLI agent that reads my AI bills" post.
- Cross-post on X (@macambax_ai), Indie Hackers, r/selfhosted, Product Hunt.
- Write a `CONTRIBUTING.md` with clear provider-plugin development guide.
- Add CI/CD with GitHub Actions — automated tests on every PR.
- Focus on GitHub stars and community contributions, not users yet.
- Respond to every GitHub issue personally in the first 60 days.

### Technical Recommendations
- Add a local web UI at `http://localhost:4242` alongside the CLI for visual users.
- Use FastAPI + a single HTML page reading from SQLite — keep it simple.
- Add optional cloud LLM support (Claude Haiku, GPT-4o-mini, Gemini Flash) for better accuracy.
- Build the plugin architecture for community providers.
- Add CSV and JSON export.
- Add manual-entry subscription tracker for flat-fee tools (Cursor, Notion, Figma).
- Add MCP server so Claude Code users can ask "what did I spend this week?" inline.
- Add carbon footprint estimation per provider.
- Add cost optimization recommendations powered by AI.
- Test with at least 10 community contributors before marking Phase 2 complete.

### Trust-Building Moves
- Publish a transparent security page listing exactly what data is collected.
- Never log API keys, even in error traces.
- Document the open-core boundary clearly — what's free vs. what's paid in Phase 3.
- Self-host instructions must be first-class, not second-class.

### Phase 2 Non-Goals
- No paid tier yet
- No hosted cloud version
- No user accounts or auth
- No team features

### Phase 2 Success Criteria
- 500+ GitHub stars
- 20+ community-contributed providers
- Active Discord or GitHub Discussions
- Featured on Hacker News front page
- At least one newsletter or publication writes about it

---

## Phase 3 — SaaS Cloud

### Strategic Recommendations
- Only start Phase 3 after Phase 2 has 1000+ GitHub stars and a genuine community.
- Position as "hosted version of the open source tool you already trust" — not a new product.
- Lead marketing with the trust differentiator: "We ask for read-only billing keys, not AI API keys."
- Keep self-host option as a first-class free option forever — do not remove it.
- Start with GitHub OAuth as the first cloud integration (safest trust move).
- Launch with Solo tier only ($9/mo). Add Team and Studio tiers after 100 Solo subscribers.
- Run a public status page from day one.
- Write public post-mortems for every incident.

### Technical Recommendations
- Migrate SQLite → PostgreSQL 17 via one-line SQLAlchemy URL change.
- Add `user_id` foreign key to every table.
- Use Supabase for Google OAuth — free tier, solid enough for early stage.
- Use GCP Cloud Run — same infrastructure as Cajú for operational simplicity.
- Use GCP Secret Manager for encrypted credential storage.
- Use Stripe for subscription billing — industry standard, excellent docs.
- Use Vite + React + Recharts for the dashboard — same pattern as Cajú frontend.
- Prefer OAuth over API keys for every provider that supports it.
- Never store AI API keys — only read-only billing scopes.
- Build "Bring Your Own Database" option where possible for extreme privacy users.
- Implement audit logging for every credential access.

### Monetization Recommendations
- Freemium with 3-provider limit on free tier (real value gated behind Solo tier).
- Solo tier $9/mo is the main revenue driver — price it right, don't discount early.
- Team tier $29/mo is where volume comes from — one buyer, 5 seats.
- Studio tier $79/mo for agencies and larger teams.
- Add optimization recommendations as a Pro-only feature.
- Add affiliate/referral revenue from Anthropic, OpenAI, GCP programs.
- Consider launching a "State of AI API Costs" monthly data report for audience building.

### Trust Strategy
- Lead marketing with minimal access: "We don't need your AI keys."
- Publish security practices as technical detail, not corporate-speak.
- Start SOC 2 Type II process by month 6.
- Offer instant token revocation in the UI.
- Publish a transparency report quarterly.

### Phase 3 Non-Goals
- Do not build enterprise features until you have 100+ paying Solo customers.
- Do not pursue VC funding until you have $5K MRR.
- Do not abandon the open source CLI — it is your moat.

### Phase 3 Success Criteria
- $500 MRR within 6 months of launch
- 50+ Solo subscribers
- Net promoter score above 40
- Self-host users still account for 30%+ of total active users (proves trust)

---

## Cross-Phase Principles

### What Never Changes
- The CLI always works, in every phase.
- The open source core is always free and auditable.
- User credentials are always read-only billing scopes, never AI keys.
- Mandacarú is always local-first. Cloud is a convenience, not a requirement.
- The code is always Apache 2.0 licensed.

### Development Methodology
- Use Spec Kit for Phase 1 implementation — spec is already locked.
- Consider BMAD for Phase 2 community planning (generative discovery needed).
- Return to Spec Kit for Phase 3 — requirements will be known by then.

### What to Avoid
- Do not build Phase 2 features during Phase 1.
- Do not build Phase 3 features during Phase 2.
- Do not clone Helicone or Langfuse — differentiate on local-first and privacy.
- Do not break the CLI to serve the web UI.
- Do not remove the self-host option ever.

---

## Related Documents

- `mandacaru_spec.md` — Full product specification
- `mandacaru_schema.sql` — Raw SQL schema
- `mandacaru_models.py` — SQLAlchemy ORM models
- `mandacaru_startup.py` — CLI startup screen with ASCII cactus

---

*Mandacarú · MacambaX AI LLC · April 2026*
*"Every dollar your dev stack costs. One place. Runs on your machine."*
