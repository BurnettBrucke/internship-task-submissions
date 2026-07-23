from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .forms import StudentForm
from .models import Student


class StudentModelTests(TestCase):
    """Student model creation."""

    def test_create_student(self):
        student = Student.objects.create(
            name="Asha Verma",
            email="asha@example.com",
            age=21,
            course="Python and Django",
            marks=75,
        )
        self.assertEqual(Student.objects.count(), 1)
        self.assertTrue(student.is_active)
        self.assertIsNotNone(student.joined_date)

    def test_str_method(self):
        student = Student.objects.create(
            name="Rohit Sharma",
            email="rohit@example.com",
            age=22,
            course="Data Science",
            marks=60,
        )
        self.assertEqual(str(student), "Rohit Sharma (Data Science)")

    def test_marks_boundary_values(self):
        """Marks boundary values: 0, 40 and 100."""
        cases = [
            (0, "Fail"),
            (39.99, "Fail"),
            (40, "Pass"),
            (100, "Pass"),
        ]
        for marks, expected in cases:
            student = Student.objects.create(
                name=f"Student {marks}",
                email=f"student{marks}@example.com",
                age=20,
                course="Testing",
                marks=marks,
            )
            self.assertEqual(student.result_status, expected)


class StudentListViewTests(TestCase):
    """Student list page."""

    def setUp(self):
        Student.objects.create(
            name="Active One", email="active1@example.com", age=20,
            course="Course A", marks=50, is_active=True,
        )
        Student.objects.create(
            name="Inactive One", email="inactive1@example.com", age=25,
            course="Course B", marks=30, is_active=False,
        )

    def test_status_code_and_template(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')

    def test_context_contains_students_and_counts(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['active_students'], 1)
        self.assertEqual(len(response.context['students']), 2)

    def test_empty_student_list(self):
        """Empty student list renders without error."""
        Student.objects.all().delete()
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_students'], 0)
        self.assertContains(response, "No students found yet.")

    def test_pass_fail_labels_render(self):
        response = self.client.get(reverse('student_list'))
        self.assertContains(response, "Pass")
        self.assertContains(response, "Fail")


class StudentFormTests(TestCase):
    """Invalid student form data / valid student form submission."""

    def valid_data(self, **overrides):
        data = {
            "name": "New Student",
            "email": "new.student@example.com",
            "age": 22,
            "course": "Web Development",
            "marks": 55,
        }
        data.update(overrides)
        return data

    def test_valid_form(self):
        form = StudentForm(data=self.valid_data())
        self.assertTrue(form.is_valid())

    def test_empty_name_invalid(self):
        form = StudentForm(data=self.valid_data(name=""))
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_invalid_email(self):
        form = StudentForm(data=self.valid_data(email="not-an-email"))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_age_out_of_range(self):
        form = StudentForm(data=self.valid_data(age=15))
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

        form = StudentForm(data=self.valid_data(age=61))
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

    def test_marks_out_of_range(self):
        form = StudentForm(data=self.valid_data(marks=-1))
        self.assertFalse(form.is_valid())
        self.assertIn("marks", form.errors)

        form = StudentForm(data=self.valid_data(marks=101))
        self.assertFalse(form.is_valid())
        self.assertIn("marks", form.errors)

    def test_empty_course_invalid(self):
        form = StudentForm(data=self.valid_data(course=""))
        self.assertFalse(form.is_valid())
        self.assertIn("course", form.errors)

    def test_marks_boundary_values_in_form(self):
        for marks in [0, 40, 100]:
            form = StudentForm(data=self.valid_data(marks=marks, email=f"m{marks}@example.com"))
            self.assertTrue(form.is_valid(), form.errors)


class AddStudentViewTests(TestCase):
    """Valid student form submission via the add-student view."""

    def test_get_add_student_page(self):
        response = self.client.get(reverse('add_student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/add_student.html')

    def test_valid_submission_redirects_and_saves(self):
        data = {
            "name": "Priya Singh",
            "email": "priya.singh@example.com",
            "age": 23,
            "course": "Machine Learning",
            "marks": 88,
        }
        response = self.client.post(reverse('add_student'), data=data)
        self.assertRedirects(response, reverse('student_list'))
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.first().name, "Priya Singh")

    def test_invalid_submission_shows_errors_and_does_not_save(self):
        data = {
            "name": "",
            "email": "bad-email",
            "age": 5,
            "course": "",
            "marks": 200,
        }
        response = self.client.post(reverse('add_student'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)
        self.assertFormError(response.context['form'], 'name', 'This field is required.')


class HomeAboutPageTests(TestCase):

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug Network Private Limited")

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Page")
