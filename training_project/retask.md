# Retask: Day 5 Student Training Portal Corrections

## Assessment result

The Django development server starts and the public dashboard responds successfully. Django reports no pending model changes, and the submitted migrations are already applied to the committed database.

The project is not ready for final acceptance. Major Day 4 and Day 5 functionality is missing, the submitted test file contains no tests, search is broken at runtime, authorization is insufficient, the academic relationships do not support course-specific marks, and the required FastAPI project is absent.

Verified findings:

- Django system check passes.
- Django discovers **0 tests**.
- The search queryset raises `FieldError` because it uses the nonexistent relationship name `courses` instead of `course`.
- The committed database contains 11 students, 5 courses, 3 departments, 4 users, and 5 student profiles.
- Django's deployment check reports seven security warnings.
- No FastAPI project is present.
- No custom 403, 404, or 500 templates are present.
- No seed fixture or management command is present.

## 1. Correct the models and academic relationships

### Remove the overwritten course declaration

`Student` declares `course` twice:

```python
course = models.CharField(max_length=100)
course = models.ManyToManyField(Course, related_name="students")
```

The second class attribute overwrites the first in Python. Migration history has removed the old text field, but the obsolete declaration remains in source and is misleading. Remove the `CharField` declaration.

### Add an explicit Enrollment model

The current structure is:

```text
Student -- ManyToMany -- Course
   |
   +-- one global marks value
```

A student can have multiple courses but only one mark. The system therefore cannot identify the mark for each course.

Use:

```text
Student --< Enrollment >-- Course
                 |
                 +-- current mark/result
                 +--< MarksHistory
                 +--< Feedback
```

The `Enrollment` model should contain:

- student
- course
- enrollment date
- enrollment/completion status
- current mark or result
- a unique constraint on `(student, course)`

### Add missing academic models

- Add a `MarksHistory` model linked to an enrollment/course, with old mark, new mark, trainer/updater, reason, and timestamp.
- Add a `Feedback` model linked to an enrollment/course, student, trainer, rating, comments, visibility, and timestamps.
- Add trainer/course assignment relationships and enforce that assigned users actually have the trainer role.
- Add the required authentication role/profile model for administrator, trainer, and student roles.
- Link `Student` to the Django `User` account so ownership can be enforced.

### Add model-level validation and constraints

- Add model validators for age 16-60 and marks 0-100. Current validation exists only in `StudentForm` and can be bypassed by admin, scripts, or direct ORM writes.
- Make `Course.code` unique.
- Define the unit and validation for `Course.duration`; an unrestricted float is ambiguous.
- Consider making `Department.name` unique.
- Use `PROTECT` or `SET_NULL` for departments if deleting a department must not delete all related students.
- Validate profile dates of birth and prevent future dates.
- Decide whether every student must have a `StudentProfile`; currently many student records have none.
- Avoid exposing `active_status` and marks through a general-purpose form to unauthorized roles.

## 2. Implement roles, ownership, and permissions

The project currently has no application role model and no trainer workflow.

### Critical authorization problems

- Registration creates only a Django user, logs the user in, and redirects directly to the complete student list.
- Every authenticated user can see every student's name, email, marks, department, courses, and status.
- Every authenticated user can add students.
- Every authenticated user can edit every student, including marks, active status, department, and course relationships.
- Every authenticated user can access any student detail by changing the URL ID.
- Delete is restricted to `is_staff`, but unauthorized users are still shown delete actions in templates.
- There is no student ownership restriction because `Student` is not linked to `User`.

Required behavior:

- Administrators may manage students, departments, courses, accounts, and audit logs.
- Trainers may see only assigned students/enrollments and update only their marks/feedback.
- Students may see only their own profile, enrollments, marks history, and visible feedback.
- Add direct-URL manipulation tests for every protected operation.
- Use reusable role and ownership decorators/helpers.

## 3. Fix view defects

### Broken search

The student search uses:

```python
Q(courses__course_name__icontains=search)
```

The actual field is named `course`, so any nonempty search request raises `FieldError`. Correct the lookup and add a test that executes the search.

### Other view corrections

- Protect the dashboard if global student totals, averages, highest scorer, and recent students are not intended to be public.
- Convert logout from a state-changing GET request to a CSRF-protected POST request.
- Add pagination to the student list; no student pagination is implemented.
- Preserve search and filter parameters across pagination links.
- Use `active_students.count()` for totals rather than sending and rendering every active student's name in the header.
- Make pass/fail logic consistent: the backend treats 40 as pass, while the template uses `marks > 40` and displays 40 as fail.
- Correct `about()` to render the intended template/context or return a normal `HttpResponse`; the current context argument is not used.
- Remove unused imports and dead/commented template/view code.
- Add audit logging for login, logout, failed login, create, update, delete, marks, feedback, and account-status actions.
- Move dashboard, marks, feedback, and audit behavior into a reusable service module.
- Wrap multi-model account/student creation and marks updates in database transactions.

## 4. Complete missing Django workflows

Implement:

- administrator dashboard and role-restricted workflows
- trainer dashboard and approval/assignment workflow
- student-owned dashboard
- user/account activation management
- department CRUD
- course CRUD
- enrollment management
- trainer marks submission/update
- marks-history display
- trainer feedback create/update
- student-visible feedback list
- audit-log search, filtering, and pagination
- password change
- password reset
- failed-login lockout

## 5. URLs and HTTP behavior

- Add `app_name` and namespace the students application URLs.
- Give `home/` and `about/` named URL patterns.
- Use descriptive path parameters such as `student_id` instead of `id`.
- Make logout POST-only.
- Add URLs for role dashboards, accounts, departments, courses, enrollments, marks history, feedback, and audit logs.
- Add and verify custom 403, 404, and 500 handlers/templates with `DEBUG=False`.
- Return a genuine 403 response for authenticated users without permission instead of relying only on navigation visibility.

## 6. Templates and frontend corrections

- Add `<meta name="viewport">` to the base template for correct mobile behavior.
- Add a responsive navigation toggle for tablet/mobile widths.
- Add breadcrumbs to workflow pages.
- Add a project-owned static CSS file instead of relying entirely on the Bootstrap CDN.
- Add Bootstrap JavaScript if interactive Bootstrap components are used.
- Add loading/disabled submit states to prevent double submission.
- Convert logout to a POST form.
- Render messages according to message type; the base template currently styles every message as success.
- Correct the malformed search input: `<inputtype="text"name="search"...>`.
- Move filters above the results table and preserve selected filter values.
- Show active-student count instead of printing every active student name in the page header.
- Correct empty-table `colspan` values to match the actual number of columns.
- Hide edit/delete actions from roles without those permissions.
- Remove large blocks of commented duplicate HTML.
- Add consistent page titles, empty states, validation errors, badges, and responsive layouts across all new workflows.

## 7. Testing requirements

`students/tests.py` contains only the default placeholder, so Django runs 0 tests. Add at least 30 meaningful Django tests covering:

- model relationships and constraints
- model and form validation
- valid and invalid registration/login
- role permissions
- student ownership
- trainer assignment restrictions
- direct URL manipulation
- student CRUD
- department/course/enrollment workflows
- marks updates and history
- feedback visibility and ownership
- audit events
- dashboard totals and ORM reports
- search, combined filters, and pagination
- custom 403, 404, and 500 pages
- query counts and N+1 prevention

Tests must assert business behavior and database effects, not only status code 200.

## 8. Add the required FastAPI project

The required `fastapi_training/` project is completely absent. Add:

```text
fastapi_training/
    app/
        __init__.py
        main.py
        schemas.py
        services.py
    requirements.txt
    README.md
```

Implement:

- `GET /health`
- `GET /students`
- `GET /students/{student_id}`
- `POST /students`
- `PATCH /students/{student_id}`
- `DELETE /students/{student_id}`
- 404 responses for missing students
- Pydantic request and response models
- email validation
- age validation from 16-60
- marks validation from 0-100
- active-status and minimum-marks filtering
- `skip` and `limit` pagination
- correct create and delete status codes
- at least 10 API tests or documented test cases

## 9. Seed data and demo preparation

The committed database contains 11 students, while at least 20 are required. A committed database is not a reproducible seed strategy.

- Add an idempotent management command or fixture.
- Create at least 20 students and 5 courses.
- Add realistic administrators, trainers, departments, enrollments, marks, feedback, and audit events.
- Add non-production demo credentials for every role.
- Verify the seed command works on a clean database.
- Remove `db.sqlite3` from version control after seed tooling is available.

## 10. Production and repository configuration

Current settings contain a committed secret key, `DEBUG=True`, empty `ALLOWED_HOSTS`, SQLite-only configuration, and no `STATIC_ROOT`. Django's deployment check reports seven warnings.

- Add a separate production settings example with `DEBUG=False`.
- Load `SECRET_KEY`, database settings, and allowed hosts from environment variables.
- Configure `STATIC_ROOT` and document `collectstatic`.
- Configure HTTPS redirect, HSTS, secure session cookies, and secure CSRF cookies for production.
- Keep development and production settings separate.
- Expand `.gitignore` to exclude virtual environments, `.env`, `db.sqlite3`, collected static files, and IDE files.
- Remove the 23 committed Python cache/bytecode artifacts.
- Align the Django version used to generate the project/migrations with `requirements.txt` and document a compatible Python version.
- Correct setup instructions: use `python -m venv <name>` and clearly state that commands run inside `training_project`.

## 11. Missing documentation

- Add the required `api_design.md` covering students, courses, enrollments, marks, and feedback, including methods, payloads, responses, permissions, and status codes.
- Document five important generated SQL queries.
- Document one measured before/after query optimization.
- Document setup, migrations, seed data, static collection, tests, Django run, FastAPI run, Swagger/ReDoc, and deployment commands.
- Document demo credentials without using production secrets.

## Reassessment priority

1. Implement roles and close add/edit/detail ownership vulnerabilities.
2. Fix search and add a real automated test suite.
3. Introduce Enrollment, course-specific marks history, feedback, trainers, and audit logs.
4. Add the missing FastAPI project and tests.
5. Add seed tooling, custom error pages, pagination, and service boundaries.
6. Complete production settings, static frontend work, API design, performance documentation, and repository cleanup.
