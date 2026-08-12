# Retask: Day 5 Student Training Portal Corrections

## Assessment result

This Django submission includes role-based dashboards, ownership checks, student CRUD, feedback, marks history, audit logs, password management, login lockout, query helpers, seed tooling, and a substantial automated test suite.

Verified results:

- Django discovers and passes all 71 submitted tests.
- Models and existing migrations can create a clean test database.
- Search/filter behavior, roles, feedback ownership, marks permissions, audit behavior, and authentication have test coverage.
- A reusable dashboard/filter service module is present.
- Seed and ORM documentation files are present.

The project is not ready for final acceptance because migration checks fail, the academic marks relationship is still incorrect, important state changes use GET, required release/error/API artifacts are missing, seed data is incomplete and destructive, and the required FastAPI project is absent.

## 1. Fix migration cleanliness first

`python manage.py makemigrations --check --dry-run` exits with status 1 and proposes migration `0006` altering the primary-key field on eight models:

- AuditLog
- Course
- Department
- Feedback
- MarksHistory
- Student
- StudentProfile
- UserProfile

Django also reports `models.W042` for these models.

- Configure `DEFAULT_AUTO_FIELD` consistently in settings or `StudentsConfig.default_auto_field`.
- Generate and commit the required migration.
- Re-run `makemigrations --check --dry-run` until it reports no changes.
- Verify the complete migration chain on a new empty database.

## 2. Correct the enrollment and marks relationships

### Remove duplicate course storage

`Student` contains both:

- `course = CharField(...)`
- `courses = ManyToManyField(Course)`

These can disagree. The seed command demonstrates the problem by saving the text value `Python` for every student while assigning two to four unrelated relational courses.

Remove the legacy text field and keep one relational source of truth.

### Add an explicit Enrollment model

Current structure:

```text
Student -- ManyToMany -- Course
   |
   +-- one global marks value
```

Although `MarksHistory` stores an optional course, each update overwrites `Student.marks`. A student enrolled in several courses therefore still has only one current mark.

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

`MarksHistory` and `Feedback` should reference the enrollment.

### Current marks update ambiguity

- A trainer assigned to multiple shared courses updates the global student mark.
- The quick trainer edit records only the first assigned course, which may not be the course the trainer intended to grade.
- Admin edits create marks-history records with `course=None`.
- The history can say a mark belongs to one course while the current value is shared by every course.

Remove these ambiguous flows after introducing enrollment-specific marks.

## 3. Strengthen model integrity

- Add model-level validators for `Student.age` (16-60) and marks (0-100); form validation alone can be bypassed by scripts/admin/direct ORM writes.
- Add validators for `MarksHistory.previous_marks` and `new_marks`.
- Enforce that `Course.assigned_trainer` has the trainer role. A plain foreign key to `User` permits any user.
- Enforce that feedback trainer, course, and student belong to the same authorized enrollment.
- Add uniqueness where appropriate for department names.
- Validate profile date of birth and reject future dates.
- Review whether `Student.user` should remain nullable when ownership workflows depend on it.
- Prevent `Student.email` and `User.email` from becoming inconsistent.
- Wrap User/Student/Profile creation in `transaction.atomic()`.

## 4. Fix state-changing GET requests

### Account activation

`toggle_user_status` changes `User.is_active` immediately without checking `request.method`. A GET request, crawler, browser prefetch, or embedded link can activate/deactivate an account.

- Make this view POST-only with `@require_POST`.
- Use a CSRF-protected confirmation form.
- Keep the self-deactivation guard.
- Test GET rejection and authorized POST behavior.

### Logout

Logout is also performed through GET.

- Replace logout links with a CSRF-protected POST form.
- Reject GET for session-changing actions.

## 5. Authentication and audit security

- Validate the login `next` parameter with `url_has_allowed_host_and_scheme()` before redirecting; directly redirecting an untrusted value can create an open redirect.
- Login lockout is cache-backed, which is better than a browser-session counter, but document the cache backend required in production and test behavior after cache restart.
- Do not trust `X-Forwarded-For` unless requests come through a configured trusted proxy; otherwise audit IP values can be spoofed.
- Consider recording who approved trainer accounts separately from generic active-status changes.
- Add `select_related("user")` to audit-log queries to avoid N+1 queries when rendering usernames.
- Preserve audit-filter parameters through pagination using URL encoding rather than manually concatenating unsafe values.

## 6. Complete service-layer extraction

The existing `services.py` cleanly handles dashboard statistics and student filtering. Complex marks, feedback, audit, and registration logic remains in `views.py`.

- Move course-specific marks updates and history creation into one atomic service function.
- Move feedback creation/editing and its audit event into reusable services.
- Move multi-model registration into an atomic service.
- Create reusable permission/ownership helpers for enrollment access.
- Keep views focused on request parsing, authorization, and response selection.
- Document how these services can be reused by an API.

## 7. Add student-list pagination

Audit logs are paginated, but the main student list is not.

- Paginate the admin/trainer student list.
- Preserve search, department, course, active, and pass/fail parameters in page links.
- Add tests for combined filter and pagination behavior.
- Add query-count tests for student, trainer, admin, and audit pages.

## 8. Add required custom error pages

The required templates are absent:

- `403.html`
- `404.html`
- `500.html`

Add and verify them under `DEBUG=False`. Existing `PermissionDenied` responses should render the custom 403 page.

Tests should cover:

- unauthorized role access returns custom 403
- nonexistent URL renders custom 404
- configured server-error handler renders custom 500

## 9. Correct seed/demo preparation

The management command is not suitable for the Day 5 release requirement:

- It deletes all existing profiles, students, departments, and courses before seeding.
- It creates only 10 students instead of at least 20.
- It creates no administrators or trainers.
- It does not assign course trainers.
- It creates no feedback, marks-history, or seed audit events.
- It does not provide role demo credentials.
- It uses random data, so output is not fully deterministic.

Replace it with an idempotent, safe demo command that:

- creates or updates at least 20 students and 5 courses
- creates admin, trainer, and student accounts
- assigns trainers to courses/enrollments
- adds profiles, course-specific marks, history, feedback, and audit events
- documents non-production credentials
- does not destroy unrelated existing records
- can be run repeatedly without duplicates

The committed database currently has 11 students, 5 courses, 3 departments, 5 users, 18 audit logs, and no feedback or marks-history records. Do not rely on the committed SQLite file as the seed mechanism.

## 10. Add the required FastAPI project

The required separate FastAPI submission is absent. Add:

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
- missing-student 404 responses
- Pydantic request/response models
- email validation
- age validation from 16-60
- marks validation from 0-100
- active-status and minimum-marks filtering
- `skip` and `limit` pagination
- correct create/delete status codes
- at least 10 automated API tests or documented test cases

## 11. Complete API and query documentation

### API design

Add the required `api_design.md` for:

- students
- courses
- enrollments
- marks
- feedback

For every endpoint document method, URL, request data, response data, permissions, and expected status codes.

### Query/performance documentation

The ORM document contains useful query examples, but it does not satisfy all Day 5 performance requirements.

- Include the actual generated SQL for at least five important querysets.
- Measure query counts for important pages.
- Document one real before/after optimization with query counts or timings.
- Correct ORM documentation that assumes global student marks represent course averages; that calculation is invalid until marks are enrollment-specific.
- Correct the “enrolled students with no marks” example because the current `marks` field is non-nullable.

## 12. Production configuration

Current settings contain a committed secret key, `DEBUG=True`, empty `ALLOWED_HOSTS`, SQLite-only database configuration, no `STATIC_ROOT`, and no separate production settings example.

- Add a production settings example with `DEBUG=False`.
- Read `SECRET_KEY`, database configuration, and allowed hosts from environment variables.
- Configure `STATIC_ROOT` and document `collectstatic`.
- Configure HTTPS redirect, HSTS, secure session cookies, and secure CSRF cookies for production.
- Set and migrate a consistent `DEFAULT_AUTO_FIELD`.
- Add a pinned/compatible requirements file and document the required Python version.
- Run `manage.py check --deploy` against production settings until security warnings are resolved.

## 13. Repository hygiene and setup

- Expand `.gitignore` to exclude virtual environments, `.env`, `db.sqlite3`, collected static files, and IDE files; it currently covers mainly Python caches and OS files.
- Remove the committed SQLite database after the safe seed command is available.
- Keep generated test-output files out of the submission unless they are intentionally maintained documentation.
- Document setup, migrations, clean-database testing, seed data, static collection, Django run, FastAPI run, Swagger/ReDoc, and deployment commands.

## 14. Templates and frontend

Positive items:

- Shared base template is present.
- Responsive viewport is configured.
- Common navbar/messages/form-error includes are present.
- Several list pages include empty states.

Remaining work:

- Move the large base-template CSS and page-specific `<style>` blocks into project static CSS files.
- Reduce excessive inline styles.
- Add consistent breadcrumbs across workflow pages.
- Add loading/disabled states to forms where double submission is possible.
- Replace logout links with POST forms.
- Verify all dashboards, tables, filters, and forms on desktop, tablet, and mobile widths.
- Ensure every page has a specific title and accessible labels.
- Document external CDN dependencies or provide a production static strategy.

## 15. Testing additions

The 71-test Django suite is a strong foundation. Add tests for the remaining risks:

- clean migration check produces no changes
- enrollment uniqueness and course-specific marks
- model-level age/marks validation through direct model operations
- GET rejection for logout and account toggling
- safe handling of external `next` URLs
- custom 403, 404, and 500 pages
- student-list pagination with combined filters
- seed command idempotency and minimum record counts
- service atomicity for marks/history/audit and feedback/audit
- production settings/deployment checks
- at least 10 FastAPI endpoint tests

## Reassessment priority

1. Commit the missing primary-key migration and make migration checks clean.
2. Replace global marks and duplicate course storage with Enrollment-based records.
3. Convert account toggling/logout to POST and secure `next` redirects.
4. Add the missing FastAPI project and tests.
5. Correct seed data, custom error pages, and student pagination.
6. Complete services, production settings, API/query documentation, static CSS, and repository cleanup.
