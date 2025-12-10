# Agentic Loan Officer - Demo

## Setup
1. Create and activate virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\activate`

2. Install deps:
   - `pip install fastapi uvicorn streamlit fpdf2 python-multipart requests`

## Run backend
From project root:
`uvicorn backend.main:app --reload --port 8000`

## Run Streamlit UI
`streamlit run streamlit_app/app.py`

Open Streamlit UI at the URL it shows (usually http://localhost:8501)

## Notes
- This is a demo with mock APIs and synthetic data.
- Salary slip handling is simplified for demo purposes.
