# backend/app/db/migrations/versions/20250810_000001_rls_core.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, INET

revision = "20250810_000001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")  # для PII-шифрования

    op.create_table(
        "tenants",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.Text(), nullable=False, unique=True),
        sa.Column("plan", sa.Text(), nullable=False),
        sa.CheckConstraint("plan in ('basic','pro','enterprise')"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("email_enc", sa.LargeBinary(), nullable=False),  # pgp_sym_encrypt(email)
        sa.Column("email_deterministic", sa.Text(), nullable=False, unique=True),  # digest(email||salt, 'sha256')
        sa.Column("role", sa.Text(), nullable=False),
        sa.CheckConstraint("role in ('owner','admin','member')"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "lead_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("lead_id", UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("payload", sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("ts", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_lead_events_tenant_lead_ts", "lead_events", ["tenant_id", "lead_id", "ts"])

    op.execute("""
    CREATE MATERIALIZED VIEW leads AS
    SELECT DISTINCT ON (lead_id)
      tenant_id, lead_id,
      (SELECT jsonb_object_agg(e.event_type, e.payload)
         FROM lead_events e WHERE e.lead_id = le.lead_id AND e.tenant_id = le.tenant_id) AS state
    FROM lead_events le
    ORDER BY lead_id, ts DESC;
    """)
    op.execute("CREATE UNIQUE INDEX ON leads(tenant_id, lead_id);")

    # Consent store по §25 TDDDG
    op.create_table(
        "consent_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("tenant_id", UUID(as_uuid=True), nullable=False),
        sa.Column("user_agent", sa.Text()),
        sa.Column("ip", INET()),
        sa.Column("consent_id", UUID(as_uuid=True), nullable=False),
        sa.Column("policy_version", sa.Text(), nullable=False),
        sa.Column("choice", sa.dialects.postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("ts", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_consent_tenant_ts", "consent_events", ["tenant_id", "ts"])

    # Включаем RLS и политики через current_setting('app.tenant_id')
    for t in ("lead_events", "consent_events"):
        op.execute(f"ALTER TABLE {t} ENABLE ROW LEVEL SECURITY;")
        op.execute(f"""
        CREATE POLICY tenant_isolation_{t} ON {t}
        USING (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid)
        WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid);
        """)
    # опционально FORCE RLS
    for t in ("lead_events", "consent_events"):
        op.execute(f"ALTER TABLE {t} FORCE ROW LEVEL SECURITY;")
