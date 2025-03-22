from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
