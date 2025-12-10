import os
import shutil
import base64
from urllib.parse import quote

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# import your routers and agent orchestrator
from backend.apis import mock_crm, mock_credit_bureau, mock_offermart
from backend.agents import master_agent

# App init
app = FastAPI(title="Agentic Loan Officer - Demo")

# Include mock API routers
app.include_router(mock_crm.router)
app.include_router(mock_credit_bureau.router)
app.include_router(mock_offermart.router)

# CORS: allow all for demo (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload / output directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "salary_slips")
SANCTION_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SANCTION_DIR, exist_ok=True)


@app.post("/master/apply")
async def apply_loan(customer_id: str, amount: float, tenure: int, file: UploadFile = File(None)):
    """
    Orchestrates loan application and returns JSON.
    If approved, returns PDF as base64 bytes + filename so Streamlit can provide a direct download button.
    """
    # Save uploaded file (if provided)
    saved_path = None
    if file:
        filename = f"{customer_id}_{file.filename}"
        saved_path = os.path.join(UPLOAD_DIR, filename)
        with open(saved_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    # Orchestrate using master agent (this returns dict with status / pdf path / loan_details or pending/rejected)
    result = master_agent.orchestrate_application(customer_id, amount, tenure, salary_slip_file=saved_path)

    # If approved and we received a filesystem path for pdf, read and encode it
    if isinstance(result, dict) and result.get("status") == "approved" and result.get("pdf"):
        pdf_path = result.get("pdf")  # filesystem path like backend/uploads/sanction_...pdf
        # normalize backslashes for safety (Windows)
        pdf_path = pdf_path.replace("\\", os.path.sep)
        if os.path.isabs(pdf_path) is False:
            # if relative path, make absolute relative to project root
            # sometimes sanction_agent returns path relative to project root; ensure we can locate it
            candidate = os.path.join(os.getcwd(), pdf_path)
            if os.path.exists(candidate):
                pdf_path = candidate

        if os.path.exists(pdf_path):
            # Read bytes and base64 encode
            with open(pdf_path, "rb") as pf:
                pdf_bytes = pf.read()
            pdf_b64 = base64.b64encode(pdf_bytes).decode()
            # return a clean payload (do not expose raw filesystem path)
            return {
                "status": "approved",
                "loan_details": result.get("loan_details", {}),
                "pdf_filename": os.path.basename(pdf_path),
                "pdf_base64": pdf_b64
            }
        else:
            # PDF path missing on disk — return error
            return {"status": "error", "message": "sanction PDF not found on server"}
    else:
        # return whatever the orchestrator returned (pending/rejected/error)
        return result


@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Simple endpoint to upload salary-slip file only.
    Returns the saved path (filesystem) as demo convenience.
    """
    filename = file.filename
    saved_path = os.path.join(UPLOAD_DIR, filename)
    with open(saved_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "uploaded", "path": saved_path}


@app.get("/sanction/pdf")
def get_pdf(path: str):
    """
    Optional: serve PDF file if needed via URL (not used by Streamlit download_button approach).
    Keep for manual access/debugging.
    """
    # Normalize separators
    safe_path = path.replace("\\", os.path.sep)
    if os.path.exists(safe_path):
        return FileResponse(safe_path, media_type="application/pdf", filename=os.path.basename(safe_path))
    return {"error": "file not found"}
