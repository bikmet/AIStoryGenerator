from sqlalchemy import create_engine #create engine which wraps around the database
from sqlalchemy.orm import sessionmaker #create session so we can interact with the engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #so all models inherits from the base class

def get_db(): #give access to a database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)