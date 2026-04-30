from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


@lru_cache
def get_engine():
    return create_engine(
        url=SQLALCHEMY_DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False},
    )


_session_locale = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)


def get_db():
    db = _session_locale()
    try:
        yield db
    finally:
        db.close()
