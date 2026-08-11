from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from students.models import Course, Department, Student, UserProfile


class Command(BaseCommand):
    help = "Create one demo user per role (admin_demo / trainer_demo / student_demo, all password: DemoPass123!) plus a linked student record and course, for quickly trying out the role-based dashboards."

    def handle(self, *args, **options):
        password = "DemoPass123!"

        admin_user, _ = User.objects.get_or_create(
            username="admin_demo", defaults={"email": "admin_demo@example.com", "is_staff": True}
        )
        admin_user.set_password(password)
        admin_user.is_staff = True
        admin_user.save()
        admin_user.profile.role = UserProfile.ROLE_ADMIN
        admin_user.profile.save()

        trainer_user, _ = User.objects.get_or_create(
            username="trainer_demo", defaults={"email": "trainer_demo@example.com"}
        )
        trainer_user.set_password(password)
        trainer_user.save()
        trainer_user.profile.role = UserProfile.ROLE_TRAINER
        trainer_user.profile.save()

        student_user, _ = User.objects.get_or_create(
            username="student_demo", defaults={"email": "student_demo@example.com"}
        )
        student_user.set_password(password)
        student_user.save()
        student_user.profile.role = UserProfile.ROLE_STUDENT
        student_user.profile.save()

        department, _ = Department.objects.get_or_create(
            name="Computer Science", defaults={"description": "CS department"}
        )
        course, _ = Course.objects.get_or_create(
            code="PYDJ101",
            defaults={"name": "Python and Django", "duration_weeks": 6, "trainer": trainer_user},
        )
        if course.trainer_id is None:
            course.trainer = trainer_user
            course.save()

        student, _ = Student.objects.get_or_create(
            email="student_demo@example.com",
            defaults={
                "name": "Demo Student",
                "age": 21,
                "marks": 72,
                "department": department,
                "user": student_user,
            },
        )
        if student.user_id is None:
            student.user = student_user
            student.save()
        student.courses.add(course)

        self.stdout.write(self.style.SUCCESS(
            "Demo users created: admin_demo / trainer_demo / student_demo (password: DemoPass123!)"
        ))
