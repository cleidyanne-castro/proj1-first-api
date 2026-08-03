import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "tasks.db"

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database() -> None:
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            
            
            )
            """
        )

        cursor.execute(
            "SELECT COUNT(*) AS total FROM tasks"

        )
        result = cursor.fetchone()

        if result["total"] == 0:
            seed_tasks = [
                ("Learn FastAPI", 0),
                ("Connect API to SQLite", 0),
                ("Practice SQL queries", 0),


            ]

            cursor.executemany(
                """
                INSERT INTO tasks (title, done)
                VALUES (?, ?)
                """,
                seed_tasks,

            )

        connection.commit()
    finally:
        connection.close()