from fastapi import FastAPI
from app.database import SessionLocal, engine
from app.models import Base
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router
from app.routes.admin import router as admin_router
from app.routes.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def test():
    return {"Hello!"}

app.include_router(auth_router,  prefix="/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/task", tags=["task"])
app.include_router(admin_router, prefix="/admin", tags=['admin'])
app.include_router(users_router, prefix="/users",tags=['users'])

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

