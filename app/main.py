from fastapi import FastAPI
from pydantic import BaseModel
from app.intents import detect_intent, parse_params
from app.tools.calculators import compound, loan_payment
from app.rag.retriever import answer_with_knowledge

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