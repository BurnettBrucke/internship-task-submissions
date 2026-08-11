"""Data-handling logic for the student API, kept out of main.py.

This is an in-memory store (a plain dict), which is intentional for this
learning project -- there's no database here. Every function below is the
single place that touches `_students`/`_next_id`, so main.py's route
handlers stay thin: parse the request, call a service function, shape the
response. If this were swapped for a real database later, only this file
would need to change -- the routes in main.py wouldn't.
"""
from typing import Optional

from .schemas import StudentCreate, StudentUpdate

_students: dict[int, dict] = {}
_next_id = 1


def reset():
    """Used by the test suite to get a clean slate between tests."""
    global _students, _next_id
    _students = {}
    _next_id = 1


def seed_initial_data():
    """A few starter records so GET /students isn't empty on first run."""
    reset()
    for student in [
        StudentCreate(name="Asha Verma", email="asha@example.com", age=21, marks=75, is_active=True),
        StudentCreate(name="Ravi Kumar", email="ravi@example.com", age=23, marks=38, is_active=True),
        StudentCreate(name="Zara Khan", email="zara@example.com", age=24, marks=91, is_active=False),
    ]:
        create_student(student)


def list_students(
    skip: int = 0, limit: int = 20,
    is_active: Optional[bool] = None, min_marks: Optional[float] = None,
) -> tuple[list[dict], int]:
    """Returns (page_of_results, total_count_before_pagination)."""
    items = list(_students.values())

    if is_active is not None:
        items = [s for s in items if s["is_active"] == is_active]
    if min_marks is not None:
        items = [s for s in items if s["marks"] >= min_marks]

    items.sort(key=lambda s: s["id"])
    total = len(items)
    page = items[skip: skip + limit]
    return page, total


def get_student(student_id: int) -> Optional[dict]:
    return _students.get(student_id)


def create_student(payload: StudentCreate) -> dict:
    global _next_id
    record = payload.model_dump()
    record["id"] = _next_id
    _students[_next_id] = record
    _next_id += 1
    return record


def update_student(student_id: int, payload: StudentUpdate) -> Optional[dict]:
    record = _students.get(student_id)
    if record is None:
        return None
    updates = payload.model_dump(exclude_unset=True)  # only the fields actually sent in the PATCH
    record.update(updates)
    return record


def delete_student(student_id: int) -> bool:
    if student_id in _students:
        del _students[student_id]
        return True
    return False


seed_initial_data()
