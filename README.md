# Agentic AI Loan Officer — Demo (EY Teachathon 6.0 — Tata Capital Challenge)


---

## 🚀 Live Demo Links

### **Frontend (Streamlit):**  
🔗 https://eyproject.streamlit.app/

### **Backend (Render — FastAPI):**  
🔗 https://agentic-backend-u1m1.onrender.com

---

## 🎥 Demo Video  
Click to watch the working prototype:  
👉 https://screenapp.io/app/v/iMx50MC_3c

---

## 🧠 Project Overview
This project automates personal loan processing using an Agentic AI workflow.  
A Master Agent orchestrates worker agents to complete:

- Customer verification  
- Credit underwriting  
- PDF sanction letter generation  
- Conversational customer interaction  

The system is fully deployed & functional end-to-end.

---

## ✨ Key Features

- 🗣️ Conversational AI loan approval  
- 🤖 Master Agent coordinating multiple Worker Agents  
- 👤 Verification Agent → Mock CRM API  
- 💳 Underwriting Agent → Mock Credit Bureau API  
- 📄 Auto-generated PDF sanction letter  
- ☁️ Streamlit Cloud + Render deployment  
- 📁 Salary slip upload supported  
- 🎨 Modern and attractive UI  

---

## 🏗️ Architecture Summary

**User (Streamlit UI)**  
→ **FastAPI backend (Render)**  
→ **Master Agent (Orchestrator)**  
→ **Verification Agent** (Mock CRM API)  
→ **Underwriting Agent** (Mock Credit Bureau API)  
→ **Sanction Letter Agent** (PDF Generator)  
→ **Returns sanctioned PDF to the user**

This mimics a real NBFC workflow.

---

## 📂 Repository Structure

```
agentic-loan-officer/
│
├── backend/
│   ├── main.py
│   ├── agents/
│   │   ├── master_agent.py
│   │   ├── sales_agent.py
│   │   ├── verification_agent.py
│   │   ├── underwriting_agent.py
│   │   ├── sanction_agent.py
│   ├── apis/
│   │   ├── mock_crm.py
│   │   ├── mock_credit_bureau.py
│   ├── utils/
│   │   ├── pdf_generator.py
│   ├── data/
│   │   └── customers.json
│   └── uploads/
│
├── streamlit_app/
│   ├── app.py
│   └── assets/
│
├── requirements.txt
└── README.md


