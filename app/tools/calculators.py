def compound(principal: float, rate: float, years: int, n: int = 12):
    amount = principal * (1 + rate / n) ** (n * years)
    return {"principal": principal, "rate": rate, "years": years, "n": n, "future_value": round(amount, 2)}

def loan_payment(principal: float, rate: float, years: int, n: int = 12):
    r = rate / n
    N = years * n
    if r == 0:
        pmt = principal / N
    else:
        pmt = principal * (r * (1 + r) ** N) / ((1 + r) ** N - 1)
    return {"principal": principal, "rate": rate, "years": years, "payment": round(pmt, 2), "periods": N}