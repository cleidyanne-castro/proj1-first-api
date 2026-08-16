from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response, status
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