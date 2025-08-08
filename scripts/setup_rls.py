"""Enable basic row-level security for multi-tenant isolation."""

from sqlalchemy import text
from app.database import engine


def main() -> None:
    """Create RLS policies for tenant isolation on core tables."""
    with engine.begin() as conn:
        for table in ["leads", "quizzes", "questions", "options"]:
            conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
            conn.execute(text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))
            conn.execute(text(f"DROP POLICY IF EXISTS tenant_isolation_{table} ON {table}"))
            conn.execute(
                text(
                    f"CREATE POLICY tenant_isolation_{table} ON {table} "
                    f"USING (tenant_id = current_setting('app.tenant_id')::text) "
                    f"WITH CHECK (tenant_id = current_setting('app.tenant_id')::text)"
                )
            )


if __name__ == "__main__":
    main()
