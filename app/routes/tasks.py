from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
from app.models import Task
from app.database import SessionLocal
from app.routes.auth import get_current_user
from app.schemas import TaskCreate, TaskUpdate


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


@router.get('/task/{task_id}')
async def get_task(user : user_dependency, db: db_dependency, task_id : int = Path(gt=0)):
    
    if user is None:
         raise HTTPException(status_code=401, detail='Authentication failed')
    
    task_to_return = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get('id')).first()

    if not task_to_return:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_to_return
    

@router.post('/task', status_code=status.HTTP_201_CREATED)
async def create_task(user : user_dependency, db : db_dependency, task_create : TaskCreate):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    existing_task = db.query(Task).filter(Task.title == task_create.title, Task.user_id == user.get('id')).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Task already exists")

    task_model = Task(**task_create.model_dump(), user_id=user.get('id'))

    db.add(task_model)
    db.commit()
    return {'message' : "Task successfully created"}

@router.put('/task/{task_id}', status_code=status.HTTP_200_OK)
async def update_task(user : user_dependency, db : db_dependency, task_update : TaskUpdate, task_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate user")
    
    task_model = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get('id')).first()

    if task_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found" )
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task_model, key, value)

    db.commit()
    db.refresh(task_model)

    return {"message" : "Task successfully updated!", "task" : task_model}
    
@router.delete('/task/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(user : user_dependency, db : db_dependency, task_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail="Couldn't validate user")

    task_model = db.query(Task).filter(Task.id == task_id, Task.user_id == user.get('id')).first()

    if task_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(task_model)
    db.commit()

    return {"message" : "Task successfully deleted!"}
