from decimal import Decimal

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from . import reports, services
from .forms import RegisterForm, StudentForm, TrainerRegisterForm
from .models import (
    AuditLog,
    Course,
    Department,
    Feedback,
    MarksHistory,
    Student,
    StudentProfile,
    UserProfile,
)
from .security import MAX_ATTEMPTS, is_locked_out, register_failed_attempt, reset_attempts


def make_user(username, role, password='TesterPass123', **extra):
    """Create a user and immediately set their role (the post_save signal
    gives every new user a default 'student' UserProfile first)."""
    user = User.objects.create_user(username=username, password=password, **extra)
    user.profile.role = role
    user.profile.save()
    return user


class BaseAuthenticatedTestCase(TestCase):
    """Shared setup: a logged-in Administrator plus some reference data."""

    def setUp(self):
        self.user = make_user('tester', UserProfile.ROLE_ADMIN)
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

    def test_trainer_cannot_add_student(self):
        make_user('trainer1', UserProfile.ROLE_TRAINER)
        self.client.logout()
        self.client.login(username='trainer1', password='TesterPass123')
        response = self.client.get(reverse('add_student'))
        self.assertEqual(response.status_code, 403)


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

    def test_admin_user_can_delete(self):
        response = self.client.post(reverse('delete_student', args=[self.student.pk]))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_non_admin_user_cannot_delete(self):
        make_user('regular', UserProfile.ROLE_STUDENT)
        self.client.logout()
        self.client.login(username='regular', password='TesterPass123')
        response = self.client.post(reverse('delete_student', args=[self.student.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())


# ---------------------------------------------------------------------------
# Task 4 - Authentication & role-based access
# ---------------------------------------------------------------------------

class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = make_user('authuser', UserProfile.ROLE_STUDENT)

    def test_login_page_loads(self):
        """7. Login page."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_successful_login_redirects_to_dispatcher(self):
        """8. Successful login sends the user to the role dispatcher, which
        then forwards a student to their own dashboard."""
        response = self.client.post(reverse('login'), {
            'username': 'authuser', 'password': 'TesterPass123',
        })
        self.assertRedirects(
            response, reverse('post_login_redirect'),
            target_status_code=302, fetch_redirect_response=False,
        )

    def test_protected_page_redirects_anonymous_user(self):
        """9. Protected page redirect."""
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_register_creates_student_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertRedirects(
            response, reverse('post_login_redirect'),
            target_status_code=302, fetch_redirect_response=False,
        )
        new_user = User.objects.get(username='newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(new_user.profile.role, UserProfile.ROLE_STUDENT)

    def test_logout_redirects_to_login(self):
        self.client.login(username='authuser', password='TesterPass123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


class RoleBasedDashboardTests(TestCase):
    """Each role gets its own dashboard, and cannot access another role's."""

    def setUp(self):
        self.admin = make_user('roleadmin', UserProfile.ROLE_ADMIN)
        self.trainer = make_user('roletrainer', UserProfile.ROLE_TRAINER)
        self.student_user = make_user('rolestudent', UserProfile.ROLE_STUDENT)

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(username='roleadmin', password='TesterPass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_trainer_cannot_access_admin_dashboard(self):
        self.client.login(username='roletrainer', password='TesterPass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_student_cannot_access_trainer_dashboard(self):
        self.client.login(username='rolestudent', password='TesterPass123')
        response = self.client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_student_can_access_own_dashboard(self):
        self.client.login(username='rolestudent', password='TesterPass123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)


class StudentOwnershipTests(TestCase):
    """A student may only view their own record, even if they know another
    student's primary key."""

    def setUp(self):
        self.department = Department.objects.create(name="Business")
        self.owner_user = make_user('owner', UserProfile.ROLE_STUDENT)
        self.other_user = make_user('other', UserProfile.ROLE_STUDENT)

        self.owner_student = Student.objects.create(
            name="Owner Student", email="owner@example.com", age=20, marks=60,
            department=self.department, user=self.owner_user,
        )
        self.other_student = Student.objects.create(
            name="Other Student", email="other@example.com", age=21, marks=70,
            department=self.department, user=self.other_user,
        )

    def test_student_can_view_own_record(self):
        self.client.login(username='owner', password='TesterPass123')
        response = self.client.get(reverse('student_detail', args=[self.owner_student.pk]))
        self.assertEqual(response.status_code, 200)

    def test_student_cannot_view_other_student_record(self):
        self.client.login(username='owner', password='TesterPass123')
        response = self.client.get(reverse('student_detail', args=[self.other_student.pk]))
        self.assertEqual(response.status_code, 403)


class TrainerOwnershipTests(TestCase):
    """A trainer may only see/update students enrolled in their own courses."""

    def setUp(self):
        self.trainer = make_user('trainer_owner', UserProfile.ROLE_TRAINER)
        self.other_trainer = make_user('trainer_other', UserProfile.ROLE_TRAINER)

        self.course = Course.objects.create(name="Data Science", code="DS101", trainer=self.trainer)
        self.other_course = Course.objects.create(
            name="UX Basics", code="UX101", trainer=self.other_trainer
        )

        self.student = Student.objects.create(
            name="Trainee One", email="trainee1@example.com", age=20, marks=55,
        )
        self.student.courses.add(self.course)

        self.other_student = Student.objects.create(
            name="Trainee Two", email="trainee2@example.com", age=22, marks=65,
        )
        self.other_student.courses.add(self.other_course)

    def test_trainer_can_view_own_student(self):
        self.client.login(username='trainer_owner', password='TesterPass123')
        response = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertEqual(response.status_code, 200)

    def test_trainer_cannot_view_other_trainers_student(self):
        self.client.login(username='trainer_owner', password='TesterPass123')
        response = self.client.get(reverse('student_detail', args=[self.other_student.pk]))
        self.assertEqual(response.status_code, 403)

    def test_trainer_can_update_marks_for_own_student(self):
        self.client.login(username='trainer_owner', password='TesterPass123')
        response = self.client.post(
            reverse('update_marks', args=[self.student.pk]), {"marks": 90, "reason": "Resit exam"}
        )
        self.assertRedirects(response, reverse('student_detail', args=[self.student.pk]))
        self.student.refresh_from_db()
        self.assertEqual(self.student.marks, 90)

    def test_trainer_cannot_update_marks_for_other_students(self):
        self.client.login(username='trainer_owner', password='TesterPass123')
        response = self.client.post(
            reverse('update_marks', args=[self.other_student.pk]), {"marks": 90}
        )
        self.assertEqual(response.status_code, 403)

    def test_student_list_scoped_to_trainer(self):
        self.client.login(username='trainer_owner', password='TesterPass123')
        response = self.client.get(reverse('student_list'))
        self.assertContains(response, "Trainee One")
        self.assertNotContains(response, "Trainee Two")


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

    def test_every_user_gets_a_profile(self):
        """The post_save signal should give every new User a UserProfile
        with the default 'student' role."""
        user = User.objects.create_user(username="plainuser", password="x")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.role, UserProfile.ROLE_STUDENT)

    def test_feedback_visible_only_when_flagged(self):
        trainer = make_user('fbtrainer', UserProfile.ROLE_TRAINER)
        course = Course.objects.create(name="Feedback Course", code="FB101", trainer=trainer)
        self.student.courses.add(course)
        Feedback.objects.create(
            student=self.student, course=course, trainer=trainer,
            rating=4, comment="Great progress!", is_visible_to_student=False,
        )
        visible = Feedback.objects.filter(student=self.student, is_visible_to_student=True)
        self.assertEqual(visible.count(), 0)


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
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['total_departments'], 1)
        self.assertEqual(response.context['total_courses'], 1)
        self.assertEqual(response.context['top_student'].name, "High Scorer")

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('admin_dashboard'))
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


# ---------------------------------------------------------------------------
# Task 2/3 - Account security, audit log, feedback, marks history, ORM
# ---------------------------------------------------------------------------

class PasswordValidationTests(TestCase):
    """29 (part). Password and registration validation work."""

    def test_registration_rejects_weak_password(self):
        form = RegisterForm(data={
            'username': 'weakpw', 'email': 'weakpw@example.com',
            'password1': 'password123', 'password2': 'password123',
        })
        self.assertFalse(form.is_valid())

    def test_registration_rejects_password_missing_special_character(self):
        form = RegisterForm(data={
            'username': 'nospecial', 'email': 'nospecial@example.com',
            'password1': 'ComplexPass123', 'password2': 'ComplexPass123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_registration_accepts_strong_password(self):
        form = RegisterForm(data={
            'username': 'stronguser', 'email': 'stronguser@example.com',
            'password1': 'ComplexPass123!', 'password2': 'ComplexPass123!',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(username='existing', email='dup@example.com', password='Whatever123!')
        form = RegisterForm(data={
            'username': 'newperson', 'email': 'dup@example.com',
            'password1': 'ComplexPass123!', 'password2': 'ComplexPass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_rejects_password_matching_username(self):
        form = RegisterForm(data={
            'username': 'sameuser1', 'email': 'sameuser1@example.com',
            'password1': 'sameuser1', 'password2': 'sameuser1',
        })
        self.assertFalse(form.is_valid())


class TrainerApprovalTests(TestCase):
    """Trainer accounts require administrator approval before they can use
    the trainer dashboard or touch marks/feedback."""

    def setUp(self):
        self.admin = make_user('approvaladmin', UserProfile.ROLE_ADMIN)

    def test_trainer_registration_creates_unapproved_account(self):
        response = self.client.post(reverse('trainer_register'), {
            'username': 'newtrainer', 'email': 'newtrainer@example.com',
            'password1': 'ComplexPass123!', 'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newtrainer')
        self.assertEqual(user.profile.role, UserProfile.ROLE_TRAINER)
        self.assertFalse(user.profile.is_approved)

    def test_unapproved_trainer_sees_pending_page_not_dashboard(self):
        trainer = make_user('pendingtrainer', UserProfile.ROLE_TRAINER)
        trainer.profile.is_approved = False
        trainer.profile.save()
        self.client.login(username='pendingtrainer', password='TesterPass123')
        response = self.client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboards/pending_approval.html')

    def test_unapproved_trainer_cannot_update_marks(self):
        trainer = make_user('pendingtrainer2', UserProfile.ROLE_TRAINER)
        trainer.profile.is_approved = False
        trainer.profile.save()
        course = Course.objects.create(name="Course X", code="CX101", trainer=trainer)
        student = Student.objects.create(name="S1", email="s1@example.com", age=20, marks=50)
        student.courses.add(course)

        self.client.login(username='pendingtrainer2', password='TesterPass123')
        response = self.client.post(reverse('update_marks', args=[student.pk]), {"marks": 80, "reason": "x"})
        self.assertEqual(response.status_code, 403)

    def test_admin_can_approve_trainer(self):
        trainer = make_user('toapprove', UserProfile.ROLE_TRAINER)
        trainer.profile.is_approved = False
        trainer.profile.save()

        self.client.login(username='approvaladmin', password='TesterPass123')
        response = self.client.post(reverse('approve_trainer', args=[trainer.profile.pk]))
        self.assertRedirects(response, reverse('manage_users'))
        trainer.profile.refresh_from_db()
        self.assertTrue(trainer.profile.is_approved)

    def test_non_admin_cannot_approve_trainer(self):
        trainer = make_user('cantapprove', UserProfile.ROLE_TRAINER)
        trainer.profile.is_approved = False
        trainer.profile.save()
        other_trainer = make_user('someothertrainer', UserProfile.ROLE_TRAINER)

        self.client.login(username='someothertrainer', password='TesterPass123')
        response = self.client.post(reverse('approve_trainer', args=[trainer.profile.pk]))
        self.assertEqual(response.status_code, 403)


class AccountActivationTests(TestCase):
    """Administrator-controlled account activation/deactivation."""

    def setUp(self):
        self.admin = make_user('activationadmin', UserProfile.ROLE_ADMIN)
        self.target = make_user('deactivateme', UserProfile.ROLE_STUDENT)

    def test_admin_can_deactivate_user(self):
        self.client.login(username='activationadmin', password='TesterPass123')
        response = self.client.post(reverse('toggle_user_active', args=[self.target.pk]))
        self.assertRedirects(response, reverse('manage_users'))
        self.target.refresh_from_db()
        self.assertFalse(self.target.is_active)

    def test_deactivated_user_cannot_log_in(self):
        self.target.is_active = False
        self.target.save()
        logged_in = self.client.login(username='deactivateme', password='TesterPass123')
        self.assertFalse(logged_in)

    def test_admin_cannot_deactivate_own_account(self):
        self.client.login(username='activationadmin', password='TesterPass123')
        response = self.client.post(reverse('toggle_user_active', args=[self.admin.pk]))
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_non_admin_cannot_toggle_activation(self):
        self.client.login(username='deactivateme', password='TesterPass123')
        response = self.client.post(reverse('toggle_user_active', args=[self.admin.pk]))
        self.assertEqual(response.status_code, 403)


class FailedLoginLockoutTests(TestCase):
    """8-11. Failed login attempts are tracked, the account is temporarily
    blocked after five failures, a clear alert is shown, and each event is
    recorded in the audit log."""

    def setUp(self):
        self.user = make_user('lockoutuser', UserProfile.ROLE_STUDENT, password='RealPass123!')
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_failed_attempts_are_tracked(self):
        self.assertFalse(is_locked_out('lockoutuser'))
        for _ in range(MAX_ATTEMPTS - 1):
            register_failed_attempt('lockoutuser')
        self.assertFalse(is_locked_out('lockoutuser'))
        register_failed_attempt('lockoutuser')
        self.assertTrue(is_locked_out('lockoutuser'))

    def test_login_blocked_after_five_failed_attempts(self):
        for _ in range(5):
            self.client.post(reverse('login'), {'username': 'lockoutuser', 'password': 'WrongPass!'})

        response = self.client.post(reverse('login'), {'username': 'lockoutuser', 'password': 'RealPass123!'})
        # Even the *correct* password is rejected while locked out.
        self.assertContains(response, "temporarily locked")

    def test_failed_logins_are_recorded_in_audit_log(self):
        self.client.post(reverse('login'), {'username': 'lockoutuser', 'password': 'WrongPass!'})
        self.assertTrue(
            AuditLog.objects.filter(action_type=AuditLog.ACTION_LOGIN_FAILED, username='lockoutuser').exists()
        )

    def test_successful_login_resets_counter(self):
        register_failed_attempt('lockoutuser')
        register_failed_attempt('lockoutuser')
        self.client.post(reverse('login'), {'username': 'lockoutuser', 'password': 'RealPass123!'})
        self.assertFalse(is_locked_out('lockoutuser'))

    def test_successful_login_is_recorded_in_audit_log(self):
        self.client.post(reverse('login'), {'username': 'lockoutuser', 'password': 'RealPass123!'})
        self.assertTrue(
            AuditLog.objects.filter(action_type=AuditLog.ACTION_LOGIN, user=self.user).exists()
        )

    def test_logout_is_recorded_in_audit_log(self):
        self.client.login(username='lockoutuser', password='RealPass123!')
        self.client.post(reverse('logout'))
        self.assertTrue(
            AuditLog.objects.filter(action_type=AuditLog.ACTION_LOGOUT, user=self.user).exists()
        )


class AuditLogViewTests(TestCase):
    """Only administrators may view the audit log; it supports filters and
    pagination."""

    def setUp(self):
        self.admin = make_user('auditadmin', UserProfile.ROLE_ADMIN)
        self.student = make_user('auditstudent', UserProfile.ROLE_STUDENT)
        AuditLog.objects.create(
            user=self.admin, username='auditadmin', action_type=AuditLog.ACTION_CREATE,
            description="Created something", object_repr="Thing: X",
        )

    def test_admin_can_view_audit_log(self):
        self.client.login(username='auditadmin', password='TesterPass123')
        response = self.client.get(reverse('audit_log'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Created something")

    def test_student_cannot_view_audit_log(self):
        self.client.login(username='auditstudent', password='TesterPass123')
        response = self.client.get(reverse('audit_log'))
        self.assertEqual(response.status_code, 403)

    def test_audit_log_filters_by_action_type(self):
        AuditLog.objects.create(
            user=self.admin, username='auditadmin', action_type=AuditLog.ACTION_DELETE,
            description="Deleted something",
        )
        self.client.login(username='auditadmin', password='TesterPass123')
        response = self.client.get(reverse('audit_log'), {'action_type': AuditLog.ACTION_DELETE})
        self.assertContains(response, "Deleted something")
        self.assertNotContains(response, "Created something")


class FeedbackWorkflowTests(TestCase):
    """Trainers add feedback only for assigned students and can edit only
    their own; students see only feedback marked visible; admins see all;
    ratings must be 1-5."""

    def setUp(self):
        self.trainer = make_user('fb_trainer', UserProfile.ROLE_TRAINER)
        self.other_trainer = make_user('fb_other_trainer', UserProfile.ROLE_TRAINER)
        self.course = Course.objects.create(name="FB Course", code="FBC101", trainer=self.trainer)
        self.student_user = make_user('fb_student', UserProfile.ROLE_STUDENT)
        self.student = Student.objects.create(
            name="FB Student", email="fbstudent@example.com", age=20, marks=60, user=self.student_user,
        )
        self.student.courses.add(self.course)

    def test_trainer_can_add_feedback_for_assigned_student(self):
        self.client.login(username='fb_trainer', password='TesterPass123')
        response = self.client.post(reverse('add_feedback', args=[self.student.pk]), {
            'course': self.course.id, 'rating': 4, 'comment': 'Doing well.', 'is_visible_to_student': 'on',
        })
        self.assertRedirects(response, reverse('student_detail', args=[self.student.pk]))
        self.assertTrue(Feedback.objects.filter(student=self.student, trainer=self.trainer).exists())

    def test_trainer_cannot_add_feedback_for_unassigned_student(self):
        other_student = Student.objects.create(name="Other", email="other_fb@example.com", age=21, marks=55)
        self.client.login(username='fb_trainer', password='TesterPass123')
        response = self.client.post(reverse('add_feedback', args=[other_student.pk]), {
            'course': self.course.id, 'rating': 3, 'comment': 'x', 'is_visible_to_student': 'on',
        })
        self.assertEqual(response.status_code, 403)

    def test_rating_must_be_between_1_and_5(self):
        self.client.login(username='fb_trainer', password='TesterPass123')
        response = self.client.post(reverse('add_feedback', args=[self.student.pk]), {
            'course': self.course.id, 'rating': 9, 'comment': 'x', 'is_visible_to_student': 'on',
        })
        self.assertEqual(response.status_code, 200)  # form re-rendered with errors
        self.assertFalse(Feedback.objects.filter(student=self.student).exists())

    def test_trainer_can_edit_own_feedback(self):
        feedback = Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=3, comment="Initial", is_visible_to_student=True,
        )
        self.client.login(username='fb_trainer', password='TesterPass123')
        response = self.client.post(reverse('edit_feedback', args=[feedback.pk]), {
            'course': self.course.id, 'rating': 5, 'comment': 'Updated', 'is_visible_to_student': 'on',
        })
        self.assertRedirects(response, reverse('student_detail', args=[self.student.pk]))
        feedback.refresh_from_db()
        self.assertEqual(feedback.comment, 'Updated')
        self.assertEqual(feedback.rating, 5)

    def test_trainer_cannot_edit_other_trainers_feedback(self):
        feedback = Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=3, comment="Initial", is_visible_to_student=True,
        )
        self.client.login(username='fb_other_trainer', password='TesterPass123')
        response = self.client.post(reverse('edit_feedback', args=[feedback.pk]), {
            'course': self.course.id, 'rating': 1, 'comment': 'Hijacked', 'is_visible_to_student': 'on',
        })
        self.assertEqual(response.status_code, 403)

    def test_student_sees_only_visible_feedback(self):
        Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=5, comment="Visible one", is_visible_to_student=True,
        )
        Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=2, comment="Draft one", is_visible_to_student=False,
        )
        self.client.login(username='fb_student', password='TesterPass123')
        response = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertContains(response, "Visible one")
        self.assertNotContains(response, "Draft one")

    def test_admin_sees_all_feedback(self):
        admin = make_user('fb_admin', UserProfile.ROLE_ADMIN)
        Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=5, comment="Visible one", is_visible_to_student=True,
        )
        Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=2, comment="Draft one", is_visible_to_student=False,
        )
        self.client.login(username='fb_admin', password='TesterPass123')
        response = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertContains(response, "Visible one")
        self.assertContains(response, "Draft one")


class MarksHistoryWorkflowTests(TestCase):
    """Only an assigned trainer may update marks; every change is recorded
    with old/new value, updater, date, and reason; students are blocked
    from updating marks even via a direct POST."""

    def setUp(self):
        self.trainer = make_user('mh_trainer', UserProfile.ROLE_TRAINER)
        self.course = Course.objects.create(name="MH Course", code="MHC101", trainer=self.trainer)
        self.student = Student.objects.create(name="MH Student", email="mhstudent@example.com", age=20, marks=40)
        self.student.courses.add(self.course)
        self.student_user = make_user('mh_studentuser', UserProfile.ROLE_STUDENT)

    def test_marks_update_creates_history_record(self):
        self.client.login(username='mh_trainer', password='TesterPass123')
        self.client.post(reverse('update_marks', args=[self.student.pk]), {
            'marks': 75, 'reason': 'Resit exam',
        })
        history = MarksHistory.objects.get(student=self.student)
        self.assertEqual(history.old_marks, Decimal('40.00'))
        self.assertEqual(history.new_marks, Decimal('75.00'))
        self.assertEqual(history.updated_by, self.trainer)
        self.assertEqual(history.reason, 'Resit exam')

    def test_marks_update_creates_audit_log_entry(self):
        self.client.login(username='mh_trainer', password='TesterPass123')
        self.client.post(reverse('update_marks', args=[self.student.pk]), {
            'marks': 75, 'reason': 'Resit exam',
        })
        self.assertTrue(
            AuditLog.objects.filter(action_type=AuditLog.ACTION_MARKS_UPDATE, user=self.trainer).exists()
        )

    def test_marks_update_requires_a_reason(self):
        self.client.login(username='mh_trainer', password='TesterPass123')
        response = self.client.post(reverse('update_marks', args=[self.student.pk]), {'marks': 75})
        self.assertEqual(response.status_code, 200)  # form re-rendered with errors
        self.student.refresh_from_db()
        self.assertEqual(self.student.marks, Decimal('40.00'))

    def test_student_direct_post_to_update_marks_is_blocked(self):
        """27. Unauthorized direct POST requests return an appropriate error."""
        self.client.login(username='mh_studentuser', password='TesterPass123')
        response = self.client.post(reverse('update_marks', args=[self.student.pk]), {
            'marks': 100, 'reason': 'Trying to cheat',
        })
        self.assertEqual(response.status_code, 403)
        self.student.refresh_from_db()
        self.assertEqual(self.student.marks, Decimal('40.00'))

    def test_anonymous_direct_post_to_update_marks_redirects_to_login(self):
        response = self.client.post(reverse('update_marks', args=[self.student.pk]), {
            'marks': 100, 'reason': 'Trying to cheat',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)


class ORMReportTests(TestCase):
    """13-22. Sanity checks for the ORM challenge helper functions."""

    def setUp(self):
        self.trainer = make_user('orm_trainer', UserProfile.ROLE_TRAINER)
        self.idle_trainer = make_user('orm_idle_trainer', UserProfile.ROLE_TRAINER)
        self.course = Course.objects.create(name="ORM Course", code="ORM101", trainer=self.trainer)
        self.low_course = Course.objects.create(name="Low Course", code="LOW101", trainer=self.trainer)

        self.student_a = Student.objects.create(name="ORM A", email="orma@example.com", age=20, marks=80)
        self.student_a.courses.add(self.course)
        self.student_b = Student.objects.create(name="ORM B", email="ormb@example.com", age=21, marks=30)
        self.student_b.courses.add(self.low_course)

        Feedback.objects.create(
            student=self.student_a, course=self.course, trainer=self.trainer,
            rating=5, comment="Great", is_visible_to_student=True,
        )

        for _ in range(4):
            AuditLog.objects.create(username='bruteforcer', action_type=AuditLog.ACTION_LOGIN_FAILED, description="fail")

        MarksHistory.objects.create(
            student=self.student_a, course=self.course, old_marks=70, new_marks=80,
            updated_by=self.trainer, reason="Improved",
        )

        self.inactive_user = User.objects.create_user(username='wasactive', password='Whatever123!')
        self.inactive_user.last_login = self.inactive_user.date_joined
        self.inactive_user.is_active = False
        self.inactive_user.save()

    def test_trainer_student_counts(self):
        counts = {row.user.username: row.student_count for row in reports.trainer_student_counts()}
        self.assertEqual(counts['orm_trainer'], 2)
        self.assertEqual(counts['orm_idle_trainer'], 0)

    def test_students_with_no_visible_feedback(self):
        names = {s.name for s in reports.students_with_no_visible_feedback()}
        self.assertIn("ORM B", names)
        self.assertNotIn("ORM A", names)

    def test_trainers_without_feedback(self):
        usernames = {p.user.username for p in reports.trainers_without_feedback()}
        self.assertIn('orm_idle_trainer', usernames)
        self.assertNotIn('orm_trainer', usernames)

    def test_latest_audit_actions_limit(self):
        self.assertLessEqual(len(list(reports.latest_audit_actions(limit=5))), 5)

    def test_users_with_excess_failed_logins(self):
        rows = list(reports.users_with_excess_failed_logins(threshold=3))
        usernames = {row['username'] for row in rows}
        self.assertIn('bruteforcer', usernames)

    def test_marks_updated_this_week(self):
        self.assertEqual(reports.marks_updated_this_week().count(), 1)

    def test_average_rating_by_trainer(self):
        row = reports.average_rating_by_trainer().get(user__username='orm_trainer')
        self.assertEqual(row.average_rating, 5)

    def test_courses_below_average_marks(self):
        codes = {c.code for c in reports.courses_below_average_marks(threshold=50)}
        self.assertIn('LOW101', codes)
        self.assertNotIn('ORM101', codes)

    def test_inactive_users_who_previously_logged_in(self):
        usernames = {u.username for u in reports.inactive_users_who_previously_logged_in()}
        self.assertIn('wasactive', usernames)

    def test_enrolled_students_with_no_marks(self):
        never_graded = Student.objects.create(name="Never Graded", email="ng@example.com", age=19, marks=0)
        never_graded.courses.add(self.course)
        names = {s.name for s in reports.enrolled_students_with_no_marks()}
        self.assertIn("Never Graded", names)
        self.assertNotIn("ORM A", names)


class MobileTemplateRenderTests(TestCase):
    """31. Templates extend base.html and render without errors (a stand-in
    for checking they render correctly at mobile widths, since Bootstrap's
    responsive grid classes are what's actually doing that work -- this
    test just confirms the markup itself is present and valid)."""

    def setUp(self):
        self.admin = make_user('mobileadmin', UserProfile.ROLE_ADMIN)
        self.client.login(username='mobileadmin', password='TesterPass123')

    def test_pages_include_viewport_meta_and_bootstrap(self):
        for url_name in ['admin_dashboard', 'student_list', 'manage_users', 'audit_log', 'reports']:
            response = self.client.get(reverse(url_name))
            self.assertContains(response, 'name="viewport"')
            self.assertContains(response, 'bootstrap')


# ---------------------------------------------------------------------------
# Day 5, Task 2 - Service layer tests
#
# These call students/services.py functions directly, with plain Python
# arguments -- no HttpRequest, no test client, no rendered template. That's
# the point: the service layer is reusable by anything (a view, a future
# API endpoint, a management command) so it should be testable the same way.
# ---------------------------------------------------------------------------

class MarksServiceTests(TestCase):

    def setUp(self):
        self.trainer = make_user('svc_trainer', UserProfile.ROLE_TRAINER)
        self.other_trainer = make_user('svc_other_trainer', UserProfile.ROLE_TRAINER)
        self.course = Course.objects.create(name="Service Course", code="SVC101", trainer=self.trainer)
        self.student = Student.objects.create(
            name="Service Student", email="svc_student@example.com", age=20, marks=50,
        )
        self.student.courses.add(self.course)

    def test_update_student_marks_success(self):
        updated = services.update_student_marks(
            student=self.student, trainer_user=self.trainer, new_marks=88, reason="Resit",
        )
        self.assertEqual(updated.marks, 88)
        self.assertTrue(MarksHistory.objects.filter(student=self.student, new_marks=88).exists())
        self.assertTrue(
            AuditLog.objects.filter(action_type=AuditLog.ACTION_MARKS_UPDATE, object_repr__contains="Service Student").exists()
        )

    def test_update_student_marks_rejects_non_owning_trainer(self):
        from django.core.exceptions import PermissionDenied
        with self.assertRaises(PermissionDenied):
            services.update_student_marks(
                student=self.student, trainer_user=self.other_trainer, new_marks=88, reason="Resit",
            )

    def test_update_student_marks_rejects_out_of_range(self):
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            services.update_student_marks(
                student=self.student, trainer_user=self.trainer, new_marks=150, reason="Oops",
            )

    def test_update_student_marks_requires_reason(self):
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            services.update_student_marks(
                student=self.student, trainer_user=self.trainer, new_marks=70, reason="   ",
            )

    def test_marks_history_records_old_and_new_values(self):
        services.update_student_marks(
            student=self.student, trainer_user=self.trainer, new_marks=99, reason="Great work",
        )
        entry = MarksHistory.objects.filter(student=self.student).latest('updated_at')
        self.assertEqual(entry.old_marks, Decimal('50.00'))
        self.assertEqual(entry.new_marks, Decimal('99.00'))
        self.assertEqual(entry.updated_by, self.trainer)


class FeedbackServiceTests(TestCase):

    def setUp(self):
        self.trainer = make_user('fb_svc_trainer', UserProfile.ROLE_TRAINER)
        self.other_trainer = make_user('fb_svc_other', UserProfile.ROLE_TRAINER)
        self.course = Course.objects.create(name="Feedback Service Course", code="FBS101", trainer=self.trainer)
        self.other_course = Course.objects.create(name="Other Course", code="FBS102", trainer=self.other_trainer)
        self.student = Student.objects.create(
            name="FB Service Student", email="fbsvc@example.com", age=21, marks=60,
        )
        self.student.courses.add(self.course)

    def test_create_feedback_success(self):
        feedback = services.create_feedback(
            student=self.student, trainer_user=self.trainer, course=self.course,
            rating=5, comment="Excellent!",
        )
        self.assertEqual(feedback.rating, 5)
        self.assertTrue(AuditLog.objects.filter(action_type=AuditLog.ACTION_FEEDBACK).exists())

    def test_create_feedback_rejects_non_owning_trainer(self):
        from django.core.exceptions import PermissionDenied
        with self.assertRaises(PermissionDenied):
            services.create_feedback(
                student=self.student, trainer_user=self.other_trainer, course=self.course,
                rating=5, comment="Should fail",
            )

    def test_create_feedback_rejects_out_of_range_rating(self):
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            services.create_feedback(
                student=self.student, trainer_user=self.trainer, course=self.course,
                rating=9, comment="Invalid rating",
            )

    def test_visible_feedback_for_student_only_shows_visible(self):
        Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=3, comment="Draft", is_visible_to_student=False,
        )
        Feedback.objects.create(
            student=self.student, course=self.course, trainer=self.trainer,
            rating=4, comment="Published", is_visible_to_student=True,
        )
        visible = services.visible_feedback_for(self.student, viewer_role=UserProfile.ROLE_STUDENT)
        self.assertEqual(visible.count(), 1)
        self.assertEqual(visible.first().comment, "Published")

    def test_dashboard_totals_matches_direct_queries(self):
        totals = services.dashboard_totals()
        self.assertEqual(totals["total_students"], Student.objects.count())
        self.assertEqual(totals["total_courses"], Course.objects.count())


class PaginationRegressionTests(BaseAuthenticatedTestCase):
    """Regression test for a real bug found while testing with realistic seed
    data: includes/pagination.html used to call page_obj.previous_page_number
    /next_page_number unconditionally (only hiding the link with CSS), which
    raises EmptyPage and 500s the page as soon as there's more than one page
    and you're sitting on the first or last one."""

    def setUp(self):
        super().setUp()
        for i in range(15):
            Student.objects.create(
                name=f"Pagination Student {i}", email=f"pagination{i}@example.com",
                age=20, marks=50, department=self.department,
            )

    def test_first_page_does_not_crash(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)

    def test_last_page_does_not_crash(self):
        response = self.client.get(reverse('student_list'), {'page': 2})
        self.assertEqual(response.status_code, 200)

    def test_manage_users_pagination_does_not_crash(self):
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)
