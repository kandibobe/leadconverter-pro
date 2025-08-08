"""Utility script to create database tables."""

from backend.database import Base, engine


def main() -> None:
    """Create all tables in the configured database."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
