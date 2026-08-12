from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Department, Course, Student, UserProfile
from .forms import StudentForm, RegisterForm
from .models import Feedback, MarksHistory, AuditLog


class AuthenticationTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student1",
            password="Test@12345",
            email="student@test.com"
        )

        UserProfile.objects.create(
            user=self.user,
            role="student"
        )

    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        login = self.client.login(
            username="student1",
            password="Test@12345"
        )
        self.assertTrue(login)

    def test_logout(self):
        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302)

    def test_register_page(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_student_dashboard_requires_login(self):
        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(response.status_code, 302)



class FormTests(TestCase):

    def setUp(self):

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.course = Course.objects.create(
            course_name="Python",
            code="PY101",
            duration="3 Months"
        )

    def test_student_form_valid(self):

        form = StudentForm(data={
            "name": "Jaya",
            "email": "jaya@test.com",
            "age": 22,
            "course": "B.Tech",
            "marks": 90,
            "department": self.department.id,
            "active": True,
            "courses": [self.course.id],
        })

        self.assertTrue(form.is_valid())

    def test_student_form_invalid_marks(self):

        form = StudentForm(data={
            "name": "Jaya",
            "email": "jaya@test.com",
            "age": 22,
            "course": "B.Tech",
            "marks": 150,
            "department": self.department.id,
            "active": True,
            "courses": [self.course.id],
        })

        self.assertFalse(form.is_valid())

    def test_student_form_invalid_age(self):

        form = StudentForm(data={
            "name": "Jaya",
            "email": "jaya@test.com",
            "age": 10,
            "course": "B.Tech",
            "marks": 80,
            "department": self.department.id,
            "active": True,
            "courses": [self.course.id],
        })

        self.assertFalse(form.is_valid())

    def test_register_form_valid(self):

        form = RegisterForm(data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "Test@12345",
            "password2": "Test@12345",
        })

        self.assertTrue(form.is_valid())

    def test_register_duplicate_email(self):

        User.objects.create_user(
            username="abc",
            email="abc@test.com",
            password="Test@12345"
        )

        form = RegisterForm(data={
            "username": "xyz",
            "email": "abc@test.com",
            "password1": "Test@12345",
            "password2": "Test@12345",
        })

        self.assertFalse(form.is_valid())




class ModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="trainer",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.user,
            role="trainer"
        )

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.course = Course.objects.create(
            course_name="Python",
            code="PY101",
            duration="3 Months"
        )

        self.student = Student.objects.create(
            name="Jaya",
            email="jaya@test.com",
            age=22,
            course="B.Tech",
            marks=85,
            department=self.department
        )

        self.student.courses.add(self.course)

    def test_student_str(self):
        self.assertEqual(str(self.student), "Jaya")

    def test_department_str(self):
        self.assertEqual(str(self.department), "CSE")

    def test_course_str(self):
        self.assertEqual(str(self.course), "Python")

    def test_feedback_create(self):

        feedback = Feedback.objects.create(
            trainer=self.user,
            student=self.student,
            rating=5,
            comments="Excellent"
        )

        self.assertEqual(feedback.rating, 5)

    def test_marks_history_create(self):

        history = MarksHistory.objects.create(
            student=self.student,
            previous_marks=85,
            new_marks=95,
            updated_by=self.user,
            reason="Internal Test"
        )

        self.assertEqual(history.new_marks, 95)

class ExtraTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="Jaya",
            password="Jaya2003"
        )

        UserProfile.objects.create(
            user=self.user,
            role="admin"
        )

        self.department = Department.objects.create(
            name="IT",
            description="Information Technology"
        )

        self.course = Course.objects.create(
            course_name="Django",
            code="DJ101",
            duration="2 Months"
        )

        self.student = Student.objects.create(
            name="Divya",
            email="divya@test.com",
            age=21,
            course="B.Tech",
            marks=88,
            department=self.department
        )

        self.student.courses.add(self.course)

    def test_student_count(self):
        self.assertEqual(Student.objects.count(), 1)

    def test_department_count(self):
        self.assertEqual(Department.objects.count(), 1)

    def test_course_count(self):
        self.assertEqual(Course.objects.count(), 1)

    def test_userprofile_created(self):
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_student_active(self):
        self.assertTrue(self.student.active)

class ViewTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="admin_test",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.user,
            role="admin"
        )

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.student = Student.objects.create(
            name="Test Student",
            email="test@student.com",
            age=21,
            course="B.Tech",
            marks=80,
            department=self.department
        )

    def test_student_list_requires_login(self):

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_student_list_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_student_detail_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                args=[self.student.id]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_add_student_page_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("add_student")
        )

        self.assertEqual(response.status_code, 200)

    def test_edit_student_page_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "edit_student",
                args=[self.student.id]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_student_page_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "delete_student",
                args=[self.student.id]
            )
        )

        self.assertIn(response.status_code, [200, 302])

    def test_student_search(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {"search": "Test Student"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Student")


    def test_department_filter(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {"department": self.department.id}
        )

        self.assertEqual(response.status_code, 200)


    def test_active_filter(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {"active": "yes"}
        )

        self.assertEqual(response.status_code, 200)


    def test_result_filter(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {"result": "pass"}
        )

        self.assertEqual(response.status_code, 200)
