from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from students.models import (
    AuditLog,
    Course,
    Department,
    Feedback,
    MarksHistory,
    Student,
    StudentProfile,
    TrainerAssignment,
    UserProfile,
)


class Command(BaseCommand):
    help = "Create realistic demo data for the Student Training Portal."

    ADMIN_USERNAME = "demo_admin"
    ADMIN_PASSWORD = "DemoAdmin@123"

    TRAINER_PASSWORD = "DemoTrainer@123"
    STUDENT_PASSWORD = "DemoStudent@123"

    def handle(self, *args, **options):
        self.stdout.write("Starting demo data setup...")

        departments = self.create_departments()
        courses = self.create_courses()

        admin = self.create_admin()
        trainers = self.create_trainers()
        students = self.create_students(departments, courses)

        self.create_assignments(trainers, students, courses)
        self.create_marks_history(trainers, students, courses)
        self.create_feedback(trainers, students, courses)
        self.create_audit_logs(admin, trainers, students)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created successfully."
            )
        )

        self.stdout.write("")
        self.stdout.write("Demo credentials:")
        self.stdout.write(
            f"Admin   : {self.ADMIN_USERNAME} / {self.ADMIN_PASSWORD}"
        )
        self.stdout.write(
            f"Trainer : demo_trainer1 / {self.TRAINER_PASSWORD}"
        )
        self.stdout.write(
            f"Student : demo_student1 / {self.STUDENT_PASSWORD}"
        )

    def create_departments(self):
        department_data = [
            (
                "Computer Science",
                "Computer Science and software development training.",
            ),
            (
                "Data Science",
                "Data analytics, machine learning and data science training.",
            ),
            (
                "Information Technology",
                "Web development, databases and IT fundamentals.",
            ),
        ]

        departments = []

        for name, description in department_data:
            department, _ = Department.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                },
            )

            departments.append(department)

        self.stdout.write(
            self.style.SUCCESS(
                f"Departments ready: {len(departments)}"
            )
        )

        return departments

    def create_courses(self):
        course_data = [
            ("Python Development", "PY101", "12 Weeks"),
            ("Django Web Development", "DJ201", "10 Weeks"),
            ("Data Science", "DS301", "16 Weeks"),
            ("Machine Learning", "ML401", "14 Weeks"),
            ("FastAPI Development", "FA501", "8 Weeks"),
        ]

        courses = []

        for course_name, code, duration in course_data:
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    "course_name": course_name,
                    "duration": duration,
                    "is_active": True,
                },
            )

            if not created:
                course.course_name = course_name
                course.duration = duration
                course.is_active = True
                course.save(
                    update_fields=[
                        "course_name",
                        "duration",
                        "is_active",
                    ]
                )

            courses.append(course)

        self.stdout.write(
            self.style.SUCCESS(
                f"Courses ready: {len(courses)}"
            )
        )

        return courses

    def create_admin(self):
        user, created = User.objects.get_or_create(
            username=self.ADMIN_USERNAME,
            defaults={
                "email": "demo.admin@example.com",
                "first_name": "Demo",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(self.ADMIN_PASSWORD)
            user.save()
        else:
            user.email = "demo.admin@example.com"
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(self.ADMIN_PASSWORD)
            user.save(
                update_fields=[
                    "email",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "password",
                ]
            )

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "role": UserProfile.UserRole.ADMIN,
                "is_approved": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Admin account ready."
            )
        )

        return user

    def create_trainers(self):
        trainers = []

        for number in range(1, 6):
            username = f"demo_trainer{number}"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": (
                        f"demo.trainer{number}"
                        "@example.com"
                    ),
                    "first_name": "Demo",
                    "last_name": f"Trainer {number}",
                    "is_active": True,
                },
            )

            if created:
                user.set_password(self.TRAINER_PASSWORD)
                user.save()
            else:
                user.email = (
                    f"demo.trainer{number}"
                    "@example.com"
                )
                user.is_active = True
                user.set_password(self.TRAINER_PASSWORD)
                user.save(
                    update_fields=[
                        "email",
                        "is_active",
                        "password",
                    ]
                )

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": UserProfile.UserRole.TRAINER,
                    "is_approved": True,
                },
            )

            trainers.append(user)

        self.stdout.write(
            self.style.SUCCESS(
                f"Trainers ready: {len(trainers)}"
            )
        )

        return trainers

    def create_students(self, departments, courses):
        students = []

        first_names = [
            "Aarav",
            "Vivaan",
            "Aditya",
            "Arjun",
            "Rohan",
            "Karan",
            "Rahul",
            "Vikram",
            "Nikhil",
            "Yash",
            "Ananya",
            "Priya",
            "Kavya",
            "Sneha",
            "Isha",
            "Riya",
            "Neha",
            "Pooja",
            "Meera",
            "Simran",
        ]

        for number, first_name in enumerate(first_names, start=1):
            username = f"demo_student{number}"
            email = f"demo.student{number}@example.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": "Demo",
                    "is_active": True,
                },
            )

            if created:
                user.set_password(self.STUDENT_PASSWORD)
                user.save()
            else:
                user.email = email
                user.is_active = True
                user.set_password(self.STUDENT_PASSWORD)
                user.save(
                    update_fields=[
                        "email",
                        "is_active",
                        "password",
                    ]
                )

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": UserProfile.UserRole.STUDENT,
                    "is_approved": True,
                },
            )

            department = departments[(number - 1) % len(departments)]

            student, _ = Student.objects.update_or_create(
                email=email,
                defaults={
                    "user": user,
                    "name": f"{first_name} Demo",
                    "age": 18 + ((number - 1) % 8),
                    "department": department,
                    "marks": 45 + ((number * 3) % 51),
                    "joined_date": (
                        date.today()
                        - timedelta(days=number * 7)
                    ),
                    "is_active": number != 20,
                },
            )

            profile_date = date(
                2000 + ((number - 1) % 6),
                ((number - 1) % 12) + 1,
                ((number - 1) % 28) + 1,
            )

            StudentProfile.objects.update_or_create(
                student=student,
                defaults={
                    "phone": f"90000000{number:02d}",
                    "address": f"Demo Address {number}, India",
                    "date_of_birth": profile_date,
                },
            )

            student.courses.set(
                [
                    courses[(number - 1) % len(courses)],
                    courses[number % len(courses)],
                ]
            )

            students.append(student)

        self.stdout.write(
            self.style.SUCCESS(
                f"Students ready: {len(students)}"
            )
        )

        return students

    def create_assignments(self, trainers, students, courses):
        assignment_count = 0

        for number, student in enumerate(students, start=1):
            trainer = trainers[(number - 1) % len(trainers)]

            assigned_courses = list(
                student.courses.all()
            )

            for course in assigned_courses:
                _, created = TrainerAssignment.objects.get_or_create(
                    trainer=trainer,
                    student=student,
                    course=course,
                )

                if created:
                    assignment_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Trainer assignments ready: {assignment_count}"
            )
        )

    def create_marks_history(self, trainers, students, courses):
        history_count = 0

        for number, student in enumerate(students, start=1):
            trainer = trainers[(number - 1) % len(trainers)]
            assigned_courses = list(
                student.courses.all()
            )

            for course in assigned_courses:
                existing = MarksHistory.objects.filter(
                    student=student,
                    course=course,
                ).exists()

                if existing:
                    continue

                previous_marks = max(
                    0,
                    int(student.marks) - 5,
                )

                MarksHistory.objects.create(
                    student=student,
                    course=course,
                    previous_marks=previous_marks,
                    new_marks=student.marks,
                    updated_by=trainer,
                    reason="Initial demo assessment.",
                )

                history_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Marks history records ready: {history_count}"
            )
        )

    def create_feedback(self, trainers, students, courses):
        feedback_count = 0

        feedback_messages = [
            "Good progress and consistent participation.",
            "Strong understanding of the course concepts.",
            "Needs more practice with practical assignments.",
            "Excellent performance and problem-solving skills.",
            "Shows steady improvement throughout the training.",
        ]

        for number, student in enumerate(students, start=1):
            trainer = trainers[(number - 1) % len(trainers)]
            assigned_courses = list(
                student.courses.all()
            )

            for course in assigned_courses:
                if Feedback.objects.filter(
                    trainer=trainer,
                    student=student,
                    course=course,
                ).exists():
                    continue

                Feedback.objects.create(
                    trainer=trainer,
                    student=student,
                    course=course,
                    rating=1 + ((number - 1) % 5),
                    feedback=feedback_messages[
                        (number - 1) % len(feedback_messages)
                    ],
                    is_visible=True,
                )

                feedback_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Feedback records ready: {feedback_count}"
            )
        )

    def create_audit_logs(self, admin, trainers, students):
        if AuditLog.objects.filter(
            object_name="Demo Data",
        ).exists():
            return

        AuditLog.objects.create(
            user=admin,
            action=AuditLog.Action.CREATE,
            object_name="Demo Data",
            description="Demo dataset initialized.",
            ip_address="127.0.0.1",
        )

        AuditLog.objects.create(
            user=admin,
            action=AuditLog.Action.STATUS_CHANGE,
            object_name="Demo Data",
            description="Demo student account status changed.",
            ip_address="127.0.0.1",
        )

        AuditLog.objects.create(
            user=trainers[0],
            action=AuditLog.Action.MARKS_UPDATE,
            object_name="Demo Data",
            description=(
                f"Demo marks updated for "
                f"{students[0].name}."
            ),
            ip_address="127.0.0.1",
        )

        AuditLog.objects.create(
            user=trainers[0],
            action=AuditLog.Action.FEEDBACK,
            object_name="Demo Data",
            description=(
                f"Demo feedback added for "
                f"{students[0].name}."
            ),
            ip_address="127.0.0.1",
        )

        AuditLog.objects.create(
            user=admin,
            action=AuditLog.Action.LOGIN,
            object_name="Demo Data",
            description="Demo administrator login event.",
            ip_address="127.0.0.1",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Audit log demo events created."
            )
        )