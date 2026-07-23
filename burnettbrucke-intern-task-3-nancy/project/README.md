# Training Project — Django Models & Admin Panel + Add Student Form

## Setup
```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Pages
- `/` — Home page
- `/about/` — About page
- `/students/` — Student list (shows every student, active count, total count, Pass/Fail per marks)
- `/students/add/` — Add Student form (validated ModelForm, redirects to the list on success, flashes a success message)
- `/admin/` — Django admin, where the `Student` model is registered

## Model — `students/models.py`
`Student`: name, email (unique), age (16–60), course, marks (0–100), joined_date
(auto-set on creation), is_active (defaults to True). `__str__` returns
`"<name> (<course>)"`. A `result_status` property returns `"Pass"` when
marks >= 40, otherwise `"Fail"`.

## Form — `students/forms.py`
`StudentForm` is a `ModelForm` over `name`, `email`, `age`, `course`, `marks`
with explicit `clean_*` validators enforcing:
- Name and Course cannot be empty (whitespace-only counts as empty).
- Email must be a valid address (built-in `EmailField` validation).
- Age must be between 16 and 60.
- Marks must be between 0 and 100.

## Tests — `students/tests.py`
19 tests covering: model creation and `__str__`, marks boundary values
(0, 40, 100), the student-list view (context counts, empty state,
Pass/Fail rendering), form validation (valid data, empty name, bad email,
out-of-range age/marks, empty course), the add-student view (valid POST
redirects and persists, invalid POST re-renders with errors and saves
nothing), and the home/about pages.

Run with:
```bash
python manage.py test students -v 2
```
All 19 tests pass.

## Seed data / demo admin account
For convenience while testing, you can create a superuser and add students
either through `/admin/` or by using the shell:
```bash
python manage.py createsuperuser
```
Then log in at `/admin/` and add Student records, or use `/students/add/`.

## Note on the task sheet's "employee JSON" testing requirements
The task sheet's testing list also mentions employee-JSON-file scenarios
(missing/empty file, duplicate employee ID, invalid salary, empty employee
list). Those belong to a separate exercise (an employee/JSON-based task) that
isn't part of this Django project's scope (Student model, admin, list page,
add-student form) — nothing in the provided codebase or this task's
requirements involves employee JSON files, so no code or tests were added
for that unrelated piece. Everything else in the testing checklist (student
model creation, student list page, invalid/valid student form data, and
marks boundary values 0/40/100) is covered above.
