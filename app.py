import streamlit as st
import speech_recognition as sr

from ai.assistant import generate_response
from ai.tts import text_to_speech
from auth.roles import ROLES


# =========================================================
# SPEECH TO TEXT
# =========================================================

def speech_to_text(audio_file, language):

    recognizer = sr.Recognizer()

    language_codes = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Tamil": "ta-IN",
        "Telugu": "te-IN",
        "Marathi": "mr-IN",
        "Bengali": "bn-IN",
        "Gujarati": "gu-IN",
        "Punjabi": "pa-IN",
        "Kannada": "kn-IN",
        "Malayalam": "ml-IN",
        "Urdu": "ur-IN"
    }

    language_code = language_codes.get(
        language,
        "en-IN"
    )

    try:

        with sr.AudioFile(audio_file) as source:

            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language=language_code
        )

        return text

    except sr.UnknownValueError:

        return None

    except sr.RequestError:

        return None

    except Exception:

        return None


# =========================================================
# AI AVATAR
# =========================================================

def show_ai_avatar():

    st.markdown(
        """
        <style>
        .ai-avatar {
            width: 120px;
            height: 120px;
            margin: 20px auto;
            border-radius: 50%;
            background: linear-gradient(145deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 65px;
            box-shadow: 0 0 25px rgba(118, 75, 162, 0.5);
            animation: avatar-pulse 1.2s infinite;
        }

        @keyframes avatar-pulse {
            0% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.06);
            }

            100% {
                transform: scale(1);
            }
        }
        </style>

        <div class="ai-avatar">
            🤖
        </div>
        """,
        unsafe_allow_html=True
    )

    
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="XYZ AI School Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 XYZ AI")
st.subheader("Human-Like AI School Assistant")


# =========================================================
# ROLE SELECTION
# =========================================================

role_name = st.sidebar.selectbox(
    "Select your role",
    list(ROLES.keys())
)


# =========================================================
# RESET CONTEXT WHEN ROLE CHANGES
# =========================================================

if "previous_role" not in st.session_state:
    st.session_state.previous_role = role_name

if st.session_state.previous_role != role_name:

    st.session_state.context = {}
    st.session_state.previous_role = role_name


role = ROLES[role_name]

st.sidebar.write(
    f"Current Role: **{role_name}**"
)


# =========================================================
# LANGUAGE SELECTION
# =========================================================

language = st.sidebar.selectbox(
    "Select language",
    [
        "English",
        "Hindi",
        "Tamil",
        "Telugu",
        "Marathi",
        "Bengali",
        "Gujarati",
        "Punjabi",
        "Kannada",
        "Malayalam",
        "Urdu"
    ]
)

st.sidebar.write(
    f"Language: **{language}**"
)


# =========================================================
# CONVERSATION HISTORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = {}


# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================
# Chat input with voice support
chat_input = st.chat_input(
    "Ask XYZ AI something...",
    accept_audio=True
)

user_message = None

if chat_input:

    # Text message
    if chat_input.text:

        user_message = chat_input.text

    # Voice message
    elif chat_input.audio:

        st.audio(chat_input.audio)

        user_message = speech_to_text(
            chat_input.audio,
            language
        )

        if user_message is None:

            st.error(
                "Sorry, I could not understand the voice message."
            )

# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_message:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_message)

    # Generate AI response
    response = generate_response(
        role,
        user_message,
        st.session_state.context,
        language
    )

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Display AI response
    with st.chat_message("assistant"):

        # AI Avatar
        show_ai_avatar()

        # AI Text Response
        st.write(response)

        # Text-to-Speech
        audio_file = text_to_speech(
            response,
            language
        )

        if audio_file:

            st.audio(
                audio_file,
                format="audio/mp3"
            )