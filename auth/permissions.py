ROLE_PERMISSIONS = {
    "student": {
        "view_own_attendance"
    },

    "parent": {
        "view_child_attendance"
    },

    "teacher": {
        "mark_attendance",
        "view_school_attendance"
    },

    "principal": {
        "view_school_attendance",
        "view_attendance_analytics"
    }
}


def has_permission(role, permission):
    """
    Application-layer authorization check.
    """

    allowed_permissions = ROLE_PERMISSIONS.get(role, set())

    return permission in allowed_permissions