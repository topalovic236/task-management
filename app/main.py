from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from routes.auth import router as auth_router
app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["/auth"])

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
