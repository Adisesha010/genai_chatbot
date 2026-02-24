import base64
import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Gemini Chatbot",
    page_icon="💰",
    layout="centered"
)

# ---------------- API KEY (STREAMLIT CLOUD) ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- SET BACKGROUND IMAGE ----------------
def set_bg_image(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .chat-box {{
            background-color: rgba(255, 255, 255, 0.88);
            padding: 20px;
            border-radius: 15px;
        }}

        .user-msg {{
            color: #0b5394;
            background-color: #e7f3ff;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 8px;
        }}

        .bot-msg {{
            color: #1b5e20;
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 8px;
        }}

        .footer-text {{
            color: #555;
            font-size: 12px;
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# 👉 Put your image in same folder (example: finance_bg.jpg)
set_bg_image("finance_bg.jpg")

# ---------------- HEADER ----------------
st.markdown("""
<div class="chat-box">
    <h2 style="text-align:center;">💰 Finance Gemini Chatbot</h2>
    <p class="footer-text">Finance domain only | Smart & professional assistant</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- MODEL (FREE TIER SAFE) ----------------
model = genai.GenerativeModel("models/gemini-pro")

# ---------------- USER DATA ----------------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-msg'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><b>Bot:</b> {text}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are a finance-domain AI assistant.

Allowed:
- Greetings
- Asking and remembering name
- Finance topics:
  Accounting, GST, TDS, Banking, Investments, Financial Statements, FP&A

Rules:
- If NON-finance question → reply EXACTLY:
"I'm designed to answer only finance-related questions. Please ask something related to finance or accounting."

Safety:
- No stock buy/sell advice
- Educational answers only
"""

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Say hi or ask a finance question...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    # Capture name
    if st.session_state.user_name is None and "my name is" in user_input.lower():
        st.session_state.user_name = user_input.split()[-1]

    try:
        full_prompt = system_prompt + "\nUser: " + user_input

        response = model.generate_content(full_prompt)
        bot_reply = response.text if response.text else "No response generated"

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Personalize
    if st.session_state.user_name:
        bot_reply = bot_reply.replace("Hello", f"Hello {st.session_state.user_name}")

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()