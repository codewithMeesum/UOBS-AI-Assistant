import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="UOBS AI Assistant | University of Baltistan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .portal-card {
        padding: 0.8rem;
        border-radius: 8px;
        background-color: #1E232A;
        border: 1px solid #2E3642;
        margin-bottom: 0.6rem;
    }
    .portal-card a {
        text-decoration: none;
        color: #4DA6FF;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .portal-desc {
        font-size: 0.8rem;
        color: #A0AAB8;
        margin-top: 3px;
    }
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        background-color: #1C3829;
        color: #4EFA94;
        border: 1px solid #285A3D;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

UOBS_SYSTEM_INSTRUCTION = """
You are the official Virtual Assistant for the University of Baltistan, Skardu (UOBS).
Your role is to assist students, prospective applicants, faculty, and visitors.

Key Knowledge Base:
- Identity: Public sector higher education institution located in Skardu, Gilgit-Baltistan, Pakistan (HEC chartered).
- Campuses: Main Campus (Muhib Road / Skardu) and Hussainabad Campus.
- Academic Departments:
  * Computer Sciences (BS Artificial Intelligence, BS Computer Science, BS Software Engineering).
  * Business Management (BBA, MBA Executive).
  * Biological Sciences (BS Botany, BS Zoology).
  * Educational Development & Languages (English, etc.).
  * Natural & Mathematical Sciences (Mathematics, Chemistry).
- Official Links:
  * Official Website: uobs.edu.pk
  * Online Admission Portal: admissions.uobs.edu.pk
  * Student LMS Portal: elm.uobs.edu.pk
- Admissions & Criteria: Minimum 45% marks in Intermediate (HSSC / equivalent).

Tone & Guidelines:
- Professional, welcoming, clear, and structured.
- Use concise bullet points, bold headers, and direct steps.
- If an administrative query requires in-person follow-up, direct users to the relevant departmental office or IT section.
"""

@st.cache_resource
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        st.error(
            "GEMINI_API_KEY is not configured. "
            "Add it to .env locally or Streamlit Secrets when deployed."
        )
        st.stop()

    return genai.Client(api_key=api_key)

client = get_client()

with st.sidebar:
    st.markdown('<div class="status-badge">● Systems Operational</div>', unsafe_allow_html=True)
    st.title("🎓 UOBS Hub")
    st.caption("Official Digital Support Desk")
    st.divider()

    st.subheader("🌐 Quick Portals")
    st.markdown("""
    <div class="portal-card">
        <a href="https://elm.uobs.edu.pk" target="_blank">🔗 Student LMS (ELM)</a>
        <div class="portal-desc">Access courses, attendance, and semester results.</div>
    </div>
    <div class="portal-card">
        <a href="https://admissions.uobs.edu.pk" target="_blank">📝 Admissions Portal</a>
        <div class="portal-desc">Apply online, track merit lists & fee vouchers.</div>
    </div>
    <div class="portal-card">
        <a href="https://uobs.edu.pk" target="_blank">🏛️ Official Website</a>
        <div class="portal-desc">Academic notices, tenders & university news.</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    with st.expander("📊 Merit Aggregate Calculator"):
        matric_marks = st.number_input("Matric Percentage (%)", 0.0, 100.0, 70.0, 0.5)
        hssc_marks = st.number_input("HSSC / Inter Percentage (%)", 0.0, 100.0, 65.0, 0.5)
        aggregate = (matric_marks * 0.30) + (hssc_marks * 0.70)
        st.metric(label="Calculated Aggregate", value=f"{aggregate:.2f}%")
        if aggregate >= 45.0:
            st.success("Eligible for Undergraduate Admission!")
        else:
            st.warning("Minimum 45% aggregate required.")

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("University of Baltistan, Skardu")
st.caption("AI-Powered Student Services & Academic Admissions Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

def set_prompt(query_text):
    st.session_state["pending_prompt"] = query_text

st.markdown("##### ⚡ Common Topics")
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    if st.button("🎓 BS AI & CS Details", use_container_width=True):
        set_prompt("What are the eligibility criteria and subjects for BS AI and BS Computer Science?")
with col_b:
    if st.button("💳 Fee & Scholarships", use_container_width=True):
        set_prompt("Tell me about fee payment procedures and available scholarships at UOBS.")
with col_c:
    if st.button("🔑 LMS Portal Help", use_container_width=True):
        set_prompt("How do I log into the ELM Student Portal and check my grades?")
with col_d:
    if st.button("📍 Campuses & Locations", use_container_width=True):
        set_prompt("Where are the Main and Hussainabad campuses located, and which departments are there?")

st.divider()

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown(
            "Salam & Welcome! 👋 I am the **UOBS Virtual Assistant**. "
            "How can I assist you with admissions, portals, or campus details today?"
        )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

chat_input = st.chat_input("Ask about admissions, programs, fee structure, or portals...")
active_prompt = None

if chat_input:
    active_prompt = chat_input
elif "pending_prompt" in st.session_state and st.session_state["pending_prompt"]:
    active_prompt = st.session_state.pop("pending_prompt")

if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})

    with st.chat_message("user"):
        st.markdown(active_prompt)

    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part.from_text(text=m["content"])]
        )
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("Consulting UOBS records..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=UOBS_SYSTEM_INSTRUCTION,
                        temperature=0.3,
                    )
                )
                bot_reply = response.text
                st.markdown(bot_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": bot_reply}
                )
            except Exception as e:
                st.error(f"Error: {e}")
