# Student Management System

A Django-based web application to manage student records, courses, departments, grades, and trainer feedback with role-based access control.

## Features
* **Admin Portal:** Management of students, trainers, courses, and departments. Includes access to system audit logs.
* **Trainer Portal:** View assigned students, update marks with history logging, and submit feedback.
* **Student Portal:** Access individual profile data, view enrolled courses, and read feedback.
* **Security:** Password strength requirements and session lockout protection for multiple failed login attempts.

## How to Run

1. **Set up virtual environment:**
   ```bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Django:**
   ```bash
   pip install django
   ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the local server:**
   ```bash
   python manage.py runserver
   ```

5. Access the application in your browser at: `http://127.0.0.1:8000/`
