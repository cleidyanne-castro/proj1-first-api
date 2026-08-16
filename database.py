import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


@contextmanager
def get_connection():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                );
                """
            )

            cur.execute("SELECT COUNT(*) AS count FROM tasks;")
            count = cur.fetchone()["count"]

            if count == 0:
                cur.executemany(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, %s);
                    """,
                    [
                        ("Learn FastAPI", False),
                        ("Practice SQLite CRUD", True),
                        ("Containerize with Postgres", False),
                    ],
                )

        conn.commit()


def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id;")
            return cur.fetchall()


def get_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s;",
                (task_id,),
            )
            return cur.fetchone()


def create_task(title: str, done: bool = False):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done;
                """,
                (title, done),
            )
            task = cur.fetchone()

        conn.commit()
        return task


def update_task(task_id: int, title: str, done: bool):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                RETURNING id, title, done;
                """,
                (title, done, task_id),
            )
            task = cur.fetchone()

        conn.commit()
        return task


def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id;
                """,
                (task_id,),
            )
            deleted = cur.fetchone()

        conn.commit()
        return deleted is not None