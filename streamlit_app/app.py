# streamlit_app/app.py
# Agentic AI Loan Officer — Polished UI (full file)
# UI-only changes; backend logic unchanged.
import streamlit as st
import requests
import base64
import time
from io import BytesIO
from PIL import Image

# -------------------------
# Backend base URL (Render)
# -------------------------
BACKEND = "https://agentic-backend-u1m1.onrender.com"  # <-- Render deployment URL

# -------------------------
# Page / session config
# -------------------------
st.set_page_config(page_title="Agentic AI Loan Officer", page_icon="🤖", layout="wide")

if "chat" not in st.session_state:
    st.session_state.chat = []
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "last_pdf" not in st.session_state:
    st.session_state.last_pdf = None
if "last_pdf_name" not in st.session_state:
    st.session_state.last_pdf_name = None

# -------------------------
# Assets
# -------------------------
HERO_IMG = "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=1200"
FALLBACK_HERO = "https://picsum.photos/400/240"
PDF_ICON = "https://img.icons8.com/fluency/48/000000/pdf.png"

CUSTOMERS = ["C001","C002","C003","C004","C005","C006","C007","C008","C009","C010"]

# -------------------------
# Top controls: theme + debug
# -------------------------
col_top_left, col_top_right = st.columns([0.85, 0.15])
with col_top_right:
    light_checked = st.checkbox("Light theme", value=(st.session_state.theme == "light"))
    st.session_state.theme = "light" if light_checked else "dark"
    st.session_state.show_debug = st.checkbox("Show debug logs", value=st.session_state.show_debug)

# -------------------------
# CSS (conditional)
# -------------------------
if st.session_state.theme == "dark":
    css = """
    <style>
    :root { --ey-yellow: #ffd400; --muted: #98a0b4; --card-bg: rgba(255,255,255,0.03); }
    .stApp { background: linear-gradient(180deg,#071019 0%, #0b1220 50%); color: #EAF0FF; }
    .hero { display:flex; gap:16px; align-items:center; padding:14px; border-radius:12px; background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border:1px solid rgba(255,255,255,0.04); box-shadow: 0 10px 30px rgba(2,6,23,0.45); margin-bottom:14px; }
    .hero img { width:140px; height:85px; object-fit:cover; border-radius:10px; }
    .card { background: var(--card-bg); border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,0.04); box-shadow: 0 10px 30px rgba(0,0,0,0.35); margin-bottom:12px; }
    .stButton>button { background: linear-gradient(90deg,var(--ey-yellow), #f2b800); color:#111; font-weight:700; padding:10px 16px; border-radius:12px; border:none; box-shadow:0 8px 20px rgba(0,0,0,0.25); }
    .bubble-user { background: linear-gradient(90deg,#2a6aa8,#1f5488); color:#fff; padding:12px 16px; border-radius:16px; margin:10px 0; display:inline-block; max-width:78%; box-shadow: 0 8px 20px rgba(10,20,40,0.45); }
    .bubble-bot { background: rgba(255,255,255,0.96); color:#0b1220; padding:12px 16px; border-radius:16px; margin:10px 0; display:inline-block; max-width:78%; border:1px solid rgba(0,0,0,0.04); }
    .muted { color: var(--muted); font-size:13px; }
    .file-preview { display:flex; gap:12px; align-items:center; padding:8px; border-radius:10px; border:1px solid rgba(255,255,255,0.04); background: rgba(0,0,0,0.02); }
    .file-preview img { width:64px; height:64px; object-fit:cover; border-radius:8px; }
    .footer { text-align:center; color:var(--muted); margin-top:10px; font-size:13px; }
    </style>
    """
else:
    css = """
    <style>
    :root { --ey-yellow: #ffd400; --muted: #6b7280; --card-bg: rgba(0,0,0,0.03); }
    .stApp { background: linear-gradient(180deg,#ffffff 0%, #f1f7ff 50%); color: #0b1220; }
    .hero { display:flex; gap:16px; align-items:center; padding:14px; border-radius:12px; background: linear-gradient(90deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01)); border:1px solid rgba(0,0,0,0.04); box-shadow: 0 8px 20px rgba(100,100,120,0.05); margin-bottom:14px; }
    .hero img { width:140px; height:85px; object-fit:cover; border-radius:10px; }
    .card { background: var(--card-bg); border-radius:12px; padding:16px; border:1px solid rgba(0,0,0,0.04); box-shadow: 0 6px 20px rgba(0,0,0,0.04); margin-bottom:12px; }
    .stButton>button { background: linear-gradient(90deg,var(--ey-yellow), #f2b800); color:#111; font-weight:700; padding:10px 16px; border-radius:12px; border:none; box-shadow:0 6px 18px rgba(0,0,0,0.08); }
    .bubble-user { background: linear-gradient(90deg,#2a6aa8,#1f5488); color:#fff; padding:12px 16px; border-radius:16px; margin:10px 0; display:inline-block; max-width:78%; box-shadow: 0 6px 12px rgba(0,0,0,0.06); }
    .bubble-bot { background: #ffffff; color:#0b1220; padding:12px 16px; border-radius:16px; margin:10px 0; display:inline-block; max-width:78%; border:1px solid rgba(0,0,0,0.04); }
    .muted { color: var(--muted); font-size:13px; }
    .file-preview { display:flex; gap:12px; align-items:center; padding:8px; border-radius:10px; border:1px solid rgba(0,0,0,0.04); background: rgba(0,0,0,0.02); }
    .file-preview img { width:64px; height:64px; object-fit:cover; border-radius:8px; }
    .footer { text-align:center; color:var(--muted); margin-top:10px; font-size:13px; }
    </style>
    """
st.markdown(css, unsafe_allow_html=True)

# -------------------------
# HERO (st.image for reliability) + backend info (Render)
# -------------------------
hero_col_img, hero_col_txt = st.columns([0.18, 0.82])
with hero_col_img:
    try:
        st.image(HERO_IMG, width=140)
    except Exception:
        st.image(FALLBACK_HERO, width=140)
with hero_col_txt:
    st.markdown(
        f"""
        <div style="padding-left:8px;">
          <div style="font-size:20px; font-weight:700">🤖 Agentic AI Loan Officer — Demo
             <span style="background:#ffd400; padding:6px 10px; border-radius:999px; font-weight:700; margin-left:10px;">LIVE</span>
          </div>
          <div class="muted" style="margin-top:6px">Conversational sales • Real-time underwriting • Auto PDF sanction letters</div>
          <div class="muted" style="margin-top:6px; font-size:13px">Frontend: Streamlit • Backend: <a href="{BACKEND}" target="_blank" style="color:#ffd400;">Render</a></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# -------------------------
# Layout: Conversation | Applicant
# -------------------------
left_col, right_col = st.columns([2, 1])

# ---------- Right: Applicant ----------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin:0 0 6px 0'>Applicant 👤</h3>", unsafe_allow_html=True)

    customer_id = st.selectbox("Customer ID", CUSTOMERS)
    amount = st.number_input("Loan Amount (₹)", min_value=1000.0, value=50000.0, step=1000.0, format="%.0f")
    tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48])
    uploaded_file = st.file_uploader("Upload salary slip (optional)", type=["pdf", "png", "jpg", "jpeg"])

    # small EMI preview (UI-only)
    monthly_rate = 0.01
    est_emi = int((amount * (1 + monthly_rate * tenure)) / tenure) if tenure else 0
    st.markdown(f"<div class='muted' style='margin-top:8px'>Estimated EMI (UI preview): <b>₹{est_emi:,}</b> / month</div>", unsafe_allow_html=True)

    # file preview compact
    if uploaded_file:
        fbytes = uploaded_file.getvalue()
        fname = uploaded_file.name
        fsize_kb = int(len(fbytes) / 1024)
        if any(fname.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
            img = Image.open(BytesIO(fbytes))
            img.thumbnail((160, 160))
            buf = BytesIO()
            img.save(buf, format="PNG")
            thumb_b64 = base64.b64encode(buf.getvalue()).decode()
            st.markdown(f'<div class="file-preview"><img src="data:image/png;base64,{thumb_b64}" /><div><b>{fname}</b><div class="muted">{fsize_kb} KB</div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="file-preview"><img src="{PDF_ICON}" /><div><b>{fname}</b><div class="muted">{fsize_kb} KB - PDF</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("Apply for Loan"):
        st.session_state.chat.append(("user", f"I request ₹{int(amount)} for {tenure} months."))

        files = None
        if uploaded_file:
            file_bytes = uploaded_file.getvalue()
            content_type = uploaded_file.type if hasattr(uploaded_file, "type") else "application/octet-stream"
            files = {"file": (uploaded_file.name, file_bytes, content_type)}

        typing_ph = st.empty()
        typing_ph.markdown('<div class="muted">Agent processing... please wait.</div>', unsafe_allow_html=True)

        try:
            resp = requests.post(
                f"{BACKEND}/master/apply",
                params={"customer_id": customer_id, "amount": amount, "tenure": tenure},
                files=files,
                timeout=20
            )
        except Exception as e:
            st.session_state.chat.append(("bot", f"Error connecting to backend: {e}"))
            resp = None

        time.sleep(0.5)
        typing_ph.empty()

        if resp is None:
            st.session_state.chat.append(("bot", "Error connecting to backend"))
        else:
            try:
                data = resp.json()
            except Exception as e:
                st.session_state.chat.append(("bot", f"Invalid JSON: {e}"))
                data = {"status": "error"}

            if data.get("status") == "approved" and data.get("pdf_base64"):
                loan = data.get("loan_details", {})
                emi = loan.get("emi", "N/A")
                st.session_state.chat.append(("bot", f"✅ Approved! EMI: ₹{emi}. Sanction letter ready."))

                try:
                    pdf_bytes = base64.b64decode(data["pdf_base64"])
                    filename = data.get("pdf_filename", "sanction_letter.pdf")
                    st.session_state.last_pdf = pdf_bytes
                    st.session_state.last_pdf_name = filename
                    st.download_button("📄 Download Sanction Letter", data=pdf_bytes, file_name=filename, mime="application/pdf")
                    st.session_state.chat.append(("bot", f"📑 Sanction letter generated: {filename}"))
                except Exception as e:
                    st.session_state.chat.append(("bot", f"Error preparing PDF: {e}"))
            elif data.get("status") == "pending":
                st.session_state.chat.append(("bot", "⚠️ Salary slip required. Please upload and try again."))
            elif data.get("status") == "rejected":
                st.session_state.chat.append(("bot", f"❌ Rejected: {data.get('reason','Not eligible')}"))
            else:
                st.session_state.chat.append(("bot", f"Error: {data}"))

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Left: Conversation ----------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin:0 0 8px 0'>Conversation 💬</h2>", unsafe_allow_html=True)

    if not st.session_state.chat:
        st.markdown("<div class='muted'>No messages yet — fill the form on the right and click <b>Apply for Loan</b>.</div>", unsafe_allow_html=True)

    for who, message in st.session_state.chat:
        if who == "user":
            st.markdown(f"<div class='bubble-user'>🧑‍💼 {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bubble-bot'>🤖 {message}</div>", unsafe_allow_html=True)

    if st.session_state.last_pdf:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.download_button("📄 Download Latest Sanction Letter", data=st.session_state.last_pdf, file_name=st.session_state.last_pdf_name or "sanction_letter.pdf", mime="application/pdf")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Demo notes: Upload salary slip only if required. This demo uses mock CRM & credit-bureau APIs.</div>", unsafe_allow_html=True)

    if st.session_state.show_debug:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:700; margin-bottom:6px;'>Debug logs (conversation tuples)</div>", unsafe_allow_html=True)
        st.write(st.session_state.chat)

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Built with ❤️ • Streamlit • Backend: Render • Agentic AI demo • <a href='https://github.com/Pruthvichinna/EY_Project' target='_blank'>Code</a></div>", unsafe_allow_html=True)
