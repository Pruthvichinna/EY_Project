def compute_emi(amount: float, tenure_months: int, annual_rate_percent: float):
    r = annual_rate_percent / 12 / 100
    n = tenure_months
    if r == 0:
        emi = amount / n
    else:
        emi = (amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return round(emi)
