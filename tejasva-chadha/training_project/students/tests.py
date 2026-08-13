from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Student, Department, Course, StudentProfile, UserProfile, AuditLog, Feedback, MarksHistory
from . import services

class StudentsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Link user to a student profile if needed
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        # Explicitly assign admin role to staff user profile
        self.staff_user.profile.role = 'admin'
        self.staff_user.profile.save()
        self.client.force_login(self.staff_user)

    def test_home_page_status_code(self):
        # Home page is accessible without auth but redirects authenticated users
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302) # Redirects to dashboard redirect
        
        # Test anonymous access
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

    def test_invalid_student_form_data(self):
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

    def test_student_detail_view(self):
        student = Student.objects.create(
            name="Charlie",
            email="charlie@example.com",
            age=21,
            course="Python",
            marks=75,
            joined_date=timezone.localdate(),
            active_status=True
        )
        response = self.client.get(reverse('student_detail', kwargs={'id': student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertContains(response, 'Charlie')
        self.assertContains(response, 'charlie@example.com')

    def test_student_detail_not_found(self):
        response = self.client.get(reverse('student_detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_student_edit_view_get(self):
        student = Student.objects.create(
            name="Charlie",
            email="charlie@example.com",
            age=21,
            course="Python",
            marks=75,
            joined_date=timezone.localdate(),
            active_status=True
        )
        response = self.client.get(reverse('edit_student', kwargs={'id': student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_form.html')
        self.assertContains(response, 'Edit Student Record')

    def test_student_edit_view_post_valid(self):
        student = Student.objects.create(
            name="Charlie",
            email="charlie@example.com",
            age=21,
            course="Python",
            marks=75,
            joined_date=timezone.localdate(),
            active_status=True
        )
        response = self.client.post(reverse('edit_student', kwargs={'id': student.id}), {
            'name': 'Charlie Updated',
            'email': 'charlie-new@example.com',
            'age': 22,
            'course': 'Python Web',
            'marks': 80,
            'joined_date': student.joined_date,
            'active_status': False
        })
        self.assertRedirects(response, reverse('student_detail', kwargs={'id': student.id}))
        student.refresh_from_db()
        self.assertEqual(student.name, 'Charlie Updated')

    def test_student_delete_view_get_staff(self):
        student = Student.objects.create(
            name="Charlie",
            email="charlie@example.com",
            age=21,
            course="Python",
            marks=75,
            joined_date=timezone.localdate(),
            active_status=True
        )
        response = self.client.get(reverse('delete_student', kwargs={'id': student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_confirm_delete.html')
        self.assertContains(response, 'Confirm Deletion')

    def test_student_delete_view_post_staff(self):
        student = Student.objects.create(
            name="Charlie",
            email="charlie@example.com",
            age=21,
            course="Python",
            marks=75,
            joined_date=timezone.localdate(),
            active_status=True
        )
        response = self.client.post(reverse('delete_student', kwargs={'id': student.id}))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(id=student.id).exists())


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'ComplexPass123!'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # Default role for self.user is 'student'
        
        self.staff_user = User.objects.create_user(username='admin_staff', password=self.password, is_staff=True)
        self.staff_user.profile.role = 'admin'
        self.staff_user.profile.save()
        
        self.student = Student.objects.create(
            name="Test Student",
            email="student@example.com",
            age=22,
            course="Python",
            marks=90,
            joined_date=timezone.localdate()
        )

    def test_registration_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Create Account')

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
        self.assertContains(response, 'Welcome Back')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        # Login redirects to home which forwards to redirect dashboard
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

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

    def test_public_home_page_accessible_without_auth(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_display_logged_in_username_in_navbar(self):
        self.client.login(username=self.username, password=self.password)
        # Regular user (student role) gets home page redirects to student dashboard
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.username)

    def test_non_staff_user_cannot_add_student(self):
        self.client.login(username=self.username, password=self.password)
        initial_count = Student.objects.count()
        response = self.client.post(reverse('add_student'), {
            'name': 'Unauthorized Student',
            'email': 'unauth@example.com',
            'age': 20,
            'course': 'Python',
            'marks': 80,
            'joined_date': '2026-07-25',
            'active_status': True
        })
        # Standard students are unauthorized and receive a 403 Forbidden error
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Student.objects.count(), initial_count)

    def test_non_staff_user_cannot_edit_student(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('edit_student', kwargs={'id': self.student.id}), {
            'name': 'Hacked Name',
            'email': self.student.email,
            'age': self.student.age,
            'course': self.student.course,
            'marks': self.student.marks,
            'joined_date': self.student.joined_date,
            'active_status': True
        })
        self.assertEqual(response.status_code, 403)
        self.student.refresh_from_db()
        self.assertNotEqual(self.student.name, 'Hacked Name')

    def test_non_staff_user_cannot_delete_student(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('delete_student', kwargs={'id': self.student.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())

    def test_staff_user_can_delete_student(self):
        self.client.login(username='admin_staff', password=self.password)
        response = self.client.post(reverse('delete_student', kwargs={'id': self.student.id}))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())


class StudentRelationshipsTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            name="Computer Science",
            description="CS Department"
        )
        self.course_django = Course.objects.create(
            course_name="Django Web Development",
            code="CS303",
            duration=12,
            active_status=True
        )
        self.course_python = Course.objects.create(
            course_name="Python Fundamentals",
            code="CS101",
            duration=8,
            active_status=True
        )
        self.student = Student.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            age=20,
            course="Python",
            marks=85,
            joined_date=timezone.localdate(),
            department=self.dept
        )
        self.student.courses.add(self.course_django, self.course_python)
        
        self.profile = StudentProfile.objects.create(
            student=self.student,
            phone="1234567890",
            address="123 Main St",
            date_of_birth=timezone.localdate() - timezone.timedelta(days=7300)
        )

    def test_department_relationship(self):
        self.assertEqual(self.student.department, self.dept)
        self.assertIn(self.student, self.dept.students.all())

    def test_course_relationship(self):
        courses = self.student.courses.all()
        self.assertEqual(courses.count(), 2)
        self.assertIn(self.course_django, courses)
        self.assertIn(self.course_python, courses)
        self.assertIn(self.student, self.course_django.students.all())

    def test_profile_relationship(self):
        self.assertEqual(self.student.profile, self.profile)
        self.assertEqual(self.profile.student, self.student)


class StudentServicesAndFilteringTest(TestCase):
    def setUp(self):
        self.cs_dept = Department.objects.create(name="Computer Science", description="CS")
        self.ee_dept = Department.objects.create(name="Electrical Engineering", description="EE")

        self.py_course = Course.objects.create(course_name="Python 101", code="CS101", duration=4)
        self.web_course = Course.objects.create(course_name="Web Dev", code="CS202", duration=6)

        self.s1 = Student.objects.create(
            name="Alice Alpha", email="alice@test.com", age=20, course="Python",
            marks=95, joined_date=timezone.localdate(), active_status=True, department=self.cs_dept
        )
        self.s1.courses.add(self.py_course)

        self.s2 = Student.objects.create(
            name="Bob Beta", email="bob@test.com", age=22, course="Web Dev",
            marks=40, joined_date=timezone.localdate() - timezone.timedelta(days=5), active_status=False, department=self.ee_dept
        )
        self.s2.courses.add(self.web_course)

        self.s3 = Student.objects.create(
            name="Charlie Gamma", email="charlie@test.com", age=21, course="Python",
            marks=70, joined_date=timezone.localdate() - timezone.timedelta(days=10), active_status=True, department=self.cs_dept
        )

    def test_dashboard_stats_services(self):
        stats = services.get_dashboard_stats()
        self.assertEqual(stats['total_students'], 3)
        self.assertEqual(stats['active_students'], 2)
        self.assertEqual(stats['total_departments'], 2)
        self.assertEqual(stats['total_courses'], 2)
        self.assertEqual(stats['avg_marks'], 68.3)
        self.assertEqual(stats['highest_scoring_student'], self.s1)
        self.assertEqual(len(stats['recently_joined_students']), 3)

    def test_filter_by_department(self):
        qs = services.filter_students({'department': str(self.cs_dept.id)})
        self.assertEqual(qs.count(), 2)
        self.assertIn(self.s1, qs)
        self.assertIn(self.s3, qs)

    def test_filter_by_course(self):
        qs = services.filter_students({'course': str(self.web_course.id)})
        self.assertEqual(qs.count(), 1)
        self.assertIn(self.s2, qs)

    def test_filter_by_active_status(self):
        active_qs = services.filter_students({'active_status': 'active'})
        self.assertEqual(active_qs.count(), 2)
        self.assertIn(self.s1, active_qs)
        self.assertIn(self.s3, active_qs)

        inactive_qs = services.filter_students({'active_status': 'inactive'})
        self.assertEqual(inactive_qs.count(), 1)
        self.assertIn(self.s2, inactive_qs)

    def test_filter_by_pass_fail_status(self):
        pass_qs = services.filter_students({'pass_fail_status': 'pass'})
        self.assertEqual(pass_qs.count(), 2)
        self.assertIn(self.s1, pass_qs)
        self.assertIn(self.s3, pass_qs)

        fail_qs = services.filter_students({'pass_fail_status': 'fail'})
        self.assertEqual(fail_qs.count(), 1)
        self.assertIn(self.s2, fail_qs)

    def test_search_query(self):
        # Search name
        qs_name = services.filter_students({'q': 'Alice'})
        self.assertEqual(qs_name.count(), 1)
        self.assertIn(self.s1, qs_name)

        # Search email
        qs_email = services.filter_students({'q': 'bob@test.com'})
        self.assertEqual(qs_email.count(), 1)
        self.assertIn(self.s2, qs_email)

        # Search course
        qs_course = services.filter_students({'q': 'Web Dev'})
        self.assertEqual(qs_course.count(), 1)
        self.assertIn(self.s2, qs_course)


class RoleBasedAccessControlTests(TestCase):
    def setUp(self):
        self.password = 'ComplexPass123!'
        
        self.admin = User.objects.create_user(username='admin_role', password=self.password)
        self.admin.profile.role = 'admin'
        self.admin.profile.save()
        
        self.trainer = User.objects.create_user(username='trainer_role', password=self.password)
        self.trainer.profile.role = 'trainer'
        self.trainer.profile.save()
        
        self.student_user = User.objects.create_user(username='student_role', password=self.password)
        self.student_user.profile.role = 'student'
        self.student_user.profile.save()
        
        self.dept = Department.objects.create(name="Design", description="Design Dept")
        self.course = Course.objects.create(
            course_name="UX Research", code="UX101", duration=6, assigned_trainer=self.trainer
        )
        
        self.student_record = Student.objects.create(
            name="Arianne Design",
            email="arianne@design.com",
            age=24,
            course="UX Research",
            marks=88,
            joined_date=timezone.localdate(),
            department=self.dept,
            user=self.student_user
        )
        self.student_record.courses.add(self.course)

    def test_dashboard_redirect_admin(self):
        self.client.login(username='admin_role', password=self.password)
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_dashboard_redirect_trainer(self):
        self.client.login(username='trainer_role', password=self.password)
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('trainer_dashboard'))

    def test_dashboard_redirect_student(self):
        self.client.login(username='student_role', password=self.password)
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(username='admin_role', password=self.password)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_trainer_cannot_access_admin_dashboard(self):
        self.client.login(username='trainer_role', password=self.password)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_student_cannot_access_admin_dashboard(self):
        self.client.login(username='student_role', password=self.password)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_ownership_filtering_student_profile(self):
        # Create another student
        other_user = User.objects.create_user(username='other_student', password=self.password)
        other_student = Student.objects.create(
            name="Other Student", email="other@test.com", age=21, course="Python",
            marks=90, joined_date=timezone.localdate()
        )
        
        # Log in as first student, try to view other student's detail view
        self.client.login(username='student_role', password=self.password)
        response = self.client.get(reverse('student_detail', kwargs={'id': other_student.id}))
        self.assertEqual(response.status_code, 403)

        # But can view own profile
        response = self.client.get(reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.assertEqual(response.status_code, 200)

    def test_trainer_grading_permissions(self):
        # Trainer can update marks for assigned student
        self.client.login(username='trainer_role', password=self.password)
        response = self.client.post(reverse('edit_student', kwargs={'id': self.student_record.id}), {
            'marks': 95
        })
        self.assertRedirects(response, reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.student_record.refresh_from_db()
        self.assertEqual(self.student_record.marks, 95)
        
        # Trainer cannot update other fields (e.g. name remains unchanged in views logic)
        response = self.client.post(reverse('edit_student', kwargs={'id': self.student_record.id}), {
            'name': 'Hacked Name',
            'marks': 90
        })
        self.student_record.refresh_from_db()
        self.assertEqual(self.student_record.name, "Arianne Design")


class SecureAccountManagementTests(TestCase):
    def setUp(self):
        self.password = 'Pass123!@#'
        self.admin_user = User.objects.create_superuser(username='admin_user', email='admin@test.com', password=self.password)
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
        
        self.trainer_user = User.objects.create_user(username='trainer_user', email='trainer@test.com', password=self.password)
        self.trainer_user.profile.role = 'trainer'
        self.trainer_user.profile.save()

    def test_student_registration_active(self):
        # Register a student
        response = self.client.post(reverse('register'), {
            'username': 'new_student',
            'email': 'student@test.com',
            'role': 'student',
            'password1': 'NewPass123!@#',
            'password2': 'NewPass123!@#',
        })
        self.assertRedirects(response, reverse('login'))
        new_user = User.objects.get(username='new_student')
        self.assertTrue(new_user.is_active)
        self.assertEqual(new_user.profile.role, 'student')
        self.assertTrue(AuditLog.objects.filter(action='create', affected_object='User: new_student').exists())

    def test_trainer_registration_pending_approval(self):
        # Register a trainer
        response = self.client.post(reverse('register'), {
            'username': 'new_trainer',
            'email': 'new_trainer@test.com',
            'role': 'trainer',
            'password1': 'NewPass123!@#',
            'password2': 'NewPass123!@#',
        })
        self.assertRedirects(response, reverse('login'))
        new_user = User.objects.get(username='new_trainer')
        self.assertFalse(new_user.is_active)
        self.assertEqual(new_user.profile.role, 'trainer')
        self.assertTrue(AuditLog.objects.filter(action='create', affected_object='User: new_trainer').exists())

    def test_email_uniqueness_validation(self):
        # First register a user
        User.objects.create_user(username='existing_user', email='exist@test.com', password=self.password)
        # Register another with same email
        response = self.client.post(reverse('register'), {
            'username': 'another_user',
            'email': 'exist@test.com',
            'role': 'student',
            'password1': 'NewPass123!@#',
            'password2': 'NewPass123!@#',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'A user with this email address already exists.')

    def test_password_complexity_validation(self):
        # Too short
        response = self.client.post(reverse('register'), {
            'username': 'test_user',
            'email': 'test@test.com',
            'role': 'student',
            'password1': 'Pa1!@#',
            'password2': 'Pa1!@#',
        })
        self.assertEqual(response.status_code, 200)
        
        # No uppercase
        response = self.client.post(reverse('register'), {
            'username': 'test_user',
            'email': 'test@test.com',
            'role': 'student',
            'password1': 'pass123!@#',
            'password2': 'pass123!@#',
        })
        self.assertEqual(response.status_code, 200)

        # Matches username
        response = self.client.post(reverse('register'), {
            'username': 'MatchUser123!',
            'email': 'test@test.com',
            'role': 'student',
            'password1': 'MatchUser123!',
            'password2': 'MatchUser123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_protection_lockout(self):
        # Clear cache first to isolate test
        from django.core.cache import cache
        cache.clear()
        
        # Create user
        test_user = User.objects.create_user(username='locked_user', password=self.password)
        
        # Try to log in with wrong password 5 times
        for i in range(5):
            response = self.client.post(reverse('login'), {
                'username': 'locked_user',
                'password': 'wrongpassword'
            })
            
        # The 5th or 6th login attempt should say locked out
        response = self.client.post(reverse('login'), {
            'username': 'locked_user',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'temporarily blocked')
        
        # Successful login is also blocked
        response = self.client.post(reverse('login'), {
            'username': 'locked_user',
            'password': self.password
        })
        self.assertContains(response, 'temporarily blocked')
        
        # AuditLog should contain failed login logs
        self.assertTrue(AuditLog.objects.filter(action='failed_login', user=test_user).exists())

    def test_admin_toggle_user_status(self):
        # Log in as admin
        self.client.login(username='admin_user', password=self.password)
        
        # Toggle trainer status (active -> inactive)
        self.assertTrue(self.trainer_user.is_active)
        response = self.client.get(reverse('toggle_user_status', kwargs={'user_id': self.trainer_user.id}))
        self.assertRedirects(response, reverse('user_management'))
        
        self.trainer_user.refresh_from_db()
        self.assertFalse(self.trainer_user.is_active)
        
        # Audit log verification
        self.assertTrue(AuditLog.objects.filter(
            action='status_change',
            affected_object=f"User: {self.trainer_user.username}"
        ).exists())


class TaskThreeTests(TestCase):
    def setUp(self):
        self.password = 'ComplexPass123!'
        
        # Admin
        self.admin = User.objects.create_user(username='admin_user', password=self.password)
        self.admin.profile.role = 'admin'
        self.admin.profile.save()
        
        # Trainer 1 (Assigned)
        self.trainer1 = User.objects.create_user(username='trainer_one', password=self.password)
        self.trainer1.profile.role = 'trainer'
        self.trainer1.profile.save()
        
        # Trainer 2 (Unassigned)
        self.trainer2 = User.objects.create_user(username='trainer_two', password=self.password)
        self.trainer2.profile.role = 'trainer'
        self.trainer2.profile.save()
        
        # Student user
        self.student_user = User.objects.create_user(username='student_user', password=self.password)
        self.student_user.profile.role = 'student'
        self.student_user.profile.save()
        
        # Course
        self.course = Course.objects.create(
            course_name="Python Core", code="PY101", duration=6, assigned_trainer=self.trainer1
        )
        # Student model record
        self.student_record = Student.objects.create(
            name="Alice Student", email="alice@test.com", age=20, course="Python Core",
            marks=80, joined_date=timezone.localdate(), user=self.student_user
        )
        self.student_record.courses.add(self.course)

    def test_trainer_add_feedback_success(self):
        # Assigned trainer can add feedback
        self.client.login(username='trainer_one', password=self.password)
        response = self.client.post(reverse('add_feedback', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'rating': 5,
            'comments': 'Excellent performance in projects.',
            'is_visible': True
        })
        self.assertRedirects(response, reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.assertEqual(Feedback.objects.count(), 1)
        fb = Feedback.objects.first()
        self.assertEqual(fb.rating, 5)
        self.assertEqual(fb.trainer, self.trainer1)
        self.assertTrue(fb.is_visible)

    def test_trainer_add_feedback_unassigned(self):
        # Unassigned trainer cannot add feedback
        self.client.login(username='trainer_two', password=self.password)
        response = self.client.post(reverse('add_feedback', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'rating': 4,
            'comments': 'Good effort.',
            'is_visible': True
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Feedback.objects.count(), 0)

    def test_student_add_feedback_forbidden(self):
        # Student cannot add feedback
        self.client.login(username='student_user', password=self.password)
        response = self.client.post(reverse('add_feedback', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'rating': 3,
            'comments': 'Self-eval.',
            'is_visible': True
        })
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_add_feedback_redirect(self):
        response = self.client.get(reverse('add_feedback', kwargs={'student_id': self.student_record.id}))
        self.assertEqual(response.status_code, 302)

    def test_trainer_edit_own_feedback_success(self):
        fb = Feedback.objects.create(
            student=self.student_record, trainer=self.trainer1, course=self.course,
            rating=4, comments='Original comments', is_visible=True
        )
        self.client.login(username='trainer_one', password=self.password)
        response = self.client.post(reverse('edit_feedback', kwargs={'feedback_id': fb.id}), {
            'course': self.course.id,
            'rating': 5,
            'comments': 'Updated comments',
            'is_visible': False
        })
        self.assertRedirects(response, reverse('student_detail', kwargs={'id': self.student_record.id}))
        fb.refresh_from_db()
        self.assertEqual(fb.rating, 5)
        self.assertEqual(fb.comments, 'Updated comments')
        self.assertFalse(fb.is_visible)

    def test_trainer_edit_other_feedback_forbidden(self):
        fb = Feedback.objects.create(
            student=self.student_record, trainer=self.trainer1, course=self.course,
            rating=4, comments='Original', is_visible=True
        )
        self.client.login(username='trainer_two', password=self.password)
        response = self.client.post(reverse('edit_feedback', kwargs={'feedback_id': fb.id}), {
            'course': self.course.id,
            'rating': 5,
            'comments': 'Hacked',
            'is_visible': True
        })
        self.assertEqual(response.status_code, 403)
        fb.refresh_from_db()
        self.assertEqual(fb.rating, 4)

    def test_feedback_rating_validation_bounds(self):
        self.client.login(username='trainer_one', password=self.password)
        # Rating 6 is invalid (choices are 1-5)
        response = self.client.post(reverse('add_feedback', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'rating': 6,
            'comments': 'Out of bounds rating',
            'is_visible': True
        })
        self.assertEqual(response.status_code, 200) # Form errors
        self.assertFormError(response.context['form'], 'rating', 'Ensure this value is less than or equal to 5.')

    def test_student_view_visible_feedback(self):
        Feedback.objects.create(
            student=self.student_record, trainer=self.trainer1, course=self.course,
            rating=5, comments='Visible feedback', is_visible=True
        )
        self.client.login(username='student_user', password=self.password)
        response = self.client.get(reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visible feedback')

    def test_student_cannot_view_hidden_feedback(self):
        Feedback.objects.create(
            student=self.student_record, trainer=self.trainer1, course=self.course,
            rating=5, comments='Hidden feedback', is_visible=False
        )
        self.client.login(username='student_user', password=self.password)
        response = self.client.get(reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Hidden feedback')

    def test_admin_view_all_feedback(self):
        Feedback.objects.create(
            student=self.student_record, trainer=self.trainer1, course=self.course,
            rating=5, comments='Hidden feedback to student', is_visible=False
        )
        self.client.login(username='admin_user', password=self.password)
        response = self.client.get(reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hidden feedback to student')

    def test_trainer_update_marks_success(self):
        self.client.login(username='trainer_one', password=self.password)
        response = self.client.post(reverse('update_marks', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'new_marks': 95,
            'reason': 'Did outstanding on exams.'
        })
        self.assertRedirects(response, reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.student_record.refresh_from_db()
        self.assertEqual(self.student_record.marks, 95)
        
        # Verify MarksHistory entry
        self.assertEqual(MarksHistory.objects.count(), 1)
        history = MarksHistory.objects.first()
        self.assertEqual(history.previous_marks, 80)
        self.assertEqual(history.new_marks, 95)
        self.assertEqual(history.reason, 'Did outstanding on exams.')
        self.assertEqual(history.updater, self.trainer1)

    def test_trainer_update_marks_unassigned(self):
        self.client.login(username='trainer_two', password=self.password)
        response = self.client.post(reverse('update_marks', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'new_marks': 95,
            'reason': 'Hacker attempt'
        })
        self.assertEqual(response.status_code, 403)
        self.student_record.refresh_from_db()
        self.assertEqual(self.student_record.marks, 80)

    def test_student_update_marks_forbidden(self):
        self.client.login(username='student_user', password=self.password)
        response = self.client.post(reverse('update_marks', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'new_marks': 100,
            'reason': 'Self boost'
        })
        self.assertEqual(response.status_code, 403)

    def test_marks_update_validation_bounds(self):
        self.client.login(username='trainer_one', password=self.password)
        # Marks > 100 is invalid
        response = self.client.post(reverse('update_marks', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'new_marks': 105,
            'reason': 'Bonus points'
        })
        self.assertEqual(response.status_code, 200) # Form error
        self.assertFormError(response.context['form'], 'new_marks', 'Ensure this value is less than or equal to 100.')

    def test_marks_history_records_previous_new(self):
        self.client.login(username='trainer_one', password=self.password)
        self.client.post(reverse('update_marks', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'new_marks': 90,
            'reason': 'Regular update'
        })
        history = MarksHistory.objects.get(student=self.student_record)
        self.assertEqual(history.previous_marks, 80)
        self.assertEqual(history.new_marks, 90)

    def test_latest_updater_metadata_displayed(self):
        # Update marks
        MarksHistory.objects.create(
            student=self.student_record, course=self.course, previous_marks=80,
            new_marks=90, updater=self.trainer1, reason='Class improvement'
        )
        self.client.login(username='admin_user', password=self.password)
        response = self.client.get(reverse('student_detail', kwargs={'id': self.student_record.id}))
        self.assertContains(response, 'Latest update by')
        self.assertContains(response, 'trainer_one')

    def test_audit_log_created_on_feedback_creation(self):
        self.client.login(username='trainer_one', password=self.password)
        self.client.post(reverse('add_feedback', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'rating': 4,
            'comments': 'Decent',
            'is_visible': True
        })
        self.assertTrue(AuditLog.objects.filter(action='feedback_creation', user=self.trainer1).exists())

    def test_audit_log_created_on_marks_update(self):
        self.client.login(username='trainer_one', password=self.password)
        self.client.post(reverse('update_marks', kwargs={'student_id': self.student_record.id}), {
            'course': self.course.id,
            'new_marks': 85,
            'reason': 'Exam review'
        })
        self.assertTrue(AuditLog.objects.filter(action='marks_update', user=self.trainer1).exists())

    def test_audit_log_created_on_student_creation(self):
        self.client.login(username='admin_user', password=self.password)
        self.client.post(reverse('add_student'), {
            'name': 'New Student Audit',
            'email': 'newaudit@test.com',
            'age': 20,
            'course': 'Python Core',
            'marks': 75,
            'joined_date': '2026-08-01',
            'active_status': True
        })
        self.assertTrue(AuditLog.objects.filter(action='create', affected_object='Student: New Student Audit').exists())

    def test_audit_log_created_on_student_deletion(self):
        self.client.login(username='admin_user', password=self.password)
        self.client.post(reverse('delete_student', kwargs={'id': self.student_record.id}))
        self.assertTrue(AuditLog.objects.filter(action='delete', affected_object='Student: Alice Student').exists())

    def test_audit_log_admin_only(self):
        # Student gets 403
        self.client.login(username='student_user', password=self.password)
        response = self.client.get(reverse('audit_logs'))
        self.assertEqual(response.status_code, 403)
        
        # Trainer gets 403
        self.client.login(username='trainer_one', password=self.password)
        response = self.client.get(reverse('audit_logs'))
        self.assertEqual(response.status_code, 403)
        
        # Admin gets 200
        self.client.login(username='admin_user', password=self.password)
        response = self.client.get(reverse('audit_logs'))
        self.assertEqual(response.status_code, 200)

    def test_audit_log_filters_search_pagination(self):
        # Create a few audit logs
        AuditLog.objects.create(user=self.admin, action='create', description='Admin created a resource')
        AuditLog.objects.create(user=self.trainer1, action='marks_update', description='Trainer updated marks')
        
        self.client.login(username='admin_user', password=self.password)
        response = self.client.get(reverse('audit_logs'), {'q': 'resource'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin created a resource')
        self.assertNotContains(response, 'Trainer updated marks')
        
        # Test action filter
        response = self.client.get(reverse('audit_logs'), {'action_type': 'marks_update'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Trainer updated marks')
        self.assertNotContains(response, 'Admin created a resource')


class ServiceLayerTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Computer Science", description="CS Dept")
        self.admin = User.objects.create_user(username="srv_admin", password="password123")
        self.admin.profile.role = 'admin'
        self.admin.profile.save()

        self.trainer = User.objects.create_user(username="srv_trainer", password="password123")
        self.trainer.profile.role = 'trainer'
        self.trainer.profile.save()

        self.student_user = User.objects.create_user(username="srv_student", password="password123")
        self.student_user.profile.role = 'student'
        self.student_user.profile.save()

        self.course = Course.objects.create(
            course_name="Data Structures",
            code="CS201",
            duration=12,
            assigned_trainer=self.trainer
        )

        self.student = Student.objects.create(
            user=self.student_user,
            name="Service Student",
            email="service@test.com",
            age=22,
            marks=70,
            joined_date=timezone.localdate(),
            department=self.dept
        )
        self.student.courses.add(self.course)

    def test_update_student_marks_service(self):
        updated_student, history = services.update_student_marks(
            student=self.student,
            course=self.course,
            new_marks=95,
            updater_user=self.trainer,
            reason="Excellent exam performance",
            ip_address="127.0.0.1"
        )
        self.assertEqual(updated_student.marks, 95)
        self.assertEqual(history.previous_marks, 70)
        self.assertEqual(history.new_marks, 95)
        self.assertEqual(history.updater, self.trainer)
        self.assertTrue(AuditLog.objects.filter(action='marks_update', user=self.trainer).exists())

    def test_create_feedback_service(self):
        feedback = services.create_feedback(
            student=self.student,
            trainer_user=self.trainer,
            course=self.course,
            rating=5,
            comments="Outstanding progress!",
            is_visible=True,
            ip_address="127.0.0.1"
        )
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.comments, "Outstanding progress!")
        self.assertEqual(feedback.trainer, self.trainer)
        self.assertTrue(AuditLog.objects.filter(action='feedback_creation', user=self.trainer).exists())

    def test_get_trainer_dashboard_stats_service(self):
        data = services.get_trainer_dashboard_stats(self.trainer)
        self.assertEqual(data['stats']['total_courses'], 1)
        self.assertEqual(data['stats']['total_students'], 1)
        self.assertEqual(data['stats']['avg_marks'], 70.0)

    def test_get_student_dashboard_data_service(self):
        data = services.get_student_dashboard_data(self.student_user)
        self.assertEqual(data['student'], self.student)
        self.assertEqual(list(data['courses']), [self.course])

    def test_permission_helpers_service(self):
        # View permissions
        self.assertTrue(services.can_user_view_student(self.admin, self.student))
        self.assertTrue(services.can_user_view_student(self.trainer, self.student))
        self.assertTrue(services.can_user_view_student(self.student_user, self.student))

        other_student_user = User.objects.create_user(username="other_student", password="password123")
        other_student_user.profile.role = 'student'
        other_student_user.profile.save()
        self.assertFalse(services.can_user_view_student(other_student_user, self.student))

        # Edit permissions
        self.assertTrue(services.can_user_edit_student(self.admin, self.student))
        self.assertTrue(services.can_user_edit_student(self.trainer, self.student))
        self.assertFalse(services.can_user_edit_student(self.student_user, self.student))

