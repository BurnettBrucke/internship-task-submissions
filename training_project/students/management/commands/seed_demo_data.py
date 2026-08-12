from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from students.models import (
    Department,
    Course,
    Student,
    StudentProfile,
    UserProfile,
    Feedback,
    MarksHistory,
    AuditLog,
)


class Command(BaseCommand):

    help = "Create demo data for the Student Training Portal"

    def handle(self, *args, **options):

        self.stdout.write("Creating demo data...")

        # =====================================================
        # 1. DEPARTMENTS
        # =====================================================

        departments_data = [
            ("Computer Science", "Computer Science and Engineering"),
            ("Information Technology", "Information Technology"),
            ("Electronics", "Electronics and Communication"),
            ("Mechanical", "Mechanical Engineering"),
            ("Civil", "Civil Engineering"),
        ]

        departments = []

        for name, description in departments_data:
            department, _ = Department.objects.get_or_create(
                name=name,
                defaults={
                    "description": description
                }
            )
            departments.append(department)

        # =====================================================
        # 2. COURSES
        # =====================================================

        courses_data = [
            ("Python Development", "PY101", "6 Months"),
            ("Django Development", "DJ101", "6 Months"),
            ("FastAPI Development", "FA101", "4 Months"),
            ("Web Development", "WEB101", "6 Months"),
            ("Data Science", "DS101", "8 Months"),
        ]

        courses = []

        for course_name, code, duration in courses_data:
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={
                    "course_name": course_name,
                    "duration": duration,
                    "active": True,
                }
            )
            courses.append(course)

        # =====================================================
        # 3. ADMIN USER
        # =====================================================

        admin_user, created = User.objects.get_or_create(
            username="demo_admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Demo",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            }
        )

        if created:
            admin_user.set_password("Admin@123")
            admin_user.save()

        UserProfile.objects.update_or_create(
            user=admin_user,
            defaults={
                "role": "admin",
                "is_approved": True,
            }
        )

        # =====================================================
        # 4. TRAINERS
        # =====================================================

        trainers = []

        for i in range(1, 3):

            username = f"demo_trainer{i}"

            trainer, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"trainer{i}@example.com",
                    "first_name": f"Trainer{i}",
                    "is_active": True,
                }
            )

            if created:
                trainer.set_password("Trainer@123")
                trainer.save()

            UserProfile.objects.update_or_create(
                user=trainer,
                defaults={
                    "role": "trainer",
                    "is_approved": True,
                }
            )

            trainers.append(trainer)

        # =====================================================
        # 5. STUDENTS - 20
        # =====================================================

        students = []

        for i in range(1, 21):

            username = f"demo_student{i}"

            student_user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"student{i}@example.com",
                    "first_name": f"Student{i}",
                    "is_active": True,
                }
            )

            if created:
                student_user.set_password("Student@123")
                student_user.save()

            UserProfile.objects.update_or_create(
                user=student_user,
                defaults={
                    "role": "student",
                    "is_approved": True,
                }
            )

            department = departments[(i - 1) % len(departments)]
            trainer = trainers[(i - 1) % len(trainers)]

            student, _ = Student.objects.get_or_create(
                email=f"student{i}@example.com",
                defaults={
                    "user": student_user,
                    "department": department,
                    "assigned_trainer": trainer,
                    "name": f"Demo Student {i}",
                    "age": 18 + (i % 8),
                    "course": courses[(i - 1) % len(courses)].course_name,
                    "marks": 45 + (i * 2),
                    "active": True,
                }
            )

            # Connect student with courses
            student.courses.set([
                courses[(i - 1) % len(courses)]
            ])

            # Student profile
            StudentProfile.objects.get_or_create(
                student=student,
                defaults={
                    "phone": f"90000000{i:02d}",
                    "address": f"Indore, Madhya Pradesh",
                    "date_of_birth": date(
                        2000 + (i % 6),
                        ((i - 1) % 12) + 1,
                        ((i - 1) % 25) + 1,
                    ),
                }
            )

            students.append(student)

        # =====================================================
        # 6. MARKS HISTORY
        # =====================================================

        for i, student in enumerate(students):

            trainer = student.assigned_trainer

            MarksHistory.objects.get_or_create(
                student=student,
                previous_marks=40 + i,
                new_marks=student.marks,
                updated_by=trainer,
                defaults={
                    "reason": "Initial demo marks update"
                }
            )

        # =====================================================
        # 7. FEEDBACK
        # =====================================================

        for i, student in enumerate(students):

            trainer = student.assigned_trainer

            Feedback.objects.get_or_create(
                trainer=trainer,
                student=student,
                defaults={
                    "rating": 4 + (i % 2),
                    "comments": (
                        "Good progress. Keep improving "
                        "technical and communication skills."
                    ),
                    "visible_to_student": True,
                }
            )

        # =====================================================
        # 8. AUDIT LOGS
        # =====================================================

        AuditLog.objects.get_or_create(
            user=admin_user,
            action="CREATE",
            description="Demo data created for Student Training Portal.",
        )

        for trainer in trainers:

            AuditLog.objects.get_or_create(
                user=trainer,
                action="FEEDBACK",
                description="Demo trainer feedback activity.",
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created successfully!"
            )
        )

        self.stdout.write("")
        self.stdout.write("Demo Credentials:")
        self.stdout.write("Admin   : demo_admin / Admin@123")
        self.stdout.write("Trainer : demo_trainer1 / Trainer@123")
        self.stdout.write("Student : demo_student1 / Student@123")
        self.stdout.write("")
        self.stdout.write("Students created: 20")
        self.stdout.write("Courses created: 5")
        self.stdout.write("Departments created: 5")