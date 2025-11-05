from app.tools.calculators import compound, loan_payment

def test_compound():
    out = compound(1000, 0.05, 1, n=1)
    assert round(out["future_value"],2) == 1050.0

def test_loan():
    out = loan_payment(1200, 0.12, 1, n=12)
    assert "payment" in out and out["payment"] > 0