from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from students.models import (
    Department, Course, Student, StudentProfile, UserProfile,
    AuditLog, Feedback, MarksHistory
)
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds sample data for Departments, Courses, Users, Students, Feedback, Marks History, and Audit Logs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        Feedback.objects.all().delete()
        MarksHistory.objects.all().delete()
        AuditLog.objects.all().delete()
        StudentProfile.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()
        Department.objects.all().delete()
        
        # Keep non-demo superusers if any, or clear demo users
        User.objects.filter(username__in=[
            'admin', 'trainer1', 'trainer2', 'trainer3'
        ] + [f'student{i}' for i in range(1, 21)]).delete()

        self.stdout.write(self.style.SUCCESS("Existing data cleared."))

        # 1. Create Demo Users & Roles
        self.stdout.write("Creating demo user accounts...")
        
        # Admin User
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('Admin@123')
        admin_user.save()
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        self.stdout.write("  Created Admin: admin / Admin@123")

        # Trainer Users
        trainers = []
        trainer_data = [
            ("trainer1", "Dr. Alan Turing", "turing@example.com"),
            ("trainer2", "Prof. Grace Hopper", "hopper@example.com"),
            ("trainer3", "Dr. Margaret Hamilton", "hamilton@example.com"),
        ]
        for uname, name, email in trainer_data:
            t_user, _ = User.objects.get_or_create(
                username=uname,
                defaults={'email': email, 'first_name': name.split()[0], 'last_name': name.split()[-1], 'is_active': True}
            )
            t_user.set_password('Trainer@123')
            t_user.save()
            t_user.profile.role = 'trainer'
            t_user.profile.save()
            trainers.append(t_user)
            self.stdout.write(f"  Created Trainer: {uname} / Trainer@123 ({name})")

        # 2. Create 5 Departments
        self.stdout.write("Creating 5 departments...")
        depts_data = [
            {"name": "Computer Science", "description": "Study of software, algorithms, data structures, and computer architecture."},
            {"name": "Data Science & AI", "description": "Study of machine learning, statistical modeling, big data, and neural networks."},
            {"name": "Web Development", "description": "Study of modern web application technologies, frontend systems, and backend frameworks."},
            {"name": "Software QA & Testing", "description": "Study of software quality assurance, test automation, and validation protocols."},
            {"name": "DevOps & Cloud", "description": "Study of continuous integration, deployment infrastructure, containers, and cloud architecture."}
        ]
        departments = []
        for dept_info in depts_data:
            dept = Department.objects.create(**dept_info)
            departments.append(dept)
            self.stdout.write(f"  Created Department: {dept.name}")

        # 3. Create 5 Courses
        self.stdout.write("Creating 5 courses...")
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
            course = Course.objects.create(assigned_trainer=trainer_u, **c_info)
            courses.append(course)
            self.stdout.write(f"  Created Course: {course.course_name} ({course.code}) assigned to {trainer_u.username}")

        # 4. Create 20 Student Accounts and Profiles
        self.stdout.write("Creating 20 student accounts & records...")
        student_names = [
            "Rahul Sharma", "Priya Patel", "Amit Kumar", "Sneha Gupta", "Karan Verma",
            "Riya Singh", "Neha Joshi", "Rohit Mehta", "Ankit Das", "Pooja Reddy",
            "Vikas Malhotra", "Ananya Roy", "Siddharth Rao", "Divya Nair", "Aarav Kapoor",
            "Ishita Sen", "Kabir Bhatia", "Meera Saxena", "Tarun Choudhury", "Kavya Iyer"
        ]

        today = timezone.localdate()
        created_students = []

        for i, name in enumerate(student_names, start=1):
            username = f"student{i}"
            email = f"student{i}@example.com"
            
            # User account
            s_user, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': name.split()[0], 'last_name': name.split()[-1], 'is_active': True}
            )
            s_user.set_password('Student@123')
            s_user.save()
            s_user.profile.role = 'student'
            s_user.profile.save()

            # Student model record
            dept = random.choice(departments)
            marks = random.randint(35, 98)
            active_status = True if i % 6 != 0 else False
            joined_date = today - timedelta(days=random.randint(10, 150))
            
            student = Student.objects.create(
                user=s_user,
                name=name,
                email=email,
                age=random.randint(19, 26),
                course="Python Web Engineering",
                marks=marks,
                joined_date=joined_date,
                active_status=active_status,
                department=dept
            )
            
            # Enroll in 2-3 courses
            assigned_courses = random.sample(courses, k=random.randint(2, 3))
            student.courses.set(assigned_courses)
            
            # Create profile
            dob = date(1998 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28))
            StudentProfile.objects.create(
                student=student,
                phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                address=f"{random.randint(100, 999)} Tech Boulevard, Suite {random.randint(10, 99)}, Cityville",
                date_of_birth=dob
            )
            
            created_students.append(student)

        self.stdout.write(f"  Successfully created {len(created_students)} student records.")

        # 5. Create Feedback Records
        self.stdout.write("Creating feedback records...")
        feedback_comments = [
            "Demonstrates excellent problem-solving skills and code organization.",
            "Consistently completes assignments on time. Great team player.",
            "Shows steady improvement in algorithm design and debugging.",
            "Needs extra practice with asynchronous programming concepts.",
            "Outstanding active participation in interactive coding workshops!"
        ]

        feedback_count = 0
        for student in created_students:
            for course in student.courses.all():
                if course.assigned_trainer:
                    Feedback.objects.create(
                        student=student,
                        trainer=course.assigned_trainer,
                        course=course,
                        rating=random.randint(3, 5),
                        comments=random.choice(feedback_comments),
                        is_visible=True
                    )
                    feedback_count += 1

        self.stdout.write(f"  Created {feedback_count} feedback entries.")

        # 6. Create Marks History Records
        self.stdout.write("Creating marks history entries...")
        history_count = 0
        for student in created_students[:10]: # Create historical updates for first 10 students
            old_marks = max(0, student.marks - random.randint(5, 15))
            course = student.courses.first()
            updater = course.assigned_trainer if course and course.assigned_trainer else admin_user
            MarksHistory.objects.create(
                student=student,
                course=course,
                previous_marks=old_marks,
                new_marks=student.marks,
                updater=updater,
                reason="Mid-term assessment score update"
            )
            history_count += 1
            
        self.stdout.write(f"  Created {history_count} marks history entries.")

        # 7. Create Audit Logs
        self.stdout.write("Creating sample audit logs...")
        AuditLog.objects.create(
            user=admin_user,
            action='create',
            affected_object="System Data Seed",
            description="Admin executed sample data seeding command.",
            ip_address="127.0.0.1"
        )
        AuditLog.objects.create(
            user=trainers[0],
            action='login',
            description=f"Trainer {trainers[0].username} logged into portal.",
            ip_address="192.168.1.50"
        )
        AuditLog.objects.create(
            user=trainers[1],
            action='marks_update',
            affected_object=f"Student: {created_students[0].name}",
            description=f"Trainer {trainers[1].username} updated marks for {created_students[0].name}.",
            ip_address="192.168.1.51"
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded all sample data!"))
        self.stdout.write(self.style.SUCCESS("Demo Credentials:"))
        self.stdout.write("  Admin: admin / Admin@123")
        self.stdout.write("  Trainer: trainer1 / Trainer@123")
        self.stdout.write("  Student: student1 / Student@123")
