from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings


engine = create_engine(settings.SQL_ALCHEMY_DATABASE_URI, pool_pre_ping=True)
# engine = create_engine( DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)