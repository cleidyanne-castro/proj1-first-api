from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "My first backend API is running!"}

@app.get("/health")
def health():
    return {"status": "Ok"}
