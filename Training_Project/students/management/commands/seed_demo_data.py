from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from students.models import (
    AuditLog,
    Course,
    CourseMark,
    Department,
    Feedback,
    MarksHistory,
    Student,
    UserProfile,
)


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
        # Demo Admin
        # -------------------------
        admin_user, admin_created = User.objects.get_or_create(
            username="demo_admin",
            defaults={
                "email": "demo_admin@example.com",
                "first_name": "Demo",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if admin_created:
            admin_user.set_password("DemoAdmin@123")
            admin_user.save()

        UserProfile.objects.update_or_create(
            user=admin_user,
            defaults={
                "role": "admin",
                "is_approved": True,
            },
        )

        # -------------------------
        # Demo Trainer
        # -------------------------
        trainer_user, trainer_created = User.objects.get_or_create(
            username="demo_trainer",
            defaults={
                "email": "demo_trainer@example.com",
                "first_name": "Demo",
                "last_name": "Trainer",
                "is_active": True,
            },
        )

        if trainer_created:
            trainer_user.set_password("DemoTrainer@123")
            trainer_user.save()

        UserProfile.objects.update_or_create(
            user=trainer_user,
            defaults={
                "role": "trainer",
                "is_approved": True,
            },
        )

        # Assign trainer to all demo courses
        for course in courses.values():
            course.trainer.add(trainer_user)

        # -------------------------
        # Demo Students
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
            ("Aditya Joshi", "aditya.demo@example.com", 22, 81, "Information Technology"),
            ("Kavya Mishra", "kavya.demo@example.com", 21, 94, "Data Science"),
            ("Arjun Yadav", "arjun.demo@example.com", 23, 72, "Computer Science"),
            ("Simran Kaur", "simran.demo@example.com", 22, 87, "Information Technology"),
            ("Mohit Agarwal", "mohit.demo@example.com", 24, 79, "Data Science"),
            ("Isha Tiwari", "isha.demo@example.com", 21, 90, "Computer Science"),
            ("Nikhil Soni", "nikhil.demo@example.com", 23, 68, "Information Technology"),
            ("Riya Kapoor", "riya.demo@example.com", 22, 86, "Data Science"),
            ("Yash Dubey", "yash.demo@example.com", 24, 74, "Computer Science"),
            ("Muskan Khan", "muskan.demo@example.com", 21, 93, "Information Technology"),
        ]

        created_students = []

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

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": "student",
                    "is_approved": True,
                },
            )

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

            # Update important fields if student already exists
            student.name = name
            student.age = age
            student.marks = marks
            student.feedback = "Good performance"
            student.active = True
            student.department = departments[department_name]
            student.user = user
            student.save()

            created_students.append(student)

        # -------------------------
        # Assign Courses to Students
        # -------------------------
        course_list = list(courses.values())

        for index, student in enumerate(created_students):

            first_course = course_list[index % len(course_list)]
            second_course = course_list[(index + 1) % len(course_list)]

            student.courses.add(
                first_course,
                second_course,
            )

        # -------------------------
        # Course Marks
        # -------------------------
        for index, student in enumerate(created_students):

            assigned_courses = list(student.courses.all())

            for course_index, course in enumerate(assigned_courses):

                course_marks = min(
                    100,
                    max(
                        40,
                        student.marks + ((course_index * 3) - 2),
                    ),
                )

                course_mark, created = CourseMark.objects.update_or_create(
                    student=student,
                    course=course,
                    defaults={
                        "marks": course_marks,
                        "updated_by": trainer_user,
                    },
                )

                # -------------------------
                # Marks History
                # -------------------------
                if created:
                    MarksHistory.objects.create(
                        student=student,
                        course=course,
                        previous_marks=0,
                        new_marks=course_marks,
                        updated_by=trainer_user,
                        reason="Initial demo marks entry",
                    )

        # -------------------------
        # Feedback
        # -------------------------
        feedback_comments = [
            "Good understanding of the concepts.",
            "Shows consistent progress.",
            "Good practical performance.",
            "Needs more practice but improving well.",
            "Excellent participation and performance.",
        ]

        for index, student in enumerate(created_students):

            assigned_courses = list(student.courses.all())

            if assigned_courses:
                course = assigned_courses[0]

                Feedback.objects.get_or_create(
                    student=student,
                    trainer=trainer_user,
                    course=course,
                    defaults={
                        "rating": (index % 5) + 1,
                        "comment": feedback_comments[index % len(feedback_comments)],
                        "is_visible": True,
                    },
                )

        # -------------------------
        # Audit Logs
        # -------------------------
        audit_events = [
            (
                "SEED_DATA",
                "Demo departments and courses created/verified.",
                "Department/Course",
            ),
            (
                "SEED_USERS",
                "Demo admin and trainer accounts created/verified.",
                "demo_admin, demo_trainer",
            ),
            (
                "SEED_STUDENTS",
                "Demo student records created/verified.",
                "20 students",
            ),
            (
                "SEED_MARKS",
                "Demo course marks and marks history created/verified.",
                "CourseMark/MarksHistory",
            ),
            (
                "SEED_FEEDBACK",
                "Demo trainer feedback created/verified.",
                "Feedback",
            ),
        ]

        for action, description, affected_object in audit_events:
            AuditLog.objects.get_or_create(
                user=admin_user,
                action=action,
                description=description,
                affected_object=affected_object,
                defaults={
                    "ip_address": None,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created/verified successfully!"
            )
        )