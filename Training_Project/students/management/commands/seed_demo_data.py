from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from students.models import Course, Department, Student, UserProfile


class Command(BaseCommand):
    help = "Create demo data for the Student Management System"

    def handle(self, *args, **options):

        # -------------------------
        # Departments
        # -------------------------
        departments_data = [
            ("Computer Science", "Computer Science and Programming"),
            ("Information Technology", "Information Technology and Software"),
            ("Data Science", "Data Science and Analytics"),
        ]

        departments = {}

        for name, description in departments_data:
            department, created = Department.objects.get_or_create(
                name=name,
                defaults={"description": description},
            )
            departments[name] = department

        # -------------------------
        # Courses
        # -------------------------
        courses_data = [
            ("Python Programming", "PY101", "3 Months"),
            ("Django Development", "DJ101", "3 Months"),
            ("Data Science", "DS101", "4 Months"),
            ("Machine Learning", "ML101", "4 Months"),
            ("Web Development", "WD101", "3 Months"),
        ]

        courses = {}

        for course_name, code, duration in courses_data:
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    "course_name": course_name,
                    "duration": duration,
                    "active": True,
                },
            )
            courses[course_name] = course

        # -------------------------
        # Demo Users + Students
        # -------------------------
        students_data = [
            ("Aarav Sharma", "aarav.demo@example.com", 22, 85, "Computer Science"),
            ("Priya Verma", "priya.demo@example.com", 23, 78, "Information Technology"),
            ("Rohan Patel", "rohan.demo@example.com", 21, 91, "Data Science"),
            ("Ananya Singh", "ananya.demo@example.com", 22, 88, "Computer Science"),
            ("Rahul Mehta", "rahul.demo@example.com", 23, 76, "Information Technology"),
            ("Sneha Gupta", "sneha.demo@example.com", 21, 92, "Data Science"),
            ("Vikas Jain", "vikas.demo@example.com", 24, 69, "Computer Science"),
            ("Neha Sharma", "neha.demo@example.com", 22, 84, "Information Technology"),
            ("Karan Malhotra", "karan.demo@example.com", 23, 73, "Data Science"),
            ("Pooja Verma", "pooja.demo@example.com", 21, 89, "Computer Science"),
        ]

        for name, email, age, marks, department_name in students_data:

            username = email.split("@")[0]

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": name.split()[0],
                    "last_name": name.split()[-1],
                    "is_active": True,
                },
            )

            if user_created:
                user.set_password("DemoStudent@123")
                user.save()

            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "role": "student",
                    "is_approved": True,
                },
            )

            if not profile_created:
                profile.role = "student"
                profile.is_approved = True
                profile.save()

            student, student_created = Student.objects.get_or_create(
                email=email,
                defaults={
                    "name": name,
                    "age": age,
                    "marks": marks,
                    "feedback": "Good performance",
                    "joined_date": date.today(),
                    "active": True,
                    "department": departments[department_name],
                    "user": user,
                },
            )

            student.courses.add(
                courses["Python Programming"],
                courses["Django Development"],
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created/verified successfully!"
            )
        )