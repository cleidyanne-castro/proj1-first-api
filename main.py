from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from auth import (
    security,
    signup_user,
    login_user,
    get_current_user,
    logout_user,
)
from pydantic import BaseModel, Field

from database import (
    init_db,
    get_tasks as db_get_tasks,
    get_task as db_get_task,
    create_task as db_create_task,
    update_task as db_update_task,
    delete_task as db_delete_task,
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    done: bool = False


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


class Task(BaseModel):
    id: int
    title: str
    done: bool

class AuthRequest(BaseModel):
    email: str
    password: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Task CRUD API",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "My first backend API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(auth_data: AuthRequest):
    if not auth_data.email or not auth_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    response = signup_user(auth_data.email, auth_data.password)

    return {
        "user": {
            "id": response.user.id,
            "email": response.user.email,
            "created_at": str(response.user.created_at),
        }
    }


@app.post("/auth/login")
def login(auth_data: AuthRequest):
    if not auth_data.email or not auth_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    response = login_user(auth_data.email, auth_data.password)

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "token_type": "bearer",
    }

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user = get_current_user(credentials)

    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at),
    }

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return db_get_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = db_get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found"},
        )

    return task


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def add_task(task_data: TaskCreate):
    return db_create_task(task_data.title.strip(), task_data.done)


@app.put("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, task_data: TaskUpdate):
    updated_task = db_update_task(task_id, task_data.title.strip(), task_data.done)

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found"},
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_task(task_id: int):
    deleted = db_delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found"},
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)