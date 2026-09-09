from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Student, Department, StudentProfile, Course
from .forms import StudentForm


class StudentPortalTests(TestCase):

    def setUp(self):
        # Create a user for login tests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create department
        self.department = Department.objects.create(
            name='Computer Science',
            description='Computer Science Department'
        )

        # Create student
        self.student = Student.objects.create(
            name='Rahul',
            email='rahul@gmail.com',
            age=22,
            course='Python',
            marks=80,
            joined_date='2026-09-01',
            active=True,
            department=self.department
        )

        # Create course
        self.course = Course.objects.create(
            course_name='Django',
            code='DJ101',
            duration='3 Months',
            active=True
        )

    # 1. Student list loads
    def test_student_list_loads(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('student_list')
        )

        self.assertEqual(response.status_code, 200)

    # 2. Student detail loads
    def test_student_detail_loads(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse(
                'student_detail',
                args=[self.student.id]
            )
        )

        self.assertEqual(response.status_code, 200)

    # 3. Valid student creation
    def test_valid_student_creation(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        data = {
            'name': 'Priya',
            'email': 'priya@gmail.com',
            'age': 21,
            'course': 'Python',
            'marks': 75,
            'joined_date': '2026-09-02',
            'active': True,
        }

        response = self.client.post(
            reverse('add_student'),
            data
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Student.objects.filter(
                email='priya@gmail.com'
            ).exists()
        )

    # 4. Invalid form
    def test_invalid_student_form(self):
        form = StudentForm(data={
            'name': '',
            'email': 'wrong-email',
            'age': 10,
            'course': '',
            'marks': 150,
            'joined_date': '2026-09-01',
            'active': True,
        })

        self.assertFalse(form.is_valid())

    # 5. Student update
    def test_student_update(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        data = {
            'name': 'Rahul Updated',
            'email': 'rahul_updated@gmail.com',
            'age': 23,
            'course': 'Django',
            'marks': 90,
            'joined_date': '2026-09-01',
            'active': True,
        }

        response = self.client.post(
            reverse(
                'edit_student',
                args=[self.student.id]
            ),
            data
        )

        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.name,
            'Rahul Updated'
        )

    # 6. Student delete
    def test_student_delete(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.post(
            reverse(
                'delete_student',
                args=[self.student.id]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Student.objects.filter(
                id=self.student.id
            ).exists()
        )

    # 7. Login page loads
    def test_login_page_loads(self):
        response = self.client.get(
            reverse('login')
        )

        self.assertEqual(response.status_code, 200)

    # 8. Successful login
    def test_successful_login(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'testpassword'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse('dashboard')
        )

    # 9. Protected page redirects unauthenticated user
    def test_protected_page_redirects(self):
        response = self.client.get(
            reverse('student_list')
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            '/login/',
            response.url
        )

    # 10. Department relationship
    def test_department_relationship(self):
        self.assertEqual(
            self.student.department,
            self.department
        )

        self.assertIn(
            self.student,
            self.department.students.all()
        )

    # 11. One-to-One StudentProfile
    def test_student_profile_one_to_one(self):
        profile = StudentProfile.objects.create(
            student=self.student,
            phone='9876543210',
            address='Indore',
            date_of_birth='2004-07-06'
        )

        self.assertEqual(
            profile.student,
            self.student
        )

        self.assertEqual(
            self.student.profile,
            profile
        )

    # 12. Many-to-Many Course
    def test_course_many_to_many(self):
        self.course.students.add(self.student)

        self.assertIn(
            self.student,
            self.course.students.all()
        )

        self.assertIn(
            self.course,
            self.student.courses.all()
        )

    # 13. Student search
    def test_student_search(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('student_list'),
            {'search': 'Rahul'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'Rahul'
        )

    # 14. Department filter
    def test_department_filter(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('student_list'),
            {'department': self.department.id}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'Rahul'
        )

    # 15. Dashboard totals
    def test_dashboard_totals(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context['total_students'],
            1
        )

        self.assertEqual(
            response.context['total_active_students'],
            1
        )

        self.assertEqual(
            response.context['total_departments'],
            1
        )

        self.assertEqual(
            response.context['total_courses'],
            1
        )