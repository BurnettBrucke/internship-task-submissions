# Student Training Portal — Day 4

A secure, multi-role Django application (Administrator / Trainer / Student) with
server-side permission enforcement, reusable Bootstrap 5 templates, an audit
trail, a trainer feedback and marks workflow, and a full account-security
flow (registration, login lockout, password reset, activation).

---

## 1. Getting started

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install django

python manage.py makemigrations students
python manage.py migrate
python manage.py createsuperuser  # then set their role to Administrator in /admin/
python manage.py seed_roles       # optional: creates admin_demo/trainer_demo/student_demo
python manage.py test students    # 90 tests
python manage.py runserver
```

Demo accounts created by `seed_roles` (all use password `DemoPass123!`):

| Username | Role |
|---|---|
| `admin_demo` | Administrator |
| `trainer_demo` | Trainer (pre-approved, has a course + a student) |
| `student_demo` | Student (linked to a student record) |

---

## 2. Role and permission matrix

| Action | Administrator | Trainer (approved) | Trainer (pending) | Student |
|---|:---:|:---:|:---:|:---:|
| View own dashboard | ✅ | ✅ | Pending-approval page only | ✅ |
| View another role's dashboard | ✅ (admin only sees its own; can't view others by design either) | ❌ 403 | ❌ 403 | ❌ 403 |
| List all students | ✅ | Own students only | ❌ 403 | ❌ (redirected to own dashboard) |
| View a specific student | ✅ any | Only students in own courses | ❌ 403 | Only own record |
| Add / edit / delete student | ✅ | ❌ 403 | ❌ 403 | ❌ 403 |
| Update a student's marks | ✅ (via edit) | Only for own students, with mandatory reason | ❌ 403 | ❌ 403 |
| Add / edit feedback | ❌ (not a trainer action) | Own students only; can edit only own feedback | ❌ 403 | ❌ (view only) |
| View feedback | All (including drafts) | Own feedback given | ❌ | Only feedback marked visible |
| Manage users (activate/deactivate) | ✅ | ❌ 403 | ❌ 403 | ❌ 403 |
| Approve trainer accounts | ✅ | ❌ 403 | ❌ 403 | ❌ 403 |
| View audit log | ✅ | ❌ 403 | ❌ 403 | ❌ 403 |
| View reports (ORM challenges page) | ✅ | ❌ 403 | ❌ 403 | ❌ 403 |
| Self-register | Creates a Student account (public form) | Creates an unapproved Trainer account (separate public form) | — | — |
| Change own password | ✅ | ✅ | ✅ | ✅ |
| Reset forgotten password | ✅ | ✅ | ✅ | ✅ |

Every row above is enforced in the **view layer** (`students/decorators.py:role_required`,
plus explicit ownership checks in `students/views.py`), not just by hiding
buttons in templates — see Review Question 34 below.

---

## 3. Security notes

### Cookie / session settings and HTTPS

`training_project/settings.py` sets:

- `SESSION_COOKIE_HTTPONLY = True` — safe everywhere, including local HTTP
  development. Stops JavaScript from reading the session cookie.
- `SESSION_COOKIE_SECURE = False` and `CSRF_COOKIE_SECURE = False` — **these
  are left off deliberately.** Both settings tell the browser to only ever
  send the cookie over HTTPS. If turned on while running
  `manage.py runserver` on plain `http://127.0.0.1:8000`, the browser will
  silently refuse to send the cookie back, breaking login in a confusing
  way. They should only be switched to `True` in a production settings file
  once the app is actually served over HTTPS (e.g. behind an SSL-terminating
  load balancer/reverse proxy).
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = True` and `SESSION_COOKIE_AGE = 7200`
  (2 hours) — safe locally, reasonable defaults for a portal handling marks
  and personal feedback.

### Password rules

Enforced via `AUTH_PASSWORD_VALIDATORS` in settings.py:
- `UserAttributeSimilarityValidator` — rejects passwords too similar to
  username/email.
- `MinimumLengthValidator` (8 characters).
- `CommonPasswordValidator`.
- `NumericPasswordValidator`.
- **Custom** `students.validators.ComplexityValidator` — requires at least
  one uppercase letter, one lowercase letter, one digit, and one special
  character.

Password rules are displayed to the user before submission on the
registration and password-reset-confirm pages.

### Login protection (failed attempts / lockout) — design and known limitations

**Design:** `students/security.py` uses Django's cache framework (default
`LocMemCache` in this project) as a fast, live counter of failed attempts
per username, with a lockout flag set once 5 failures occur within a
15-minute window. Every attempt — successful, failed, and blocked-by-lockout
— is additionally written to the persistent `AuditLog` model via Django's
`user_logged_in` / `user_logged_out` / `user_login_failed` signals
(`students/signals.py`), so the historical record survives even if the
cache is cleared.

**Known limitations (and how production would improve on this):**

1. **`LocMemCache` is per-process and resets on restart.** In a real
   deployment with multiple worker processes (gunicorn/uWSGI) or containers,
   each process would have its own counter, so an attacker could get more
   than 5 real attempts by hitting different workers. Production should use
   a shared cache backend (Redis or Memcached) so all workers see the same
   counter.
2. **Lockout is keyed by username, not IP.** This protects a specific
   account from brute-forcing but doesn't stop one IP from hammering many
   different usernames (a "credential stuffing" pattern). Production should
   add IP-based rate limiting as well (e.g. `django-axes`, `django-ratelimit`,
   or a WAF/reverse-proxy rule).
3. **No exponential backoff.** The lockout window is a fixed 15 minutes
   regardless of how many times the limit has been hit. Production systems
   typically increase the lockout duration on repeated offenses.
4. **No CAPTCHA / bot detection.** Automated attempts are only slowed by the
   lockout, not distinguished from real users.
5. **Cache TTL isn't exposed**, so the lockout page can't tell the user
   precisely how many minutes remain — only that they should try again
   later. A Redis-backed implementation could store an expiry timestamp
   directly to display an accurate countdown.

### Email

`EMAIL_BACKEND` is set to the console backend for local development —
password-reset emails print to the terminal running `runserver` instead of
being sent. Swap this for a real backend (SMTP/SES/SendGrid/etc.) in
production settings.

---

## 4. Audit log

`students/models.py:AuditLog` records: `user` (+ `username` snapshot in case
the user is later deleted), `action_type` (LOGIN / LOGOUT / LOGIN_FAILED /
CREATE / UPDATE / DELETE / MARKS_UPDATE / FEEDBACK / ACCOUNT_STATUS),
`description`, `object_repr` (the affected object), `ip_address`, and
`timestamp`. Only Administrators can view it (`/admin-tools/audit-log/`),
with filters for username, action type, and a date range, plus pagination
and color-coded badges per action type.

## 5. ORM challenges (13–22)

Implemented as standalone, independently-tested functions in
`students/reports.py`, and surfaced to Administrators on the Reports page
(`/admin-tools/reports/`). See `students/tests.py:ORMReportTests` for
correctness checks on each one.

## 6. Testing

`students/tests.py` contains 90 tests covering CRUD, model relationships,
role-based dashboards, ownership rules (student/trainer), search/filtering,
password validation, trainer approval, account activation, login lockout,
audit log access and filtering, the feedback workflow (assignment, edit-own,
visibility, rating bounds), the marks workflow (reason required, history
recorded, students blocked from direct POST), and the ORM report functions.

Run with:
```bash
python manage.py test students
```

---

## 7. Known limitations

- The login-lockout counter uses the default in-memory cache (see Security
  notes above) — fine for a training project, not production-ready as-is.
- Email is console-only; no real SMTP is configured.
- IP address capture uses `REMOTE_ADDR` / `X-Forwarded-For` without
  validating the proxy chain — acceptable for a dev server, but a real
  deployment behind a load balancer needs `SECURE_PROXY_SSL_HEADER` and a
  trusted-proxy configuration to avoid IP spoofing via the header.
- Trainers currently have exactly one course each (`Course.trainer` is a
  single ForeignKey) — the workbook doesn't require multiple trainers per
  course, but a real system might want a many-to-many relationship there.
- "Enrolled students with no marks" is approximated as `marks == 0` with no
  `MarksHistory` entry, since `Student.marks` is a required (non-nullable)
  field in the existing schema rather than allowing a true NULL "ungraded"
  state.

---

## 8. Review questions

**33. What is the difference between authentication and authorization?**
Authentication answers "who are you?" — verifying identity, e.g. checking a
username/password pair. Authorization answers "what are you allowed to do?"
— once identity is known, deciding which actions/data that identity may
access. In this project, Django's login system handles authentication; the
`role_required` decorator and the ownership checks in `views.py` handle
authorization.

**34. Why is hiding a button not sufficient security?**
Hiding a button only changes what's rendered in the browser — it doesn't
stop someone from typing the URL directly, replaying a captured request, or
using a tool like curl/Postman to POST straight to the endpoint. Real
security has to be enforced server-side, on every request, regardless of
how the client got there. This project checks permissions in the view (via
`role_required` and functions like `_can_view_student`) rather than relying
only on templates conditionally showing links.

**35. What is ownership-based access control?**
A permission rule based on *whether the record belongs to the requesting
user*, not just their role. Two trainers both have the "Trainer" role, but
Trainer A should only manage Trainer A's own students — that's ownership,
layered on top of role. Implemented here via checks like
`student.courses.filter(trainer=request.user).exists()`.

**36. What is HTTP 403?**
The "Forbidden" status code: the server understood the request and
identified the user, but refuses to authorize it. This project raises
`PermissionDenied`, which Django turns into a 403 response, and renders a
custom `403.html` page (see `handler403` in `training_project/urls.py`).

**37. What is template inheritance?**
A Django templating feature where a "child" template
(`{% extends "base.html" %}`) reuses the structure of a parent template and
overrides specific `{% block %}` regions (title, content, extra_css,
extra_js here) rather than duplicating the surrounding HTML on every page.

**38. Why should repeated HTML be moved into include files?**
So there's a single source of truth: fixing a bug in the navbar, changing
how messages are styled, or improving pagination markup only requires
editing one file (`includes/navbar.html`, `includes/messages.html`,
`includes/pagination.html`) instead of hunting through every template that
copy-pasted the same block. It also reduces the chance that pages drift out
of sync with each other.

**39. What is the purpose of Bootstrap's grid system?**
A 12-column, responsive layout system (`.row` / `.col-*`) that lets a page
rearrange itself across screen sizes without custom CSS for every
breakpoint — e.g. dashboard cards that sit four-across on desktop
automatically stack to one or two per row on a phone.

**40. What is CSRF and how does Django protect against it?**
Cross-Site Request Forgery: a malicious site tricks a logged-in user's
browser into submitting a request (e.g. a form POST) to another site where
they're authenticated, performing an action they didn't intend. Django
protects against this with the `CsrfViewMiddleware` plus a per-session
token that must be included in every POST form (`{% csrf_token %}`) — a
request without a valid, matching token is rejected.

**41. How does Django store passwords?**
Never in plain text. By default Django hashes passwords with PBKDF2 (a
salted, iterated hash), storing the algorithm name, iteration count, salt,
and hash together in the `password` field. Even with full database access,
the original password can't be recovered directly — it must be brute-forced
against the hash.

**42. What is an audit log?**
A persistent, append-only record of who did what, to which object, from
where, and when — used to reconstruct history after the fact (e.g.
investigating a suspicious marks change or repeated failed logins). This
project's `AuditLog` model is exactly that.

**43. What is the difference between a role and a permission?**
A role is a named bundle of permissions assigned to a user (Administrator,
Trainer, Student). A permission is a single, specific allowed action (e.g.
"can delete a student", "can view the audit log"). Roles are a convenience
for grouping permissions so you don't have to assign each one individually;
this project uses a single `role` field plus explicit checks per view
rather than Django's full `Permission`/`Group` framework, since three
fixed roles cover the requirements.

**44. What is the difference between `LoginRequiredMixin` and
`UserPassesTestMixin`?**
`LoginRequiredMixin` (class-based-view equivalent of `@login_required`) only
checks that *someone* is authenticated — it doesn't care who. 
`UserPassesTestMixin` runs a custom test function against the logged-in
user and denies access if it returns `False` — used for authorization logic
beyond "are you logged in", e.g. "is this user staff" or "does this user
own this object". This project's function-based views use the equivalent
pattern via `@login_required` plus the custom `@role_required` decorator
(which itself is closer in spirit to `UserPassesTestMixin`, just for
function-based views).

**45. Why should direct POST requests still be permission-checked?**
Because a POST can be sent by anything, not just by clicking a link in the
rendered page — a browser's dev tools, curl, a saved HTML form, or a
malicious script. If the server only trusted "well, they got a POST request
to this URL" without re-checking who's allowed to do that, hiding the
button in the UI would be worthless. This project's `update_marks` view is
a concrete example: `role_required(ROLE_TRAINER)` blocks a student from
updating marks via a direct POST even though there's no "update marks"
button anywhere in the student's UI in the first place.

**46. What is pagination and why is it useful?**
Splitting a long result set into fixed-size pages (`Paginator` /
`page_obj` here) instead of rendering everything at once. It keeps page
load fast, keeps the UI usable (a table with thousands of rows is not
readable), and reduces database/query load per request. Used here for the
student list, user management list, and audit log.

**47. What is the purpose of Django messages?**
The `django.contrib.messages` framework lets a view attach a one-time
notification (success, error, info, warning) that survives the redirect to
the next page — e.g. "Student added successfully!" after a POST-redirect-GET
flow. This project renders them as dismissible Bootstrap alerts via
`includes/messages.html`.

---

## 9. Submission checklist

- [x] Updated `training_project` source code
- [x] Reusable templates and include files (`includes/navbar.html`,
      `includes/messages.html`, `includes/pagination.html`,
      `includes/form_errors.html`)
- [x] Role and permission matrix (this file, section 2)
- [x] Audit log, feedback, and marks-history implementation
- [x] 90 automated tests (`python manage.py test students`)
- [ ] Screenshots of the three dashboards and major forms — take these from
      a running `manage.py runserver` instance; not included in this
      generated package.
- [ ] Git commit ID — assign once this code is committed to your repository.

---

## 10. Query optimization (Day 5, Task 2)

### Before/after: the student list page

The clearest example in the project. `student_list` (and the underlying
`Student` queryset) needs each student's `department` (a `ForeignKey`) and
`courses` (a `ManyToMany`) to render the table. Measured directly with
Django's `CaptureQueriesContext` against 24 seeded students:

```python
# BEFORE -- naive queryset, one extra query per student per relation
for s in Student.objects.all():
    _ = s.department.name if s.department else None
    _ = list(s.courses.all())
# -> 49 queries

# AFTER -- students/views.py:student_list actually does this
for s in Student.objects.select_related('department').prefetch_related('courses').all():
    _ = s.department.name if s.department else None
    _ = list(s.courses.all())
# -> 2 queries
```

`select_related('department')` performs a SQL `JOIN` so the `ForeignKey` is
fetched in the same query as the students. `prefetch_related('courses')`
can't use a `JOIN` (a `ManyToMany` would multiply rows), so instead it runs
one extra query for *all* students' courses at once and stitches the results
together in Python — still a fixed 2 queries total regardless of how many
students there are, instead of 1 + N.

### A second N+1, found and fixed while testing with realistic seed data

`dashboards/trainer_dashboard.html` looped over a trainer's courses and
called `{{ course.students.count }}` inside the loop — one query per course
row. Fixed in `students/views.py:trainer_dashboard` by annotating the count
in the same queryset instead:

```python
# BEFORE
courses = Course.objects.filter(trainer=request.user)
# template: {% for course in courses %}{{ course.students.count }}{% endfor %}
# -> 1 query for courses + 1 query per course

# AFTER
courses = Course.objects.filter(trainer=request.user).annotate(student_count=Count('students'))
# template: {{ course.student_count }}
```

Verified with the test client + query counting: the trainer dashboard now
runs in a fixed **9 queries** regardless of how many courses/students exist,
where before it grew linearly with the number of courses. Covered by
`students/tests.py` view tests to make sure the page still renders correctly
with the annotation in place.

### Where `select_related` / `prefetch_related` are used elsewhere

| View | Optimization | Why |
|---|---|---|
| `student_list` | `select_related('department')`, `prefetch_related('courses')` | ForeignKey + ManyToMany needed per row |
| `student_detail` | `select_related('department', 'profile', 'user')`, `prefetch_related('courses')` | Multiple one-to-one/FK lookups on a single object |
| `manage_users` | `select_related('user')` | Every `UserProfile` row needs its `User` |
| `audit_log_view` | `select_related('user')` | Every log row displays the acting user |
| `trainer_dashboard` recent feedback | `select_related('student', 'course')` | Avoids a query per feedback row for its student and course |

### `count()` / `exists()` / `values()` / `values_list()`

- `_can_view_student()` and the ownership checks in `update_marks`/
  `add_feedback` use `.exists()` rather than `.count() > 0` or fetching the
  queryset — `exists()` runs a lightweight `SELECT 1 ... LIMIT 1` instead of
  counting or materializing rows.
- `trainer_dashboard` builds its student list via
  `.values_list('id', flat=True).distinct()` — pulling only the `id` column
  instead of full `Student` objects for the intermediate lookup.
- `reports.py`'s `users_with_excess_failed_logins()` uses
  `.values('username').annotate(...)` to group and count without needing
  full model instances for the intermediate aggregation.
- Dashboard totals (`services.dashboard_totals()`) use `.count()` and
  `.aggregate()` directly rather than `len(queryset)`, so the database does
  the counting instead of Django loading every row into Python first.

### Inspecting generated SQL

Five queries were inspected directly via `django.test.utils.CaptureQueriesContext`
and `str(queryset.query)` during development: the student list queryset
above, the trainer dashboard course-count fix, `reports.courses_below_average_marks()`,
`reports.trainer_student_counts()`, and the audit log's filtered/paginated
queryset. All confirmed to produce a small, fixed number of queries rather
than scaling with row count.
