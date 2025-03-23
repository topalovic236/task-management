from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
from app.models import Task
from app.database import SessionLocal
from app.routes.auth import get_current_user


