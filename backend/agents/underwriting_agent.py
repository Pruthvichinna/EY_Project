from backend.apis import mock_credit_bureau
from backend.agents.sales_agent import compute_emi

def evaluate_eligibility(customer, requested_amount, tenure_months, salary_slip_provided=False, salary_value=None):
    # fetch credit score
    score = mock_credit_bureau.get_score_sync(customer["customer_id"])
    pre_limit = customer.get("preapproved_limit", 0)
    result = {"decision": "reject", "reason": ""}

    # Rule 1: If credit score < 700 -> reject
    if score < 700:
        result["reason"] = f"Credit score {score} < 700"
        return result

    # If amount ≤ pre-approved -> approve instantly
    if requested_amount <= pre_limit:
        emi = compute_emi(requested_amount, tenure_months, annual_rate_percent=12)
        result.update({"decision":"approve","emi":emi,"interest_rate":12})
        return result

    # If amount ≤ 2x preapproved -> require salary slip and EMI<=50% salary
    if requested_amount <= 2 * pre_limit:
        if not salary_slip_provided or not salary_value:
            result["reason"] = "Salary slip required"
            result["decision"] = "needs_salary_slip"
            return result
        emi = compute_emi(requested_amount, tenure_months, annual_rate_percent=12)
        if emi <= 0.5 * float(salary_value):
            result.update({"decision":"approve","emi":emi,"interest_rate":12})
            return result
        else:
            result["reason"] = f"EMI {emi} > 50% of salary {salary_value}"
            result["decision"] = "reject"
            return result

    # If amount > 2x preapproved -> reject
    result["reason"] = f"Requested amount > 2× pre-approved limit ({pre_limit})"
    result["decision"] = "reject"
    return result
