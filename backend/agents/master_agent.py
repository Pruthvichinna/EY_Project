from backend.agents import verification_agent, underwriting_agent, sales_agent, sanction_agent
from backend.apis import mock_offermart, mock_crm
import os

def orchestrate_application(customer_id, amount, tenure_months, salary_slip_file=None):
    # 1. Verify customer
    v = verification_agent.verify_customer(customer_id)
    if v["status"] != "verified":
        return {"status":"error","message":"Customer not found"}

    customer = v["data"]

    # 2. Underwriting - initial (may request salary slip)
    uw = underwriting_agent.evaluate_eligibility(customer, amount, tenure_months, salary_slip_provided=False)

    # If needs salary slip
    if uw["decision"] == "needs_salary_slip":
        if not salary_slip_file:
            return {"status":"pending","action":"upload_salary_slip","message":"Salary slip required"}
        # save salary slip
        save_path = os.path.join("backend","uploads","salary_slips", os.path.basename(salary_slip_file))
        # For demo, assume file already saved by upload endpoint; pass salary from customer
        salary_val = customer.get("salary")
        uw2 = underwriting_agent.evaluate_eligibility(customer, amount, tenure_months, salary_slip_provided=True, salary_value=salary_val)
        if uw2["decision"] == "approve":
            loan_details = {"amount": amount, "tenure": tenure_months, "emi": uw2["emi"], "interest_rate": uw2["interest_rate"]}
            pdf = sanction_agent.create_sanction_letter(customer, loan_details)
            return {"status":"approved","pdf":pdf,"loan_details":loan_details}
        else:
            return {"status":"rejected","reason":uw2.get("reason","")}
    elif uw["decision"] == "approve":
        loan_details = {"amount": amount, "tenure": tenure_months, "emi": uw["emi"], "interest_rate": uw["interest_rate"]}
        pdf = sanction_agent.create_sanction_letter(customer, loan_details)
        return {"status":"approved","pdf":pdf,"loan_details":loan_details}
    else:
        return {"status":"rejected","reason":uw.get("reason","")}
