import random
from datetime import date

from django.core.management.base import BaseCommand

from students.models import Course, Department, Student, StudentProfile


class Command(BaseCommand):
    help = "Seed the database with sample departments, courses, and students."

    def handle(self, *args, **options):
        random.seed(42)

        # --- Departments ---
        dept_names = ["Computer Science", "Business Administration", "Design"]
        departments = [
            Department.objects.get_or_create(
                name=name, defaults={"description": f"{name} department"}
            )[0]
            for name in dept_names
        ]

        # --- Courses ---
        course_data = [
            ("Python and Django", "PYDJ101", 6),
            ("Data Science", "DS201", 8),
            ("Web Development", "WEBDEV110", 6),
            ("Machine Learning", "ML301", 10),
            ("Cloud Computing", "CLOUD210", 6),
        ]
        courses = [
            Course.objects.get_or_create(
                code=code, defaults={"name": name, "duration_weeks": weeks, "is_active": True}
            )[0]
            for name, code, weeks in course_data
        ]

        # --- Students ---
        student_data = [
            ("Asha Verma", "asha.verma@example.com", 21, 82, True),
            ("Rohit Sharma", "rohit.sharma@example.com", 24, 35, True),
            ("Priya Singh", "priya.singh@example.com", 19, 91, True),
            ("Karan Mehta", "karan.mehta@example.com", 27, 40, False),
            ("Sneha Rao", "sneha.rao@example.com", 22, 58, True),
            ("Arjun Nair", "arjun.nair@example.com", 23, 45, True),
            ("Divya Iyer", "divya.iyer@example.com", 20, 29, True),
            ("Vikram Joshi", "vikram.joshi@example.com", 26, 67, False),
            ("Neha Kulkarni", "neha.kulkarni@example.com", 25, 73, True),
            ("Aditya Kapoor", "aditya.kapoor@example.com", 18, 88, True),
        ]

        created_students = []
        for i, (name, email, age, marks, active) in enumerate(student_data):
            student, _ = Student.objects.get_or_create(
                email=email,
                defaults={
                    "name": name,
                    "age": age,
                    "marks": marks,
                    "is_active": active,
                    "department": departments[i % len(departments)],
                },
            )
            # Assign at least two courses to every student.
            assigned = random.sample(courses, k=2)
            if courses[i % len(courses)] not in assigned:
                assigned.append(courses[i % len(courses)])
            student.courses.set(assigned)
            created_students.append(student)

        # --- Profiles for at least five students ---
        for student in created_students[:6]:
            StudentProfile.objects.get_or_create(
                student=student,
                defaults={
                    "phone": f"9{random.randint(100000000, 999999999)}",
                    "address": f"{random.randint(1, 200)} Main Street",
                    "date_of_birth": date(1998, (student.id % 12) + 1, (student.id % 27) + 1),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Department.objects.count()} departments, "
            f"{Course.objects.count()} courses, "
            f"{Student.objects.count()} students, "
            f"{StudentProfile.objects.count()} profiles."
        ))
