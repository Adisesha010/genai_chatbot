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

# ---------------- FULL SCREEN BACKGROUND + UI FIX ----------------
st.markdown("""
<style>

/* Remove default padding */
.block-container {
    padding: 0rem !important;
}

/* Full screen background */
.stApp {
    margin: 0;
    padding: 0;
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                url("https://images.unsplash.com/photo-1639322537228-f710d846310a");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Hide Streamlit header */
header {
    visibility: hidden;
}

/* Chat styles */
.user-msg {
    color: #0b5394;
    background-color: rgba(231, 243, 255, 0.9);
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 8px;
    max-width: 70%;
}

.bot-msg {
    color: #1b5e20;
    background-color: rgba(232, 245, 233, 0.9);
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 8px;
    max-width: 70%;
}

/* Footer text */
.footer-text {
    color: #d1d1d1;
    font-size: 14px;
}

/* Center content */
.center-box {
    max-width: 900px;
    margin: auto;
    padding-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="center-box">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white;'>💰 Finance Gemini Chatbot</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='footer-text' style='text-align:center;'>Finance domain with professional interaction</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- GEMINI CLIENT ----------------
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

# ---------------- USER DATA STORAGE ----------------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are a finance-domain AI assistant with professional and friendly behavior.

Allowed:
1. Greeting messages
2. Asking and remembering the user's name
3. Finance-related questions only:
   - Accounting (P&L, Balance Sheet, Cash Flow)
   - GST, TDS, TCS
   - Investments (basic knowledge only)
   - Banking and finance concepts
   - FP&A and budgeting

Rules:
- Non-finance → reply EXACTLY:
"I'm designed to answer only finance-related questions. Please ask something related to finance or accounting."

Safety:
- No investment advice
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
        st.markdown(f"<div class='user-msg'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><b>Bot:</b> {text}</div>", unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Say hi or ask a finance question...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    # Capture user name
    if st.session_state.user_name is None:
        if "i am" in user_input.lower() or "my name is" in user_input.lower():
            st.session_state.user_name = user_input.split()[-1]

    chat = st.session_state.chat_session
    response = chat.send_message(user_input)

    bot_reply = response.text.strip()

    # Personalize
    if st.session_state.user_name:
        bot_reply = bot_reply.replace("Hello", f"Hello {st.session_state.user_name}")

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)