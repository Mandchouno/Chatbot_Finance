import re

def detect_intent(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["intérêt composé","interets composés","compound"]):
        return "calc:compound"
    if any(k in t for k in ["mensualité","monthly payment","loan","prêt","pret"]):
        return "calc:loan"
    return "rag"

import re

def parse_params(text: str):
    t = text.lower()

    # Valeur par défaut
    principal, rate, years = 1000.0, 0.05, 5

    # Taux : cherche un nombre suivi de %
    rate_match = re.search(r"(\d+(?:[\.,]\d+)?)\s*%", t)
    if rate_match:
        rate = float(rate_match.group(1).replace(",", ".")) / 100.0

    # Années : cherche un nombre suivi de "an" ou "année"
    year_match = re.search(r"(\d+(?:[\.,]\d+)?)\s*(ans|an|année|années)", t)
    if year_match:
        years = float(year_match.group(1))

    # Montant : cherche un nombre suivi de $ ou mots-clés
    principal_match = re.search(r"(\d+(?:[\.,]\d+)?)\s*(\$|usd|dollar|euros?)", t)
    if principal_match:
        principal = float(principal_match.group(1).replace(",", "."))

    return {"principal": principal, "rate": rate, "years": int(round(years))}