import time

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import DATABASE_URL


def create_engine_with_retry(database_url, retries=5, delay=5):
    while retries > 0:
        try:
            engine = create_engine(database_url)
            connection = engine.connect()
            connection.close()
            return engine
        except Exception as e:
            print(f"Database connection failed: {e}")
            retries -= 1
            time.sleep(delay)

    raise Exception("Could not connect to the database after multiple retries")


engine = create_engine_with_retry(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
