from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_multi_tenant_rls_baseline"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 1) UUID-расширение (идемпотентно)
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # 2) Таблица арендаторов
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("slug", sa.Text(), nullable=False, unique=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # 3) (Опционально) Добавим tenant_id + включим RLS для доменных таблиц.
    # ВПИШИТЕ реальные имена ваших таблиц с данными арендаторов:
    tables = ("quizzes", "leads")  # <- замените на ваши (если отличаются)
    for table in tables:
        # Добавляем колонку tenant_id, если её нет
        op.execute(f'ALTER TABLE IF EXISTS {table} ADD COLUMN IF NOT EXISTS tenant_id uuid;')
        # FK на tenants
        op.execute(f'ALTER TABLE IF EXISTS {table} '
                   f'ADD CONSTRAINT IF NOT EXISTS fk_{table}_tenant '
                   f'FOREIGN KEY (tenant_id) REFERENCES tenants(id);')

        # Включаем и форсируем RLS
        op.execute(f'ALTER TABLE IF EXISTS {table} ENABLE ROW LEVEL SECURITY;')
        op.execute(f'ALTER TABLE IF EXISTS {table} FORCE ROW LEVEL SECURITY;')

        # Сбрасываем, если уже была политика с таким именем
        op.execute(f'DROP POLICY IF EXISTS {table}_isolation ON {table};')

        # Политика: видим и изменяем только строки своего арендатора
        # Тенант приходит в GUC-переменной app.tenant_id (см. FastAPI-зависимость ниже)
        op.execute(f"""
        CREATE POLICY {table}_isolation ON {table}
          USING (
            COALESCE(current_setting('app.tenant_id', true), '') <> ''
            AND tenant_id = current_setting('app.tenant_id', true)::uuid
          )
          WITH CHECK (
            COALESCE(current_setting('app.tenant_id', true), '') <> ''
            AND tenant_id = current_setting('app.tenant_id', true)::uuid
          );
        """)

        # Если в таблице уже есть данные — вам нужно будет проставить tenant_id и затем сделать NOT NULL.
        # Пример (после backfill):
        # op.execute(f"ALTER TABLE {table} ALTER COLUMN tenant_id SET NOT NULL;")

def downgrade():
    tables = ("quizzes", "leads")
    for table in tables:
        op.execute(f"DROP POLICY IF EXISTS {table}_isolation ON {table};")
        op.execute(f'ALTER TABLE IF EXISTS {table} DROP CONSTRAINT IF EXISTS fk_{table}_tenant;')
        op.execute(f'ALTER TABLE IF EXISTS {table} DROP COLUMN IF EXISTS tenant_id;')
    op.drop_table("tenants")
