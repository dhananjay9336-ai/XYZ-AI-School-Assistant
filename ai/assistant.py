# =========================================================
# AI ASSISTANT
# =========================================================

# ---------------------------------------------------------
# ESCALATION IMPORT
# ---------------------------------------------------------

from mock_api import escalation


# ---------------------------------------------------------
# ATTENDANCE IMPORT
# ---------------------------------------------------------

from mock_api.attendance import (
    STUDENT_DATA,
    get_student_attendance,
    get_school_attendance,
    mark_student_absent,
    mark_student_present
)


# ---------------------------------------------------------
# AI IMPORTS
# ---------------------------------------------------------

from ai.intent import (
    detect_intent,
    extract_student_name
)

from ai.language import get_text


# =========================================================
# ESCALATION FUNCTIONS
# =========================================================

def call_teacher(role, reason):

    """
    Supports both possible function names:
    request_teacher_call
    request_teacher_contact
    """

    if hasattr(escalation, "request_teacher_call"):
        return escalation.request_teacher_call(
            role,
            reason
        )

    if hasattr(escalation, "request_teacher_contact"):
        return escalation.request_teacher_contact(
            role,
            reason
        )

    return {
        "success": False,
        "error": "Teacher call service is not available."
    }


def call_management(role, reason):

    """
    Supports both possible function names:
    request_management_call
    request_management_contact
    """

    if hasattr(escalation, "request_management_call"):
        return escalation.request_management_call(
            role,
            reason
        )

    if hasattr(escalation, "request_management_contact"):
        return escalation.request_management_contact(
            role,
            reason
        )

    return {
        "success": False,
        "error": "Management call service is not available."
    }


# =========================================================
# MULTI-LANGUAGE SUCCESS MESSAGES
# =========================================================

TEACHER_SUCCESS = {

    "English": (
        "Your request to talk to a teacher has been submitted "
        "successfully. Request ID: {request_id}."
    ),

    "Hindi": (
        "Aapki teacher se baat karne ki request successfully "
        "submit ho gayi hai. Request ID: {request_id}."
    ),

    "Tamil": (
        "ஆசிரியருடன் பேசுவதற்கான உங்கள் கோரிக்கை வெற்றிகரமாக "
        "சமர்ப்பிக்கப்பட்டது. கோரிக்கை ID: {request_id}."
    ),

    "Telugu": (
        "ఉపాధ్యాయుడితో మాట్లాడటానికి మీ అభ్యర్థన విజయవంతంగా "
        "సమర్పించబడింది. అభ్యర్థన ID: {request_id}."
    ),

    "Marathi": (
        "शिक्षकांशी बोलण्याची तुमची विनंती यशस्वीपणे "
        "सबमिट झाली आहे. विनंती ID: {request_id}."
    ),

    "Bengali": (
        "শিক্ষকের সঙ্গে কথা বলার জন্য আপনার অনুরোধ সফলভাবে "
        "জমা হয়েছে। অনুরোধ ID: {request_id}."
    ),

    "Gujarati": (
        "શિક્ષક સાથે વાત કરવાની તમારી વિનંતી સફળતાપૂર્વક "
        "સબમિટ થઈ ગઈ છે. Request ID: {request_id}."
    ),

    "Punjabi": (
        "ਅਧਿਆਪਕ ਨਾਲ ਗੱਲ ਕਰਨ ਲਈ ਤੁਹਾਡੀ ਬੇਨਤੀ ਸਫਲਤਾਪੂਰਵਕ "
        "ਜਮ੍ਹਾਂ ਹੋ ਗਈ ਹੈ। ਬੇਨਤੀ ID: {request_id}."
    ),

    "Kannada": (
        "ಶಿಕ್ಷಕರೊಂದಿಗೆ ಮಾತನಾಡಲು ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ "
        "ಸಲ್ಲಿಸಲಾಗಿದೆ. ವಿನಂತಿ ID: {request_id}."
    ),

    "Malayalam": (
        "അധ്യാപകനുമായി സംസാരിക്കാനുള്ള നിങ്ങളുടെ അഭ്യർത്ഥന "
        "വിജയകരമായി സമർപ്പിച്ചു. അഭ്യർത്ഥന ID: {request_id}."
    ),

    "Urdu": (
        "استاد سے بات کرنے کی آپ کی درخواست کامیابی سے "
        "جمع ہو گئی ہے۔ درخواست ID: {request_id}۔"
    )
}


MANAGEMENT_SUCCESS = {

    "English": (
        "Your request to contact school management has been "
        "submitted successfully. Request ID: {request_id}."
    ),

    "Hindi": (
        "School management se contact karne ki request "
        "successfully submit ho gayi hai. Request ID: {request_id}."
    ),

    "Tamil": (
        "பள்ளி நிர்வாகத்தை தொடர்புகொள்ளும் உங்கள் கோரிக்கை "
        "வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது. கோரிக்கை ID: {request_id}."
    ),

    "Telugu": (
        "పాఠశాల యాజమాన్యాన్ని సంప్రదించడానికి మీ అభ్యర్థన "
        "విజయవంతంగా సమర్పించబడింది. అభ్యర్థన ID: {request_id}."
    ),

    "Marathi": (
        "शाळेच्या व्यवस्थापनाशी संपर्क साधण्याची तुमची विनंती "
        "यशस्वीपणे सबमिट झाली आहे. विनंती ID: {request_id}."
    ),

    "Bengali": (
        "স্কুল কর্তৃপক্ষের সঙ্গে যোগাযোগের জন্য আপনার অনুরোধ "
        "সফলভাবে জমা হয়েছে। অনুরোধ ID: {request_id}."
    ),

    "Gujarati": (
        "શાળા મેનેજમેન્ટનો સંપર્ક કરવાની તમારી વિનંતી સફળતાપૂર્વક "
        "સબમિટ થઈ ગઈ છે. Request ID: {request_id}."
    ),

    "Punjabi": (
        "ਸਕੂਲ ਪ੍ਰਬੰਧਨ ਨਾਲ ਸੰਪਰਕ ਕਰਨ ਲਈ ਤੁਹਾਡੀ ਬੇਨਤੀ "
        "ਸਫਲਤਾਪੂਰਵਕ ਜਮ੍ਹਾਂ ਹੋ ਗਈ ਹੈ। ਬੇਨਤੀ ID: {request_id}."
    ),

    "Kannada": (
        "ಶಾಲಾ ನಿರ್ವಹಣೆಯನ್ನು ಸಂಪರ್ಕಿಸಲು ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು "
        "ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ. ವಿನಂತಿ ID: {request_id}."
    ),

    "Malayalam": (
        "സ്കൂൾ മാനേജ്മെന്റുമായി ബന്ധപ്പെടാനുള്ള നിങ്ങളുടെ "
        "അഭ്യർത്ഥന വിജയകരമായി സമർപ്പിച്ചു. അഭ്യർത്ഥന ID: {request_id}."
    ),

    "Urdu": (
        "اسکول انتظامیہ سے رابطہ کرنے کی آپ کی درخواست کامیابی سے "
        "جمع ہو گئی ہے۔ درخواست ID: {request_id}۔"
    )
}


# =========================================================
# ABSENT SUCCESS
# =========================================================

ABSENT_MESSAGES = {

    "English":
        "{name} has been marked absent today.",

    "Hindi":
        "{name} ko aaj absent mark kar diya gaya hai.",

    "Tamil":
        "{name} இன்று வரவில்லை என்று குறிக்கப்பட்டுள்ளார்.",

    "Telugu":
        "{name} ఈరోజు గైర్హాజరుగా గుర్తించబడ్డారు.",

    "Marathi":
        "{name} यांना आज अनुपस्थित म्हणून चिन्हांकित केले आहे.",

    "Bengali":
        "{name}-কে আজ অনুপস্থিত হিসেবে চিহ্নিত করা হয়েছে।",

    "Gujarati":
        "{name} ને આજે ગેરહાજર તરીકે માર્ક કરવામાં આવ્યા છે.",

    "Punjabi":
        "{name} ਨੂੰ ਅੱਜ ਗੈਰਹਾਜ਼ਰ ਵਜੋਂ ਦਰਜ ਕੀਤਾ ਗਿਆ ਹੈ।",

    "Kannada":
        "{name} ಅವರನ್ನು ಇಂದು ಗೈರುಹಾಜರಾಗಿ ಗುರುತಿಸಲಾಗಿದೆ.",

    "Malayalam":
        "{name} ഇന്ന് ഹാജരാകാത്തതായി രേഖപ്പെടുത്തിയിരിക്കുന്നു.",

    "Urdu":
        "{name} کو آج غیر حاضر نشان زد کر دیا گیا ہے۔"
}


# =========================================================
# PRESENT SUCCESS
# =========================================================

PRESENT_MESSAGES = {

    "English":
        "{name} has been marked present today.",

    "Hindi":
        "{name} ko aaj present mark kar diya gaya hai.",

    "Tamil":
        "{name} இன்று வந்ததாக குறிக்கப்பட்டுள்ளார்.",

    "Telugu":
        "{name} ఈరోజు హాజరైనట్లు గుర్తించబడ్డారు.",

    "Marathi":
        "{name} यांना आज उपस्थित म्हणून चिन्हांकित केले आहे.",

    "Bengali":
        "{name}-কে আজ উপস্থিত হিসেবে চিহ্নিত করা হয়েছে।",

    "Gujarati":
        "{name} ને આજે હાજર તરીકે માર્ક કરવામાં આવ્યા છે.",

    "Punjabi":
        "{name} ਨੂੰ ਅੱਜ ਹਾਜ਼ਰ ਵਜੋਂ ਦਰਜ ਕੀਤਾ ਗਿਆ ਹੈ।",

    "Kannada":
        "{name} ಅವರನ್ನು ಇಂದು ಹಾಜರಾಗಿ ಗುರುತಿಸಲಾಗಿದೆ.",

    "Malayalam":
        "{name} ഇന്ന് ഹാജരായതായി രേഖപ്പെടുത്തിയിരിക്കുന്നു.",

    "Urdu":
        "{name} کو آج حاضر نشان زد کر دیا گیا ہے۔"
}


# =========================================================
# HELPER FUNCTION
# =========================================================

def localized_message(messages, language, **kwargs):

    text = messages.get(
        language,
        messages.get("English", "")
    )

    return text.format(**kwargs)


# =========================================================
# KNOWN STUDENTS
# =========================================================

KNOWN_STUDENTS = [
    "rahul",
    "aman",
    "priya"
]


# =========================================================
# GET STUDENT NAME
# =========================================================

def get_name_from_message(message):

    student_name = extract_student_name(message)

    if student_name:
        return student_name.lower()

    for name in KNOWN_STUDENTS:

        if name in message.lower():
            return name

    return None


# =========================================================
# MAIN RESPONSE FUNCTION
# =========================================================

def generate_response(
    role,
    message,
    context=None,
    language="English"
):

    # =====================================================
    # CONTEXT
    # =====================================================

    if context is None:
        context = {}

    # =====================================================
    # ROLE CHANGE
    # =====================================================

    previous_role = context.get(
        "current_role"
    )

    if previous_role != role:

        context.clear()

        context["current_role"] = role

    # =====================================================
    # CLEAN MESSAGE
    # =====================================================

    original_message = message.strip()

    message = original_message.lower().strip(
        " ?!.,:"
    )

    # =====================================================
    # INTENT
    # =====================================================

    try:

        intent = detect_intent(
            message
        )

    except Exception:

        intent = None

    # =====================================================
    # STUDENT NAME
    # =====================================================

    extracted_name = get_name_from_message(
        message
    )

    # =====================================================
    # HUMAN ESCALATION
    # =====================================================

    if role in [
        "student",
        "parent"
    ]:

        # -------------------------------------------------
        # TEACHER CALL
        # -------------------------------------------------

        if (
            "talk to teacher" in message
            or "talk to my teacher" in message
            or "talk to my child's teacher" in message
            or "contact teacher" in message
            or "contact my teacher" in message
            or "contact my child's teacher" in message
            or "teacher se baat" in message
            or "teacher ko call" in message
        ):

            context["pending_escalation"] = "teacher"

            return get_text(
                language,
                "teacher_confirmation"
            )

        # -------------------------------------------------
        # MANAGEMENT CALL
        # -------------------------------------------------

        if (
            "school management" in message
            or "contact management" in message
            or "management se baat" in message
            or "principal se baat" in message
        ):

            context["pending_escalation"] = "management"

            return get_text(
                language,
                "management_confirmation"
            )

        # -------------------------------------------------
        # CONFIRMATION
        # -------------------------------------------------

        if context.get(
            "pending_escalation"
        ):

            confirmation_messages = [

                "yes",
                "yes please",
                "sure",
                "haan",
                "ha",
                "ji",
                "ji haan",
                "ok",
                "okay"
            ]

            if message in confirmation_messages:

                escalation_type = (
                    context["pending_escalation"]
                )

                # =========================================
                # TEACHER
                # =========================================

                if escalation_type == "teacher":

                    result = call_teacher(
                        role,
                        "User requested human assistance."
                    )

                    context.pop(
                        "pending_escalation",
                        None
                    )

                    if not result.get(
                        "success",
                        False
                    ):

                        return result.get(
                            "error",
                            "Unable to submit request."
                        )

                    return localized_message(
                        TEACHER_SUCCESS,
                        language,
                        request_id=result.get(
                            "request_id",
                            "N/A"
                        )
                    )

                # =========================================
                # MANAGEMENT
                # =========================================

                if escalation_type == "management":

                    result = call_management(
                        role,
                        "User requested human assistance."
                    )

                    context.pop(
                        "pending_escalation",
                        None
                    )

                    if not result.get(
                        "success",
                        False
                    ):

                        return result.get(
                            "error",
                            "Unable to submit request."
                        )

                    return localized_message(
                        MANAGEMENT_SUCCESS,
                        language,
                        request_id=result.get(
                            "request_id",
                            "N/A"
                        )
                    )

    # =====================================================
    # STUDENT
    # =====================================================

    if role == "student":

        # -------------------------------------------------
        # SCHOOL ATTENDANCE RESTRICTION
        # -------------------------------------------------

        if (
            "overall" in message
            or "school attendance" in message
            or "school ki attendance" in message
            or "school ka attendance" in message
        ):

            return get_text(
                language,
                "unauthorized_school"
            )

        # -------------------------------------------------
        # FOLLOW-UP
        # -------------------------------------------------

        follow_up_questions = [

            "what about now",
            "how about now",
            "and now",
            "now what",
            "current status",
            "what is it now",
            "how is it now",

            "abhi kya hai",
            "ab kya hai",
            "abhi attendance kitni hai",
            "ab attendance kitni hai",
            "abhi attendance kya hai",
            "current attendance kya hai",
            "attendance abhi kitni hai",
            "abhi meri attendance kitni hai",
            "ab meri attendance kitni hai"
        ]

        if (
            message in follow_up_questions
            and context.get("student_name")
        ):

            student_name = context[
                "student_name"
            ]

            result = get_student_attendance(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            student = result["data"]

            return get_text(
                language,
                "student_attendance",
                attendance=student["attendance"]
            )

        # -------------------------------------------------
        # WAITING FOR STUDENT NAME
        # -------------------------------------------------

        if context.get(
            "waiting_for"
        ) == "student_name":

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                return get_text(
                    language,
                    "child_name"
                )

            context["student_name"] = (
                student_name
            )

            context.pop(
                "waiting_for",
                None
            )

            result = get_student_attendance(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            student = result["data"]

            return get_text(
                language,
                "student_attendance",
                attendance=student["attendance"]
            )

        # -------------------------------------------------
        # STUDENT ATTENDANCE
        # -------------------------------------------------

        if (
            "attendance" in message
            or "meri attendance" in message
            or "my attendance" in message
        ):

            context.pop(
                "student_name",
                None
            )

            context["waiting_for"] = (
                "student_name"
            )

            student_question = {

                "English":
                    "Sure. Which student's attendance would you like to see?",

                "Hindi":
                    "Bilkul. Aap kis student ki attendance dekhna chahte hain?",

                "Tamil":
                    "நிச்சயமாக. எந்த மாணவரின் வருகையைப் பார்க்க விரும்புகிறீர்கள்?",

                "Telugu":
                    "తప్పకుండా. ఏ విద్యార్థి హాజరును చూడాలనుకుంటున్నారు?",

                "Marathi":
                    "नक्कीच. कोणत्या विद्यार्थ्याची उपस्थिती पाहायची आहे?",

                "Bengali":
                    "অবশ্যই। কোন শিক্ষার্থীর উপস্থিতি দেখতে চান?",

                "Gujarati":
                    "ચોક્કસ. કયા વિદ્યાર્થીની હાજરી જોવા માંગો છો?",

                "Punjabi":
                    "ਜ਼ਰੂਰ। ਤੁਸੀਂ ਕਿਸ ਵਿਦਿਆਰਥੀ ਦੀ ਹਾਜ਼ਰੀ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?",

                "Kannada":
                    "ಖಂಡಿತ. ಯಾವ ವಿದ್ಯಾರ್ಥಿಯ ಹಾಜರಾತಿಯನ್ನು ನೋಡಲು ಬಯಸುತ್ತೀರಿ?",

                "Malayalam":
                    "തീർച്ചയായും. ഏത് വിദ്യാർത്ഥിയുടെ ഹാജർ കാണണം?",

                "Urdu":
                    "ضرور۔ آپ کس طالب علم کی حاضری دیکھنا چاہتے ہیں؟"
            }

            return localized_message(
                student_question,
                language
            )

        # -------------------------------------------------
        # DEFAULT
        # -------------------------------------------------

        student_default = {

            "English":
                "I'm your Academic Assistant. I can help with attendance and academic queries.",

            "Hindi":
                "Main aapka Academic Assistant hoon. Main attendance aur academic queries mein aapki help kar sakta hoon.",

            "Tamil":
                "நான் உங்கள் கல்வி உதவியாளர். வருகை மற்றும் கல்வி தொடர்பான கேள்விகளில் உங்களுக்கு உதவ முடியும்.",

            "Telugu":
                "నేను మీ అకాడెమిక్ అసిస్టెంట్‌ను. హాజరు మరియు విద్యా సంబంధిత ప్రశ్నల్లో నేను మీకు సహాయం చేయగలను.",

            "Marathi":
                "मी तुमचा शैक्षणिक सहाय्यक आहे. मी उपस्थिती आणि शैक्षणिक प्रश्नांमध्ये तुमची मदत करू शकतो.",

            "Bengali":
                "আমি আপনার একাডেমিক সহকারী। আমি উপস্থিতি এবং একাডেমিক প্রশ্নে আপনাকে সাহায্য করতে পারি।",

            "Gujarati":
                "હું તમારો શૈક્ષણિક સહાયક છું. હું હાજરી અને શૈક્ષણિક પ્રશ્નોમાં તમારી મદદ કરી શકું છું.",

            "Punjabi":
                "ਮੈਂ ਤੁਹਾਡਾ ਅਕਾਦਮਿਕ ਸਹਾਇਕ ਹਾਂ। ਮੈਂ ਹਾਜ਼ਰੀ ਅਤੇ ਅਕਾਦਮਿਕ ਸਵਾਲਾਂ ਵਿੱਚ ਤੁਹਾਡੀ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ।",

            "Kannada":
                "ನಾನು ನಿಮ್ಮ ಶೈಕ್ಷಣಿಕ ಸಹಾಯಕ. ಹಾಜರಾತಿ ಮತ್ತು ಶೈಕ್ಷಣಿಕ ಪ್ರಶ್ನೆಗಳಲ್ಲಿ ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು.",

            "Malayalam":
                "ഞാൻ നിങ്ങളുടെ അക്കാദമിക് അസിസ്റ്റന്റാണ്. ഹാജർ, അക്കാദമിക് ചോദ്യങ്ങൾ എന്നിവയിൽ നിങ്ങളെ സഹായിക്കാം.",

            "Urdu":
                "میں آپ کا تعلیمی معاون ہوں۔ میں حاضری اور تعلیمی سوالات میں آپ کی مدد کر سکتا ہوں।"
        }

        return localized_message(
            student_default,
            language
        )

    # =====================================================
    # PARENT
    # =====================================================

    elif role == "parent":

        # -------------------------------------------------
        # SCHOOL ATTENDANCE
        # -------------------------------------------------

        if (
            "overall" in message
            or "school attendance" in message
            or "school ki attendance" in message
            or "school ka attendance" in message
        ):

            result = get_school_attendance(
                role
            )

            if not result["success"]:
                return result["error"]

            return get_text(
                language,
                "school_attendance",
                attendance=result["attendance"]
            )

        # -------------------------------------------------
        # DIRECT CHILD NAME
        # -------------------------------------------------

        if message in KNOWN_STUDENTS:

            context["student_name"] = message

            context.pop(
                "waiting_for",
                None
            )

            result = get_student_attendance(
                role,
                message
            )

            if not result["success"]:
                return result["error"]

            student = result["data"]

            return get_text(
                language,
                "parent_attendance",
                name=student["name"],
                attendance=student["attendance"]
            )

        # -------------------------------------------------
        # FOLLOW-UP
        # -------------------------------------------------

        follow_up_questions = [

            "what about now",
            "how about now",
            "and now",
            "now what",
            "current status",
            "what is it now",
            "how is it now",

            "abhi kya hai",
            "ab kya hai",
            "abhi attendance kitni hai",
            "ab attendance kitni hai",
            "abhi attendance kya hai",
            "current attendance kya hai",
            "attendance abhi kitni hai",
            "abhi child ki attendance kitni hai",
            "ab child ki attendance kitni hai",
            "abhi bachche ki attendance kitni hai",
            "ab bachche ki attendance kitni hai"
        ]

        if (
            message in follow_up_questions
            and context.get("student_name")
        ):

            student_name = context[
                "student_name"
            ]

            result = get_student_attendance(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            student = result["data"]

            return get_text(
                language,
                "parent_attendance",
                name=student["name"],
                attendance=student["attendance"]
            )

        # -------------------------------------------------
        # CHILD ATTENDANCE
        # -------------------------------------------------

        if (
            "attendance" in message
            or "child attendance" in message
            or "my child's attendance" in message
            or "my child attendance" in message
        ):

            student_name = context.get(
                "student_name"
            )

            if not student_name:

                context["waiting_for"] = (
                    "student_name"
                )

                return get_text(
                    language,
                    "child_name"
                )

            result = get_student_attendance(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            student = result["data"]

            return get_text(
                language,
                "parent_attendance",
                name=student["name"],
                attendance=student["attendance"]
            )

        # -------------------------------------------------
        # DEFAULT
        # -------------------------------------------------

        return localized_message(
            {
                "English":
                    "Of course. I can help you with your child's attendance and other school-related queries.",

                "Hindi":
                    "Bilkul. Main aapke child ki attendance aur school-related queries mein help kar sakta hoon."
            },
            language
        )

    # =====================================================
    # TEACHER
    # =====================================================

    elif role == "teacher":

        # -------------------------------------------------
        # OVERALL SCHOOL ATTENDANCE
        # -------------------------------------------------

        if (
            "overall" in message
            or "school attendance" in message
            or "school ki attendance" in message
            or "school ka attendance" in message
            or "school attendance dikhao" in message
            or "show school attendance" in message
        ):

            result = get_school_attendance(
                role
            )

            if not result["success"]:
                return result["error"]

            return get_text(
                language,
                "school_attendance",
                attendance=result["attendance"]
            )

        # -------------------------------------------------
        # PENDING ABSENT STUDENT
        # -------------------------------------------------

        if context.get(
            "waiting_for"
        ) == "absent_student":

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                return localized_message(
                    {
                        "English":
                            "Please tell me the student's name.",
                        "Hindi":
                            "Kripya student ka naam bataiye."
                    },
                    language
                )

            result = mark_student_absent(
                role,
                student_name
            )

            context.pop(
                "waiting_for",
                None
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                ABSENT_MESSAGES,
                language,
                name=student_name.title()
            )

        # -------------------------------------------------
        # PENDING PRESENT STUDENT
        # -------------------------------------------------

        if context.get(
            "waiting_for"
        ) == "present_student":

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                return localized_message(
                    {
                        "English":
                            "Please tell me the student's name.",
                        "Hindi":
                            "Kripya student ka naam bataiye."
                    },
                    language
                )

            result = mark_student_present(
                role,
                student_name
            )

            context.pop(
                "waiting_for",
                None
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                PRESENT_MESSAGES,
                language,
                name=result["data"]["name"]
            )

        # -------------------------------------------------
        # MARK ABSENT
        # -------------------------------------------------

        if (
            "mark" in message
            and "absent" in message
        ):

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                context["waiting_for"] = (
                    "absent_student"
                )

                return localized_message(
                    {
                        "English":
                            "Sure. Which student's attendance would you like me to mark as absent?",

                        "Hindi":
                            "Bilkul. Aap kis student ki attendance absent mark karna chahte hain?"
                    },
                    language
                )

            result = mark_student_absent(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                ABSENT_MESSAGES,
                language,
                name=student_name.title()
            )

        # -------------------------------------------------
        # MARK PRESENT
        # -------------------------------------------------

        if (
            "mark" in message
            and "present" in message
        ):

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                context["waiting_for"] = (
                    "present_student"
                )

                return localized_message(
                    {
                        "English":
                            "Sure. Which student's attendance would you like me to mark as present?",

                        "Hindi":
                            "Bilkul. Aap kis student ki attendance present mark karna chahte hain?"
                    },
                    language
                )

            result = mark_student_present(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                PRESENT_MESSAGES,
                language,
                name=result["data"]["name"]
            )

        # -------------------------------------------------
        # SHOW STUDENT ATTENDANCE
        # -------------------------------------------------

        if "attendance" in message:

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                return localized_message(
                    {
                        "English":
                            "Sure. Which student's attendance would you like to see?",

                        "Hindi":
                            "Bilkul. Aap kis student ki attendance dekhna chahte hain?"
                    },
                    language
                )

            result = get_student_attendance(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            student = result["data"]

            return localized_message(
                {
                    "English":
                        "{name}'s current attendance is {attendance}%.",

                    "Hindi":
                        "{name} ki current attendance {attendance}% hai."
                },
                language,
                name=student["name"],
                attendance=student["attendance"]
            )

        # -------------------------------------------------
        # DEFAULT
        # -------------------------------------------------

        return localized_message(
            {
                "English":
                    "I'm your Teaching Assistant. I can help with attendance and teaching-related tasks.",

                "Hindi":
                    "Main aapka Teaching Assistant hoon. Main attendance aur teaching-related tasks mein help kar sakta hoon."
            },
            language
        )

    # =====================================================
    # PRINCIPAL
    # =====================================================

    elif role == "principal":

        # -------------------------------------------------
        # MARK ABSENT
        # -------------------------------------------------

        if (
            "mark" in message
            and "absent" in message
        ):

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                context["waiting_for"] = (
                    "principal_absent_student"
                )

                return localized_message(
                    {
                        "English":
                            "Sure. Which student's attendance would you like me to mark as absent?",

                        "Hindi":
                            "Bilkul. Aap kis student ki attendance absent mark karna chahte hain?"
                    },
                    language
                )

            result = mark_student_absent(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                ABSENT_MESSAGES,
                language,
                name=student_name.title()
            )

        # -------------------------------------------------
        # PENDING ABSENT NAME
        # -------------------------------------------------

        if context.get(
            "waiting_for"
        ) == "principal_absent_student":

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                return localized_message(
                    {
                        "English":
                            "Please tell me the student's name.",
                        "Hindi":
                            "Kripya student ka naam bataiye."
                    },
                    language
                )

            result = mark_student_absent(
                role,
                student_name
            )

            context.pop(
                "waiting_for",
                None
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                ABSENT_MESSAGES,
                language,
                name=student_name.title()
            )

        # -------------------------------------------------
        # MARK PRESENT
        # -------------------------------------------------

        if (
            "mark" in message
            and "present" in message
        ):

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                context["waiting_for"] = (
                    "principal_present_student"
                )

                return localized_message(
                    {
                        "English":
                            "Sure. Which student's attendance would you like me to mark as present?",

                        "Hindi":
                            "Bilkul. Aap kis student ki attendance present mark karna chahte hain?"
                    },
                    language
                )

            result = mark_student_present(
                role,
                student_name
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                PRESENT_MESSAGES,
                language,
                name=result["data"]["name"]
            )

        # -------------------------------------------------
        # PENDING PRESENT NAME
        # -------------------------------------------------

        if context.get(
            "waiting_for"
        ) == "principal_present_student":

            student_name = get_name_from_message(
                message
            )

            if not student_name:

                return localized_message(
                    {
                        "English":
                            "Please tell me the student's name.",
                        "Hindi":
                            "Kripya student ka naam bataiye."
                    },
                    language
                )

            result = mark_student_present(
                role,
                student_name
            )

            context.pop(
                "waiting_for",
                None
            )

            if not result["success"]:
                return result["error"]

            return localized_message(
                PRESENT_MESSAGES,
                language,
                name=result["data"]["name"]
            )

        # -------------------------------------------------
        # OVERALL SCHOOL ATTENDANCE
        # -------------------------------------------------

        if (
            "overall" in message
            or "school attendance" in message
            or "school ki attendance" in message
            or "school ka attendance" in message
            or "show school attendance" in message
        ):

            result = get_school_attendance(
                role
            )

            if not result["success"]:
                return result["error"]

            return get_text(
                language,
                "school_attendance",
                attendance=result["attendance"]
            )

        # -------------------------------------------------
        # PRINCIPAL - STUDENT ATTENDANCE
        # -------------------------------------------------

        if "attendance" in message:

            student_name = get_name_from_message(
                message
            )

            if student_name:

                result = get_student_attendance(
                    role,
                    student_name
                )

                if not result["success"]:
                    return result["error"]

                student = result["data"]

                return localized_message(
                    {
                        "English":
                            "{name}'s current attendance is {attendance}%.",

                        "Hindi":
                            "{name} ki current attendance {attendance}% hai."
                    },
                    language,
                    name=student["name"],
                    attendance=student["attendance"]
                )

        # -------------------------------------------------
        # DEFAULT PRINCIPAL
        # -------------------------------------------------

        return localized_message(
            {
                "English":
                    "I'm your Management Assistant. I can help with school attendance analytics and management information.",

                "Hindi":
                    "Main aapka Management Assistant hoon. Main school attendance analytics aur management information mein help kar sakta hoon."
            },
            language
        )

    # =====================================================
    # INVALID ROLE
    # =====================================================

    return "Please select a valid role."