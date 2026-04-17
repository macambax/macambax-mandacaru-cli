"""
Mandacarú — SQLAlchemy Models
Phase 1: SQLite  |  Phase 3: PostgreSQL (change DATABASE_URL only)
MacambaX AI LLC · April 2026
"""

from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    create_engine, Column, Integer, Text, Float, Boolean,
    Date, DateTime, ForeignKey, UniqueConstraint, CheckConstraint,
    Index, event
)
Real = Float  # SQLAlchemy uses Float; maps to REAL in SQLite, DOUBLE PRECISION in PostgreSQL
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.sql import func
import os

# ── Database URL ──────────────────────────────────────────────────────────────
# Phase 1: SQLite local
# Phase 3: swap to "postgresql://user:pass@host/mandacaru"
DB_PATH = os.path.expanduser("~/.mandacaru/mandacaru.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite only
    echo=False,
)

# Enable WAL mode and foreign keys for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, _):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()


# ══════════════════════════════════════════════════════════════════════════════
class Provider(Base):
    """
    One row per billing provider.
    billing_model: subscription | usage | infra
    collection_method: api | playwright
    """
    __tablename__ = "providers"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    slug                = Column(Text, nullable=False, unique=True)
    name                = Column(Text, nullable=False)
    billing_model       = Column(Text, nullable=False)
    collection_method   = Column(Text, nullable=False)
    website_url         = Column(Text)
    api_docs_url        = Column(Text)
    is_active           = Column(Integer, nullable=False, default=1)
    notes               = Column(Text)
    created_at          = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at          = Column(DateTime, nullable=False, default=datetime.utcnow,
                                 onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(
            "billing_model IN ('subscription','usage','infra')",
            name="ck_providers_billing_model"
        ),
        CheckConstraint(
            "collection_method IN ('api','playwright')",
            name="ck_providers_collection_method"
        ),
    )

    # Relationships
    invoices        = relationship("Invoice",     back_populates="provider",
                                   cascade="all, delete-orphan")
    daily_usages    = relationship("DailyUsage",  back_populates="provider",
                                   cascade="all, delete-orphan")
    sync_logs       = relationship("SyncLog",     back_populates="provider",
                                   cascade="all, delete-orphan")
    budgets         = relationship("Budget",      back_populates="provider")

    def __repr__(self):
        return f"<Provider slug={self.slug} model={self.billing_model}>"


# ══════════════════════════════════════════════════════════════════════════════
class Invoice(Base):
    """
    Subscription billing cycles — one row per provider per billing period.
    Also used for manual-entry flat-fee tools (Cursor, Notion, Figma, etc.)
    billing_period format: "2026-04" (YYYY-MM)
    """
    __tablename__ = "invoices"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    provider_id     = Column(Integer, ForeignKey("providers.id"), nullable=False)
    billing_period  = Column(Text, nullable=False)          # "2026-04"
    amount_usd      = Column(Real, nullable=False)
    currency        = Column(Text, nullable=False, default="USD")
    invoice_date    = Column(Date)
    invoice_ref     = Column(Text)                          # provider's invoice ID
    payment_method  = Column(Text)                          # e.g. "Mercury Visa"
    notes           = Column(Text)
    created_at      = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("provider_id", "billing_period",
                         name="uq_invoices_provider_period"),
    )

    provider = relationship("Provider", back_populates="invoices")

    def __repr__(self):
        return f"<Invoice provider_id={self.provider_id} period={self.billing_period} amount=${self.amount_usd}>"


# ══════════════════════════════════════════════════════════════════════════════
class DailyUsage(Base):
    """
    Usage-based costs per provider + model + day.
    One row per (provider, date, model) combination.
    raw_response stores the full API JSON for future mining.
    """
    __tablename__ = "daily_usage"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    provider_id     = Column(Integer, ForeignKey("providers.id"), nullable=False)
    usage_date      = Column(Date, nullable=False)
    model_name      = Column(Text, nullable=False, default="default")
    input_tokens    = Column(Integer)                       # nullable for non-LLM
    output_tokens   = Column(Integer)
    total_tokens    = Column(Integer)
    requests_count  = Column(Integer)
    compute_units   = Column(Real)                          # for GPU/infra providers
    cost_usd        = Column(Real, nullable=False, default=0.0)
    raw_response    = Column(Text)                          # JSON blob
    created_at      = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at      = Column(DateTime, nullable=False, default=datetime.utcnow,
                             onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("provider_id", "usage_date", "model_name",
                         name="uq_daily_usage_provider_date_model"),
        Index("idx_daily_usage_provider_date", "provider_id", "usage_date"),
        Index("idx_daily_usage_date", "usage_date"),
    )

    provider = relationship("Provider", back_populates="daily_usages")

    def __repr__(self):
        return f"<DailyUsage provider_id={self.provider_id} date={self.usage_date} model={self.model_name} cost=${self.cost_usd}>"


# ══════════════════════════════════════════════════════════════════════════════
class SyncLog(Base):
    """
    Audit trail for every sync attempt.
    Critical for debugging silent playwright failures.
    status: success | failed | partial
    """
    __tablename__ = "sync_log"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    provider_id         = Column(Integer, ForeignKey("providers.id"), nullable=False)
    synced_at           = Column(DateTime, nullable=False, default=datetime.utcnow)
    status              = Column(Text, nullable=False)
    records_fetched     = Column(Integer, nullable=False, default=0)
    error_message       = Column(Text)
    duration_ms         = Column(Integer)
    collection_method   = Column(Text)
    notes               = Column(Text)

    __table_args__ = (
        CheckConstraint(
            "status IN ('success','failed','partial')",
            name="ck_sync_log_status"
        ),
        Index("idx_sync_log_provider", "provider_id", "synced_at"),
    )

    provider = relationship("Provider", back_populates="sync_logs")

    def __repr__(self):
        return f"<SyncLog provider_id={self.provider_id} status={self.status} at={self.synced_at}>"


# ══════════════════════════════════════════════════════════════════════════════
class Budget(Base):
    """
    Per-provider or overall spending limits.
    provider_id NULL = overall budget across all providers.
    alert_threshold = fraction — 0.80 means alert at 80% of budget.
    """
    __tablename__ = "budgets"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    provider_id     = Column(Integer, ForeignKey("providers.id"), nullable=True)
    label           = Column(Text)                          # e.g. "Monthly AI Budget"
    period_type     = Column(Text, nullable=False, default="monthly")
    amount_usd      = Column(Real, nullable=False)
    alert_threshold = Column(Real, nullable=False, default=0.80)
    is_active       = Column(Integer, nullable=False, default=1)
    created_at      = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at      = Column(DateTime, nullable=False, default=datetime.utcnow,
                             onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(
            "period_type IN ('monthly','weekly')",
            name="ck_budgets_period_type"
        ),
        UniqueConstraint("provider_id", "period_type",
                         name="uq_budgets_provider_period"),
    )

    provider        = relationship("Provider", back_populates="budgets")
    alerts          = relationship("BudgetAlert", back_populates="budget",
                                   cascade="all, delete-orphan")

    def __repr__(self):
        scope = f"provider_id={self.provider_id}" if self.provider_id else "OVERALL"
        return f"<Budget {scope} amount=${self.amount_usd} threshold={self.alert_threshold}>"


# ══════════════════════════════════════════════════════════════════════════════
class BudgetAlert(Base):
    """
    History of every budget alert fired.
    acknowledged = user has seen it in terminal.
    """
    __tablename__ = "budget_alerts"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    budget_id       = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    fired_at        = Column(DateTime, nullable=False, default=datetime.utcnow)
    billing_period  = Column(Text, nullable=False)          # "2026-04"
    spend_at_alert  = Column(Real, nullable=False)
    budget_amount   = Column(Real, nullable=False)
    pct_used        = Column(Real, nullable=False)
    acknowledged    = Column(Integer, nullable=False, default=0)
    acknowledged_at = Column(DateTime)

    __table_args__ = (
        Index("idx_budget_alerts_unacked", "acknowledged", "fired_at"),
    )

    budget = relationship("Budget", back_populates="alerts")

    def __repr__(self):
        return f"<BudgetAlert budget_id={self.budget_id} pct={self.pct_used:.0%} acked={bool(self.acknowledged)}>"


# ══════════════════════════════════════════════════════════════════════════════
class Setting(Base):
    """
    Key-value store for user config and app state.
    """
    __tablename__ = "settings"

    key         = Column(Text, primary_key=True)
    value       = Column(Text)
    description = Column(Text)
    updated_at  = Column(DateTime, nullable=False, default=datetime.utcnow,
                         onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Setting {self.key}={self.value}>"


# ══════════════════════════════════════════════════════════════════════════════
# Database initialization
# ══════════════════════════════════════════════════════════════════════════════
def init_db():
    """Create all tables and seed initial data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(engine)
    _seed_providers()
    _seed_settings()
    print(f"✅ Database initialized at {DB_PATH}")


def get_session() -> Session:
    """Return a new SQLAlchemy session."""
    return Session(engine)


def _seed_providers():
    """Insert default providers if not already present."""
    with get_session() as session:
        providers = [
            # ── Phase 1 — your personal stack ──────────────────────────────
            dict(slug="anthropic_pro",  name="Claude Pro",
                 billing_model="subscription", collection_method="playwright",
                 website_url="https://console.anthropic.com/settings/billing",
                 notes="Monthly flat. Vision via Ollama.", is_active=1),

            dict(slug="github_copilot", name="GitHub Copilot",
                 billing_model="subscription", collection_method="playwright",
                 website_url="https://github.com/settings/billing",
                 notes="Pro Max $39/mo. 1500 premium req/month.", is_active=1),

            dict(slug="openai_api",     name="OpenAI API",
                 billing_model="usage",        collection_method="api",
                 website_url="https://platform.openai.com/usage",
                 api_docs_url="https://platform.openai.com/docs/api-reference/usage",
                 notes="Direct billing API. No vision needed.", is_active=1),

            dict(slug="gcp",            name="GCP / Vertex AI",
                 billing_model="infra",        collection_method="api",
                 website_url="https://console.cloud.google.com/billing",
                 api_docs_url="https://cloud.google.com/billing/docs/reference/rest",
                 notes="Project macambax-website-dev.", is_active=1),

            dict(slug="vercel",         name="Vercel",
                 billing_model="infra",        collection_method="api",
                 website_url="https://vercel.com/account/billing",
                 api_docs_url="https://vercel.com/docs/rest-api",
                 notes="Frontend hosting.", is_active=1),

            # ── Phase 2 — community providers (seeded inactive) ────────────
            dict(slug="mistral",        name="Mistral AI",
                 billing_model="usage",        collection_method="api",
                 website_url="https://console.mistral.ai/billing", is_active=0),

            dict(slug="groq",           name="Groq",
                 billing_model="usage",        collection_method="api",
                 website_url="https://console.groq.com/settings/billing", is_active=0),

            dict(slug="cohere",         name="Cohere",
                 billing_model="usage",        collection_method="api",
                 website_url="https://dashboard.cohere.com/billing", is_active=0),

            dict(slug="huggingface",    name="Hugging Face",
                 billing_model="usage",        collection_method="api",
                 website_url="https://huggingface.co/settings/billing", is_active=0),

            dict(slug="replicate",      name="Replicate",
                 billing_model="usage",        collection_method="api",
                 website_url="https://replicate.com/account/billing", is_active=0),

            dict(slug="elevenlabs",     name="ElevenLabs",
                 billing_model="usage",        collection_method="api",
                 website_url="https://elevenlabs.io/app/subscription", is_active=0),

            dict(slug="supabase",       name="Supabase",
                 billing_model="infra",        collection_method="api",
                 website_url="https://supabase.com/dashboard/account/billing", is_active=0),

            dict(slug="cloudflare",     name="Cloudflare Workers",
                 billing_model="infra",        collection_method="api",
                 website_url="https://dash.cloudflare.com/?to=/:account/billing", is_active=0),

            dict(slug="pinecone",       name="Pinecone",
                 billing_model="infra",        collection_method="api",
                 website_url="https://app.pinecone.io/organizations/billing", is_active=0),

            dict(slug="github_actions", name="GitHub Actions",
                 billing_model="infra",        collection_method="api",
                 website_url="https://github.com/settings/billing", is_active=0),
        ]

        for p in providers:
            exists = session.query(Provider).filter_by(slug=p["slug"]).first()
            if not exists:
                session.add(Provider(**p))

        session.commit()


def _seed_settings():
    """Insert default settings if not already present."""
    with get_session() as session:
        defaults = [
            ("app_version",     "0.1.0",                    "Current Mandacarú version"),
            ("ollama_base_url", "http://localhost:11434",    "Ollama server URL"),
            ("ollama_model",    "llama3.2-vision",           "Vision model for screenshot extraction"),
            ("llm_provider",    "ollama",                    "LLM provider: ollama|anthropic|openai"),
            ("sync_hour",       "7",                         "Hour for daily auto-sync (24h format)"),
            ("currency",        "USD",                       "Display currency"),
            ("db_version",      "1",                         "Schema version for migrations"),
            ("first_run",       "1",                         "1 = first run not yet completed"),
            ("phase",           "1",                         "Mandacarú phase: 1=local 2=oss 3=saas"),
        ]
        for key, value, description in defaults:
            exists = session.query(Setting).filter_by(key=key).first()
            if not exists:
                session.add(Setting(key=key, value=value, description=description))
        session.commit()


# ══════════════════════════════════════════════════════════════════════════════
# Quick helper queries
# ══════════════════════════════════════════════════════════════════════════════
def get_active_providers(session: Session):
    return session.query(Provider).filter_by(is_active=1).all()


def get_monthly_spend(session: Session, billing_period: str):
    """
    Returns total spend per provider for a given billing period.
    billing_period format: '2026-04'
    """
    from sqlalchemy import text
    result = session.execute(text("""
        SELECT
            p.slug,
            p.name,
            p.billing_model,
            COALESCE(i.amount_usd, 0)       AS subscription_cost,
            COALESCE(SUM(d.cost_usd), 0)    AS usage_cost,
            COALESCE(i.amount_usd, 0)
                + COALESCE(SUM(d.cost_usd), 0) AS total_cost
        FROM providers p
        LEFT JOIN invoices i
            ON i.provider_id = p.id
            AND i.billing_period = :period
        LEFT JOIN daily_usage d
            ON d.provider_id = p.id
            AND strftime('%Y-%m', d.usage_date) = :period
        WHERE p.is_active = 1
        GROUP BY p.id
        ORDER BY total_cost DESC
    """), {"period": billing_period})
    return result.fetchall()


def get_unacknowledged_alerts(session: Session):
    return (
        session.query(BudgetAlert)
        .filter_by(acknowledged=0)
        .order_by(BudgetAlert.fired_at.desc())
        .all()
    )


def get_last_sync(session: Session, provider_id: int):
    return (
        session.query(SyncLog)
        .filter_by(provider_id=provider_id)
        .order_by(SyncLog.synced_at.desc())
        .first()
    )


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    init_db()

    # Quick smoke test
    with get_session() as session:
        providers = get_active_providers(session)
        print(f"\n✅ {len(providers)} active providers seeded:")
        for p in providers:
            print(f"   {p.slug:<20} {p.billing_model:<14} {p.collection_method}")

        settings = session.query(Setting).all()
        print(f"\n✅ {len(settings)} settings seeded:")
        for s in settings:
            print(f"   {s.key:<22} = {s.value}")
