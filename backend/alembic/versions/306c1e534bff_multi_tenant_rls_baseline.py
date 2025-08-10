from alembic import op
import sqlalchemy as sa

# ревизии
revision = "multi_tenant_rls_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Расширение для gen_random_uuid()
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    # Таблица арендаторов
    op.create_table(
        "tenants",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.Text(), nullable=False, unique=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # Пример: включить RLS на будущих таблицах с tenant_id
    # Здесь мы показываем базовый каркас политики:
    #   - политика читает tenant_id из сессии (app.tenant_id)
    #   - применять будешь при создании доменных таблиц (leads, quizzes и т.д.)

    # Сама tenants обычно без RLS или с узкой политикой — оставим без RLS
    # на первых порах, чтобы админ мог видеть всех.

    # Хранимка-помощник (опционально) — не обязательно, но удобно:
    op.execute("""
    CREATE OR REPLACE FUNCTION app_current_tenant() RETURNS uuid AS $$
      SELECT NULLIF(current_setting('app.tenant_id', true), '')::uuid;
    $$ LANGUAGE SQL STABLE;
    """)


def downgrade():
    op.execute("DROP FUNCTION IF EXISTS app_current_tenant();")
    op.drop_table("tenants")
    op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
