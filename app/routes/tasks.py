from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
from app.models import Task
from app.database import SessionLocal
from app.routes.auth import get_current_user
from app.schemas import TaskCreate


router = APIRouter(
    
    tags=['task']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[str, Depends(get_current_user)]

@router.post('/task', status_code=status.HTTP_201_CREATED)
async def create_task(user : user_dependency, db:db_dependency, task_create : TaskCreate):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    existing_task = db.query(Task).filter(Task.title == task_create.title, Task.user_id == user.get('id')).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Task already exists")

    task_model = Task(**task_create.model_dump(), user_id=user.get('id'))

    db.add(task_model)
    db.commit()
    return {'message' : "Task successfully created"}


