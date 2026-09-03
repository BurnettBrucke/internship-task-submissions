# EOD Report - Training Project

**Intern Name:** Deepika Vishwakarma  
**Date:** September 3, 2026  
**Training Module:** Django Basics, Models, Admin Panel, Templates, Forms and Validation  
**Repository Branch:** `burnettbrucke-intern-task-deepika`

---

## Task 1: Mini Django Setup

Completed the basic Django project setup.

### Work Completed:
- Created Django project named `training_project`.
- Created Django application named `students`.
- Ran the Django development server successfully.
- Created Home page.
- Created About page.
- Added separate URL paths for Home and About pages.
- Created HTML template for the Home page.
- Passed company name from view to template.
- Displayed the message:

`Welcome to Bug Network Private Limited Training Program`

---

## Task 2: Django Models and Admin

Completed the Student model and Django Admin functionality.

### Work Completed:
- Created `Student` model.
- Added fields:
  - Name
  - Email
  - Age
  - Course
  - Marks
  - Joined Date
  - Active Status
- Added meaningful `__str__()` method.
- Created and applied migrations.
- Registered Student model in Django Admin.
- Created a superuser.
- Added student records through the Admin Panel.
- Created Student List page.
- Displayed all students using Django templates.
- Displayed active students and total student count.
- Added Pass/Fail status based on marks.
- Students with marks >= 40 are displayed as Pass.
- Students with marks < 40 are displayed as Fail.
- Created `/students/` URL.

---

## Task 3: Django Form - Add Student

Completed the Add Student form using Django ModelForm.

### Work Completed:
- Created `StudentForm` using ModelForm.
- Created Add Student page.
- Added `/students/add/` URL.
- Created HTML template for the form.
- Added form validation.
- Saved valid student data to the database.
- Redirected to Student List page after successful submission.
- Displayed validation errors for invalid input.
- Added navigation links between Student List and Add Student pages.

### Validation Added:
- Name cannot be empty.
- Email must be valid.
- Age must be between 16 and 60.
- Marks must be between 0 and 100.
- Course cannot be empty.

---

## Testing Completed

The following cases were tested:

- Django development server.
- Home page.
- About page.
- Student model creation.
- Student records in Admin Panel.
- Student List page.
- Active student display.
- Total student count.
- Pass/Fail status.
- Add Student form.
- Empty name validation.
- Invalid email validation.
- Invalid age validation.
- Invalid marks validation.
- Valid student submission.
- Marks values 0, 40 and 100.

---

## Key Concepts Learned

- Django Project and App
- Django URL Routing
- Django Views
- Django Templates
- Template Context
- Django Models
- Model Fields
- Database Migrations
- Django Admin Panel
- Superuser
- QuerySets
- ModelForm
- Form Validation
- Template Loops and Conditions
- Redirects

---

## Challenges Faced

- Understanding the connection between URLs, Views and Templates.
- Understanding Django Models and Migrations.
- Creating and registering the Student model in Admin.
- Passing data from views to templates.
- Implementing form validation.
- Connecting the Add Student form with the database.

---

## Learning Outcome

I learned how to create a basic Django project and application. I also learned how to create models, perform migrations, use the Django Admin Panel, display database records using templates, and create forms using ModelForm with validation.

---

## Status

**All assigned Training Project tasks have been completed successfully.**