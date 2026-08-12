# Retask: Day 5 Student Training Portal Corrections

## Assessment result

The submission contains working Django and FastAPI projects.

Verified results:

- Django system check passes.
- Django has no pending model migrations.
- Migrations apply successfully to a clean test database.
- All 34 submitted Django tests pass.
- FastAPI imports and starts successfully with `uvicorn app.main:app`.
- FastAPI health, list, detail, create, patch, delete, filtering, pagination, validation, and missing-ID smoke checks return the expected status codes.
- `.gitignore` correctly excludes virtual environments, Python caches, environment files, and the SQLite database.

The project still needs corrections before final acceptance. The most important problems are the course/marks relationship, student data exposure, hardcoded admin credentials, missing production configuration, missing FastAPI tests, and missing Day 5 documentation/data deliverables.

## 1. Correct the course, enrollment, and marks relationships

### Remove duplicate course fields

`Student` currently contains both:

- `course = CharField(...)`
- `enrolled_courses = ManyToManyField(Course)`

These two fields can disagree. For example, the text field can say "Python" while the relational courses contain Django and FastAPI. Remove the text `course` field and use one relational source of truth.

### Add an explicit Enrollment model

The current relationship is:

```text
Student -- ManyToMany -- Course
   |
   +-- one global marks value
```

This cannot store a different mark for every course. It also cannot represent enrollment status, enrollment date, completion date, or course-specific marks history.

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

`MarksHistory` must reference the enrollment/course. It currently records only the student, so a history entry does not identify which course was graded.

### Resolve trainer relationship conflicts

The project stores a trainer on both `Course` and `Student`. These relationships can conflict—for example, a student may have trainer A while an enrolled course has trainer B.

- Decide whether trainer assignment is per course/enrollment, which is normally the clearer design.
- Ensure a trainer can update marks or feedback only for an enrollment they teach.
- `limit_choices_to` only filters forms; it does not enforce trainer roles at the model/database layer.
- Validate that `Feedback.trainer`, `Feedback.course`, and `Feedback.student` belong to the same authorized assignment/enrollment.
- Do not allow optional/general feedback when the requirement expects course-specific feedback.

### Add model-level validation and integrity

- Add model validators for age 16-60 and marks 0-100. Form validation alone does not protect admin, scripts, services, or direct ORM writes.
- Add explicit numeric validators for old and new marks in `MarksHistory`.
- Retain or strengthen rating validation at the model level.
- Consider making `Department.name` unique.
- Use a structured duration field or validated duration format instead of unrestricted text.
- Decide whether deleting a user should leave a student record with `user=NULL`; document and test the intended behavior.
- Keep `User.email` and `Student.email` synchronized or store the email in one authoritative place.
- Wrap multi-model registration operations in `transaction.atomic()` so a failure cannot leave partial User/Student/UserProfile records.

## 2. Fix privacy and direct-URL authorization

### Student portal data exposure

`student_portal` queries and displays the complete student collection and global dashboard statistics for every authenticated user. A student should normally see only their own record, enrollments, marks, and visible feedback.

- Do not expose all student names, emails, marks, departments, and results to ordinary students.
- Do not expose top-student and recent-student data publicly or to students unless explicitly required.
- Give administrators a full directory, trainers only their assigned students, and students only their own data.

### Student detail ownership

`student_detail_view` accepts any student ID and does not verify that a student user owns that record. It filters feedback visibility but still exposes the selected student's profile, courses, marks, and latest marks update.

- Students must be restricted to their own `Student` record.
- Trainers must be restricted to students/enrollments assigned to them.
- Admins may access all student records.
- Add direct-ID manipulation tests for each role.

### Other authorization corrections

- Add an explicit student-role check to self-edit instead of relying only on the existence of a linked profile.
- Validate course/enrollment ownership when trainers add or edit feedback.
- Continue enforcing assigned-student ownership for marks updates and extend it to every related view.
- Use reusable permission helpers/services rather than repeating partial role checks.

## 3. Remove hardcoded admin credentials

The Django views contain a hardcoded admin username and password:

```text
admin / Admin@1234
```

This is a critical security defect.

- Remove the hardcoded credential constants and password comparison.
- Authenticate admins using Django authentication and role/permission checks.
- Do not restrict admin login to one fixed username.
- Never store real or demo passwords in application source code.
- If demo credentials are required, create them through seed tooling and document them as non-production credentials.
- Review the `_is_admin` fallback that grants admin behavior based on `is_staff` plus an `@admin.com` email address; authorization should use explicit permissions/roles, not an email suffix.

## 4. Improve authentication and audit security

- Login lockout is stored in the browser session, so it can be bypassed with a new browser/session. Track lockout against the account in persistent storage or document an appropriate cache-backed account key.
- Add a lockout expiry/unlock workflow; the current message tells the user to contact an administrator but account-management behavior is not integrated with the session counter.
- Make logout a CSRF-protected POST action instead of a state-changing GET route.
- Do not trust `X-Forwarded-For` unless the application is behind a configured trusted proxy; otherwise audit IP values can be spoofed.
- Use `PermissionDenied` or custom handlers instead of returning hardcoded HTML from role decorators.
- Add tests for unauthorized actions, logout method restrictions, lockout bypass resistance, and audit events.

## 5. Add missing error pages and HTTP handling

The required custom templates are absent:

- `403.html`
- `404.html`
- `500.html`

Add and verify them with `DEBUG=False`. Ensure permission failures render the custom 403 page rather than plain `HttpResponseForbidden` HTML.

Also:

- Add `app_name` and namespace application URL names.
- Make logout POST-only.
- Add an enrollment management URL/workflow.
- Add a full course-specific marks-history view, not only the latest history item.
- Preserve resource naming and use consistent authorization on every ID-based URL.

## 6. Add Django service boundaries

Complex dashboard, marks-history, feedback, audit, and account-management behavior is implemented directly in `views.py`.

- Create a `services.py` module for marks updates, feedback creation/editing, registration, and dashboard calculations.
- Keep views responsible for request validation, permission checks, and response selection.
- Make marks updates and history creation one atomic service operation.
- Add reusable ownership/assignment helpers.
- Document why these services can be reused by an API.

## 7. Student-list pagination and query review

- Search and filters exist, but the main student portal does not paginate its student queryset.
- Add pagination and preserve all search/filter parameters in pagination links.
- Review trainer/admin dashboards for query counts and N+1 behavior.
- Use `select_related()` for single-valued relations and `prefetch_related()` for collections wherever templates consume them.
- Inspect and document generated SQL for at least five important querysets.
- Add a measured before/after query optimization document as required.
- Add query-count tests for important list and dashboard pages.

## 8. Frontend and design corrections

- The shared base template and responsive viewport are present.
- Breadcrumbs and empty states exist on several pages.

Remaining work:

- Move the large CSS block from `base.html` into a project-owned static CSS file.
- Remove excessive inline `style` attributes throughout templates.
- Add loading/disabled states consistently where forms can be double-submitted.
- Convert the logout link into a POST form.
- Verify every page at desktop, tablet, and mobile widths; several fixed grid layouts may not collapse correctly.
- Ensure every page has a specific title, breadcrumb, consistent field errors, and accessible labels.
- Add local/static fallbacks or document reliance on external Google Fonts and Bootstrap CDNs.

## 9. FastAPI completion

The required FastAPI endpoints and validation work in smoke testing. Remaining work:

- Add at least 10 automated API tests or documented test cases. No FastAPI tests are currently included.
- Test all CRUD status codes, missing IDs, invalid email, invalid age, invalid marks, filtering, and pagination.
- Test duplicate email behavior and decide whether duplicates should be rejected.
- Add a FastAPI-specific README with install, run, Swagger, ReDoc, and test commands.
- Rename `requirement.txt` to the conventional `requirements.txt` requested by the task.
- Pin or constrain dependency versions for reproducible installation.
- Avoid global mutable test data leaking between test cases by resetting the in-memory list in fixtures.

## 10. Missing data, documentation, and release artifacts

### Seed/demo data

No fixture or management command is included.

- Add realistic administrators, trainers, students, departments, and courses.
- Create at least 20 students and 5 courses.
- Add enrollments, marks, feedback, and audit events.
- Provide non-production demo credentials for every role.
- Make the seed operation repeatable/idempotent.

### API and performance documentation

- Add the required `api_design.md` covering students, courses, enrollments, marks, and feedback.
- For each endpoint document method, request data, response data, permissions, and expected status codes.
- Add the required SQL/query optimization documentation.

### Production configuration

Current settings contain a committed secret key, `DEBUG=True`, an empty `ALLOWED_HOSTS`, and no `STATIC_ROOT`. Django's deployment check reports seven security warnings.

- Add a separate production settings example with `DEBUG=False`.
- Load `SECRET_KEY`, database settings, and allowed hosts from environment variables.
- Configure `STATIC_ROOT` and document `collectstatic`.
- Configure HTTPS redirect, HSTS, secure session cookies, and secure CSRF cookies for production.
- Keep development and production behavior separate so local HTTP remains usable.

### Project setup documentation

- Add a reproducible Django dependency file; the README currently says only `pip install django`.
- Document Django and FastAPI setup, migrations, clean-database tests, seed data, static collection, and deployment commands.
- Document how to run the 34 Django tests and the new FastAPI tests.

## Reassessment priority

1. Remove hardcoded admin credentials and fix student/detail privacy authorization.
2. Replace duplicate course/global marks fields with Enrollment-based course-specific records.
3. Add model-level validation and atomic service-layer operations.
4. Add custom error pages and student-list pagination.
5. Add at least 10 FastAPI tests and required seed data.
6. Complete API design, query optimization, production settings, static CSS, and setup documentation.
