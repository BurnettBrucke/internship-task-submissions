from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Student

class StudentsViewsTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/home.html')
        self.assertContains(response, 'Bug Network Private Limited')

    def test_about_page_status_code(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>About Page</h1>')
        self.assertContains(response, 'Welcome to the About page of our Django application!')

    def test_student_model_creation(self):
        student = Student.objects.create(
            name="Test Student",
            email="test@example.com",
            age=20,
            course="Python",
            marks=85,
            joined_date=timezone.localdate()
        )
        self.assertEqual(student.name, "Test Student")
        self.assertEqual(student.email, "test@example.com")
        self.assertEqual(student.age, 20)
        self.assertEqual(student.course, "Python")
        self.assertEqual(student.marks, 85)
        self.assertEqual(str(student), "Test Student (Python)")

    def test_student_list_page(self):
        Student.objects.create(
            name="Alice",
            email="alice@example.com",
            age=22,
            course="Django",
            marks=90,
            joined_date=timezone.localdate(),
            active_status=True
        )
        Student.objects.create(
            name="Bob",
            email="bob@example.com",
            age=25,
            course="Flask",
            marks=30,
            joined_date=timezone.localdate(),
            active_status=False
        )
        
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'Pass')
        self.assertContains(response, 'Fail')
        self.assertContains(response, '2')  # Total count
        self.assertContains(response, '1')  # Active count

    def test_invalid_student_form_data(self):
        # 1. Invalid age (under 16)
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 15,
            'course': 'Python',
            'marks': 50,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'age', 'Age must be between 16 and 60.')
        
        # 2. Invalid age (over 60)
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 61,
            'course': 'Python',
            'marks': 50,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'age', 'Age must be between 16 and 60.')

        # 3. Invalid email
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'email': 'invalid-email',
            'age': 20,
            'course': 'Python',
            'marks': 50,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue('email' in form.errors)

        # 4. Empty name
        response = self.client.post(reverse('add_student'), {
            'name': '',
            'email': 'john@example.com',
            'age': 20,
            'course': 'Python',
            'marks': 50,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue('name' in form.errors)

        # 5. Empty course
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 20,
            'course': '',
            'marks': 50,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue('course' in form.errors)

    def test_valid_student_form_submission(self):
        self.assertEqual(Student.objects.count(), 0)
        
        response = self.client.post(reverse('add_student'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'age': 25,
            'course': 'Python Web Development',
            'marks': 85,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        
        self.assertRedirects(response, reverse('student_list'))
        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()
        self.assertEqual(student.name, 'Jane Doe')
        self.assertEqual(student.email, 'jane@example.com')
        self.assertEqual(student.age, 25)

    def test_marks_boundary_values(self):
        # Test valid boundary 0
        response = self.client.post(reverse('add_student'), {
            'name': 'Boundary Zero',
            'email': 'zero@example.com',
            'age': 20,
            'course': 'Python',
            'marks': 0,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(Student.objects.filter(email='zero@example.com').exists())

        # Test valid boundary 40
        response = self.client.post(reverse('add_student'), {
            'name': 'Boundary Forty',
            'email': 'forty@example.com',
            'age': 20,
            'course': 'Python',
            'marks': 40,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(Student.objects.filter(email='forty@example.com').exists())

        # Test valid boundary 100
        response = self.client.post(reverse('add_student'), {
            'name': 'Boundary Hundred',
            'email': 'hundred@example.com',
            'age': 20,
            'course': 'Python',
            'marks': 100,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(Student.objects.filter(email='hundred@example.com').exists())

        # Test invalid boundary -1
        response = self.client.post(reverse('add_student'), {
            'name': 'Boundary Negative',
            'email': 'negative@example.com',
            'age': 20,
            'course': 'Python',
            'marks': -1,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'marks', 'Marks must be between 0 and 100.')

        # Test invalid boundary 101
        response = self.client.post(reverse('add_student'), {
            'name': 'Boundary Excessive',
            'email': 'excessive@example.com',
            'age': 20,
            'course': 'Python',
            'marks': 101,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'marks', 'Marks must be between 0 and 100.')
