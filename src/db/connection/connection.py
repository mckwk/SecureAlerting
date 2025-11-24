import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings

def get_connection_string() -> str:
    database_uri: str = settings.DATABASE_URI
    if not database_uri:
        load_dotenv()
        database_uri = os.getenv("DATABASE_URI", "")
    return database_uri

engine = create_engine(get_connection_string())
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]