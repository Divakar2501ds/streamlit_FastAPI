from datetime import datetime
from sqlalchemy import create_engine,Column, Integer, String, Boolean, DateTime ,func ,ForeignKey
from sqlalchemy.orm import sessionmaker ,declarative_base ,relationship ,Session, Mapped, mapped_column

DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/streamlit_fastapi"
engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
