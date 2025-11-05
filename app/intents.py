import re

def detect_intent(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["intérêt composé","interets composés","compound"]):
        return "calc:compound"
    if any(k in t for k in ["mensualité","monthly payment","loan","prêt","pret"]):
        return "calc:loan"
    return "rag"

def parse_params(text: str):
    nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[\.,]\d+)?", text)]
    # Heuristique simple: [montant, taux%, années]
    if len(nums) >= 3:
        return {"principal": nums[0], "rate": nums[1]/100.0, "years": int(round(nums[2]))}
    return {"principal": 1000.0, "rate": 0.05, "years": 5}