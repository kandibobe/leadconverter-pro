from contextlib import contextmanager

from app.database import get_db, init_db
from app.models import Quiz

@contextmanager
def db_for(tenant: str):
    gen = get_db(tenant)
    db = next(gen)
    try:
        yield db
    finally:
        try:
            next(gen)
        except StopIteration:
            pass


def main() -> None:
    init_db()
    with db_for("org1") as db:
        db.add(Quiz(title="Quiz 1", description="", tenant_id="org1"))
        db.commit()
    with db_for("org2") as db:
        db.add(Quiz(title="Quiz 2", description="", tenant_id="org2"))
        db.commit()
    with db_for("org1") as db:
        titles = [q.title for q in db.query(Quiz).all()]
        print("Org1 sees:", titles)
    with db_for("org2") as db:
        titles = [q.title for q in db.query(Quiz).all()]
        print("Org2 sees:", titles)

if __name__ == "__main__":
    main()
