from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from student.models import (
    department,
    UserProfile,
    student,
    StudentProfile,
    Course,
    CourseMark,
    MarksHistory,
    Feedback,
    AuditLog,
)

class Command(BaseCommand):
    help = "Create demo data for the Student Training Portal"

    def handle(self, *args, **options):

        # -------------------------
        # Departments
        # -------------------------
        departments = [
            ("Computer Science", "Computer Science and Software Development"),
            ("Data Science", "Data Science and Artificial Intelligence"),
            ("Information Technology", "Information Technology and Systems"),
        ]

        department_objects = {}

        for name, description in departments:
            obj, created = department.objects.get_or_create(
                name=name,
                defaults={"description": description},
            )
            department_objects[name] = obj

        # -------------------------
        # Admin
        # -------------------------
        admin_user, created = User.objects.get_or_create(
            username="demo_admin",
            defaults={
                "email": "demo_admin@example.com",
                "first_name": "Demo",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            admin_user.set_password("DemoAdmin@123")
            admin_user.save()

        UserProfile.objects.update_or_create(
            user=admin_user,
            defaults={
                "role": "admin",
                "is_approved": True,
                "is_active": True,
            },
        )

        # -------------------------
        # Trainers
        # -------------------------
        trainer_data = [
            ("demo_trainer1", "trainer1@example.com", "Rahul", "Sharma"),
            ("demo_trainer2", "trainer2@example.com", "Priya", "Verma"),
            ("demo_trainer3", "trainer3@example.com", "Amit", "Patel"),
        ]

        trainer_users = []

        for username, email, first_name, last_name in trainer_data:
            trainer, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )

            if created:
                trainer.set_password("Trainer@123")
                trainer.save()

            UserProfile.objects.update_or_create(
                user=trainer,
                defaults={
                    "role": "trainer",
                    "is_approved": True,
                    "is_active": True,
                },
            )

            trainer_users.append(trainer)


                # -------------------------
        # Students
        # -------------------------
        student_names = [
            "Aarav Sharma",
            "Vivaan Verma",
            "Aditya Patel",
            "Arjun Singh",
            "Reyansh Gupta",
            "Ananya Sharma",
            "Diya Verma",
            "Aanya Patel",
            "Ishita Singh",
            "Kavya Gupta",
            "Rohan Sharma",
            "Karan Verma",
            "Rahul Patel",
            "Sneha Singh",
            "Neha Gupta",
            "Arnav Sharma",
            "Yash Verma",
            "Meera Patel",
            "Anika Singh",
            "Riya Gupta",
        ]

        student_objects = []

        for index, name in enumerate(student_names, start=1):

            email = f"student{index}@example.com"
            username = f"demo_student{index}"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": name.split()[0],
                    "last_name": name.split()[-1],
                },
            )

            if created:
                user.set_password("Student@123")
                user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": "student",
                    "is_approved": True,
                    "is_active": True,
                },
            )

            student_obj, created = student.objects.get_or_create(
                email=email,
                defaults={
                    "user": user,
                    "name": name,
                    "age": 20 + (index % 4),
                    "course": "Python & AI/ML",
                    "marks": 60 + (index % 31),
                    "department": department_objects[
                        list(department_objects.keys())[index % 3]
                    ],
                    "active": True,
                },
            )

            if not created and student_obj.user_id != user.id:
                student_obj.user = user
                student_obj.save(update_fields=["user"])

            StudentProfile.objects.get_or_create(
                students=student_obj,
                defaults={
                    "phone": f"90000000{index:02d}",
                    "address": f"Demo Address {index}, Indore",
                },
            )

            student_objects.append(student_obj)

        self.stdout.write(
            self.style.SUCCESS("20 demo students created successfully.")
        )



                # -------------------------
        # Courses
        # -------------------------
        course_data = [
            ("Python Programming", "PY101", 3),
            ("Machine Learning", "ML201", 4),
            ("Data Science", "DS301", 4),
            ("Django Web Development", "DJ401", 3),
            ("Artificial Intelligence", "AI501", 5),
        ]

        course_objects = []

        for index, (course_name, code, duration) in enumerate(
            course_data
        ):
            trainer = trainer_users[index % len(trainer_users)]

            course, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    "course_name": course_name,
                    "duration": duration,
                    "active_status": True,
                    "trainer": trainer,
                },
            )

            if not created:
                course.trainer = trainer
                course.active_status = True
                course.save(
                    update_fields=["trainer", "active_status"]
                )

            # Enroll all demo students
            course.students.set(student_objects)

            course_objects.append(course)

        self.stdout.write(
            self.style.SUCCESS(
                "5 demo courses created and students enrolled."
            )
        )


                # -------------------------
        # Course Marks
        # -------------------------
        for course_index, course in enumerate(course_objects):
            for student_index, student_obj in enumerate(student_objects):

                marks_value = 50 + (
                    (course_index * 7 + student_index * 3) % 51
                )

                course_mark, created = CourseMark.objects.get_or_create(
                    course=course,
                    student=student_obj,
                    defaults={
                        "marks": marks_value,
                        "updated_by": course.trainer,
                    },
                )

                if not created:
                    course_mark.marks = marks_value
                    course_mark.updated_by = course.trainer
                    course_mark.save(
                        update_fields=["marks", "updated_by", "updated_at"]
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo marks created successfully."
            )
        )

                # -------------------------
        # Marks History
        # -------------------------
        for course_mark in CourseMark.objects.filter(
            course__in=course_objects,
            student__in=student_objects,
        ):
            MarksHistory.objects.get_or_create(
                course_mark=course_mark,
                previous_marks=None,
                new_marks=course_mark.marks,
                defaults={
                    "updated_by": course_mark.updated_by,
                    "reason": "Initial demo marks",
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo marks history created successfully."
            )
        )


                # -------------------------
        # Feedback
        # -------------------------
        feedback_comments = [
            "Good progress and understanding of the concepts.",
            "Shows consistent improvement during the training.",
            "Completed the assigned tasks successfully.",
            "Needs a little more practice with advanced concepts.",
            "Very good participation and practical implementation.",
        ]

        for course_index, course in enumerate(course_objects):
            trainer = course.trainer

            for student_index, student_obj in enumerate(student_objects[:10]):

                rating = 3 + (
                    (course_index + student_index) % 3
                )

                Feedback.objects.get_or_create(
                    course=course,
                    student=student_obj,
                    trainer=trainer,
                    defaults={
                        "rating": rating,
                        "comment": feedback_comments[
                            student_index % len(feedback_comments)
                        ],
                        "is_visible": True,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo feedback created successfully."
            )
        )

                # -------------------------
        # Audit Logs
        # -------------------------
        audit_events = [
            ("CREATE", "Created demo department"),
            ("CREATE", "Created demo student"),
            ("CREATE", "Created demo course"),
            ("UPDATE", "Updated demo student marks"),
            ("UPDATE", "Updated demo feedback"),
            ("LOGIN", "Demo user logged in"),
            ("LOGOUT", "Demo user logged out"),
            ("FAILED", "Demo failed login attempt"),
        ]

        for index, (action_type, description) in enumerate(audit_events):
            AuditLog.objects.get_or_create(
                user=trainer_users[index % len(trainer_users)],
                action=f"Demo {action_type.lower()} action",
                action_type=action_type,
                description=description,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo audit events created successfully."
            )
        )

        
        
        self.stdout.write(
            self.style.SUCCESS("Departments and demo users created successfully.")
        )