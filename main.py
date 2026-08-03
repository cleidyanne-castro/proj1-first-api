from contextlib import asynccontextmanager
from database import get_connection, initialize_database
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Task CRUD API",
    lifespan=lifespan,
)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


class Task(BaseModel):
    id: int
    title: str
    done: bool


tasks: list[dict] = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Connect the API to SQLite", "done": False},
]


@app.get("/")
def home():
    return {"message": "My first backend API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title, done
            FROM tasks
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"]),
            }
            for row in rows
        ]

    finally:
        connection.close()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task_data: TaskCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            (task_data.title, 0),
        )

        connection.commit()

        new_task_id = cursor.lastrowid

        cursor.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = ?
            """,
            (new_task_id,),
        )

        row = cursor.fetchone()

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
        }

    finally:
        connection.close()


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["done"] = task_data.done
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )