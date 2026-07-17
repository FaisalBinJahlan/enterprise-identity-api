from sqlalchemy import text
from core.database import SessionLocal


def test_connection():
    db = SessionLocal()

    try:
        result = db.execute(text("SELECT version();"))
        postgres_version = result.scalar()

        print("Database connection successful.")
        print(f"PostgreSQL version: {postgres_version}")

    except Exception as error:
        print("Database connection failed.")
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    test_connection()