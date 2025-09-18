from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/api/hello")
async def get_message():
    return {"message": "Hello from FastAPI 🎉"}