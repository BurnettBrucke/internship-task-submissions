# Django Training Project

## Project Overview

This project is created as part of training project tasks. It demonstrates basic Django concepts including project setup, URL routing, views, templates, models, migrations, Django Admin, ModelForms, form validation, messages, and CRUD-related operations.

## Setup Instructions

1. Make sure Python is installed.
2. Open the terminal in the `training_project` directory.
3. Install Django:

```bash
pip install django
```

4. Run the database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the Server

Start the Django development server using:

```bash
python manage.py runserver
```

The project will be available at:

`http://127.0.0.1:8000/`

## Created URLs

| URL              | Purpose                |
| ---------------- | ---------------------- |
| `/`              | Home page              |
| `/about/`        | About page             |
| `/students/`     | Student list/dashboard |
| `/students/add/` | Add new student        |
| `/admin/`        | Django Admin panel     |

## Tasks Completed

### Django Mini Setup

* Created Django project and `students` app.
* Configured URL routing.
* Created Home and About pages.
* Created a Home template.
* Passed company name from the view to the template.
* Displayed the training program message.

### Django Models and Admin

* Created the `Student` model.
* Added student fields including name, email, age, course, marks, joined date, and active status.
* Created and applied database migrations.
* Registered the Student model in Django Admin.
* Created and tested a Django Admin superuser.
* Added and managed student records through Django Admin.
* Verified that the Student model migration works successfully on a fresh database.
* Verified that the Student model appears correctly in Django Admin.

### Student List

* Created the Student List page.
* Displayed total student count.
* Displayed active student count.
* Implemented Pass/Fail result based on marks.
* Added active/inactive status display.
* Added navigation between Student List and Add Student pages.

### Student Form

* Created a `StudentForm` using Django ModelForm.
* Added form validation for:

  * Name
  * Email
  * Age
  * Course
  * Marks
* Added CSRF protection.
* Added success message after successfully adding a student.
* Tested valid and invalid form inputs.
* Tested boundary marks such as 0, 40, and 100.

## Problems Faced

* Faced migration-related issues while setting up and modifying the Student model.
* Verified the migration process on a fresh database to ensure the model can be created correctly.
* Tested the Django Admin panel after fresh migration.
* Configured form validation and tested different invalid and boundary inputs.

## Topics Learned

* Django project and app structure
* URL routing
* Views
* Templates
* Django Models
* Database migrations
* Django ORM basics
* Django Admin
* ModelForm
* Form validation
* CSRF protection
* GET and POST requests
* Django messages framework
* Redirects
* Fresh database migration testing

## Pending Work

* Final Git commit and submission.
* Push the completed work to the assigned GitHub branch.

## Git Commit ID

`To be added after the final submission commit.`
