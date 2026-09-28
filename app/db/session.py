from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine_kwargs = {
    "pool_pre_ping": True,
}

if settings.environment == "production":
    engine_kwargs.update(
        {
            "pool_recycle": 1800,
            "pool_size": 10,
            "max_overflow": 20,
        }
    )

engine = create_engine(
    settings.database_url,
    **engine_kwargs,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()