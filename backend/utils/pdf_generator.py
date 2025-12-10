import os
from fpdf import FPDF
from datetime import datetime

UPLOAD_DIR = "backend/uploads/salary_slips"
SANCTION_DIR = "backend/uploads"

def generate_sanction_pdf(customer, loan_details, filename=None):
    if not filename:
        filename = f"sanction_{customer['customer_id']}_{int(datetime.utcnow().timestamp())}.pdf"
    path = os.path.join(SANCTION_DIR, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sanction Letter", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(200, 8, txt=f"Customer: {customer['name']} ({customer['customer_id']})", ln=True)
    pdf.cell(200, 8, txt=f"Address: {customer['address']}", ln=True)
    pdf.cell(200, 8, txt=f"Loan Amount: Rs {loan_details['amount']}", ln=True)
    pdf.cell(200, 8, txt=f"Tenure (months): {loan_details['tenure']}", ln=True)
    pdf.cell(200, 8, txt=f"Interest Rate: {loan_details.get('interest_rate','N/A')}%", ln=True)
    pdf.cell(200, 8, txt=f"Monthly EMI (approx): Rs {loan_details.get('emi','N/A')}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 8, txt="This is a system-generated sanction letter for demonstration purposes only.")
    pdf.output(path)
    return path
