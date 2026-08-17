from gtts import gTTS
import tempfile


LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Urdu": "ur"
}


def text_to_speech(text, language):

    language_code = LANGUAGE_CODES.get(
        language,
        "en"
    )

    try:

        tts = gTTS(
            text=text,
            lang=language_code,
            slow=False
        )

        audio_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(audio_file.name)

        return audio_file.name

    except Exception:

        return None