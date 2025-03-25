from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import User, Task
from app.database import SessionLocal
from app.routes.auth import get_current_user
from app.schemas import UserCreate, UserUpdate, TaskCreate, TaskUpdate 

router = APIRouter(

    tags=['admin']
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[str, Depends(get_current_user)]



@router.get('/users')
async def get_users(db : db_dependency, user : user_dependency):

    if user.get('role') == 'admin':
        return db.query(User).all()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not an admin! ")



@router.get("/user/{user_id}")
async def get_user(db : db_dependency, user : user_dependency, user_id : int):

    user_to_return = db.query(User).filter(User.id == user_id).first()
    if not user_to_return:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.get('role') == 'admin':
        return user_to_return
    else:
        raise HTTPException(status_code=403, detail="User is not an admin")
    


@router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db : db_dependency, user : user_dependency, user_id : int):
    user_to_delete = db.query(User).filter(User.id == user_id).first()

    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.get('role') == 'admin':
        db.delete(user_to_delete)
        db.commit()
        return {"message" : "User successfully deleted"}
    
    raise HTTPException(status_code=403, detail="User is not an admin!")