import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("geminiapi_key")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Gemini Chatbot",
    page_icon="💰",
    layout="wide"
)

# ---------------- PREMIUM UI CSS ----------------
st.markdown("""
<style>

/* -------- FULL SCREEN BACKGROUND -------- */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                url("https://images.unsplash.com/photo-1639322537228-f710d846310a");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Remove padding */
.block-container {
    padding: 0rem 1rem !important;
}

/* Hide header */
header {visibility: hidden;}

/* -------- GLASS CONTAINER -------- */
.main-container {
    max-width: 900px;
    margin: auto;
    margin-top: 40px;
    padding: 25px;
    border-radius: 20px;

    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}

/* -------- TITLE -------- */
.title {
    text-align: center;
    color: white;
    font-size: 36px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #cfcfcf;
    font-size: 14px;
    margin-bottom: 20px;
}

/* -------- CHAT BUBBLES -------- */
.user-msg {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    padding: 12px;
    border-radius: 15px;
    margin: 8px 0;
    width: fit-content;
    max-width: 70%;
    margin-left: auto;
    font-size: 15px;
}

.bot-msg {
    background: rgba(255,255,255,0.15);
    color: #ffffff;
    padding: 12px;
    border-radius: 15px;
    margin: 8px 0;
    width: fit-content;
    max-width: 70%;
    font-size: 15px;
}

/* -------- INPUT BOX -------- */
.stChatInput {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 15px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<div class="title">💰 Finance Gemini Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Finance Assistant • Ask anything about finance</div>', unsafe_allow_html=True)

st.divider()

# ---------------- GEMINI CLIENT ----------------
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

# ---------------- USER DATA ----------------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are a finance-domain AI assistant with professional and friendly behavior.

Allowed:
- Greetings
- Asking user's name
- Finance topics:
  Accounting, GST, TDS, Financial Statements, Investments (basic), Banking, FP&A

Rules:
- Non-finance → reply EXACTLY:
"I'm designed to answer only finance-related questions. Please ask something related to finance or accounting."

Safety:
- No stock buy/sell advice
- Educational answers only
"""

# ---------------- CHAT SESSION ----------------
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
        )
    )

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-msg'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{text}</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("💬 Ask a finance question...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    # Name detection
    if st.session_state.user_name is None:
        if "i am" in user_input.lower() or "my name is" in user_input.lower():
            st.session_state.user_name = user_input.split()[-1]

    chat = st.session_state.chat_session
    response = chat.send_message(user_input)

    bot_reply = response.text.strip()

    # Personalization
    if st.session_state.user_name:
        bot_reply = bot_reply.replace("Hello", f"Hello {st.session_state.user_name}")

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)