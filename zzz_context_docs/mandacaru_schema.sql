-- ============================================================
-- Mandacarú — Database Schema
-- Phase 1: SQLite (local CLI)
-- Phase 3: PostgreSQL (SaaS — zero structural changes needed)
-- MacambaX AI LLC · April 2026
-- ============================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- providers
-- One row per billing provider.
-- billing_model: subscription | usage | infra
-- collection_method: api | playwright
-- ============================================================
CREATE TABLE IF NOT EXISTS providers (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
    slug                TEXT        NOT NULL UNIQUE,     -- e.g. "openai_api"
    name                TEXT        NOT NULL,            -- e.g. "OpenAI API"
    billing_model       TEXT        NOT NULL             -- subscription|usage|infra
                            CHECK (billing_model IN ('subscription','usage','infra')),
    collection_method   TEXT        NOT NULL             -- api|playwright
                            CHECK (collection_method IN ('api','playwright')),
    website_url         TEXT,                            -- billing page URL for playwright
    api_docs_url        TEXT,                            -- billing API docs reference
    is_active           INTEGER     NOT NULL DEFAULT 1,  -- 0=disabled, 1=enabled
    notes               TEXT,
    created_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now')),
    updated_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- invoices
-- Subscription billing cycles.
-- One row per provider per billing period.
-- Also used for manual-entry flat-fee tools (Cursor, Notion, etc.)
-- ============================================================
CREATE TABLE IF NOT EXISTS invoices (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
    provider_id         INTEGER     NOT NULL REFERENCES providers(id),
    billing_period      TEXT        NOT NULL,            -- "2026-04" (YYYY-MM)
    amount_usd          REAL        NOT NULL,
    currency            TEXT        NOT NULL DEFAULT 'USD',
    invoice_date        DATE,                            -- actual charge date
    invoice_ref         TEXT,                            -- provider's invoice ID
    payment_method      TEXT,                            -- e.g. "Mercury Visa"
    notes               TEXT,
    created_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now')),

    UNIQUE (provider_id, billing_period)
);

-- ============================================================
-- daily_usage
-- Usage-based costs broken down per provider + model + day.
-- One row per provider + model + date combination.
-- raw_response stores the full API payload for future mining.
-- ============================================================
CREATE TABLE IF NOT EXISTS daily_usage (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
    provider_id         INTEGER     NOT NULL REFERENCES providers(id),
    usage_date          DATE        NOT NULL,
    model_name          TEXT        NOT NULL DEFAULT 'default', -- e.g. "gpt-4o"
    input_tokens        INTEGER,                         -- nullable for non-LLM providers
    output_tokens       INTEGER,                         -- nullable
    total_tokens        INTEGER,                         -- nullable
    requests_count      INTEGER,                         -- API call count
    compute_units       REAL,                            -- for GPU/infra providers
    cost_usd            REAL        NOT NULL DEFAULT 0.0,
    raw_response        TEXT,                            -- JSON blob from billing API
    created_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now')),
    updated_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now')),

    UNIQUE (provider_id, usage_date, model_name)
);

-- ============================================================
-- sync_log
-- Audit trail for every sync attempt.
-- Critical for debugging playwright failures silently.
-- ============================================================
CREATE TABLE IF NOT EXISTS sync_log (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
    provider_id         INTEGER     NOT NULL REFERENCES providers(id),
    synced_at           TIMESTAMP   NOT NULL DEFAULT (datetime('now')),
    status              TEXT        NOT NULL             -- success|failed|partial
                            CHECK (status IN ('success','failed','partial')),
    records_fetched     INTEGER     NOT NULL DEFAULT 0,
    error_message       TEXT,                            -- nullable on success
    duration_ms         INTEGER,                         -- sync duration
    collection_method   TEXT,                            -- api|playwright (as used)
    notes               TEXT
);

-- ============================================================
-- budgets
-- Per-provider or overall spending limits.
-- provider_id NULL = overall budget across all providers.
-- alert_threshold = fraction e.g. 0.80 means alert at 80%.
-- ============================================================
CREATE TABLE IF NOT EXISTS budgets (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
    provider_id         INTEGER     REFERENCES providers(id), -- NULL = overall
    label               TEXT,                            -- e.g. "Monthly AI Budget"
    period_type         TEXT        NOT NULL DEFAULT 'monthly'
                            CHECK (period_type IN ('monthly','weekly')),
    amount_usd          REAL        NOT NULL,
    alert_threshold     REAL        NOT NULL DEFAULT 0.80, -- 0.0–1.0
    is_active           INTEGER     NOT NULL DEFAULT 1,
    created_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now')),
    updated_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now')),

    UNIQUE (provider_id, period_type)
);

-- ============================================================
-- budget_alerts
-- History of every alert fired.
-- acknowledged = user has seen it in terminal.
-- ============================================================
CREATE TABLE IF NOT EXISTS budget_alerts (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
    budget_id           INTEGER     NOT NULL REFERENCES budgets(id),
    fired_at            TIMESTAMP   NOT NULL DEFAULT (datetime('now')),
    billing_period      TEXT        NOT NULL,            -- "2026-04"
    spend_at_alert      REAL        NOT NULL,            -- spend when fired
    budget_amount       REAL        NOT NULL,            -- budget at time of firing
    pct_used            REAL        NOT NULL,            -- e.g. 0.83
    acknowledged        INTEGER     NOT NULL DEFAULT 0,  -- 0=unseen, 1=seen
    acknowledged_at     TIMESTAMP
);

-- ============================================================
-- settings
-- Key-value store for user config and app state.
-- ============================================================
CREATE TABLE IF NOT EXISTS settings (
    key                 TEXT        PRIMARY KEY,
    value               TEXT,
    description         TEXT,
    updated_at          TIMESTAMP   NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- INDEXES
-- ============================================================

-- Most common query: costs for a date range per provider
CREATE INDEX IF NOT EXISTS idx_daily_usage_provider_date
    ON daily_usage (provider_id, usage_date);

-- Monthly reports: group by date
CREATE INDEX IF NOT EXISTS idx_daily_usage_date
    ON daily_usage (usage_date);

-- Invoice lookups by period
CREATE INDEX IF NOT EXISTS idx_invoices_period
    ON invoices (billing_period);

-- Sync log lookups by provider
CREATE INDEX IF NOT EXISTS idx_sync_log_provider
    ON sync_log (provider_id, synced_at);

-- Unacknowledged alerts
CREATE INDEX IF NOT EXISTS idx_budget_alerts_unacked
    ON budget_alerts (acknowledged, fired_at);

-- ============================================================
-- VIEWS
-- ============================================================

-- monthly_spend: unified view across subscriptions + usage
-- Used by `mandacaru report` for the main dashboard
CREATE VIEW IF NOT EXISTS monthly_spend AS
    SELECT
        p.slug,
        p.name,
        p.billing_model,
        strftime('%Y-%m', COALESCE(i.invoice_date, d.usage_date)) AS billing_period,
        COALESCE(i.amount_usd, 0)                                  AS subscription_cost,
        COALESCE(SUM(d.cost_usd), 0)                               AS usage_cost,
        COALESCE(i.amount_usd, 0) + COALESCE(SUM(d.cost_usd), 0)  AS total_cost
    FROM providers p
    LEFT JOIN invoices i
        ON i.provider_id = p.id
    LEFT JOIN daily_usage d
        ON d.provider_id = p.id
        AND strftime('%Y-%m', d.usage_date) = strftime('%Y-%m', COALESCE(i.invoice_date, 'now'))
    WHERE p.is_active = 1
    GROUP BY p.id, billing_period;

-- provider_monthly_totals: simple cost per provider per month
-- Used by budget check
CREATE VIEW IF NOT EXISTS provider_monthly_totals AS
    SELECT
        provider_id,
        strftime('%Y-%m', usage_date) AS billing_period,
        SUM(cost_usd)                 AS total_cost,
        SUM(total_tokens)             AS total_tokens,
        SUM(requests_count)           AS total_requests
    FROM daily_usage
    GROUP BY provider_id, billing_period;

-- ============================================================
-- SEED DATA — providers
-- ============================================================

INSERT OR IGNORE INTO providers
    (slug, name, billing_model, collection_method, website_url, api_docs_url, notes)
VALUES
    -- Phase 1 — your personal stack
    ('anthropic_pro',   'Claude Pro',           'subscription', 'playwright',
     'https://console.anthropic.com/settings/billing',
     NULL,
     'Monthly flat subscription. Vision extraction via Ollama.'),

    ('github_copilot',  'GitHub Copilot',        'subscription', 'playwright',
     'https://github.com/settings/billing',
     NULL,
     'Pro Max plan. Includes 1500 premium requests/month. Vision extraction via Ollama.'),

    ('openai_api',      'OpenAI API',            'usage',        'api',
     'https://platform.openai.com/usage',
     'https://platform.openai.com/docs/api-reference/usage',
     'Pay-per-token. Direct billing API available.'),

    ('gcp',             'GCP / Vertex AI',       'infra',        'api',
     'https://console.cloud.google.com/billing',
     'https://cloud.google.com/billing/docs/reference/rest',
     'GCP project macambax-website-dev. Billing API available.'),

    ('vercel',          'Vercel',                'infra',        'api',
     'https://vercel.com/account/billing',
     'https://vercel.com/docs/rest-api',
     'Frontend hosting. Usage-based overage possible.'),

    -- Phase 2 — community providers (pre-seeded, inactive)
    ('mistral',         'Mistral AI',            'usage',        'api',
     'https://console.mistral.ai/billing',
     'https://docs.mistral.ai/',
     NULL),

    ('groq',            'Groq',                  'usage',        'api',
     'https://console.groq.com/settings/billing',
     'https://console.groq.com/docs/openai',
     NULL),

    ('cohere',          'Cohere',                'usage',        'api',
     'https://dashboard.cohere.com/billing',
     'https://docs.cohere.com/reference/about',
     NULL),

    ('huggingface',     'Hugging Face',          'usage',        'api',
     'https://huggingface.co/settings/billing',
     'https://huggingface.co/docs/api-inference/index',
     NULL),

    ('replicate',       'Replicate',             'usage',        'api',
     'https://replicate.com/account/billing',
     'https://replicate.com/docs/reference/http',
     NULL),

    ('elevenlabs',      'ElevenLabs',            'usage',        'api',
     'https://elevenlabs.io/app/subscription',
     'https://elevenlabs.io/docs/api-reference/overview',
     NULL),

    ('supabase',        'Supabase',              'infra',        'api',
     'https://supabase.com/dashboard/account/billing',
     'https://supabase.com/docs/reference/api/introduction',
     NULL),

    ('cloudflare',      'Cloudflare Workers',    'infra',        'api',
     'https://dash.cloudflare.com/?to=/:account/billing',
     'https://developers.cloudflare.com/api/',
     NULL),

    ('pinecone',        'Pinecone',              'infra',        'api',
     'https://app.pinecone.io/organizations/billing',
     'https://docs.pinecone.io/reference/api/introduction',
     NULL),

    ('github_actions',  'GitHub Actions',        'infra',        'api',
     'https://github.com/settings/billing',
     'https://docs.github.com/en/rest/billing',
     NULL);

-- ============================================================
-- SEED DATA — settings
-- ============================================================

INSERT OR IGNORE INTO settings (key, value, description) VALUES
    ('app_version',         '0.1.0',        'Current Mandacarú version'),
    ('ollama_base_url',     'http://localhost:11434', 'Ollama server URL'),
    ('ollama_model',        'llama3.2-vision', 'Vision model for screenshot extraction'),
    ('llm_provider',        'ollama',        'LLM provider: ollama|anthropic|openai'),
    ('sync_hour',           '7',            'Hour to run daily auto-sync (24h format)'),
    ('currency',            'USD',          'Display currency'),
    ('db_version',          '1',            'Schema version for migrations'),
    ('first_run',           '1',            '1=first run not completed yet'),
    ('phase',               '1',            'Mandacarú phase: 1=local, 2=open source, 3=saas');
