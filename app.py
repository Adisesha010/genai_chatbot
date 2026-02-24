import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Gemini Chatbot",
    page_icon="💰",
    layout="wide"
)

# ---------------- API KEY ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- MODEL ----------------
model = genai.GenerativeModel("gemini-1.5-flash")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---------------- UI (PREMIUM) ----------------
st.markdown("""
<style>

/* -------- FULL BACKGROUND -------- */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                url("https://images.unsplash.com/photo-1639322537228-f710d846310a");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Remove padding */
.block-container {
    padding: 1rem !important;
}

/* Hide header */
header {visibility: hidden;}

/* -------- GLASS CONTAINER -------- */
.main-box {
    max-width: 900px;
    margin: auto;
    margin-top: 30px;
    padding: 25px;
    border-radius: 20px;

    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}

/* -------- TITLE -------- */
.title {
    text-align: center;
    color: white;
    font-size: 34px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #cccccc;
    font-size: 14px;
    margin-bottom: 15px;
}

/* -------- CHAT -------- */
.user-msg {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    padding: 10px;
    border-radius: 12px;
    margin: 6px 0;
    margin-left: auto;
    max-width: 70%;
}

.bot-msg {
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 10px;
    border-radius: 12px;
    margin: 6px 0;
    max-width: 70%;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.markdown('<div class="title">💰 Finance Gemini Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask anything about finance, accounting, GST, investments</div>', unsafe_allow_html=True)

st.divider()

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

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are a finance-domain AI assistant.

Rules:
- Answer ONLY finance-related questions (accounting, GST, TDS, investments, banking, FP&A)
- If non-finance question → reply:
"I'm designed to answer only finance-related questions. Please ask something related to finance or accounting."
- Do NOT give stock buy/sell advice
- Keep answers clear and professional
"""

# ---------------- RESPONSE ----------------
if user_input:
    st.session_state.messages.append(("user", user_input))

    try:
        full_prompt = system_prompt + "\nUser: " + user_input

        response = st.session_state.chat.send_message(full_prompt)
        bot_reply = response.text

    except Exception as e:
        bot_reply = "⚠️ Error occurred. Please check API key or try again."

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)