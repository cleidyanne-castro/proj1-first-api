# Task CRUD API - FastAPI + PostgreSQL + Docker

This project is a simple CRUD API for managing tasks. It was built as part of the FlyRank Backend Track assignment sequence.

The API started with local storage and was later migrated to a real PostgreSQL database running in Docker. The full stack can now be started with one command using Docker Compose.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- psycopg

## Features

- List all tasks
- Get one task by id
- Create a new task
- Update an existing task
- Delete a task
- PostgreSQL database running in Docker
- Automatic table creation on startup
- Seed data inserted only when the table is empty
- Parameterized SQL queries
- Persistent database volume with Docker Compose

## Project Structure

```text
.
├── main.py
├── database.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env.example
├── .dockerignore
├── .gitignore
└── docs/
```

## Environment Variables

Create a `.env` file based on `.env.example`.

```bash
cp .env.example .env
```

For local development, the database URL is:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

Inside Docker Compose, the API connects to the database using the service name `db`:

```env
DATABASE_URL=postgresql://postgres:dev@db:5432/tasks
```

The real `.env` file is ignored by Git and should not be committed.

## Run With Docker Compose

Start the API and PostgreSQL database:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:3000
```

Check the API:

```bash
curl -i http://localhost:3000/tasks
```

## Run Locally Without Dockerizing the API

If PostgreSQL is already running in Docker on `localhost:5432`, install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the API locally:

```bash
python -m uvicorn main:app --port 3000
```

## Database

PostgreSQL runs in a Docker container using the official `postgres:16` image.

The application creates the `tasks` table automatically on startup if it does not exist:

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  done BOOLEAN NOT NULL DEFAULT FALSE
);
```

The app seeds three example tasks only when the table is empty:

```text
Learn FastAPI
Practice SQLite CRUD
Containerize with Postgres
```

## Persistence

The database uses a Docker volume named `taskdata`.

This means task data survives after stopping and starting the stack again:

```bash
docker compose down
docker compose up
```

## API Endpoints

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/` | API home route | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get one task by id | 200 |
| POST | `/tasks` | Create a new task | 201 |
| PUT | `/tasks/{id}` | Update an existing task | 200 |
| DELETE | `/tasks/{id}` | Delete a task | 204 |

## Example Requests

List all tasks:

```bash
curl -i http://localhost:3000/tasks
```

Get one task:

```bash
curl -i http://localhost:3000/tasks/1
```

Create a task:

```bash
curl -i -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Created from Docker Compose", "done": false}'
```

Update a task:

```bash
curl -i -X PUT http://localhost:3000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task", "done": true}'
```

Delete a task:

```bash
curl -i -X DELETE http://localhost:3000/tasks/1
```

Unknown task example:

```bash
curl -i http://localhost:3000/tasks/999
```

Expected result:

```json
{
  "detail": {
    "error": "Task not found"
  }
}
```

## Database Screenshot

The screenshot below shows the `tasks` table and rows inside the PostgreSQL container.

![PostgreSQL database screenshot](docs/postgres-database.png)

## Clean Clone Check

From a clean clone, the project can be started with:

```bash
git clone https://github.com/cleidyanne-castro/proj1-first-api.git
cd proj1-first-api
cp .env.example .env
docker compose up --build
```

Then test:

```bash
curl -i http://localhost:3000/tasks
```

Expected result: `200 OK` with the seeded tasks.

## Assignment Checklist

- PostgreSQL runs in a Docker container
- API connects to PostgreSQL using `DATABASE_URL`
- `.env` is ignored by Git
- `.env.example` is committed
- `tasks` table is created automatically
- Seed data is inserted only when the table is empty
- All CRUD endpoints work against PostgreSQL
- Queries use parameters instead of string interpolation
- Docker Compose starts the API and database together
- Database data persists through Docker volume
- README includes setup instructions, endpoints, curl example, and database screenshot

## Submission

Repository:

```text
https://github.com/cleidyanne-castro/proj1-first-api
```

## Authentication with Supabase

This project uses Supabase Auth as the identity provider for user authentication.

The API supports sign up, login, logout, public routes, and protected routes using Bearer tokens.

### Auth Environment Variables

Create a `.env` file based on `.env.example`:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
PORT=3000
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

The real `.env` file is ignored by Git and must not be committed.

### Auth Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/signup` | Create a user account | No |
| POST | `/auth/login` | Log in and return access and refresh tokens | No |
| POST | `/auth/logout` | Log out the current user session | Yes |
| GET | `/public/info` | Public route available to anyone | No |
| GET | `/protected/profile` | Return the authenticated user's profile | Yes |
| GET | `/protected/dashboard` | Example protected dashboard route | Yes |

Protected routes require this header:

```text
Authorization: Bearer <access_token>
```

### Signup

```bash
curl -i -X POST http://localhost:3000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"your.email@gmail.com","password":"password123"}'
```

### Login

```bash
curl -i -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your.email@gmail.com","password":"password123"}'
```

### Public Route

```bash
curl -i http://localhost:3000/public/info
```

### Protected Profile

```bash
curl -i http://localhost:3000/protected/profile \
  -H "Authorization: Bearer <access_token>"
```

### Protected Dashboard

```bash
curl -i http://localhost:3000/protected/dashboard \
  -H "Authorization: Bearer <access_token>"
```

### Logout

```bash
curl -i -X POST http://localhost:3000/auth/logout \
  -H "Authorization: Bearer <access_token>"
```

### Swagger UI

Swagger UI is available at:

```text
http://localhost:3000/docs
```

Click **Authorize**, paste the access token, and run protected routes directly from the browser.

![Swagger auth screenshot](docs/swagger-auth.png)