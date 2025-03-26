from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from app.routes.auth import get_current_user
from app.database import SessionLocal
from app.schemas import UserUpdate
from sqlalchemy.orm import Session
from app.models import Task,User

router = APIRouter(
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated(Session, Depends(get_db))
user_dependency = Annotated(str, Depends(get_current_user))




