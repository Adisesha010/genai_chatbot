import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Gemini Chatbot",
    page_icon="💰",
    layout="wide"
)

# ---------------- API KEY ----------------
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# ---------------- MODEL ----------------
model = genai.GenerativeModel("gemini-pro")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---------------- UI (PREMIUM) ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                url("https://images.unsplash.com/photo-1639322537228-f710d846310a");
    background-size: cover;
    background-position: center;
}

/* Container */
.main-container {
    max-width: 900px;
    margin: auto;
    margin-top: 40px;
    padding: 25px;
    border-radius: 20px;

    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
}

/* Chat */
.user-msg {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    padding: 10px;
    border-radius: 12px;
    margin: 5px 0;
    margin-left: auto;
    max-width: 70%;
}

.bot-msg {
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 10px;
    border-radius: 12px;
    margin: 5px 0;
    max-width: 70%;
}

/* Title */
.title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<div class="title">💰 Finance Chatbot</div>', unsafe_allow_html=True)
st.divider()

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY ----------------
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-msg'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{text}</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("Ask a finance question...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    response = st.session_state.chat_session.send_message(user_input)
    bot_reply = response.text

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)