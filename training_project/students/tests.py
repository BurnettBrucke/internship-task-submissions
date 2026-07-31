from django.test import TestCase
from .models import StudentProfile,Student,Department,Course,AuditLog,UserProfile
from datetime import date
from datetime import timedelta
# Create your tests here.

class DepartmentModelTest(TestCase):

    def test_create_dept(self):
        department=Department.objects.create(
            name='cse',
            description='computer science and engineering'
        )

        self.assertEqual(department.name,'cse')
        self.assertEqual(
            department.description,"computer science and engineering"
        )

class StudentModelTest(TestCase):
    def test_create_std(self):
        department=Department.objects.create(
            name='it',
            description='infomation and technology'
        )


        student = Student.objects.create(
            name="rahul",
            email="rahul@gmail.com",
            marks=90,
            join_date=date.today(),
            department=department
            )
        self.assertEqual(student.name, "rahul")
        self.assertEqual(student.email, "rahul@gmail.com")
        self.assertEqual(student.marks, 90)
        self.assertEqual(student.join_date, date.today())
        self.assertEqual(student.department.name, "it")



class StudentProfileTest(TestCase):

    def test_profile_creation(self):

        department = Department.objects.create(
            name="IT",
            description="IT Department"
        )

        student = Student.objects.create(
            name="rahul",
            email="rahul@gmail.com",
            marks=80,
            join_date=date.today(),
            department=department
        )

        profile = StudentProfile.objects.create(
            student=student,
            phone="9876543210",
            address="Indore"
        )

        self.assertEqual(profile.student.name, "rahul")
        self.assertEqual(profile.phone, "9876543210")




class CourseModelTest(TestCase):

    def test_student_course(self):

        department = Department.objects.create(
            name="IT",
            description="IT"
        )

        student = Student.objects.create(
            name="rahul",
            email="rahul@gmail.com",
            marks=88,
            join_date=date.today(),
            department=department
        )

        course = Course.objects.create(
            course_name="Python",
            code="PY101",
            duration=timedelta(days=30)
        )

        student.course.add(course)

        self.assertEqual(student.course.count(), 1)