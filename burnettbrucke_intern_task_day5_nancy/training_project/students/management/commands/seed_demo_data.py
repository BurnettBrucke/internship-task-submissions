import random
from decimal import Decimal

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
    UserProfile,
    log_action,
)

FIRST_NAMES = [
    "Asha", "Ravi", "Zara", "Mohan", "Priya", "Karan", "Neha", "Arjun", "Divya", "Rahul",
    "Meera", "Sanjay", "Anita", "Vikram", "Pooja", "Rohan", "Sneha", "Aditya", "Kavya", "Ishaan",
    "Tanya", "Nikhil", "Riya", "Amit",
]
LAST_NAMES = [
    "Verma", "Kumar", "Khan", "Sharma", "Iyer", "Mehta", "Gupta", "Nair", "Reddy", "Singh",
    "Das", "Chopra", "Rao", "Joshi", "Bhatt", "Pillai", "Agarwal", "Kapoor", "Malhotra", "Sethi",
]

DEPARTMENTS = [
    ("Computer Science", "Software engineering, algorithms, and systems."),
    ("Business", "Management, finance, and entrepreneurship."),
    ("Design", "UX/UI, visual, and product design."),
]

COURSES = [
    ("Python and Django", "PYDJ101", 6),
    ("Data Structures and Algorithms", "DSA201", 8),
    ("UX Fundamentals", "UX101", 4),
    ("Business Analytics", "BA201", 5),
    ("Cloud Fundamentals", "CLD101", 6),
]

FEEDBACK_COMMENTS = [
    "Consistently submits assignments on time and asks thoughtful questions.",
    "Strong grasp of the fundamentals; could push further on edge cases.",
    "Needs to participate more actively in group exercises.",
    "Excellent progress since the last review -- keep it up.",
    "Struggling with the pacing of the course; recommend a catch-up session.",
    "One of the strongest performers in the cohort this term.",
]

MARKS_REASONS = ["Midterm exam", "Resit exam", "Grading correction", "Final project", "Continuous assessment update"]


class Command(BaseCommand):
    help = (
        "Populate the database with realistic demo data for a release-ready demo: "
        "3 departments, 5 courses, 3 trainers, 1 administrator, 20+ students with "
        "marks history, feedback, and a handful of audit log events. Safe to run "
        "more than once -- uses get_or_create throughout."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--students", type=int, default=24,
            help="How many students to create (minimum 20 recommended). Default: 24.",
        )

    def handle(self, *args, **options):
        random.seed(42)  # deterministic output -- reruns produce the same demo data
        student_count = max(options["students"], 20)

        departments = self._create_departments()
        admin_user = self._create_admin()
        trainers = self._create_trainers()
        courses = self._create_courses(trainers)
        students = self._create_students(student_count, departments, courses)
        self._create_marks_history(students, trainers)
        self._create_feedback(students, courses, trainers)
        self._create_audit_events(admin_user, trainers, students)

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {len(departments)} departments, {len(courses)} courses, "
            f"{len(trainers)} trainers, {len(students)} students.\n"
            "Demo credentials (password for all: DemoPass123!):\n"
            "  admin_demo   - Administrator\n"
            "  trainer_demo, trainer_demo2, trainer_demo3 - Trainers (approved)\n"
            "  student_demo - Student (also see students named after real people below for browsing)\n"
        ))

    # -- departments -----------------------------------------------------
    def _create_departments(self):
        departments = []
        for name, description in DEPARTMENTS:
            dept, _ = Department.objects.get_or_create(name=name, defaults={"description": description})
            departments.append(dept)
        return departments

    # -- users -------------------------------------------------------------
    def _make_user(self, username, role, is_staff=False, is_approved=True):
        user, created = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@example.com", "is_staff": is_staff}
        )
        user.set_password("DemoPass123!")
        user.is_staff = is_staff
        user.save()
        user.profile.role = role
        user.profile.is_approved = is_approved
        user.profile.save()
        return user

    def _create_admin(self):
        return self._make_user("admin_demo", UserProfile.ROLE_ADMIN, is_staff=True)

    def _create_trainers(self):
        return [
            self._make_user("trainer_demo", UserProfile.ROLE_TRAINER),
            self._make_user("trainer_demo2", UserProfile.ROLE_TRAINER),
            self._make_user("trainer_demo3", UserProfile.ROLE_TRAINER),
        ]

    # -- courses -------------------------------------------------------------
    def _create_courses(self, trainers):
        courses = []
        for i, (name, code, weeks) in enumerate(COURSES):
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={"name": name, "duration_weeks": weeks, "trainer": trainers[i % len(trainers)]},
            )
            if course.trainer_id is None:
                course.trainer = trainers[i % len(trainers)]
                course.save()
            courses.append(course)
        return courses

    # -- students -------------------------------------------------------------
    def _create_students(self, count, departments, courses):
        students = []

        # A named, login-linked demo student first, so `student_demo` always works.
        demo_student_user = self._make_user("student_demo", UserProfile.ROLE_STUDENT)
        demo_student, _ = Student.objects.get_or_create(
            email="student_demo@example.com",
            defaults={
                "name": "Demo Student", "age": 22, "marks": Decimal("72.00"),
                "department": departments[0], "user": demo_student_user,
            },
        )
        demo_student.courses.add(courses[0])
        students.append(demo_student)

        used_names = {"Demo Student"}
        for i in range(count - 1):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            # keep names distinct enough for readable demo data, but don't loop forever
            attempt = 0
            while name in used_names and attempt < 5:
                last = random.choice(LAST_NAMES)
                name = f"{first} {last}"
                attempt += 1
            used_names.add(name)

            email = f"{first.lower()}.{last.lower()}{i}@example.com"
            marks = Decimal(random.randint(20, 100))
            department = random.choice(departments)
            is_active = random.random() > 0.15  # ~85% active
            age = random.randint(17, 45)
            # Always draw this, even if the student already exists, so the
            # random sequence stays identical across reruns (get_or_create
            # short-circuiting this draw on a rerun would desync every name/
            # email generated afterwards -- see the regression test for this).
            enrolled_courses = random.sample(courses, k=random.randint(1, 2))

            student, created = Student.objects.get_or_create(
                email=email,
                defaults={
                    "name": name, "age": age, "marks": marks,
                    "department": department, "is_active": is_active,
                },
            )
            if created:
                student.courses.add(*enrolled_courses)
            students.append(student)

        return students

    # -- marks history -------------------------------------------------------------
    def _create_marks_history(self, students, trainers):
        for student in students:
            for course in student.courses.all():
                if course.trainer_id is None:
                    continue
                if MarksHistory.objects.filter(student=student, course=course).exists():
                    continue
                old_marks = max(Decimal("0"), student.marks - Decimal(random.randint(5, 20)))
                MarksHistory.objects.create(
                    student=student, course=course, old_marks=old_marks, new_marks=student.marks,
                    updated_by=course.trainer, reason=random.choice(MARKS_REASONS),
                )

    # -- feedback -------------------------------------------------------------
    def _create_feedback(self, students, courses, trainers):
        for student in students:
            for course in student.courses.all():
                if course.trainer_id is None:
                    continue
                if Feedback.objects.filter(student=student, course=course).exists():
                    continue
                Feedback.objects.create(
                    student=student, course=course, trainer=course.trainer,
                    rating=random.randint(2, 5),
                    comment=random.choice(FEEDBACK_COMMENTS),
                    is_visible_to_student=random.random() > 0.2,  # ~80% published
                )

    # -- audit events -------------------------------------------------------------
    def _create_audit_events(self, admin_user, trainers, students):
        if AuditLog.objects.filter(description__startswith="[seed]").exists():
            return  # already seeded once; don't duplicate every rerun

        sample_students = random.sample(students, k=min(5, len(students)))
        for student in sample_students:
            log_action(
                admin_user, f"[seed] Reviewed student '{student.name}' during onboarding.",
                action_type=AuditLog.ACTION_UPDATE, object_repr=f"Student: {student.name}",
            )
        for trainer in trainers:
            log_action(
                admin_user, f"[seed] Approved trainer account '{trainer.username}'.",
                action_type=AuditLog.ACCOUNT_STATUS, object_repr=f"User: {trainer.username}",
            )
        # A couple of failed-login events, so the "users with 3+ failed logins"
        # report and the audit log filters have something to show.
        for _ in range(4):
            log_action(
                "unknown_attacker", "[seed] Failed login attempt #1 for 'unknown_attacker'.",
                action_type=AuditLog.ACTION_LOGIN_FAILED, object_repr="User: unknown_attacker",
            )
