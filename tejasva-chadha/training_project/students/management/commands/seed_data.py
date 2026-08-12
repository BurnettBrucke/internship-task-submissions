from django.core.management.base import BaseCommand
from django.utils import timezone
from students.models import Department, Course, Student, StudentProfile
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds sample data for Departments, Courses, Students, and StudentProfiles'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        StudentProfile.objects.all().delete()
        Student.objects.all().delete()
        Department.objects.all().delete()
        Course.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Existing data cleared."))

        # 1. Create 3 Departments
        self.stdout.write("Creating departments...")
        depts_data = [
            {"name": "Computer Science", "description": "Study of computers, computational systems, software, and algorithms."},
            {"name": "Electrical Engineering", "description": "Study of electromagnetism, electronics, circuits, and electrical systems."},
            {"name": "Mechanical Engineering", "description": "Study of physical machines, thermodynamics, mechanics, and structural analysis."}
        ]
        departments = []
        for dept_info in depts_data:
            dept = Department.objects.create(**dept_info)
            departments.append(dept)
            self.stdout.write(f"Created Department: {dept.name}")

        # 2. Create 5 Courses
        self.stdout.write("Creating courses...")
        courses_data = [
            {"course_name": "Intro to Programming", "code": "CS101", "duration": 12, "active_status": True},
            {"course_name": "Database Management Systems", "code": "CS202", "duration": 16, "active_status": True},
            {"course_name": "Web Development Bootcamp", "code": "CS303", "duration": 14, "active_status": True},
            {"course_name": "Applied Machine Learning", "code": "CS404", "duration": 18, "active_status": True},
            {"course_name": "Basic Circuit Analysis", "code": "EE101", "duration": 12, "active_status": True}
        ]
        courses = []
        for course_info in courses_data:
            course = Course.objects.create(**course_info)
            courses.append(course)
            self.stdout.write(f"Created Course: {course.course_name} ({course.code})")

        # 3. Create 10 Students
        self.stdout.write("Creating students...")
        students_data = [
            {"name": "Rahul", "email": "rahul@example.com", "age": 20, "marks": 85, "active_status": True},
            {"name": "Priya", "email": "priya@example.com", "age": 22, "marks": 74, "active_status": True},
            {"name": "Amit", "email": "amit@example.com", "age": 19, "marks": 35, "active_status": False},
            {"name": "Sneha", "email": "sneha@example.com", "age": 21, "marks": 92, "active_status": True},
            {"name": "Karan", "email": "karan@example.com", "age": 20, "marks": 88, "active_status": True},
            {"name": "Riya", "email": "riya@example.com", "age": 23, "marks": 61, "active_status": True},
            {"name": "Neha", "email": "neha@example.com", "age": 20, "marks": 45, "active_status": True},
            {"name": "Rohit", "email": "rohit@example.com", "age": 22, "marks": 39, "active_status": False},
            {"name": "Ankit", "email": "ankit@example.com", "age": 21, "marks": 95, "active_status": True},
            {"name": "Pooja", "email": "pooja@example.com", "age": 20, "marks": 78, "active_status": True}
        ]
        
        today = timezone.localdate()
        for i, student_info in enumerate(students_data):
            # Assign a department
            dept = random.choice(departments)
            
            # Create student
            student = Student.objects.create(
                name=student_info["name"],
                email=student_info["email"],
                age=student_info["age"],
                course="Python", # For backward compatibility with the forms and old models
                marks=student_info["marks"],
                joined_date=today - timedelta(days=random.randint(1, 100)),
                active_status=student_info["active_status"],
                department=dept
            )
            self.stdout.write(f"Created Student: {student.name}")

            # Assign at least 2 courses
            assigned_courses = random.sample(courses, k=random.randint(2, 4))
            student.courses.set(assigned_courses)
            course_names = ", ".join([c.course_name for c in assigned_courses])
            self.stdout.write(f"  Assigned courses: {course_names}")

            # 4. Create profiles for at least 5 students (we will create for all of them)
            # Create student profile
            dob = date(2000 + random.randint(3, 7), random.randint(1, 12), random.randint(1, 28))
            profile = StudentProfile.objects.create(
                student=student,
                phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                address=f"{random.randint(100, 999)} Main St, Cityville, State {random.randint(10000, 99999)}",
                date_of_birth=dob
            )
            self.stdout.write(f"  Created Profile: Phone: {profile.phone}, DOB: {profile.date_of_birth}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded all sample data!"))
