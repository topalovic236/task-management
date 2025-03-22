from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str


class UserUpdate(BaseModel):
    username : str | None = None
    email : EmailStr | None = None
    password : str | None = None


class User(BaseModel):
    id : int
    username : str
    email : EmailStr
    is_active = bool

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title : str
    description : str
    completed : bool = False
    deadline : datetime | None = None

class TaskUpdate(BaseModel):
    id : int
    title : str
    description : str
    completed : bool
    deadline : datetime
    user_id : int

    class Config:
        from_attributes = True

    