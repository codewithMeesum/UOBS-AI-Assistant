import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Page Setup & Layout Configuration
st.set_page_config(
    page_title="UOBS AI Assistant | University of Baltistan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
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

# UOBS Assistant Instructions
UOBS_SYSTEM_INSTRUCTION = """
You are the UOBS AI Assistant for the University of Baltistan, Skardu (UOBS).

Your role is to assist students, prospective applicants, faculty, and visitors.

UOBS INFORMATION:
- University of Baltistan, Skardu (UOBS) is a public sector higher education institution in Gilgit-Baltistan, Pakistan.
- Campuses include Main Campus (Muhib Road / Skardu) and Hussainabad Campus.
- Academic areas include:
  * Computer Sciences: BS Artificial Intelligence, BS Computer Science, BS Software Engineering.
  * Business Management: BBA, MBA Executive.
  * Biological Sciences: BS Botany, BS Zoology.
  * Educational Development & Languages.
  * Natural & Mathematical Sciences: Mathematics, Chemistry.
- Official Website: https://uobs.edu.pk
- Admissions Portal: https://admissions.uobs.edu.pk
- Student LMS / ELM: https://elm.uobs.edu.pk
- The application includes a configured undergraduate admission criterion of minimum 45% Intermediate/HSSC.

IMPORTANT BEHAVIOR:
- Answer using the UOBS-specific information provided above whenever relevant.
- Do not claim to have access to a live UOBS database.
- Do not invent official UOBS policies, fees, notices, deadlines, or procedures.
- If information is not available, clearly say that the student should verify it through the official UOBS website or relevant university office.
- Be professional, welcoming, clear, and concise.
- Use bullet points and bold headings when useful.
"""

@st.cache_resource
def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        st.error(
            "GROQ_API_KEY is not configured. "
            "Add it to .env locally or Streamlit Secrets when deployed."
        )
        st.stop()

    return Groq(api_key=api_key)

client = get_client()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(
        '<div class="status-badge">● Systems Operational</div>',
        unsafe_allow_html=True
    )

    st.title("🎓 UOBS Hub")
    st.caption("Official Digital Support Desk")
    st.divider()

    st.subheader("🌐 Quick Portals")

    st.markdown("""
    <div class="portal-card">
        <a href="https://elm.uobs.edu.pk" target="_blank">
            🔗 Student LMS (ELM)
        </a>
        <div class="portal-desc">
            Access courses, attendance, and semester results.
        </div>
    </div>

    <div class="portal-card">
        <a href="https://admissions.uobs.edu.pk" target="_blank">
            📝 Admissions Portal
        </a>
        <div class="portal-desc">
            Apply online, track merit lists & fee vouchers.
        </div>
    </div>

    <div class="portal-card">
        <a href="https://uobs.edu.pk" target="_blank">
            🏛️ Official Website
        </a>
        <div class="portal-desc">
            Academic notices, tenders & university news.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    with st.expander("📊 Merit Aggregate Calculator"):
        matric_marks = st.number_input(
            "Matric Percentage (%)",
            0.0,
            100.0,
            70.0,
            0.5
        )

        hssc_marks = st.number_input(
            "HSSC / Inter Percentage (%)",
            0.0,
            100.0,
            65.0,
            0.5
        )

        aggregate = (matric_marks * 0.30) + (hssc_marks * 0.70)

        st.metric(
            label="Calculated Aggregate",
            value=f"{aggregate:.2f}%"
        )

        if aggregate >= 45.0:
            st.success("Eligible for Undergraduate Admission!")
        else:
            st.warning("Minimum 45% aggregate required.")

    st.divider()

    if st.button(
        "🗑️ Clear Chat History",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# ==================== MAIN CHAT INTERFACE ====================

st.title("University of Baltistan, Skardu")
st.caption("AI-Powered Student Services & Academic Admissions Assistant")

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Query Helper
def set_prompt(query_text):
    st.session_state["pending_prompt"] = query_text

# Quick Prompt Action Pills
st.markdown("##### ⚡ Common Topics")

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    if st.button(
        "🎓 BS AI & CS Details",
        use_container_width=True
    ):
        set_prompt(
            "What are the eligibility criteria and subjects for BS AI and BS Computer Science at UOBS?"
        )

with col_b:
    if st.button(
        "💳 Fee & Scholarships",
        use_container_width=True
    ):
        set_prompt(
            "Tell me about fee payment procedures and available scholarships at UOBS."
        )

with col_c:
    if st.button(
        "🔑 LMS Portal Help",
        use_container_width=True
    ):
        set_prompt(
            "How do I access the UOBS ELM Student Portal?"
        )

with col_d:
    if st.button(
        "📍 Campuses & Locations",
        use_container_width=True
    ):
        set_prompt(
            "Where are the Main and Hussainabad campuses located?"
        )

st.divider()

# Welcome Message
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown(
            "Salam & Welcome! 👋 I am the **UOBS Virtual Assistant**. "
            "How can I assist you with admissions, portals, or campus details today?"
        )

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
chat_input = st.chat_input(
    "Ask about admissions, programs, fee structure, or portals..."
)

active_prompt = None

if chat_input:
    active_prompt = chat_input

elif (
    "pending_prompt" in st.session_state
    and st.session_state["pending_prompt"]
):
    active_prompt = st.session_state.pop("pending_prompt")

# ==================== AI RESPONSE ====================

if active_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": active_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(active_prompt)

    # Build conversation history for Groq
    messages_for_groq = [
        {
            "role": "system",
            "content": UOBS_SYSTEM_INSTRUCTION
        }
    ]

    for message in st.session_state.messages:
        messages_for_groq.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    with st.chat_message("assistant"):

        with st.spinner("Consulting UOBS records..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages_for_groq,
                    temperature=0.3,
                    max_tokens=800
                )

                bot_reply = response.choices[0].message.content

                st.markdown(bot_reply)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": bot_reply
                    }
                )

            except Exception as e:

                error_message = str(e)

                if "429" in error_message:
                    st.error(
                        "The AI service is temporarily rate-limited. "
                        "Please try again shortly."
                    )
                else:
                    st.error(f"Error: {error_message}")
