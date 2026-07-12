# First API Endpoint

This is my first backend API built with Python and FastAPI.

## Endpoints

### Home

```http
GET /
```

Response:

```json
{
  "message": "My first backend API is running!"
}
```

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

Open the API in the browser:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
```

Test with curl:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

## Technologies

* Python
* FastAPI
* Uvicorn
