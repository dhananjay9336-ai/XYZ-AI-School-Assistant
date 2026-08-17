# services/escalation.py


def request_teacher_call(student_name):
    """
    Mock service for requesting a call from the teacher.
    """

    if not student_name:
        return {
            "success": False,
            "error": "Student name is required."
        }

    # Mock request
    return {
        "success": True,
        "request_id": "TEACHER-001",
        "message": (
            f"Your call request has been submitted to "
            f"{student_name}'s teacher."
        )
    }


def request_management_contact(student_name):
    """
    Mock service for contacting school management.
    """

    if not student_name:
        return {
            "success": False,
            "error": "Student name is required."
        }

    # Mock request
    return {
        "success": True,
        "request_id": "MANAGEMENT-001",
        "message": (
            "Your request has been submitted to "
            "school management."
        )
    }