from datetime import datetime, timezone

from canvasapi import Canvas
from secrets import CANVAS_TOKEN, CANVAS_API_URL

canvas = Canvas(access_token=CANVAS_TOKEN, base_url=CANVAS_API_URL)


def get_assignments(course_id: int):
    return canvas.get_course(course_id).get_assignments()


def get_upcoming_assignments(course_id: int, limit: int = 50):
    assignments = get_assignments(course_id)
    upcoming_assignments = []
    for assignment in assignments:
        if assignment.due_at and assignment.due_at_date > datetime.now(timezone.utc):
            upcoming_assignments.append(assignment)

    upcoming_assignments.sort(key=lambda x: x.due_at_date)
    return upcoming_assignments[:limit]
