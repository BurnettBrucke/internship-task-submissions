from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from students.models import (
    Department, Course, Student, StudentProfile, UserProfile,
    AuditLog, Feedback, MarksHistory, Enrollment
)
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Idempotent demo seed data command creating departments, courses, users, enrollments, marks, feedback, and audit logs without deleting existing records.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting idempotent demo data seeding..."))

        # 1. Create Demo Users & Roles
        self.stdout.write("Ensuring demo user accounts exist...")
        
        # Admin User
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('AdminPass123!')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        self.stdout.write("  Admin: admin / AdminPass123!")

        # Trainer Users
        trainers = []
        trainer_data = [
            ("trainer1", "Alan Turing", "turing@example.com"),
            ("trainer2", "Grace Hopper", "hopper@example.com"),
            ("trainer3", "Margaret Hamilton", "hamilton@example.com"),
        ]
        for uname, name, email in trainer_data:
            first_name, last_name = name.split()[0], name.split()[-1]
            t_user, _ = User.objects.get_or_create(
                username=uname,
                defaults={'email': email, 'first_name': first_name, 'last_name': last_name, 'is_active': True}
            )
            t_user.set_password('TrainerPass123!')
            t_user.is_active = True
            t_user.save()
            t_user.profile.role = 'trainer'
            t_user.profile.save()
            trainers.append(t_user)
            self.stdout.write(f"  Trainer: {uname} / TrainerPass123! ({name})")

        # 2. Create 5 Departments
        self.stdout.write("Ensuring 5 departments exist...")
        depts_data = [
            {"name": "Computer Science", "description": "Study of software, algorithms, data structures, and computer architecture."},
            {"name": "Data Science & AI", "description": "Study of machine learning, statistical modeling, big data, and neural networks."},
            {"name": "Web Development", "description": "Study of modern web application technologies, frontend systems, and backend frameworks."},
            {"name": "Software QA & Testing", "description": "Study of software quality assurance, test automation, and validation protocols."},
            {"name": "DevOps & Cloud", "description": "Study of continuous integration, deployment infrastructure, containers, and cloud architecture."}
        ]
        departments = []
        for dept_info in depts_data:
            dept, _ = Department.objects.get_or_create(
                name=dept_info["name"],
                defaults={"description": dept_info["description"]}
            )
            departments.append(dept)

        # 3. Create 5 Courses
        self.stdout.write("Ensuring 5 courses exist...")
        courses_data = [
            {"course_name": "Full-Stack Web Development", "code": "CS101", "duration": 12, "active_status": True, "trainer": trainers[0]},
            {"course_name": "Applied Data Science & ML", "code": "DS201", "duration": 16, "active_status": True, "trainer": trainers[1]},
            {"course_name": "Automated Software Testing", "code": "QA301", "duration": 10, "active_status": True, "trainer": trainers[2]},
            {"course_name": "Cloud Infrastructure & DevOps", "code": "DO401", "duration": 14, "active_status": True, "trainer": trainers[0]},
            {"course_name": "Advanced Python Systems", "code": "PY501", "duration": 8, "active_status": True, "trainer": trainers[1]}
        ]
        courses = []
        for c_info in courses_data:
            trainer_u = c_info.pop("trainer")
            course, _ = Course.objects.get_or_create(
                code=c_info["code"],
                defaults={
                    "course_name": c_info["course_name"],
                    "duration": c_info["duration"],
                    "active_status": c_info["active_status"],
                    "assigned_trainer": trainer_u,
                }
            )
            if course.assigned_trainer != trainer_u:
                course.assigned_trainer = trainer_u
                course.save()
            courses.append(course)

        # 4. Create 20 Student Accounts, Profiles, and Enrollments
        self.stdout.write("Ensuring 20 student accounts, profiles, and enrollments exist...")
        student_names = [
            "Rahul Sharma", "Priya Patel", "Amit Kumar", "Sneha Gupta", "Karan Verma",
            "Riya Singh", "Neha Joshi", "Rohit Mehta", "Ankit Das", "Pooja Reddy",
            "Vikas Malhotra", "Ananya Roy", "Siddharth Rao", "Divya Nair", "Aarav Kapoor",
            "Ishita Sen", "Kabir Bhatia", "Meera Saxena", "Tarun Choudhury", "Kavya Iyer"
        ]

        base_date = date(2025, 1, 15)
        created_students = []

        for i, name in enumerate(student_names, start=1):
            username = f"student{i}"
            email = f"student{i}@example.com"
            
            s_user, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': name.split()[0], 'last_name': name.split()[-1], 'is_active': True}
            )
            s_user.set_password('StudentPass123!')
            s_user.is_active = True
            s_user.save()
            s_user.profile.role = 'student'
            s_user.profile.save()

            dept = departments[(i - 1) % len(departments)]
            active_status = True if i % 7 != 0 else False
            joined_date = base_date + timedelta(days=i * 5)
            age = 19 + (i % 8)
            
            student, _ = Student.objects.get_or_create(
                user=s_user,
                defaults={
                    "name": name,
                    "email": email,
                    "age": age,
                    "joined_date": joined_date,
                    "active_status": active_status,
                    "department": dept
                }
            )

            # Ensure profile exists
            dob = date(2000, 1 + (i % 12), 1 + (i % 28))
            StudentProfile.objects.get_or_create(
                student=student,
                defaults={
                    "phone": f"+1-555-01{i:02d}",
                    "address": f"{100 + i} Innovation Way, Tech City",
                    "date_of_birth": dob
                }
            )
            
            # Enroll in 2 courses deterministically
            c1 = courses[(i - 1) % len(courses)]
            c2 = courses[i % len(courses)]
            mark1 = 60 + (i * 2) % 39
            mark2 = 55 + (i * 3) % 43
            
            e1, _ = Enrollment.objects.get_or_create(
                student=student,
                course=c1,
                defaults={"current_mark": mark1, "status": "active"}
            )
            e2, _ = Enrollment.objects.get_or_create(
                student=student,
                course=c2,
                defaults={"current_mark": mark2, "status": "active"}
            )
            
            created_students.append(student)

        self.stdout.write(f"  Successfully processed {len(created_students)} student records.")

        # 5. Create Feedback Records
        self.stdout.write("Ensuring feedback records exist...")
        feedback_comments = [
            "Demonstrates excellent problem-solving skills and code organization.",
            "Consistently completes assignments on time. Great team player.",
            "Shows steady improvement in algorithm design and debugging.",
            "Needs extra practice with asynchronous programming concepts.",
            "Outstanding active participation in interactive coding workshops!"
        ]

        feedback_count = 0
        for idx, student in enumerate(created_students[:10]):
            for enrollment in student.enrollments.all():
                if enrollment.course.assigned_trainer:
                    comment = feedback_comments[(idx + enrollment.id) % len(feedback_comments)]
                    rating = 3 + (idx % 3)
                    fb, created = Feedback.objects.get_or_create(
                        enrollment=enrollment,
                        student=student,
                        trainer=enrollment.course.assigned_trainer,
                        course=enrollment.course,
                        defaults={
                            "rating": rating,
                            "comments": comment,
                            "is_visible": True
                        }
                    )
                    if created:
                        feedback_count += 1

        self.stdout.write(f"  Processed feedback entries ({feedback_count} new).")

        # 6. Create Marks History Records
        self.stdout.write("Ensuring marks history entries exist...")
        history_count = 0
        for idx, student in enumerate(created_students[:5]):
            enrollment = student.enrollments.first()
            if enrollment:
                prev = max(0, enrollment.current_mark - 10)
                mh, created = MarksHistory.objects.get_or_create(
                    enrollment=enrollment,
                    student=student,
                    course=enrollment.course,
                    previous_marks=prev,
                    new_marks=enrollment.current_mark,
                    defaults={
                        "updater": enrollment.course.assigned_trainer or admin_user,
                        "reason": "Initial assessment adjustment"
                    }
                )
                if created:
                    history_count += 1
            
        self.stdout.write(f"  Processed marks history entries ({history_count} new).")

        # 7. Create Audit Logs
        self.stdout.write("Ensuring seed audit logs exist...")
        AuditLog.objects.get_or_create(
            user=admin_user,
            action='create',
            affected_object="System Data Seed",
            defaults={
                "description": "Admin executed safe demo data seeding command.",
                "ip_address": "127.0.0.1"
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully completed safe demo data seeding!"))
        self.stdout.write(self.style.SUCCESS("Non-Production Demo Credentials:"))
        self.stdout.write("  Admin: admin / AdminPass123!")
        self.stdout.write("  Trainer: trainer1 / TrainerPass123!")
        self.stdout.write("  Student: student1 / StudentPass123!")
