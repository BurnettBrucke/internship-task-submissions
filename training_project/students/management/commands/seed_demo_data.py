from django.core.management.base import BaseCommand
from datetime import date, timedelta

from students.models import (
    Department,
    Course,
    Student,
    StudentProfile,
)


class Command(BaseCommand):
    help = "Create realistic demo data for Student Training Portal"

    def handle(self, *args, **kwargs):

        # Existing Departments
        departments = {
            "Computer Science": Department.objects.get(
                name="Computer Science"
            ),
            "Information Technology": Department.objects.get(
                name="Information Technology"
            ),
            "Electronics": Department.objects.get(
                name="Electronics"
            ),
        }

        # Existing Courses
        courses = {
            "Python Development": Course.objects.get(
                code="PY101"
            ),
            "Django Development": Course.objects.get(
                code="DJ201"
            ),
            "Core Java Programming": Course.objects.get(
                code="JA301"
            ),
            "Web Development": Course.objects.get(
                code="WD401"
            ),
            "Database Management": Course.objects.get(
                code="DB501"
            ),
        }

        # Add 4 additional demo students
        student_data = [
            (
                "Aarav Sharma",
                "aarav.demo@example.com",
                21,
                "Computer Science",
                82,
            ),
            (
                "Priya Verma",
                "priya.demo@example.com",
                22,
                "Information Technology",
                76,
            ),
            (
                "Rahul Mehta",
                "rahul.demo@example.com",
                23,
                "Electronics",
                91,
            ),
            (
                "Ananya Singh",
                "ananya.demo@example.com",
                20,
                "Computer Science",
                68,
            ),
        ]

        for index, data in enumerate(student_data):

            name, email, age, department_name, marks = data

            student, created = Student.objects.get_or_create(
                email=email,
                defaults={
                    "name": name,
                    "age": age,
                    "department": departments[department_name],
                    "marks": marks,
                    "joined_date": date.today()
                    - timedelta(days=index * 10),
                    "active_status": True,
                },
            )

            student.courses.set(
                [
                    courses["Python Development"],
                    courses["Django Development"],
                ]
            )

            StudentProfile.objects.get_or_create(
                student=student,
                defaults={
                    "phone": f"98765000{index + 21:02d}",
                    "address": f"{index + 21}, Demo Street, Indore",
                    "date_of_birth": date(
                        2000 + index,
                        index + 1,
                        index + 10,
                    ),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "4 additional demo students and their profiles "
                "created successfully."
            )
        )