from auth.permissions import has_permission


STUDENT_DATA = {
    "rahul": {
        "name": "Rahul",
        "attendance": 91.2,
        "present_days": 91,
        "total_days": 100
    },

    "aman": {
        "name": "Aman",
        "attendance": 87.5,
        "present_days": 87,
        "total_days": 100
    },

    "priya": {
        "name": "Priya",
        "attendance": 94.1,
        "present_days": 94,
        "total_days": 100
    }
}


def get_student_attendance(role, student_name):

    if role == "student":
        permission = "view_own_attendance"

    elif role == "parent":
        permission = "view_child_attendance"

    else:
        return {
            "success": False,
            "error": "Unauthorized access."
        }

    if not has_permission(role, permission):

        return {
            "success": False,
            "error": "You do not have permission to view this attendance."
        }

    student = STUDENT_DATA.get(student_name.lower())

    if not student:

        return {
            "success": False,
            "error": "Student not found."
        }

    return {
        "success": True,
        "data": student
    }


def mark_student_absent(role, student_name):

    # Application-layer permission check
    if not has_permission(role, "mark_attendance"):

        return {
            "success": False,
            "error": "You are not authorized to mark attendance."
        }

    student = STUDENT_DATA.get(student_name.lower())

    if not student:

        return {
            "success": False,
            "error": "Student not found."
        }

    # Mock attendance action
    student["total_days"] += 1

    # Student is absent, so present_days remains unchanged
    student["attendance"] = round(
        (student["present_days"] / student["total_days"]) * 100,
        2
    )

    return {
        "success": True,
        "data": student,
        "message": (
            f"{student['name']} has been marked absent today."
        )
    }


def mark_student_present(role, student_name):

    # Application-layer permission check
    if not has_permission(role, "mark_attendance"):

        return {
            "success": False,
            "error": "You are not authorized to mark attendance."
        }

    student = STUDENT_DATA.get(student_name.lower())

    if not student:

        return {
            "success": False,
            "error": "Student not found."
        }

    # Mock attendance action
    student["total_days"] += 1
    student["present_days"] += 1

    student["attendance"] = round(
        (student["present_days"] / student["total_days"]) * 100,
        2
    )

    return {
        "success": True,
        "data": student,
        "message": (
            f"{student['name']} has been marked present today."
        )
    }


def get_school_attendance(role):

    if not has_permission(
        role,
        "view_school_attendance"
    ):

        return {
            "success": False,
            "error": "You are not authorized to view school attendance."
        }

    values = [
        student["attendance"]
        for student in STUDENT_DATA.values()
    ]

    average = round(
        sum(values) / len(values),
        2
    )

    return {
        "success": True,
        "attendance": average
    }