## Day 5 — Service Layer Challenge

### Objective

The goal of the Day 5 service-layer challenge was to separate complex business and database logic from Django views.

The main objectives were:

* Move complex marks logic out of views.
* Move complex feedback logic out of views.
* Move complex dashboard logic out of views.
* Keep Django views focused on request handling and response selection.
* Create reusable validation or permission helpers where repeated logic exists.
* Structure the service layer so that the extracted logic can be reused later by an API.
* Document why the extracted service logic is easier to reuse.

---

# Service Layer Architecture

The application now uses dedicated service modules for the major business logic areas covered by this task.

```text
student/
│
├── services/
│   ├── __init__.py
│   ├── audit.py
│   ├── dashboard.py
│   ├── feedback.py
│   └── marks.py
│
├── models.py
├── forms.py
├── decorators.py
├── views.py
└── urls.py
```

The general flow is:

```text
                    Django Request
                          │
                          ▼
                       View
                          │
             Authentication / Permission
                          │
                          ▼
                   Service Function
                          │
                Business / ORM Logic
                          │
                          ▼
                      Database
                          │
                          ▼
                   Result / Context
                          │
                          ▼
                       View
                          │
                          ▼
                     HTTP Response
```

---

# 1. Marks Service

Marks-related database and business logic has been extracted into:

```text
student/services/marks.py
```

The service contains reusable functions such as:

```python
get_course_for_trainer()
get_assigned_student()
get_course_mark()
update_course_marks()
get_marks_history_for_user()
```

The view no longer needs to perform all of the database lookups itself.

For example, the marks view now follows this pattern:

```python
course = get_course_for_trainer(
    course_id=course_id,
    user=request.user,
)

assigned_student = get_assigned_student(
    course=course,
    student_id=student_id,
)

course_mark = get_course_mark(
    course=course,
    assigned_student=assigned_student,
    user=request.user,
)
```

The view is therefore responsible for:

* receiving the request
* checking the trainer role
* creating/validating the form
* calling the service
* selecting the response

The service is responsible for the underlying marks-related database and business logic.

---

# 2. Feedback Service

Feedback-related logic has been extracted into:

```text
student/services/feedback.py
```

The service contains functions such as:

```python
get_course_for_feedback()
get_assigned_student_for_feedback()
create_feedback()
get_feedback_for_edit()
update_feedback()
get_feedback_for_user()
```

For example, the feedback creation view uses:

```python
course = get_course_for_feedback(
    course_id=course_id,
    user=request.user,
)

assigned_student = get_assigned_student_for_feedback(
    course=course,
    student_id=student_id,
)
```

The actual feedback creation is then delegated to:

```python
feedback = create_feedback(
    user=request.user,
    course=course,
    assigned_student=assigned_student,
    form=form,
)
```

This keeps the view focused on HTTP handling while the service handles the reusable feedback logic.

---

# 3. Dashboard Service

Dashboard database and calculation logic has been extracted into:

```text
student/services/dashboard.py
```

It contains:

```python
get_admin_dashboard_data()
get_trainer_dashboard_data()
get_student_dashboard_data()
```

### Admin dashboard

The service handles:

* total users
* total students
* total trainers
* total courses
* recent users
* recent students
* pending trainer approvals
* course data

The view is now simply responsible for obtaining the service result and rendering the template.

```python
context = get_admin_dashboard_data()

return render(
    request,
    "dashboards/admin_dashboard.html",
    context
)
```

### Trainer dashboard

The service handles:

* trainer's assigned courses
* assigned students
* assigned course count
* assigned student count

The trainer view passes the authenticated user to the service:

```python
context = get_trainer_dashboard_data(request.user)
```

### Student dashboard

The service handles:

* student marks
* profile completion calculation
* course marks
* visible feedback
* related course and trainer information

The view first obtains the authenticated student's record and then passes it to the service:

```python
context = get_student_dashboard_data(students)
```

---

# 4. Audit Service

Audit-log creation has also been separated into:

```text
student/services/audit.py
```

The reusable function:

```python
create_audit_log()
```

is used by different parts of the application.

For example:

```python
create_audit_log(
    request=request,
    action_type="CREATE",
    description="Created student...",
    affected_object=student,
)
```

This avoids duplicating the audit-log creation implementation throughout the views.

The service is currently used by operations such as:

* successful login
* failed login
* logout
* password changes
* student creation
* student updates
* student deletion
* trainer approval
* account activation/deactivation
* marks updates
* feedback creation
* feedback updates

---

# 5. What Remains in the Views

The service-layer refactoring does not mean every piece of code should be moved out of `views.py`.

The views should continue handling HTTP-specific responsibilities.

For example:

```python
@login_required
@role_required(["trainer"])
def feedback_create(request, course_id, student_id):
```

The decorators remain in the view because authentication and authorization are part of request handling.

Similarly, the view should continue handling:

```python
request.method
request.POST
request.GET
form.is_valid()
render()
redirect()
messages.success()
messages.error()
```

These are HTTP/UI concerns and do not need to be moved into the service layer.

---

# 6. Authentication and Account Management

Authentication and account-management functionality currently remains in `views.py`.

This includes:

```text
custom_login()
custom_logout()
register_view()
CustomPasswordChangeView
CustomPasswordChangeDoneView
approve_trainer()
activate_account()
deactivate_account()
redirect_user_by_role()
```

These were intentionally not moved as part of the current service-layer challenge.

The login view currently handles:

* login form validation
* temporary login blocking
* failed login attempts
* account activation checks
* trainer approval checks
* successful authentication
* login audit logging

The registration view handles:

* user creation
* UserProfile creation
* student creation
* role assignment
* initial approval status
* registration audit logging

These areas can be candidates for future service extraction, but they are outside the current scope of the Day 5 service-layer challenge.

---

# 7. Course Management

Course-related functionality also remains in the views.

For example:

```python
assign_trainer()
```

continues to handle:

* course lookup
* trainer assignment
* form validation
* audit logging
* success messages
* response selection

Course management was not included in the current service extraction.

---

# 8. Student Management

Student management also remains in the views.

Current student views include:

```text
student_list()
student_detail()
student_create()
student_update()
student_delete()
```

These have not been moved into a separate student service because the current Day 5 challenge focuses specifically on the complex **marks, feedback, and dashboard** areas.

---

# 9. Audit Log Filtering

Audit-log creation is reusable through `services/audit.py`.

However, the current audit-log listing and filtering functionality remains in the view:

```python
audit_log_list()
```

The view currently handles:

* search
* action type filtering
* date filtering
* pagination
* rendering

The reusable audit-log creation logic and the audit-log listing/filtering logic are therefore separate concerns.

---

# 10. Permission and Validation Reusability

The application already has a reusable role-based permission decorator:

```python
@role_required(["admin"])
@role_required(["trainer"])
@role_required(["student"])
```

This avoids repeating role checks across views.

For example:

```python
@role_required(["trainer"])
def update_course_marks(...):
```

and:

```python
@role_required(["trainer"])
def feedback_create(...):
```

Both reuse the same permission mechanism.

This is preferable to repeatedly writing:

```python
if request.user.userprofile.role != "trainer":
    return HttpResponseForbidden()
```

inside every view.

Additional small permission helpers can be introduced when the same ownership rule is repeated across multiple services or views.

---

# 11. Why This Structure Helps With an API

One of the main benefits of the service layer is that the business logic is no longer tightly coupled to HTML templates.

For example, the dashboard view currently does:

```python
context = get_student_dashboard_data(student)
```

The service returns the required data without rendering an HTML page.

This means a future API endpoint could call the same service:

```text
HTML Request
     │
     ▼
Django View
     │
     ▼
Dashboard Service
     │
     ▼
Database
```

while an API could use:

```text
API Request
     │
     ▼
API View / ViewSet
     │
     ▼
Dashboard Service
     │
     ▼
Database
```

The business logic does not need to be rewritten just because the response format changes from HTML to JSON.

For example, the same:

```python
get_student_dashboard_data(student)
```

could provide the data used by an HTML view today and later be converted into serialized JSON by an API layer.

---

# 12. Benefits of the Service Layer

The current implementation provides several benefits:

### Separation of concerns

Views handle HTTP requests and responses, while services handle business and database logic.

### Reusability

Marks, feedback, dashboard, and audit functionality can be called from different parts of the application.

### Reduced duplication

Common database operations do not need to be rewritten in every view.

### Easier testing

Service functions can be tested independently from template rendering.

### API readiness

The service functions are not dependent on HTML templates, making them easier to reuse from future REST API endpoints.

### Maintainability

Changes to marks, feedback, or dashboard business rules can be made in the service layer without unnecessarily modifying the presentation layer.

---

# 13. Current Day 5 Service-Layer Result

```text
                     SERVICE LAYER
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
     Marks            Feedback          Dashboard
  marks.py          feedback.py        dashboard.py
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
                     Django Views
                          │
                          ▼
                    HTML Templates
```

The service-layer challenge therefore focuses on extracting the application's **complex marks, feedback, dashboard, and reusable audit logic**, while keeping authentication, account management, course management, and student management outside the current extraction scope.
