# Retask: Day 5 Student Training Portal Corrections

## Assessment result

The Django application starts successfully, reports no pending model changes, migrates cleanly, and all 30 submitted tests pass. The submission includes dashboards, search/filter/pagination, feedback, marks history, audit logs, seed data, shared templates, breadcrumbs, and service helpers.

The project is not ready for final acceptance because the academic relationships are still incorrect, important direct-URL permissions are missing, several server-side validations are absent, release artifacts are incomplete, and the required FastAPI project has not been submitted.

## 1. Correct the academic data model

### Remove the duplicate course representation

`Student` currently contains both:

- `courses = ManyToManyField(Course)`
- `course = CharField(...)`

These fields can disagree and produce conflicting course information. Remove the text `course` field and use one relational source of truth.

### Add an explicit Enrollment model

The current design stores multiple courses on a student but only one global `marks` value. Feedback and marks history also belong only to a student, not to a particular course.

Replace the current relationship:

```text
Student -- ManyToMany -- Course
   |
   +-- one global marks value
```

with:

```text
Student --< Enrollment >-- Course
                 |
                 +--< MarksHistory
                 +--< Feedback
```

The `Enrollment` model should contain:

- `student`
- `course`
- enrollment date
- enrollment/completion status
- a unique constraint on `(student, course)`

Marks and feedback should reference the enrollment so records identify the relevant student and course.

### Add relationship integrity

- `Student.assigned_trainer` currently accepts any `User`; ensure the selected user has the trainer role.
- `Feedback.trainer` and `MarksHistory.updated_by` also accept any user without role validation.
- Decide whether trainers are assigned per student or per course. A trainer-course relationship is normally more accurate than one global trainer on `Student`.
- Make `Course.code` unique.
- Consider making `Department.name` unique.
- Replace `CASCADE` on `Student.department` with `PROTECT` or `SET_NULL` to avoid deleting students when a department is removed.
- Review whether `Student.user` should remain nullable; authenticated student workflows expect every student to have an account.
- Prevent `Student.email` and `User.email` from becoming inconsistent.

### Add server-side model validation

- Add model validators restricting student marks and marks-history values to 0-100.
- Add model validators restricting feedback ratings to 1-5. HTML `min` and `max` attributes are not server-side validation.
- Add model validation restricting age to 16-60.
- Validate dates of birth and ensure they are not future dates.
- Prefer a structured duration field for `Course.duration` instead of unrestricted text.

## 2. Fix direct-URL permissions

Navigation visibility is not authorization. Permissions must be enforced in every view.

### Student management

- `student_list` allows every authenticated user to see the entire student directory. Students must not see other students.
- `add_student` allows every authenticated user, including students, to create student records.
- `StudentForm(fields="__all__")` exposes sensitive relationship and status fields such as user, assigned trainer, marks, active status, and courses.
- `edit_student` blocks students but allows trainers to edit every student, including students not assigned to them.
- `student_detail` limits students to their own record but lets trainers view any student instead of only assigned students.
- Restrict create/edit/delete operations to the intended roles and use separate forms for admin, trainer, and student workflows.

### Marks and feedback ownership

- `update_marks` permits a trainer to update any student by changing the URL ID. Restrict it to students assigned to that trainer.
- `add_feedback` exposes all students in the form. Limit the queryset to students assigned to the current trainer.
- `edit_feedback` correctly checks feedback ownership, but the form still permits changing the feedback to an unassigned student.
- `marks_history` is available to every logged-in user for every student ID. Students should see only their history; trainers should see only assigned students; admins may see all.
- Add explicit permission tests for all of these direct-ID manipulation cases.

### Authentication and account consistency

- `logout_user` is not protected by `login_required` and changes session state through GET. Use a CSRF-protected POST logout form.
- Registration saves the `User` and `UserProfile` before checking whether a department exists. If no department exists, it leaves a partial account without a `Student`. Check prerequisites first and wrap account creation in `transaction.atomic()`.
- Login assumes every user has `UserProfile`; handle users or superusers with missing profiles safely.
- Cache-only failed-login tracking is not tied to a persistent account state and may reset on cache restart. Document or implement the intended lock strategy.

## 3. Correct audit logging

`AuditLog.ACTION_CHOICES` defines values such as `CREATE`, `UPDATE`, `DELETE`, `MARKS_UPDATE`, and `FEEDBACK`, but the views/services save undeclared values including:

- `ADD_STUDENT`
- `EDIT_STUDENT`
- `DELETE_STUDENT`
- `PASSWORD_CHANGE`
- `MARKS_UPDATED`
- `FEEDBACK_CREATED`

Use only declared action values or update the choices and migrations. Add tests proving all logged actions are valid choices.

Also:

- Use `select_related("user")` in the audit-log list.
- Preserve filter/search parameters in pagination links.
- Add audit events for feedback edits and relevant rejected actions where required.

## 4. Improve views and service boundaries

- `dashboard` exposes global system statistics to every authenticated role. Restrict it or route each role to its own dashboard.
- The admin dashboard duplicates statistics logic already present in `services.py`; use one reusable service.
- Move permission/ownership queries into reusable helpers or services.
- Remove duplicate imports and dead/commented code in `views.py`.
- Use `get_object_or_404()` instead of `Student.objects.get()` in role-facing views where missing related data could otherwise cause a server error.
- Make marks updates atomic with model validation and assigned-trainer authorization.
- Add course and department management workflows if administrators must manage those resources outside Django admin.

## 5. URLs and HTTP behavior

- Add `app_name` and namespace the students application URLs.
- Replace generic `<int:id>` parameters with descriptive names such as `<int:student_id>` and `<int:feedback_id>`.
- Make logout POST-only.
- Ensure student deletion, marks changes, feedback changes, and role/state changes remain POST-only.
- Add explicit custom error handlers or verify custom 403, 404, and 500 rendering with `DEBUG=False` tests.
- Add URLs/workflows for enrollments and course-specific marks.
- Use consistent REST-like resource naming for audit logs (`audit-logs/` rather than `audit_log_list/`).

## 6. Templates and frontend

- Add a viewport meta tag to `base.html` for correct mobile rendering.
- Add a project-owned static CSS file; the submission currently relies mainly on Bootstrap CDN and inline styles.
- Remove repeated inline progress-bar styles where practical.
- Add loading/disabled states consistently to all forms where double submission is possible, not only the add-student form.
- Convert the logout link to a POST form.
- Add active navigation states and consistent page titles/breadcrumbs to every workflow page.
- Confirm filter selections and query parameters persist across student-list and audit-log pagination.
- Ensure forms show field-level errors consistently, including feedback and marks forms.

## 7. Testing gaps

The 30 submitted Django tests pass, but many assert only status code 200 and do not verify permissions or business results.

Add meaningful tests for:

- student ownership and direct URL manipulation
- trainer access to assigned versus unassigned students
- unauthorized add/edit/delete operations
- unauthorized marks and feedback operations
- marks and rating server-side validation
- role-specific dashboard totals
- registration rollback when prerequisites are missing
- valid audit action choices
- custom 403, 404, and 500 pages with `DEBUG=False`
- combined search, course, department, active, result, and pagination parameters
- service-layer atomic behavior
- query counts/N+1 prevention on important list and dashboard pages

## 8. Missing FastAPI submission

The required separate `fastapi_training/` project is absent. Add:

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

Implement and test:

- `GET /health`
- `GET /students`
- `GET /students/{student_id}`
- `POST /students`
- `PATCH /students/{student_id}`
- `DELETE /students/{student_id}`
- missing-ID 404 responses
- email validation
- age validation from 16-60
- marks validation from 0-100
- active-status and minimum-marks filtering
- `skip`/`limit` pagination
- correct create/delete status codes
- response models
- at least 10 API tests or documented test cases

## 9. Missing release and documentation artifacts

- Add a dependency file (`requirements.txt` or `pyproject.toml`) for reproducible Django installation.
- Add the required `api_design.md` with endpoints, methods, payloads, responses, permissions, and status codes.
- Add a separate production settings example with `DEBUG=False`; current settings default to debug mode.
- Move database configuration to environment variables for production.
- Do not use an insecure fallback secret in production settings.
- Add `.gitignore` and remove committed `__pycache__`, `.pyc`, database, and generated `staticfiles` artifacts unless explicitly required for deployment.
- The repository currently tracks 38 Python cache artifacts and 127 collected-static files.
- Document five important generated SQL queries and one measured before/after query optimization.
- Document `collectstatic`, clean-database migration, full test, seed, run, and deployment commands.

## Reassessment priority

1. Fix direct-URL authorization and ownership vulnerabilities.
2. Replace duplicate/global course and marks fields with Enrollment-based relationships.
3. Add server-side validation and correct audit action values.
4. Implement the missing FastAPI project and tests.
5. Strengthen the 30 Django tests so they verify permissions and business behavior.
6. Complete dependency, API-design, production, query-performance, and repository-hygiene requirements.
