import streamlit as st
import requests
import os
import base64

# Backend base URL
BACKEND = "http://localhost:8000"

st.set_page_config(page_title="Agentic AI Loan Officer", layout="wide")
st.title("Agentic AI Loan Officer — Demo")

# Simple customers list (matches backend/data/customers.json)
CUSTOMERS = ["C001","C002","C003","C004","C005","C006","C007","C008","C009","C010"]

if "chat" not in st.session_state:
    st.session_state.chat = []

col1, col2 = st.columns([2,1])

with col2:
    st.header("Applicant")
    customer_id = st.selectbox("Customer ID", CUSTOMERS)
    amount = st.number_input("Loan Amount (₹)", min_value=1000.0, value=50000.0, step=1000.0, format="%.0f")
    tenure = st.selectbox("Tenure (months)", [12,24,36,48])
    uploaded_file = st.file_uploader("Upload salary slip (optional)", type=["pdf","png","jpg","jpeg"])

    if st.button("Apply for Loan"):
        st.session_state.chat.append(("user", f"I request ₹{int(amount)} for {tenure} months."))

        files = None
        if uploaded_file:
            # Build multipart file tuple: (filename, bytes, content_type)
            file_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type if hasattr(uploaded_file, "type") else "application/octet-stream"
            files = {"file": (uploaded_file.name, file_bytes, content_type)}

        # Send request to backend
        try:
            resp = requests.post(
                f"{BACKEND}/master/apply",
                params={"customer_id": customer_id, "amount": amount, "tenure": tenure},
                files=files
            )
        except Exception as e:
            st.session_state.chat.append(("bot", f"Error connecting to backend: {e}"))
            resp = None

        # --- handle backend response robustly ---
        if resp is None:
            st.session_state.chat.append(("bot", "Error connecting to backend"))
        else:
            # Debug info (comment out or remove for production)
            # st.write("DEBUG status:", resp.status_code)
            # st.write("DEBUG text (first 500 chars):", (resp.text[:500] if resp.text else ""))

            try:
                data = resp.json()
            except Exception as e:
                st.session_state.chat.append(("bot", f"Invalid JSON response from backend: {e}"))
                data = {"status": "error", "message": "backend invalid response"}

            # Handle approved + base64 PDF payload
            if data.get("status") == "approved" and data.get("pdf_base64"):
                loan = data.get("loan_details", {})
                emi = loan.get("emi", "N/A")
                st.session_state.chat.append(("bot", f"✅ Approved! EMI: ₹{emi}. Sanction letter ready."))

                # Decode base64 to bytes and create Streamlit download button
                try:
                    pdf_bytes = base64.b64decode(data["pdf_base64"])
                    filename = data.get("pdf_filename", "sanction_letter.pdf")
                    # show a download button
                    st.download_button(
                        label="📄 Download Sanction Letter",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf"
                    )
                    # Optionally display a small message in chat
                    st.session_state.chat.append(("bot", f"Sanction letter generated: {filename}"))
                except Exception as e:
                    st.session_state.chat.append(("bot", f"Error preparing download: {e}"))

            elif data.get("status") == "pending" and data.get("action") == "upload_salary_slip":
                st.session_state.chat.append(("bot","⚠️ Salary slip required to continue. Please upload and re-try."))
            elif data.get("status") == "rejected":
                st.session_state.chat.append(("bot", f"❌ Rejected: {data.get('reason','Not eligible')}"))
            elif data.get("status") == "error":
                st.session_state.chat.append(("bot", f"❌ Error: {data.get('message','Unknown error')}"))
            else:
                st.session_state.chat.append(("bot", f"Error processing request: {data}"))

with col1:
    st.header("Conversation")
    for who, message in st.session_state.chat:
        if who == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Bot:** {message}")
    st.markdown("---")
    st.write("Demo notes: Run backend (uvicorn) and run this Streamlit app. Upload salary slip only if requested.")
