from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Didn't put any id constraints here because the models.py is taking care of that

class UserCreate(BaseModel):
    username : str = Field(min_length=3, max_length=50)
    email : EmailStr
    password : str = Field(min_length=8, max_length=100)
    role : str


class UserUpdate(BaseModel):
    username : str | None = Field(min_length=3, max_length=50)
    email : EmailStr | None = None
    password : str | None = Field(min_length=8, max_length=100)


class User(BaseModel):
    id : int                
    username : str
    email : EmailStr
    role : str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    description : str = Field(min_length=1, max_length=300)
    completed : bool = False
    deadline : datetime | None = None

class TaskUpdate(BaseModel):
    id : int
    title : str | None = Field(default=None, min_length=1, max_length=100)
    description : str | None = Field(default=None, min_length=1, max_length=300)
    completed : bool
    deadline : datetime
    user_id : int

    class Config:
        from_attributes = True

    