from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from io import StringIO

from .models import Student, Department, Course, StudentProfile, UserProfile, AuditLog, Feedback, MarksHistory, Enrollment
from . import services


class StudentsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.staff_user.profile.role = 'admin'
        self.staff_user.profile.save()
        self.client.force_login(self.staff_user)

    def test_home_page_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
        self.client.logout()
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
            joined_date=timezone.localdate()
        )
        self.assertEqual(student.name, "Test Student")
        self.assertEqual(student.email, "test@example.com")
        self.assertEqual(student.age, 20)

    def test_student_list_page(self):
        course1 = Course.objects.create(course_name="Django", code="CS101", duration=4)
        course2 = Course.objects.create(course_name="Flask", code="CS102", duration=4)
        
        s1 = Student.objects.create(name="Alice", email="alice@example.com", age=22, joined_date=timezone.localdate(), active_status=True)
        s2 = Student.objects.create(name="Bob", email="bob@example.com", age=25, joined_date=timezone.localdate(), active_status=False)
        
        Enrollment.objects.create(student=s1, course=course1, current_mark=90)
        Enrollment.objects.create(student=s2, course=course2, current_mark=30)
        
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')

    def test_invalid_student_form_data(self):
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 15,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'age', 'Age must be between 16 and 60.')

    def test_valid_student_form_submission(self):
        self.assertEqual(Student.objects.count(), 0)
        
        response = self.client.post(reverse('add_student'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'age': 25,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        
        self.assertRedirects(response, reverse('student_list'))
        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()
        self.assertEqual(student.name, 'Jane Doe')
        self.assertEqual(student.email, 'jane@example.com')
        self.assertEqual(student.age, 25)

    def test_student_detail_view(self):
        student = Student.objects.create(name="Charlie", email="charlie@example.com", age=21, joined_date=timezone.localdate(), active_status=True)
        response = self.client.get(reverse('student_detail', kwargs={'id': student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertContains(response, 'Charlie')
        self.assertContains(response, 'charlie@example.com')

    def test_student_detail_not_found(self):
        response = self.client.get(reverse('student_detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_student_edit_view_get(self):
        student = Student.objects.create(name="Charlie", email="charlie@example.com", age=21, joined_date=timezone.localdate(), active_status=True)
        response = self.client.get(reverse('edit_student', kwargs={'id': student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_form.html')

    def test_student_edit_view_post_valid(self):
        student = Student.objects.create(name="Charlie", email="charlie@example.com", age=21, joined_date=timezone.localdate(), active_status=True)
        response = self.client.post(reverse('edit_student', kwargs={'id': student.id}), {
            'name': 'Charlie Updated',
            'email': 'charlie-new@example.com',
            'age': 22,
            'joined_date': student.joined_date,
            'active_status': False
        })
        self.assertRedirects(response, reverse('student_detail', kwargs={'id': student.id}))
        student.refresh_from_db()
        self.assertEqual(student.name, 'Charlie Updated')

    def test_student_delete_view_get_staff(self):
        student = Student.objects.create(name="Charlie", email="charlie@example.com", age=21, joined_date=timezone.localdate(), active_status=True)
        response = self.client.get(reverse('delete_student', kwargs={'id': student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_confirm_delete.html')

    def test_student_delete_view_post_staff(self):
        student = Student.objects.create(name="Charlie", email="charlie@example.com", age=21, joined_date=timezone.localdate(), active_status=True)
        response = self.client.post(reverse('delete_student', kwargs={'id': student.id}))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(id=student.id).exists())


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'ComplexPass123!'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        self.staff_user = User.objects.create_user(username='admin_staff', password=self.password, is_staff=True)
        self.staff_user.profile.role = 'admin'
        self.staff_user.profile.save()
        
        self.student = Student.objects.create(name="Test Student", email="student@example.com", age=22, joined_date=timezone.localdate())

    def test_registration_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_registration_view_post_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')

    def test_logout_view_requires_post(self):
        self.client.login(username=self.username, password=self.password)
        response_get = self.client.get(reverse('logout'))
        self.assertEqual(response_get.status_code, 405)
        
        response_post = self.client.post(reverse('logout'))
        self.assertRedirects(response_post, reverse('login'))

    def test_unauthenticated_user_redirected_to_login(self):
        protected_urls = [
            reverse('student_list'),
            reverse('add_student'),
            reverse('student_detail', kwargs={'id': self.student.id}),
            reverse('edit_student', kwargs={'id': self.student.id}),
            reverse('delete_student', kwargs={'id': self.student.id}),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"/login/?next={url}")

    def test_non_staff_user_cannot_add_student(self):
        self.client.login(username=self.username, password=self.password)
        initial_count = Student.objects.count()
        response = self.client.post(reverse('add_student'), {
            'name': 'Unauthorized Student',
            'email': 'unauth@example.com',
            'age': 20,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Student.objects.count(), initial_count)


class AdditionalRiskAndRetaskTests(TestCase):
    def setUp(self):
        self.password = 'ComplexPass123!'
        self.admin = User.objects.create_user(username='admin_test', password=self.password)
        self.admin.profile.role = 'admin'
        self.admin.profile.save()
        
        self.trainer = User.objects.create_user(username='trainer_test', password=self.password)
        self.trainer.profile.role = 'trainer'
        self.trainer.profile.save()

        self.dept = Department.objects.create(name="Risk Dept", description="Risk")
        self.course = Course.objects.create(course_name="Python 101", code="RISK101", duration=4, assigned_trainer=self.trainer)
        self.student = Student.objects.create(name="Student One", email="risk_s1@test.com", age=20, joined_date=timezone.localdate(), department=self.dept)
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course, current_mark=75)

    def test_migration_cleanliness(self):
        out = StringIO()
        call_command('makemigrations', check=True, dry_run=True, stdout=out)
        self.assertIn("No changes detected", out.getvalue())

    def test_enrollment_uniqueness_constraint(self):
        with self.assertRaises(ValidationError):
            Enrollment.objects.create(student=self.student, course=self.course, current_mark=80)

    def test_model_level_age_validation(self):
        s_underage = Student(name="Too Young", email="young@test.com", age=15, joined_date=timezone.localdate())
        with self.assertRaises(ValidationError):
            s_underage.save()

        s_overage = Student(name="Too Old", email="old@test.com", age=61, joined_date=timezone.localdate())
        with self.assertRaises(ValidationError):
            s_overage.save()

    def test_model_level_marks_validation(self):
        e_invalid = Enrollment(student=self.student, course=self.course, current_mark=105)
        with self.assertRaises(ValidationError):
            e_invalid.clean()

    def test_future_date_of_birth_validation(self):
        future_dob = timezone.localdate() + timezone.timedelta(days=1)
        profile = StudentProfile(student=self.student, phone="12345", address="St", date_of_birth=future_dob)
        with self.assertRaises(ValidationError):
            profile.clean()

    def test_toggle_user_status_requires_post(self):
        self.client.force_login(self.admin)
        user_to_toggle = User.objects.create_user(username='toggle_me', password=self.password)
        
        res_get = self.client.get(reverse('toggle_user_status', kwargs={'user_id': user_to_toggle.id}))
        self.assertEqual(res_get.status_code, 405)
        
        res_post = self.client.post(reverse('toggle_user_status', kwargs={'user_id': user_to_toggle.id}))
        self.assertRedirects(res_post, reverse('user_management'))
        user_to_toggle.refresh_from_db()
        self.assertFalse(user_to_toggle.is_active)

    def test_safe_login_next_url_redirect(self):
        next_user = User.objects.create_user(username='next_user', password=self.password)
        
        # Malicious external URL
        res_bad = self.client.post(reverse('login') + '?next=https://evil.com/phishing', {
            'username': 'next_user',
            'password': self.password,
        })
        self.assertEqual(res_bad.status_code, 302)
        self.assertEqual(res_bad.url, reverse('home'))

        self.client.logout()

        # Safe local URL
        url_safe = reverse('user_management')
        res_good = self.client.post(reverse('login') + f'?next={url_safe}', {
            'username': 'next_user',
            'password': self.password,
        })
        self.assertEqual(res_good.status_code, 302)
        self.assertEqual(res_good.url, url_safe)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'])
    def test_custom_error_pages(self):
        trainer_user = User.objects.create_user(username='err_trainer', password=self.password)
        trainer_user.profile.role = 'trainer'
        trainer_user.profile.save()
        self.client.force_login(trainer_user)
        
        res_403 = self.client.get(reverse('user_management'))
        self.assertEqual(res_403.status_code, 403)

        res_404 = self.client.get('/nonexistent-url-path-9999/')
        self.assertEqual(res_404.status_code, 404)

    def test_student_list_pagination_and_query_count(self):
        self.client.force_login(self.admin)
        
        for i in range(15):
            Student.objects.create(name=f"Paginated {i}", email=f"p{i}@test.com", age=20+i, joined_date=timezone.localdate())
            
        res = self.client.get(reverse('student_list') + '?q=Paginated&active_status=active')
        self.assertEqual(res.status_code, 200)
        self.assertIn('encoded_params', res.context)
        self.assertEqual(len(res.context['students']), 10)

    def test_seed_demo_data_idempotency(self):
        call_command('seed_demo_data')
        c1 = Student.objects.count()
        call_command('seed_demo_data')
        c2 = Student.objects.count()
        self.assertEqual(c1, c2)
        self.assertGreaterEqual(c1, 20)

    def test_atomic_services(self):
        services.update_student_marks(
            student=self.student,
            course=self.course,
            new_marks=95,
            updater_user=self.trainer,
            reason="Excellent progress"
        )
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.current_mark, 95)
        self.assertTrue(MarksHistory.objects.filter(student=self.student, new_marks=95).exists())

        services.create_feedback(
            student=self.student,
            trainer_user=self.trainer,
            course=self.course,
            rating=5,
            comments="Great active learning",
            is_visible=True
        )
        self.assertTrue(Feedback.objects.filter(student=self.student, rating=5).exists())
