# Training Project - Django Student Management System

## Overview

This project was created as part of the Burnett Brucke internship training.

The project is a basic Django-based Student Management System that demonstrates Django project setup, models, admin panel, templates, forms, database operations, validation, and URL routing.

---

## Technology Used

- Python
- Django
- SQLite
- HTML
- Django Templates

---

## Project Structure

Training_Project/
│
├── students/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── Training_Project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── README.md
---

# Tasks Completed

### Task 1 - Mini Django Setup

- Created a Django project named: **training_project**
- Created a Django application named: **students**

#### Features Implemented

- Created the Django project and application.
- Configured the students application.
- Ran the Django development server.
- Created a Home page.
- Created an About page.
- Created separate URL paths for Home and About pages.
- Created Django views for the pages.
- Created an HTML template for the Home page.
- Passed the company name from the view to the template.

#### Home Page Message

- `Welcome to Bug Network Private Limited Training Program`

#### URLs
- /          - Home page
- /about/    - About page

---

### Task 2 - Django Models and Admin Panel

- Created a Student model in the students application.

#### Student Model Fields
- Name
- Email
- Age
- Course
- Marks
- Joined date
- Active status

#### Features Implemented
- Created the Student model.
- Added a meaningful __str__() method.
- Created and ran migrations.
- Registered the Student model in Django Admin.
- Created a Django superuser.
- Added at least five student records through the Admin Panel.
- Created a student list page.
- Displayed all students.
- Displayed active students.
- Displayed total student count.
- Displayed Pass when marks are 40 or above.
- Displayed Fail when marks are below 40.
- Created the /students/ URL.
- Used Django templates for displaying student data.
- Used template loops and conditions.

#### Student List URL

- /students/

---

### Task 3 - Django Form - Add Student

- Created a ModelForm for the Student model.

#### Add Student Page

- /students/add/

#### Features Implemented

- Created a Django ModelForm.
- Created an Add Student page.
- Displayed the form using a Django template.
- Validated submitted student data.
- Saved valid student data to the database.
- Redirected to the student list page after successful submission.
- Displayed validation errors on the page.
- Added navigation links between the Student List and Add Student pages.
- Added a success message after successfully adding a student.

--- 

### Validation Rules

- Field	  =   Validation
- Name	  =   Cannot be empty
- Email	  =   Must be valid
- Age	  =   Must be between 16 and 60
- Marks	  =   Must be between 0 and 100
- Course  =   Cannot be empty

---

### Required Django Pages

##### URL	        ##### Page
- /	              =     Home Page
- /about/	      =     About Page
- /students/	  =     Student List Page
- /students/add/  = 	Add Student Page

---

### Testing Completed

The following test cases were checked:

- Student model creation
- Student list page
- Valid student form submission
- Invalid student form data
- Marks boundary value 0
- Marks boundary value 40
- Marks boundary value 100

---

### Key Django Concepts Learned

During this project, I learned and practiced:

- Django project setup
- Django applications
- URL routing
- Django views
- Django templates
- Template context
- Template loops
- Template conditions
- Django models
- Database migrations
- SQLite database
- Django Admin Panel
- Superuser creation
- ModelForm
- Form validation
- CRUD operations
- Redirects
- Success messages
- Error handling

---

### Learning Outcome

- By completing this project, I gained practical experience in developing a basic Django web application.

- I learned how different Django components such as models, views, URLs, templates, forms, and the admin panel work together.

- I also learned how to store student data in a database, display it dynamically using templates, validate form data, and create a simple student management system.

### Project Status

- All three assigned Django training tasks have been completed successfully.