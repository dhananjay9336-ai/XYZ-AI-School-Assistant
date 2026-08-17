ROLES = {
    "Student": "student",
    "Parent": "parent",
    "Teacher": "teacher",
    "Principal": "principal"
}


def get_role_permissions(role):

    permissions = {

        "student": [
            "view_own_attendance"
        ],

        "parent": [
            "view_child_attendance"
        ],

        "teacher": [
            "mark_attendance"
        ],

        "principal": [
            "view_school_attendance",
            "view_attendance_analytics",
            "mark_attendance"
        ]
    }

    return permissions.get(role, [])