# EOD Report - Django Training Project

**Intern Name:** Deepika Vishwakarma  
**Date:** September 9, 2026  
**Training Module:** Django CRUD, Model Relationships, ORM, Authentication and Testing  
**Project:** `training_project`  
**Application:** `students`  
**Repository Branch:** `burnettbrucke-intern-task-deepika`

---

## Task 1: Student CRUD Operations

Completed complete CRUD functionality for Student records.

### Work Completed:

- Student List page
- Student Detail page
- Add Student functionality
- Edit Student functionality
- Delete Student functionality
- Delete confirmation page
- ModelForm for Add/Edit
- Form validation and success messages
- `get_object_or_404()` for student records
- Named URLs and navigation between pages

---

## Task 2: Django Model Relationships

Implemented the required model relationships.

### Work Completed:

- Created `Department` model with Student ForeignKey.
- Created `StudentProfile` with One-to-One relationship.
- Created `Course` with Many-to-Many relationship with Student.
- Added `related_name` values.
- Added meaningful `__str__()` methods.
- Created and applied migrations.
- Registered models in Django Admin.
- Added sample data for departments, courses, students and profiles.

---

## Task 3: Django ORM Queries

Completed Django ORM practice using Django Shell.

### Work Completed:

- Retrieved and filtered students.
- Applied marks and department filters.
- Ordered students and found top students.
- Worked with Course and Department relationships.
- Used `count()`, `aggregate()` and `annotate()`.
- Used `Q` objects for searching.
- Updated and deleted records using ORM.
- Practiced `select_related()` and `prefetch_related()`.
- Documented the ORM queries in `orm_queries.md`.

A total of **20 ORM queries** were practiced as required in the Day 3 task. :contentReference[oaicite:2]{index=2}

---

## Task 4: User Authentication

Implemented basic Django user authentication.

### Work Completed:

- User Registration
- User Login
- User Logout
- Protected Student pages
- Displayed logged-in username
- Used Django built-in User model
- Used authentication functions
- Used `login_required`
- Added Django messages
- Added Login/Register/Logout navigation
- Redirected users after login and logout

Student pages are accessible only to logged-in users as required. :contentReference[oaicite:3]{index=3}

---

## Task 5: Student Training Portal

Combined all Day 3 features into a Student Training Portal.

### Dashboard:

- Total Students
- Total Active Students
- Total Departments
- Total Courses
- Average Student Marks
- Highest-Scoring Student
- Recently Joined Students

### Student List:

- Student name and email
- Department
- Course count
- Marks and Pass/Fail status
- Active/Inactive status
- View, Edit and Delete actions

### Search & Filtering:

- Search by student name
- Search by email
- Search by course
- Filter by department
- Filter by course
- Filter by active/inactive status
- Filter by pass/fail status
- No-records message

### Template & Code Quality:

- Created and used a base template
- Used template inheritance
- Added navigation bar
- Added Django messages
- Used student data table
- Used named URLs and reverse URL resolution
- Avoided hard-coded URLs and duplicate code

These features cover the Day 3 Student Training Portal requirements. :contentReference[oaicite:4]{index=4}

---

## Testing Completed

Implemented and tested **15 test cases** covering:

- Student list
- Student detail
- Student creation
- Invalid form submission
- Student update
- Student deletion
- Login page
- Successful login
- Protected page redirect
- Department relationship
- One-to-one profile relationship
- Many-to-many course relationship
- Search functionality
- Department filter
- Dashboard totals

The Day 3 workbook requires at least 15 test cases, and all required cases were covered. :contentReference[oaicite:5]{index=5}

---

## Key Concepts Learned

- Django CRUD Operations
- Model Relationships
- ForeignKey
- OneToOneField
- ManyToManyField
- Django ORM
- QuerySets
- Q Objects
- Aggregation and Annotation
- Authentication
- `login_required`
- Django Messages
- Template Inheritance
- Named URLs
- Django Testing

---

## Challenges Faced

- Understanding CRUD flow in Django.
- Working with different model relationships.
- Writing and understanding ORM queries.
- Implementing authentication and protected pages.
- Applying search and multiple filters.
- Managing templates using inheritance.
- Writing tests for different Django features.

---

## Learning Outcome

I learned how to build a functional Django Student Training Portal using CRUD operations, model relationships, ORM queries, authentication, search/filtering, template inheritance and automated testing.

---

## Status

**All Day 3 assigned tasks have been completed successfully.**

**Pending Work:** None