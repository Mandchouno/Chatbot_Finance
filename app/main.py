from fastapi import FastAPI
from pydantic import BaseModel
from app.intents import detect_intent, parse_params
from app.tools.calculators import compound, loan_payment
from app.rag.retriever import answer_with_knowledge
# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI(title="Finance Copilot")

class Query(BaseModel):
    message: str
    user_id: str | None = None

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chat")
def chat(q: Query):
    intent = detect_intent(q.message)
    if intent == "calc:compound":
        return {"type": "calc", "result": compound(**parse_params(q.message))}
    if intent == "calc:loan":
        return {"type": "calc", "result": loan_payment(**parse_params(q.message))}
    ans = answer_with_knowledge(q.message)
    return {"type": "rag", "answer": ans["answer"], "sources": ans["sources"]}

from app.services.chat import chat as chat_service

app = FastAPI()

# static + templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

class ChatInput(BaseModel):
    message: str
    history: Optional[List[Dict]] = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
def chat_api(payload: ChatInput):
    result = chat_service(payload.message, payload.history or [])
    return result

if __name__ == "__main__":
    import webbrowser
    import threading
    import time
    import uvicorn

    # Fonction pour ouvrir le navigateur avec un léger délai
    def open_browser():
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:8000")

    # Lancer le navigateur dans un thread séparé
    threading.Thread(target=open_browser).start()

    # Lancer le serveur FastAPI
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)