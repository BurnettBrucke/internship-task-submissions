# API Design Plan

This document plans the REST API surface that would sit in front of the
Student Training Portal's data — the resources to expose, their endpoints,
and the permission rules each one needs. It's written before writing any API
code, as a design step: Day 5 Task 3 implements a small slice of this (the
`/students` resource) as a standalone FastAPI project to practice the
mechanics; a real rollout would likely use Django REST Framework directly on
top of this same Django project so it shares models, auth, and the service
layer in `students/services.py`.

## Resources to expose

| Resource | Backing model | Why it's exposed |
|---|---|---|
| Students | `Student` | Core CRUD entity; every other resource hangs off it |
| Courses | `Course` | Needed to enroll students and assign trainers |
| Enrollments | `Student.courses` (M2M) | Modeled as its own endpoint below so enroll/unenroll doesn't require re-sending the whole student record |
| Marks | `MarksHistory` (write) / `Student.marks` (read) | Marks changes go through the same accountable workflow as the UI (reason required, history recorded) |
| Feedback | `Feedback` | Trainer → student feedback, with the same ownership/visibility rules as the web app |
| Users / Profiles | `UserProfile` | Read-only in v1 — role and approval status, not full account management |

## Authentication & permissions (applies to every endpoint below)

- All endpoints require an authenticated request (session or token auth,
  depending on the API client — a token-based scheme like DRF's
  `TokenAuthentication` or JWT is more appropriate for API consumers than
  Django's session cookies).
- Every endpoint re-applies the same role/ownership rules already enforced
  in `students/decorators.py` and `students/services.py` — an API layer is
  not a shortcut around permission checks, it's another caller of the same
  rules. Concretely, this means: reuse `students.services.*` functions from
  the API views rather than reimplementing marks/feedback logic a second
  time.
- `403 Forbidden` for role/ownership violations, `401 Unauthorized` for
  missing/invalid credentials, `404 Not Found` for objects outside what the
  requester is allowed to know exist at all (see "ownership leaks" note
  under Students below).

---

## Students

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| GET | `/api/students/` | List permitted students (filtered/paginated) | — (query params: `department`, `course`, `status`, `result`, `q`, `page`) | `{count, next, previous, results: [StudentSummary]}` | Admin: all. Trainer: only students in their own courses. Student: only self (or empty list — the UI instead points them at `/api/students/me/`). | `200` |
| POST | `/api/students/` | Create a student | `StudentCreate` (name, email, age, marks, department, courses, is_active) | `StudentDetail` | Admin only | `201` created, `400` validation error, `403` wrong role |
| GET | `/api/students/{id}/` | Retrieve one student | — | `StudentDetail` | Admin: any. Trainer: only if they teach a course that student. Student: only if `id` is their own record. | `200`, `403` (or `404` to avoid confirming a record exists to someone with no right to know — see note below), `404` if truly missing |
| PATCH | `/api/students/{id}/` | Update selected fields | Partial `StudentUpdate` | `StudentDetail` | Admin only (matches the web app: trainers use the narrower `/api/students/{id}/marks/` endpoint instead of general PATCH) | `200`, `400`, `403`, `404` |
| DELETE | `/api/students/{id}/` | Delete a student | — | — | Admin only | `204` on success, `403`, `404` |
| GET | `/api/students/me/` | Convenience endpoint: the logged-in student's own record | — | `StudentDetail` | Student only | `200`, `404` if the account isn't linked to a Student record yet |

**Ownership-leak note:** for `GET /api/students/{id}/`, when a Trainer or
Student requests a record they're not allowed to see, the API returns `404`
rather than `403` — this avoids confirming to an unauthorized caller that a
student with that ID even exists in the system (a 403 leaks existence; a
404 doesn't). Admin-vs-role checks that are about *capability* rather than
*object existence* (e.g. "students can't POST") still return `403`.

## Courses

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| GET | `/api/courses/` | List courses | — (query params: `is_active`, `trainer`) | `[CourseSummary]` | All authenticated roles (Trainers/Students see all courses, not just their own — course *catalog* browsing is different from student *record* ownership) | `200` |
| POST | `/api/courses/` | Create a course | `CourseCreate` (name, code, duration_weeks, trainer) | `CourseDetail` | Admin only | `201`, `400`, `403` |
| GET | `/api/courses/{id}/` | Retrieve one course | — | `CourseDetail` | All authenticated roles | `200`, `404` |
| PATCH | `/api/courses/{id}/` | Update a course | Partial `CourseUpdate` | `CourseDetail` | Admin only | `200`, `400`, `403`, `404` |
| DELETE | `/api/courses/{id}/` | Delete a course | — | — | Admin only | `204`, `403`, `404` |

## Enrollments

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| GET | `/api/students/{id}/courses/` | List a student's enrolled courses | — | `[CourseSummary]` | Same visibility rule as `GET /api/students/{id}/` | `200`, `404` |
| POST | `/api/students/{id}/courses/` | Enroll a student in a course | `{"course_id": int}` | `[CourseSummary]` (updated list) | Admin only | `201`, `400` (already enrolled / invalid course), `403`, `404` |
| DELETE | `/api/students/{id}/courses/{course_id}/` | Unenroll a student from a course | — | — | Admin only | `204`, `403`, `404` |

## Marks

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| POST | `/api/marks/` | Submit/update marks for a student on a course | `{"student_id", "course_id", "new_marks", "reason"}` | `MarksHistoryEntry` | Trainer only, and only for a course they teach that the student is enrolled in (delegates to `students.services.update_student_marks`) | `201`, `400` (out of range / missing reason), `403` (not the assigned trainer, or a non-Trainer role — including a Student attempting this directly), `404` |
| GET | `/api/students/{id}/marks-history/` | List marks history for a student | — (query param: `page`) | `[MarksHistoryEntry]` | Same visibility as `GET /api/students/{id}/` | `200`, `403`/`404` |

## Feedback

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| GET | `/api/students/{id}/feedback/` | List feedback for a student | — | `[FeedbackDetail]` | Admin: all (incl. drafts). Trainer: only their own feedback for that student. Student: only `is_visible_to_student=True` entries, and only for themselves. | `200`, `403`/`404` |
| POST | `/api/students/{id}/feedback/` | Create feedback | `{"course_id", "rating", "comment", "is_visible_to_student"}` | `FeedbackDetail` | Trainer only, and only for their own students (delegates to `students.services.create_feedback`) | `201`, `400` (rating out of 1-5), `403`, `404` |
| PATCH | `/api/feedback/{id}/` | Edit feedback | Partial `{"rating", "comment", "is_visible_to_student"}` | `FeedbackDetail` | Trainer, and only if they authored it | `200`, `400`, `403`, `404` |

## Users / Profiles (read-only in v1)

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| GET | `/api/users/` | List users with role/approval/active status | — (query param: `role`) | `[UserProfileSummary]` | Admin only | `200`, `403` |
| GET | `/api/users/me/` | The logged-in user's own profile | — | `UserProfileDetail` | Any authenticated user | `200` |

Account activation/deactivation and trainer approval stay web-UI-only for
v1 (they're low-frequency, high-consequence actions better done through the
existing `manage_users` page with its confirmation buttons than exposed as
an easily-scriptable API surface).

## Audit log (read-only, admin-only)

| Method | Endpoint | Purpose | Request body | Response body | Permissions | Status codes |
|---|---|---|---|---|---|---|
| GET | `/api/audit-log/` | List audit entries | — (query params: `action_type`, `username`, `date_from`, `date_to`, `page`) | `[AuditLogEntry]` | Admin only | `200`, `403` |

---

## Pagination, filtering, and status-code conventions (applied uniformly)

- All list endpoints paginate with `page` + optional `page_size` query
  params, returning `{count, next, previous, results}` (DRF's default
  `PageNumberPagination` shape) — matches the pattern already used in the
  Django views via `django.core.paginator.Paginator`.
- Filtering query params mirror the ones already implemented in
  `student_list` (`department`, `course`, `status`, `result`, `q`) so the
  API and the web UI stay conceptually identical.
- `400` is reserved for validation failures the *client* can fix (bad
  input); `403` for permission failures; `404` for missing/hidden objects;
  `201` for successful creation; `204` for successful deletion with no
  body; `200` for successful reads/updates.

## Why this maps cleanly onto the service layer

Every write endpoint above (`POST /api/marks/`, `POST /api/students/{id}/feedback/`)
is described as delegating to a function in `students/services.py` rather
than reimplementing the business logic. That's the whole point of having
pulled `update_student_marks()` and `create_feedback()` out of the Django
views in the first place (see Day 5 Task 2, "service-layer challenge"): an
API view and a template-rendering view can both call the exact same
ownership checks, validation, and audit-logging side effects, so the rules
can't silently drift between the two surfaces over time.
