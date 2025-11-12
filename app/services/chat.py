# app/services/chat.py
from typing import List, Dict
from app.intents import detect_intent, parse_params
from app.tools.calculators import compound, loan_payment
from app.rag.retriever import answer_with_knowledge

def chat(message: str, history: list[dict]) -> dict:
    """
    Gère la logique de conversation utilisateur → réponse chatbot.
    Combine intents, calculs financiers et recherche dans la base de connaissance.
    """

    # 1. Détection d’intention
    intent = detect_intent(message)

    # 2. Traitement selon le type d’intent
    if intent == "calc:compound":
        params = parse_params(message)
        result = compound(**params)
        reply = (
            f"💰 **Intérêt composé**\n"
            f"Montant initial : {result['principal']:.2f}\n"
            f"Taux : {result['rate']*100:.2f}%\n"
            f"Durée : {result['years']} ans\n"
            f"Valeur future estimée : **{result['future_value']:.2f}**"
        )

    elif intent == "calc:loan":
        params = parse_params(message)
        result = loan_payment(**params)
        reply = (
            f"**Mensualité de prêt**\n"
            f"Montant : {result['principal']:.2f}\n"
            f"Taux : {result['rate']*100:.2f}%\n"
            f"Durée : {result['years']} ans\n"
            f"Paiement mensuel : **{result['payment']:.2f}**"
        )

    else:
        # Intent RAG (recherche de connaissances)
        ans = answer_with_knowledge(message)
        reply = ans["answer"]
        sources = ans.get("sources", [])
        if sources:
            reply += "\n\n *Sources :*\n" + "\n".join(f"- {s}" for s in sources)

    # 3. Mettre à jour l’historique
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]

    # 4. Retourner la réponse pour l’API
    return {
        "reply": reply,
        "history": history,
        "intent": intent,
    }