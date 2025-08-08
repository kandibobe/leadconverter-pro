"""Utility script to create database tables."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import Base, engine


def main() -> None:
    """Create all tables in the configured database."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
