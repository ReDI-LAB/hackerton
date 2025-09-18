from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from rag import generate_content

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/api/hello")
async def get_message():
    return {"message": "Hello from ReDI 🎉"}


class ChatRequest(BaseModel):
    question: str
    history: list[dict] = []


@app.post("/api/chat")
async def chat(req: ChatRequest):
    # Mock RAG: just echo the question
    # return {"answer": f"You asked: '{req.question}'. (RAG coming soon 🤖)"}
    messages = req.history + [
        {"role": "user", "content": req.question}
    ]
    answer = generate_content(messages)
    return {"answer": answer}
