# Retask: Student Training Portal Corrections

The current project only partially meets the Day 5 requirements. Complete the following corrections before reassessment.

## 1. Models and relationships

### Critical academic relationship correction

The current design assigns many courses to a student but stores only one `marks` value on `Student`. This cannot represent separate marks for each course or preserve marks history.

Replace the current design:

```text
Student -- ManyToMany -- Course
   |
   +-- one marks value
```

with an explicit enrollment design:

```text
Student --< Enrollment >-- Course
                 |
                 +--< MarkHistory
                 +--< Feedback
```

Required models and constraints:

- Add an `Enrollment` model containing student, course, enrollment date and status.
- Add a unique constraint for `(student, course)`.
- Move course-specific marks out of `Student` and associate them with an enrollment.
- Add a `MarkHistory` model that records the mark, trainer, timestamp and previous/new value.
- Add a `Feedback` model related to the enrollment, student/course and trainer.
- Add a unique constraint for `(trainer, course)` in `TrainerCourse`.
- Ensure only users with the `TRAINER` role can receive trainer-course assignments. `limit_choices_to` alone does not enforce this in the database or service layer.
- Remove trainer-course assignments when a trainer role is removed.
- Resolve the inconsistent state where a user can retain both trainer and student records after a role change.

### Other model corrections

- Add 0-100 model-level validation for marks.
- Make `Course.code` unique.
- Add choices/defaults for course status and result status.
- Rename `Student.active_status` because it currently represents pass/fail rather than account activity.
- Review whether `Student.user` should be mandatory instead of nullable.
- Use `PROTECT` or `SET_NULL` for `Student.department` instead of deleting students when a department is deleted.
- Store phone numbers as strings, not integers.
- Validate that date of birth is not in the future and produces an allowed age.
- Avoid querying many-to-many courses inside `Student.__str__()`.
- Prevent `User.email` and `Student.email` from becoming inconsistent.
- Allow a safe fallback when an audit-log IP address is unavailable.

## 2. Views and security

- Convert logout, activate/deactivate, make-trainer and remove-trainer actions from GET links to POST forms with CSRF protection.
- Use `PermissionDenied` or a configured 403 handler so permission failures render the custom `403.html` page.
- Remove public test-only `/forbidden/` and `/server-error/` views before release.
- Remove debug `print()` statements.
- Add enrollment management views.
- Add trainer marks submission/update views.
- Add marks-history views.
- Add feedback create/list/update views.
- Add course and department CRUD where required.
- Add search, filters and pagination to the student directory, not only the audit log.
- Move complex marks, feedback and dashboard logic into a reusable Django service module.
- Preserve submitted registration values and display field-level errors when validation fails.
- Reconcile student profiles and trainer-course assignments whenever a user's role changes.
- Use `select_related("user")` for audit log lists and review dashboard/list queries for N+1 behavior.

## 3. URLs

- Use POST-only endpoints for all state-changing actions.
- Add consistent trailing slashes.
- Replace redundant paths such as `/students/student_list/` with clearer resource paths.
- Move admin and trainer dashboards out of confusing `/students/` nesting.
- Add `app_name` and namespace application URLs.
- Prefer descriptive parameters such as `student_id` instead of `id`.
- Remove test-only error routes from release URLs.
- Add routes for courses, departments, enrollments, marks history and feedback.

### FastAPI routes

- Implement the required `POST /students`; the project currently exposes `POST /student`.
- Put filtering and pagination query parameters on `GET /students` instead of creating `/filter_students`, `/some_student` and `/filter_some_student`.
- Use package-relative imports so `uvicorn app.main:app --reload` works from `fastapi_training`.
- Add response models to student detail, update, filtering and pagination endpoints.
- Apply the 16-60 age constraint to PATCH requests as well as create requests.
- Do not store or return plain-text passwords.
- Give route functions distinct, descriptive names.

## 4. Templates and design

- Add breadcrumbs to application pages.
- Move project-specific CSS and repeated inline styles into static CSS files.
- Add loading/disabled states to forms to prevent double submission.
- Replace role/status action links with accessible POST forms and confirmation handling.
- Add an active navigation state.
- Add UI pages and empty states for enrollments, marks history and feedback.
- Improve individual field rendering and validation styling instead of relying entirely on `form.as_p`.
- Correct template class typos such as `text-infofs-4`.
- Verify every page at desktop, tablet and mobile widths.

## 5. Testing and completion requirements

- Expand the Django suite from 4 tests to at least 30 meaningful tests.
- Add model, form, view and permission tests.
- Test valid/invalid authentication and account locking.
- Test ownership restrictions and direct URL manipulation.
- Test role changes and trainer-course access.
- Test dashboard totals and ORM reports.
- Test student search/filter/pagination combinations.
- Add at least 10 FastAPI tests or documented test cases.
- Test correct FastAPI create/delete status codes, invalid email/age/marks and missing IDs.
- Document five important generated SQL queries and one before/after optimization.

## 6. Release and documentation

- Add a Django dependency/requirements file.
- Add a `.gitignore`; do not commit virtual environments, `__pycache__` directories or `.pyc` files.
- Remove the committed non-portable FastAPI virtual environment from version control.
- Add a separate production settings example with `DEBUG=False`.
- Read `SECRET_KEY`, database configuration and allowed hosts from environment variables.
- Configure `STATIC_ROOT` and document `collectstatic`.
- Add a seed-data management command or fixture with at least 20 students, 5 courses, role accounts, marks, feedback and audit events.
- Replace the generic repository README with project setup, test and deployment instructions.
- Create the required `api_design.md` containing endpoints, methods, request/response formats, permissions and status codes.

## Reassessment priority

1. Correct enrollment, marks-history and feedback relationships.
2. Correct state-changing views and role-transition consistency.
3. Complete the missing Django workflows.
4. Correct FastAPI imports, routes and validation.
5. Meet the Django and FastAPI test-count requirements.
6. Complete production configuration, seed data and documentation.
