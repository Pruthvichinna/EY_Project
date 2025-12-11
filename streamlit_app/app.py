import streamlit as st
import requests
import os
import base64

# Backend base URL
BACKEND = "https://agentic-backend-u1m1.onrender.com"

# -------------- PAGE CONFIG --------------
st.set_page_config(
    page_title="Agentic AI Loan Officer",
    page_icon="🤖",
    layout="wide"
)

# -------------- CUSTOM UI CSS --------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f0f0f 0%, #1b1b1b 100%);
}

/* MAIN CARD STYLE */
.card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

/* CHAT BUBBLES */
.user-bubble {
    background: #143d65;
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
}

.bot-bubble {
    background: #e8e8e8;
    color: #111;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
}

/* BUTTON */
div.stButton > button {
    background: linear-gradient(90deg, #ffd500, #ffb300);
    color: black;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
}

/* HEADER TEXT */
.header-title {
    font-size: 40px;
    font-weight: 700;
    color: white;
}
.header-sub {
    font-size: 17px;
    color: #bbbbbb;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER -------------------
st.markdown(
    "<div class='header-title'>🤖 Agentic AI Loan Officer — Demo</div>"
    "<div class='header-sub'>Instant approval • Real-time underwriting • PDF sanction letter</div><br>",
    unsafe_allow_html=True
)

# ---------------- INITIALIZE CHAT -------------------
CUSTOMERS = ["C001","C002","C003","C004","C005","C006","C007","C008","C009","C010"]

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- LAYOUT -------------------
col1, col2 = st.columns([2,1])

# ------------------- RIGHT SIDE (Applicant Card) ------------------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Applicant 👤")

    customer_id = st.selectbox("Customer ID", CUSTOMERS)
    amount = st.number_input("Loan Amount (₹)", min_value=1000.0, value=50000.0, step=1000.0, format="%.0f")
    tenure = st.selectbox("Tenure (months)", [12,24,36,48])

    uploaded_file = st.file_uploader("Upload salary slip (optional)", type=["pdf","png","jpg","jpeg"])

    if st.button("Apply for Loan"):
        st.session_state.chat.append(("user", f"I request ₹{int(amount)} for {tenure} months."))

        files = None
        if uploaded_file:
            file_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type if hasattr(uploaded_file, "type") else "application/octet-stream"
            files = {"file": (uploaded_file.name, file_bytes, content_type)}

        try:
            resp = requests.post(
                f"{BACKEND}/master/apply",
                params={"customer_id": customer_id, "amount": amount, "tenure": tenure},
                files=files
            )
        except Exception as e:
            st.session_state.chat.append(("bot", f"Error connecting to backend: {e}"))
            resp = None

        if resp is None:
            st.session_state.chat.append(("bot", "Error connecting to backend"))
        else:
            try:
                data = resp.json()
            except Exception as e:
                st.session_state.chat.append(("bot", f"Invalid JSON: {e}"))
                data = {"status": "error"}

            # ✓ APPROVED + PDF
            if data.get("status") == "approved" and data.get("pdf_base64"):
                loan = data.get("loan_details", {})
                emi = loan.get("emi", "N/A")

                st.session_state.chat.append(("bot", f"✅ Approved! EMI: ₹{emi}. Sanction letter ready."))

                try:
                    pdf_bytes = base64.b64decode(data["pdf_base64"])
                    filename = data.get("pdf_filename", "sanction_letter.pdf")

                    st.download_button(
                        label="📄 Download Sanction Letter",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf"
                    )

                    st.session_state.chat.append(("bot", f"📑 Sanction letter generated: {filename}"))

                except Exception as e:
                    st.session_state.chat.append(("bot", f"Error preparing PDF: {e}"))

            # ⚠️ NEEDS SALARY SLIP
            elif data.get("status") == "pending":
                st.session_state.chat.append(("bot","⚠️ Salary slip required. Please upload and try again."))

            # ❌ REJECTED
            elif data.get("status") == "rejected":
                st.session_state.chat.append(("bot", f"❌ Rejected: {data.get('reason','Not eligible')}"))

            else:
                st.session_state.chat.append(("bot", f"Error: {data}"))

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- LEFT SIDE (Conversation Card) -------------------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Conversation 💬")

    for who, message in st.session_state.chat:
        if who == "user":
            st.markdown(f"<div class='user-bubble'>🧑‍💼 {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>🤖 {message}</div>", unsafe_allow_html=True)

    st.markdown("<hr><div style='color:#bbbbbb'>Demo notes: Upload salary slip only if required.</div>",
                unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
