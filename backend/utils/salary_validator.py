import os

def validate_salary_slip(file_path, expected_salary):
    # For demo, we simply check file exists and return True if expected_salary is numeric > 0.
    # Real implementation would OCR and extract salary.
    if not os.path.exists(file_path):
        return False
    try:
        return float(expected_salary) > 0
    except:
        return False
