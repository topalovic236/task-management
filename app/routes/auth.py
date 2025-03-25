from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from ..schemas import UserCreate,  Token
import os


router = APIRouter(
    
    tags = ['auth']
)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRES_DELTA = int(os.getenv("ACCESS_TOKEN_EXPIRES", 30))

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreate):

    #Checking if user already exists
    
    existing_user = db.query(User).filter(
        (User.email == create_user_request.email) | 
        (User.username == create_user_request.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    hashed_password = bcrypt_context.hash(create_user_request.password)
    

    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        hashed_password=hashed_password,
        
        
    )
    db.add(create_user_model)
    db.commit()

    return {
        "id": create_user_model.id,
        "username": create_user_model.username,
        "email": create_user_model.email
    }

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    
       
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )

    
    
    access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    return {"access_token": access_token, "token_type": "bearer"}

#Helper functions to create access token and to get user which is implemented above

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate user"
            )
        
        return {"username": username, "id": user_id, "role": user_role}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate user"
        )