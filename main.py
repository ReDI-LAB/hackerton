from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import re

from rag import generate_content

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# === Dictionary of forms ===
FORMS = {
    "Wohnsitzanmeldung": "Anmeldung bei der Meldebehörde",
    "Wohnsitzabmeldung": "Abmeldung bei der Meldebehörde",
    "Wohnsitzumzugsmeldung": "Anmeldung bei der Meldebehörde - Umzugsmeldung",
    "kindergeld": "Kindergeld Formular",
    "Linderzuschlag": "Kinderzuschlag Formular",
    "GewA 1 - Gewerbe-Anmeldung": "GewA 1 - Gewerbe-Anmeldung",
    "GewA 2 - Gewerbe-Ummeldung": "GewA 2 - Gewerbe-Ummeldung",
    "GewA 3 - Gewerbe-Abmeldung": "GewA 3 - Gewerbe-Abmeldung",
}


@app.get("/")
async def read_root():
    return FileResponse(os.path.join("static", "index.html"))


class SearchRequest(BaseModel):
    query: str


@app.get("/api/hello")
async def get_message():
    return {"message": "Hello from ReDI 🎉"}


@app.post("/api/search_form")
async def search_form(req: SearchRequest):
    query_lower = req.query.lower()
    matches = []
    for key, form_name in FORMS.items():
        if re.search(re.escape(query_lower), key.lower()):
            matches.append(form_name)

    if matches:
        return {"forms": matches}
    else:
        return {"forms": []}

class ChatRequest(BaseModel):
    question: str
    history: list[dict] = []


@app.post("/api/chat")
async def chat(req: ChatRequest):
    messages = req.history + [
        {"role": "user", "content": req.question}
    ]
    answer = generate_content(messages)
    return {"answer": answer}
