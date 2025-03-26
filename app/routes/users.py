from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from app.routes.auth import get_current_user
from app.database import SessionLocal
from app.schemas import UserUpdate
from sqlalchemy.orm import Session
from app.models import Task,User


router = APIRouter(
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put('/user/{user_id}')
async def update_user(user_id: int, user_update: UserUpdate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    print(f"Authenticated user: {user}")  
    print(f"Trying to update user with ID: {user_id}")

    user_to_update = db.query(User).filter(User.id == user_id).first()

    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get('role') == 'admin' or user.get('id') == user_id:
            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(user_to_update, key, value)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    db.commit()
    db.refresh(user_to_update)

    return {"message": "User updated successfully"}


@router.delete('/user/{user_id}')
async def delete_user(user_id : int, user : dict = Depends(get_current_user), db : Session = Depends(get_db)):

    user_to_delete = db.query(User).filter(User.id == user_id).first()

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.get('role') != 'admin' and user.get('id') != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    db.delete(user_to_delete)
    db.commit()

    return {"message": "User deleted successfully"}

    


