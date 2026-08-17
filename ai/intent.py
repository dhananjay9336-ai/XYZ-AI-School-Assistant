import re


def detect_intent(message):

    text = message.lower().strip()

    # -----------------------------------------
    # Attendance intents
    # -----------------------------------------

    if (
        "overall attendance" in text
        or "school attendance" in text
        or "attendance of school" in text
    ):
        return "school_attendance"


    if (
        "attendance" in text
        and (
            "child" in text
            or "son" in text
            or "daughter" in text
            or "my kid" in text
        )
    ):
        return "child_attendance"


    if (
        "my attendance" in text
        or "my attendance" in text
    ):
        return "own_attendance"


    # -----------------------------------------
    # Teacher attendance action
    # -----------------------------------------

    if (
        "mark" in text
        and (
            "absent" in text
            or "present" in text
        )
    ):
        return "mark_attendance"


    # -----------------------------------------
    # Escalation
    # -----------------------------------------

    if (
        "teacher" in text
        and (
            "talk" in text
            or "contact" in text
            or "call" in text
        )
    ):
        return "contact_teacher"


    if (
        "management" in text
        or "principal" in text
    ) and (
        "contact" in text
        or "talk" in text
        or "call" in text
    ):
        return "contact_management"


    # -----------------------------------------
    # General
    # -----------------------------------------

    if (
        "hello" in text
        or "hi" in text
        or "hey" in text
    ):
        return "greeting"


    return "unknown"


def extract_student_name(message):

    names = [
        "rahul",
        "aman",
        "priya"
    ]

    text = message.lower()

    for name in names:

        if re.search(
            rf"\b{name}\b",
            text
        ):
            return name

    return None