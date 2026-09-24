from datetime import date, timedelta
from pathlib import Path
from random import randint
from shutil import copy2

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone

from students.models import (
    AuditLog,
    Course,
    Department,
    Enrollment,
    Feedback,
    MarkHistory,
    Student,
    StudentProfile,
    TrainerCourse,
    UserProfile,
)


"""
Demo Data
---------

Normal seed:

    python manage.py seed_demo_data

Reset ONLY demo data:

    python manage.py seed_demo_data --reset-demo --yes


IMPORTANT
---------

This command NEVER deletes all application data.

Only records explicitly identified as demo data can be removed.

Demo identifiers:

    demo_admin
    demo_trainer1
    demo_trainer2
    ...
    demo_student01
    demo_student02
    ...

Demo courses:

    DEMO-PY
    DEMO-DJ
    DEMO-SQL
    DEMO-DS
    DEMO-ML

Demo departments:

    Demo Computer Science
    Demo Information Technology
    Demo Data Science
    Demo Web Development
    Demo Software Engineering


Demo credentials:

Admin:

    admin.demo@example.com
    DemoAdmin123!

Trainer:

    trainer1.demo@example.com
    DemoTrainer123!

Student:

    student01.demo@example.com
    DemoStudent123!
"""


class Command(BaseCommand):

    help = "Create safe demo data for the Student Training Portal."

    # =========================================================
    # ARGUMENTS
    # =========================================================

    def add_arguments(self, parser):

        parser.add_argument(
            "--reset-demo",
            action="store_true",
            help=(
                "Delete and recreate ONLY demo data. "
                "Requires --yes."
            ),
        )

        parser.add_argument(
            "--yes",
            action="store_true",
            help=(
                "Confirm that ONLY demo data may be deleted "
                "during --reset-demo."
            ),
        )
        parser.add_argument(
    "--delete-demo",
    action="store_true",
    help="Delete ONLY demo data. Does not recreate it.",
)

    # =========================================================
    # MAIN
    # =========================================================

    def handle(self, *args, **options):
    
        reset_demo = options["reset_demo"]
        delete_demo = options["delete_demo"]
        confirmed = options["yes"]
    
        # -----------------------------------------------------
        # PREVENT CONFLICTING OPTIONS
        # -----------------------------------------------------
    
        if reset_demo and delete_demo:
            self.stdout.write(
                self.style.ERROR(
                    "Use either --reset-demo OR --delete-demo, not both."
                )
            )
            return
    
        # -----------------------------------------------------
        # DELETE ONLY DEMO DATA
        # -----------------------------------------------------
    
        if delete_demo:
        
            if not confirmed:
                self.stdout.write(
                    self.style.ERROR(
                        "Demo deletion was NOT performed."
                    )
                )
    
                self.stdout.write("")
    
                self.stdout.write(
                    self.style.WARNING(
                        "This will permanently delete ONLY demo data."
                    )
                )
    
                self.stdout.write("")
    
                self.stdout.write(
                    "If you really want to delete demo data, run:"
                )
    
                self.stdout.write("")
    
                self.stdout.write(
                    "python manage.py "
                    "seed_demo_data --delete-demo --yes"
                )
    
                return
    
            # Backup BEFORE deletion
            self.create_database_backup()
    
            # Delete demo data
            self.clear_demo_data()
    
            self.stdout.write("")
    
            self.stdout.write(
                self.style.SUCCESS(
                    "Demo data deleted successfully."
                )
            )
    
            self.stdout.write(
                "No new demo data was created."
            )
    
            return
    
        # -----------------------------------------------------
        # RESET DEMO DATA
        # -----------------------------------------------------
    
        if reset_demo:
        
            if not confirmed:
                self.stdout.write(
                    self.style.ERROR(
                        "Demo reset was NOT performed."
                    )
                )
    
                self.stdout.write("")
    
                self.stdout.write(
                    "To confirm, run:"
                )
    
                self.stdout.write(
                    "python manage.py "
                    "seed_demo_data --reset-demo --yes"
                )
    
                return
    
            # Backup BEFORE deletion
            self.create_database_backup()
    
            # Delete old demo data
            self.clear_demo_data()
    
        # -----------------------------------------------------
        # NORMAL SEEDING
        # -----------------------------------------------------
    
        self.stdout.write("")
        self.stdout.write("Creating demo data...")
        self.stdout.write("")
    
        departments = self.create_departments()
    
        courses = self.create_courses()
    
        admin = self.create_admin()
    
        trainers = self.create_trainers()
    
        students = self.create_students(
            departments
        )
    
        self.assign_trainers(
            trainers,
            courses,
        )
    
        enrollments = self.create_enrollments(
            students,
            courses,
        )
    
        self.create_mark_history(
            enrollments,
            trainers,
        )
    
        self.create_feedback(
            students,
            courses,
            trainers,
        )
    
        self.create_audit_logs(
            admin,
            trainers,
            students,
            courses,
            enrollments,
        )
    
        # -----------------------------------------------------
        # SUCCESS
        # -----------------------------------------------------
    
        self.stdout.write("")
    
        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created successfully."
            )
        )
        self.stdout.write("")

        self.stdout.write(
            "Demo credentials:"
        )

        self.stdout.write(
            "  Admin   : "
            "admin.demo@example.com / DemoAdmin123!"
        )

        self.stdout.write(
            "  Trainer : "
            "trainer1.demo@example.com / DemoTrainer123!"
        )

        self.stdout.write(
            "  Student : "
            "student01.demo@example.com / DemoStudent123!"
        )

        self.stdout.write("")

        self.stdout.write(
            "Database totals:"
        )

        self.stdout.write(
            f"  Departments : {Department.objects.count()}"
        )

        self.stdout.write(
            f"  Courses     : {Course.objects.count()}"
        )

        trainer_count = UserProfile.objects.filter(
            role=UserProfile.Role.TRAINER
        ).count()

        self.stdout.write(
            f"  Trainers    : {trainer_count}"
        )

        self.stdout.write(
            f"  Students    : {Student.objects.count()}"
        )

        self.stdout.write(
            f"  Enrollments : {Enrollment.objects.count()}"
        )

        self.stdout.write(
            f"  Feedback    : {Feedback.objects.count()}"
        )

        self.stdout.write(
            f"  Audit logs  : {AuditLog.objects.count()}"
        )

    # =========================================================
    # DATABASE BACKUP
    # =========================================================

    def create_database_backup(self):

        db_name = connection.settings_dict["NAME"]

        if not db_name:
            raise RuntimeError(
                "Database path could not be determined."
            )

        db_path = Path(db_name)

        if not db_path.exists():

            raise RuntimeError(
                f"Database file does not exist:\n{db_path}"
            )

        timestamp = timezone.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_path = db_path.with_name(
            f"{db_path.stem}"
            f"_before_demo_reset_"
            f"{timestamp}"
            f"{db_path.suffix}"
        )

        copy2(
            db_path,
            backup_path,
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Database backup created:"
            )
        )

        self.stdout.write(
            f"  {backup_path}"
        )

        self.stdout.write("")

    # =========================================================
    # CLEAR ONLY DEMO DATA
    # =========================================================

    @transaction.atomic
    def clear_demo_data(self):

        self.stdout.write("")

        self.stdout.write(
            self.style.WARNING(
                "Removing ONLY demo data..."
            )
        )

        # =====================================================
        # IDENTIFY DEMO USERS
        # =====================================================

        demo_users = User.objects.filter(
            username__startswith="demo_"
        )

        demo_trainers = demo_users.filter(
            profile__role=UserProfile.Role.TRAINER
        )

        demo_students = Student.objects.filter(
            user__in=demo_users
        )

        # =====================================================
        # IDENTIFY DEMO COURSES
        # =====================================================

        demo_courses = Course.objects.filter(
            code__startswith="DEMO-"
        )

        # =====================================================
        # IDENTIFY DEMO DEPARTMENTS
        # =====================================================

        demo_departments = Department.objects.filter(
            name__startswith="Demo "
        )

        # =====================================================
        # STORE IDS BEFORE DELETE
        # =====================================================

        demo_student_ids = list(
            demo_students.values_list(
                "id",
                flat=True,
            )
        )

        demo_course_ids = list(
            demo_courses.values_list(
                "id",
                flat=True,
            )
        )

        demo_enrollment_ids = list(
            Enrollment.objects.filter(
                student__in=demo_students
            ).values_list(
                "id",
                flat=True,
            )
        )

        # =====================================================
        # CONTENT TYPES
        # =====================================================

        student_content_type = (
            ContentType.objects.get_for_model(
                Student
            )
        )

        course_content_type = (
            ContentType.objects.get_for_model(
                Course
            )
        )

        enrollment_content_type = (
            ContentType.objects.get_for_model(
                Enrollment
            )
        )

        # =====================================================
        # AUDIT LOGS
        # =====================================================

        AuditLog.objects.filter(
            user__in=demo_users
        ).delete()

        AuditLog.objects.filter(
            content_type=student_content_type,
            object_id__in=demo_student_ids,
        ).delete()

        AuditLog.objects.filter(
            content_type=course_content_type,
            object_id__in=demo_course_ids,
        ).delete()

        AuditLog.objects.filter(
            content_type=enrollment_content_type,
            object_id__in=demo_enrollment_ids,
        ).delete()

        # =====================================================
        # MARK HISTORY
        # =====================================================

        MarkHistory.objects.filter(
            enrollment__student__in=demo_students
        ).delete()

        MarkHistory.objects.filter(
            enrollment__course__in=demo_courses
        ).delete()

        # =====================================================
        # FEEDBACK
        # =====================================================

        Feedback.objects.filter(
            student__in=demo_students
        ).delete()

        Feedback.objects.filter(
            trainer__in=demo_trainers
        ).delete()

        Feedback.objects.filter(
            course__in=demo_courses
        ).delete()

        # =====================================================
        # ENROLLMENTS
        # =====================================================

        Enrollment.objects.filter(
            student__in=demo_students
        ).delete()

        Enrollment.objects.filter(
            course__in=demo_courses
        ).delete()

        # =====================================================
        # TRAINER COURSE ASSIGNMENTS
        # =====================================================

        TrainerCourse.objects.filter(
            trainer__in=demo_trainers
        ).delete()

        TrainerCourse.objects.filter(
            course__in=demo_courses
        ).delete()

        # =====================================================
        # STUDENT PROFILES
        # =====================================================

        StudentProfile.objects.filter(
            student__in=demo_students
        ).delete()

        # =====================================================
        # STUDENTS
        # =====================================================

        demo_students.delete()

        # =====================================================
        # USER PROFILES
        # =====================================================

        UserProfile.objects.filter(
            user__in=demo_users
        ).delete()

        # =====================================================
        # USERS
        # =====================================================

        demo_users.delete()

        # =====================================================
        # COURSES
        # =====================================================

        demo_courses.delete()

        # =====================================================
        # DEPARTMENTS
        # =====================================================

        demo_departments.delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Only demo data was removed successfully."
            )
        )

    # =========================================================
    # DEPARTMENTS
    # =========================================================

    def create_departments(self):

        department_data = [
            (
                "Demo Computer Science",
                "Computer science and software development training.",
            ),
            (
                "Demo Information Technology",
                "Information technology and database training.",
            ),
            (
                "Demo Data Science",
                "Data analysis, machine learning and statistics.",
            ),
            (
                "Demo Web Development",
                "Frontend and backend web development training.",
            ),
            (
                "Demo Software Engineering",
                "Software engineering and application development.",
            ),
        ]

        departments = []

        for name, description in department_data:

            department, _ = (
                Department.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": description,
                    },
                )
            )

            departments.append(
                department
            )

        return departments

    # =========================================================
    # COURSES
    # =========================================================

    def create_courses(self):

        course_data = [
            (
                "Python Programming",
                "DEMO-PY",
                "3 Months",
                90,
            ),
            (
                "Django Web Development",
                "DEMO-DJ",
                "3 Months",
                90,
            ),
            (
                "SQL & Database Management",
                "DEMO-SQL",
                "2 Months",
                60,
            ),
            (
                "Data Science",
                "DEMO-DS",
                "4 Months",
                120,
            ),
            (
                "Machine Learning",
                "DEMO-ML",
                "4 Months",
                120,
            ),
        ]

        courses = []

        for (
            name,
            code,
            duration,
            duration_days,
        ) in course_data:

            course, _ = (
                Course.objects.get_or_create(
                    code=code,
                    defaults={
                        "course_name": name,
                        "duration": duration,
                        "duration_days": duration_days,
                        "active_status": True,
                    },
                )
            )

            courses.append(course)

        return courses

    # =========================================================
    # ADMIN
    # =========================================================

    def create_admin(self):

        user, _ = User.objects.get_or_create(
            username="demo_admin",
            defaults={
                "email": "admin.demo@example.com",
                "first_name": "Demo",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.email = "admin.demo@example.com"
        user.first_name = "Demo"
        user.last_name = "Administrator"
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.set_password(
            "DemoAdmin123!"
        )

        user.save()

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "role": UserProfile.Role.ADMIN,
                "status": UserProfile.Status.APPROVED,
                "failed_login_attempts": 0,
                "login_blocked": False,
                "login_blocked_at": None,
            },
        )

        return user

    # =========================================================
    # TRAINERS
    # =========================================================

    def create_trainers(self):

        trainers = []

        trainer_names = [
            ("Amit", "Sharma"),
            ("Priya", "Verma"),
            ("Rahul", "Patel"),
            ("Neha", "Joshi"),
            ("Arjun", "Mehta"),
        ]

        for index, (
            first_name,
            last_name,
        ) in enumerate(
            trainer_names,
            start=1,
        ):

            username = (
                f"demo_trainer{index}"
            )

            email = (
                f"trainer{index}.demo@example.com"
            )

            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                },
            )

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True

            user.set_password(
                "DemoTrainer123!"
            )

            user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": UserProfile.Role.TRAINER,
                    "status": UserProfile.Status.APPROVED,
                    "failed_login_attempts": 0,
                    "login_blocked": False,
                    "login_blocked_at": None,
                },
            )

            trainers.append(user)

        return trainers

    # =========================================================
    # STUDENTS
    # =========================================================

    def create_students(self, departments):

        students = []

        student_names = [
            ("Aarav", "Sharma"),
            ("Vivaan", "Verma"),
            ("Aditya", "Patel"),
            ("Arjun", "Joshi"),
            ("Reyansh", "Mehta"),
            ("Krishna", "Shah"),
            ("Ishaan", "Gupta"),
            ("Kabir", "Malhotra"),
            ("Rohan", "Singh"),
            ("Yash", "Jain"),
            ("Ananya", "Sharma"),
            ("Diya", "Verma"),
            ("Aadhya", "Patel"),
            ("Myra", "Joshi"),
            ("Sara", "Mehta"),
            ("Ira", "Shah"),
            ("Avni", "Gupta"),
            ("Kiara", "Malhotra"),
            ("Anika", "Singh"),
            ("Riya", "Jain"),
        ]

        for index, (
            first_name,
            last_name,
        ) in enumerate(
            student_names,
            start=1,
        ):

            username = (
                f"demo_student{index:02d}"
            )

            email = (
                f"student{index:02d}.demo@example.com"
            )

            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                },
            )

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True

            user.set_password(
                "DemoStudent123!"
            )

            user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": UserProfile.Role.STUDENT,
                    "status": UserProfile.Status.APPROVED,
                    "failed_login_attempts": 0,
                    "login_blocked": False,
                    "login_blocked_at": None,
                },
            )

            student, _ = (
                Student.objects.update_or_create(
                    user=user,
                    defaults={
                        "email": email,
                        "name": (
                            f"{first_name} "
                            f"{last_name}"
                        ),
                        "age": randint(18, 25),
                        "active": index != 20,
                        "department": departments[
                            (index - 1)
                            % len(departments)
                        ],
                    },
                )
            )

            StudentProfile.objects.update_or_create(
                student=student,
                defaults={
                    "phone": (
                        f"98"
                        f"{randint(10000000, 99999999)}"
                    ),
                    "address": (
                        f"{index} Demo Street, "
                        "Indore, Madhya Pradesh"
                    ),
                    "date_of_birth": date(
                        randint(2000, 2007),
                        randint(1, 12),
                        randint(1, 28),
                    ),
                },
            )

            students.append(student)

        return students

    # =========================================================
    # TRAINER ASSIGNMENTS
    # =========================================================

    def assign_trainers(
        self,
        trainers,
        courses,
    ):

        for index, course in enumerate(
            courses
        ):

            trainer = trainers[
                index % len(trainers)
            ]

            TrainerCourse.objects.get_or_create(
                trainer=trainer,
                course=course,
            )

    # =========================================================
    # ENROLLMENTS + MARKS
    # =========================================================

    def create_enrollments(
        self,
        students,
        courses,
    ):

        enrollments = []

        for index, student in enumerate(
            students
        ):

            number_of_courses = (
                1 + (index % 3)
            )

            selected_courses = [
                courses[
                    (index + offset)
                    % len(courses)
                ]
                for offset in range(
                    number_of_courses
                )
            ]

            for offset, course in enumerate(
                selected_courses
            ):

                enrollment, _ = (
                    Enrollment.objects.get_or_create(
                        student=student,
                        course=course,
                        defaults={
                            "enrolled_at": (
                                timezone.localdate()
                                - timedelta(
                                    days=(
                                        15
                                        + index * 2
                                    )
                                )
                            ),
                            "marks": (
                                45
                                + (
                                    (
                                        index * 7
                                        + offset * 11
                                    )
                                    % 51
                                )
                            ),
                        },
                    )
                )

                if enrollment.marks is None:

                    enrollment.marks = (
                        45
                        + (
                            (
                                index * 7
                                + offset * 11
                            )
                            % 51
                        )
                    )

                    enrollment.save(
                        update_fields=[
                            "marks"
                        ]
                    )

                enrollments.append(
                    enrollment
                )

        return enrollments

    # =========================================================
    # MARK HISTORY
    # =========================================================

    def create_mark_history(
        self,
        enrollments,
        trainers,
    ):

        for index, enrollment in enumerate(
            enrollments
        ):

            current_marks = enrollment.marks

            if current_marks is None:
                continue

            previous_marks = max(
                current_marks - 5,
                0,
            )

            updated_by = trainers[
                index % len(trainers)
            ]

            MarkHistory.objects.get_or_create(
                enrollment=enrollment,
                previous_marks=previous_marks,
                new_marks=current_marks,
                defaults={
                    "updated_by": updated_by,
                    "reason": (
                        "Demo initial marks update."
                    ),
                },
            )

    # =========================================================
    # FEEDBACK
    # =========================================================

    def create_feedback(
        self,
        students,
        courses,
        trainers,
    ):

        feedback_comments = [
            "Good progress and consistent participation.",
            "Strong understanding of the course concepts.",
            "Needs more practice with practical exercises.",
            "Very active during training sessions.",
            "Good improvement throughout the course.",
        ]

        for index, student in enumerate(
            students
        ):

            enrollment = (
                Enrollment.objects.filter(
                    student=student
                )
                .select_related("course")
                .first()
            )

            if not enrollment:
                continue

            trainer_assignment = (
                TrainerCourse.objects.filter(
                    course=enrollment.course
                )
                .select_related("trainer")
                .first()
            )

            trainer = (
                trainer_assignment.trainer
                if trainer_assignment
                else trainers[
                    index % len(trainers)
                ]
            )

            Feedback.objects.get_or_create(
                student=student,
                trainer=trainer,
                course=enrollment.course,
                defaults={
                    "rating": (
                        3 + (index % 3)
                    ),
                    "comment": (
                        feedback_comments[
                            index
                            % len(feedback_comments)
                        ]
                    ),
                    "visible": True,
                },
            )

    # =========================================================
    # AUDIT LOGS
    # =========================================================

    def create_audit_logs(
        self,
        admin,
        trainers,
        students,
        courses,
        enrollments,
    ):

        student = students[0]

        course = courses[0]

        enrollment = enrollments[0]

        student_ct = (
            ContentType.objects.get_for_model(
                Student
            )
        )

        course_ct = (
            ContentType.objects.get_for_model(
                Course
            )
        )

        enrollment_ct = (
            ContentType.objects.get_for_model(
                Enrollment
            )
        )

        audit_data = [
            {
                "user": admin,
                "action": AuditLog.Action.LOGIN,
                "description": (
                    "Demo administrator logged in."
                ),
                "content_type": None,
                "object_id": None,
            },
            {
                "user": admin,
                "action": AuditLog.Action.CREATE,
                "description": (
                    "Demo student account created."
                ),
                "content_type": student_ct,
                "object_id": student.id,
            },
            {
                "user": admin,
                "action": AuditLog.Action.UPDATE,
                "description": (
                    "Demo student profile updated."
                ),
                "content_type": student_ct,
                "object_id": student.id,
            },
            {
                "user": trainers[0],
                "action": AuditLog.Action.MARKS_UPDATE,
                "description": (
                    "Demo student marks updated."
                ),
                "content_type": enrollment_ct,
                "object_id": enrollment.id,
            },
            {
                "user": trainers[0],
                "action": AuditLog.Action.FEEDBACK_CREATE,
                "description": (
                    "Demo feedback created."
                ),
                "content_type": course_ct,
                "object_id": course.id,
            },
            {
                "user": admin,
                "action": (
                    AuditLog.Action.ACCOUNT_STATUS_CHANGE
                ),
                "description": (
                    "Demo student account status changed."
                ),
                "content_type": student_ct,
                "object_id": student.id,
            },
            {
                "user": admin,
                "action": AuditLog.Action.LOGOUT,
                "description": (
                    "Demo administrator logged out."
                ),
                "content_type": None,
                "object_id": None,
            },
        ]

        for item in audit_data:

            AuditLog.objects.get_or_create(
                user=item["user"],
                action=item["action"],
                description=item["description"],
                content_type=item["content_type"],
                object_id=item["object_id"],
                defaults={
                    "ip_address": "127.0.0.1",
                },
            )