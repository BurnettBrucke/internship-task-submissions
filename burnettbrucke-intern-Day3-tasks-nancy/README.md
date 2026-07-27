# Training Project — Student Training Portal (Day 2 + Day 3)

A Django project (`training_project`) with one app (`students`) covering:
CRUD, model relationships, ORM practice, authentication, and a small
dashboard/portal.

## Setup

```bash
python -m venv venv
venv/bin/activate      # venv\Scripts\activate 
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## Models — `students/models.py`

- **Department** — `name`, `description`. One department → many students
  (`ForeignKey` on `Student`, `related_name='students'`).
- **Course** — `name`, `code`, `duration_weeks`, `is_active`. Many-to-many
  with `Student` (`related_name='students'` on the reverse side too).
- **Student** — `name`, `email`, `age`, `marks`, `joined_date`
  (auto-set), `is_active`, `department` (FK, `on_delete=SET_NULL` so
  deleting a department never deletes students), `courses` (M2M).
  `result_status` property returns Pass/Fail from `marks >= 40`.
- **StudentProfile** — `phone`, `address`, `date_of_birth`. One-to-one with
  `Student` (`on_delete=CASCADE` — a profile has no meaning without its
  student).

## Forms — `students/forms.py`

- `StudentForm` — ModelForm for name/email/age/marks/department/courses/
  is_active, with `clean_*` methods enforcing name required, age 16–60,
  marks 0–100.
- `RegisterForm` — extends Django's `UserCreationForm` with a required
  email field.

## Views — `students/views.py`

Full CRUD (`student_list`, `student_detail`, `add_student`, `edit_student`,
`delete_student`), a `dashboard` view with aggregate queries, and
`register_view` for signup. Every student-related view is `@login_required`;
deletion additionally checks `request.user.is_staff` before actually
deleting (bonus requirement).

## ORM query practice

See **`orm_queries.md`** — all 20 required queries, each with the exact
code, real output captured against the seeded data, and a short
explanation (including why `SET_NULL` vs `CASCADE` was chosen, and how
`select_related`/`prefetch_related` avoid N+1 queries).

## Authentication

Uses Django's built-in `User` model and auth views:
- `LoginView` / `LogoutView` (project-level `urls.py`) with custom templates
  in `students/templates/registration/`.
- Custom `register_view` using `UserCreationForm` + an email field.
- `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` set in
  `settings.py` so `@login_required` redirects to `/login/?next=...`
  automatically.



## Tests — `students/tests.py`

30 tests covering (grouped, with the required 15 scenarios called out in
docstrings): list/detail pages, valid & invalid creation, update, deletion
(+ staff-only rule), login page, successful login, protected-page redirect,
registration, logout, department relationship (+ `SET_NULL` behavior),
one-to-one profile relationship (+ cascade delete), many-to-many course
relationship, search, department filter, status/result filters, and
dashboard totals.

Run with:
```bash
python manage.py test students -v 2
```
All 30 tests pass.
