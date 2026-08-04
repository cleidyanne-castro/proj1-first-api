# Task CRUD API with FastAPI and SQLite

This project started as my first FastAPI backend with two basic endpoints: a home route and a health check.

It was then expanded into a complete CRUD API for tasks and migrated from in-memory storage to a persistent SQLite database. The API endpoints remain consistent while the storage layer now saves data in `tasks.db`, allowing tasks to survive server restarts.

## Project evolution

### Assignment 1

The first version included:

- `GET /`
- `GET /health`

### Assignment 2

The project was expanded with:

- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

Task storage was migrated from a Python list in memory to SQLite.