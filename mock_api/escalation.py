from datetime import datetime


def request_teacher_call(user_role, reason):

    if user_role not in ["student", "parent"]:
        return {
            "success": False,
            "error": "Only students and parents can request a teacher call."
        }

    request_id = "TCH-" + datetime.now().strftime("%Y%m%d%H%M%S")

    return {
        "success": True,
        "request_id": request_id,
        "message": (
            f"Your request to talk to a teacher has been submitted "
            f"successfully. Request ID: {request_id}."
        )
    }


def request_management_call(user_role, reason):

    if user_role not in ["student", "parent"]:
        return {
            "success": False,
            "error": (
                "Only students and parents can request "
                "school management support."
            )
        }

    request_id = "MGT-" + datetime.now().strftime("%Y%m%d%H%M%S")

    return {
        "success": True,
        "request_id": request_id,
        "message": (
            "Your request to contact school management has been "
            f"submitted successfully. Request ID: {request_id}."
        )
    }