from backend.utils.pdf_generator import generate_sanction_pdf
import os

def create_sanction_letter(customer, loan_details):
    pdf_path = generate_sanction_pdf(customer, loan_details)
    # return relative URL path for download (we'll serve from static)
    return pdf_path
