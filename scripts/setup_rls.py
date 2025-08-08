"""Enable basic row-level security for multi-tenant isolation."""

from sqlalchemy import text
from backend.database import engine


def main() -> None:
    """Create RLS policies for tenant isolation on core tables."""
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE leads ENABLE ROW LEVEL SECURITY"))
        conn.execute(text("ALTER TABLE leads FORCE ROW LEVEL SECURITY"))
        conn.execute(
            text(
                "CREATE POLICY IF NOT EXISTS tenant_isolation_leads ON leads USING (tenant_id = current_setting('backend.tenant_id')::text)"
            )
        )
        conn.execute(text("ALTER TABLE quizzes ENABLE ROW LEVEL SECURITY"))
        conn.execute(text("ALTER TABLE quizzes FORCE ROW LEVEL SECURITY"))
        conn.execute(
            text(
                "CREATE POLICY IF NOT EXISTS tenant_isolation_quizzes ON quizzes USING (tenant_id = current_setting('backend.tenant_id')::text)"
            )
        )


if __name__ == "__main__":
    main()
