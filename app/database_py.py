from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app_lite.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit =False,autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()