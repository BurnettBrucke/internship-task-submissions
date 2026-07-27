from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import StudentForm
from .models import Course, Department, Student, StudentProfile


class BaseAuthenticatedTestCase(TestCase):
    """Shared setup: a logged-in staff user plus some reference data."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='TesterPass123', is_staff=True
        )
        self.client.login(username='tester', password='TesterPass123')

        self.department = Department.objects.create(
            name="Computer Science", description="CS department"
        )
        self.course = Course.objects.create(
            name="Python and Django", code="PYDJ101", duration_weeks=6
        )
        self.student = Student.objects.create(
            name="Asha Verma",
            email="asha@example.com",
            age=21,
            marks=75,
            department=self.department,
        )
        self.student.courses.add(self.course)


# ---------------------------------------------------------------------------
# Task 1 - CRUD
# ---------------------------------------------------------------------------

class StudentListViewTests(BaseAuthenticatedTestCase):
    """1. Student list page loads successfully."""

    def test_list_page_loads(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertContains(response, "Asha Verma")

    def test_empty_state_message(self):
        Student.objects.all().delete()
        response = self.client.get(reverse('student_list'))
        self.assertContains(response, "No students found.")


class StudentDetailViewTests(BaseAuthenticatedTestCase):
    """2. Student detail page loads successfully."""

    def test_detail_page_loads(self):
        response = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertContains(response, "Asha Verma")
        self.assertContains(response, "Computer Science")

    def test_detail_404_for_missing_student(self):
        response = self.client.get(reverse('student_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class StudentCreateViewTests(BaseAuthenticatedTestCase):
    """3. Valid student creation. / 4. Invalid student form submission."""

    def test_valid_student_creation(self):
        data = {
            "name": "New Student",
            "email": "new.student@example.com",
            "age": 22,
            "marks": 65,
            "department": self.department.id,
            "courses": [self.course.id],
            "is_active": "on",
        }
        response = self.client.post(reverse('add_student'), data=data)
        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(Student.objects.filter(email="new.student@example.com").exists())

    def test_invalid_student_form_submission(self):
        data = {
            "name": "",
            "email": "not-an-email",
            "age": 5,
            "marks": 200,
        }
        response = self.client.post(reverse('add_student'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Student.objects.filter(email="not-an-email").exists())
        self.assertFormError(response.context['form'], 'name', 'This field is required.')

    def test_marks_boundary_values(self):
        for marks in [0, 40, 100]:
            form = StudentForm(data={
                "name": f"Boundary {marks}",
                "email": f"boundary{marks}@example.com",
                "age": 20,
                "marks": marks,
            })
            self.assertTrue(form.is_valid(), form.errors)


class StudentUpdateViewTests(BaseAuthenticatedTestCase):
    """5. Student update."""

    def test_student_update(self):
        data = {
            "name": "Asha Verma Updated",
            "email": self.student.email,
            "age": 22,
            "marks": 80,
            "department": self.department.id,
            "courses": [self.course.id],
            "is_active": "on",
        }
        response = self.client.post(reverse('edit_student', args=[self.student.pk]), data=data)
        self.assertRedirects(response, reverse('student_detail', args=[self.student.pk]))
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Asha Verma Updated")
        self.assertEqual(self.student.marks, 80)


class StudentDeleteViewTests(BaseAuthenticatedTestCase):
    """6. Student deletion."""

    def test_confirmation_page_shown_on_get(self):
        response = self.client.get(reverse('delete_student', args=[self.student.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_confirm_delete.html')
        self.assertContains(response, "Are you sure")

    def test_staff_user_can_delete(self):
        response = self.client.post(reverse('delete_student', args=[self.student.pk]))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_non_staff_user_cannot_delete(self):
        User.objects.create_user(username='regular', password='RegularPass123', is_staff=False)
        self.client.logout()
        self.client.login(username='regular', password='RegularPass123')
        response = self.client.post(reverse('delete_student', args=[self.student.pk]))
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())


# ---------------------------------------------------------------------------
# Task 4 - Authentication
# ---------------------------------------------------------------------------

class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='authuser', password='AuthPass123')

    def test_login_page_loads(self):
        """7. Login page."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_successful_login(self):
        """8. Successful login."""
        response = self.client.post(reverse('login'), {
            'username': 'authuser', 'password': 'AuthPass123',
        })
        self.assertRedirects(response, reverse('student_list'))

    def test_protected_page_redirects_anonymous_user(self):
        """9. Protected page redirect."""
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_redirects_to_login(self):
        self.client.login(username='authuser', password='AuthPass123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


# ---------------------------------------------------------------------------
# Task 2 - Model relationships
# ---------------------------------------------------------------------------

class ModelRelationshipTests(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name="Design", description="Design dept")
        self.course_a = Course.objects.create(name="UX Basics", code="UX101")
        self.course_b = Course.objects.create(name="UI Design", code="UI101")
        self.student = Student.objects.create(
            name="Ravi Kumar", email="ravi@example.com", age=23, marks=70,
            department=self.department,
        )

    def test_department_relationship(self):
        """10. Department relationship (FK, related_name)."""
        self.assertEqual(self.student.department, self.department)
        self.assertIn(self.student, self.department.students.all())

    def test_department_set_null_on_delete(self):
        self.department.delete()
        self.student.refresh_from_db()
        self.assertIsNone(self.student.department)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

    def test_one_to_one_profile_relationship(self):
        """11. One-to-one profile relationship."""
        profile = StudentProfile.objects.create(
            student=self.student, phone="9999999999", address="1 MG Road",
        )
        self.assertEqual(self.student.profile, profile)
        self.assertEqual(profile.student, self.student)

    def test_profile_deleted_when_student_deleted(self):
        StudentProfile.objects.create(student=self.student, phone="123")
        self.student.delete()
        self.assertFalse(StudentProfile.objects.filter(phone="123").exists())

    def test_many_to_many_course_relationship(self):
        """12. Many-to-many course relationship."""
        self.student.courses.add(self.course_a, self.course_b)
        self.assertEqual(self.student.courses.count(), 2)
        self.assertIn(self.student, self.course_a.students.all())


# ---------------------------------------------------------------------------
# Task 5 - Filtering, search, dashboard
# ---------------------------------------------------------------------------

class SearchAndFilterTests(BaseAuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.other_department = Department.objects.create(name="Business")
        self.other_student = Student.objects.create(
            name="Zara Khan", email="zara@example.com", age=24, marks=30,
            department=self.other_department, is_active=False,
        )

    def test_search_functionality(self):
        """13. Search functionality."""
        response = self.client.get(reverse('student_list'), {'q': 'Asha'})
        self.assertContains(response, "Asha Verma")
        self.assertNotContains(response, "Zara Khan")

    def test_search_by_email(self):
        response = self.client.get(reverse('student_list'), {'q': 'zara@example.com'})
        self.assertContains(response, "Zara Khan")

    def test_department_filter(self):
        """14. Department filter."""
        response = self.client.get(reverse('student_list'), {'department': self.department.id})
        self.assertContains(response, "Asha Verma")
        self.assertNotContains(response, "Zara Khan")

    def test_status_filter(self):
        response = self.client.get(reverse('student_list'), {'status': 'inactive'})
        self.assertContains(response, "Zara Khan")
        self.assertNotContains(response, "Asha Verma")

    def test_result_filter(self):
        response = self.client.get(reverse('student_list'), {'result': 'fail'})
        self.assertContains(response, "Zara Khan")
        self.assertNotContains(response, "Asha Verma")


class DashboardTests(BaseAuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        Student.objects.create(
            name="High Scorer", email="high@example.com", age=20, marks=99,
            department=self.department,
        )

    def test_dashboard_totals(self):
        """15. Dashboard totals."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['total_departments'], 1)
        self.assertEqual(response.context['total_courses'], 1)
        self.assertEqual(response.context['top_student'].name, "High Scorer")

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)


class HomeAboutPageTests(TestCase):

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug Network Private Limited")

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Page")
