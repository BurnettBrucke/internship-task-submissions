from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import (
    Department,
    Course,
    Student,
    UserProfile,
    Enrollment,
    Feedback,
    MarksHistory,
    AuditLog,
)

from .forms import StudentForm, RegisterForm


# =========================================================
# AUTHENTICATION TESTS
# =========================================================

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

        response = self.client.get(
            reverse("login")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_login_success(self):

        login = self.client.login(
            username="student1",
            password="Test@12345"
        )

        self.assertTrue(login)

    def test_logout_requires_post(self):

        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("logout")
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_logout_post_success(self):

        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.post(
            reverse("logout")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_register_page(self):

        response = self.client.get(
            reverse("register")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_student_dashboard_requires_login(self):

        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(
            response.status_code,
            302
        )


# =========================================================
# FORM TESTS
# =========================================================

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
            "department": self.department.id,
        })

        self.assertTrue(
            form.is_valid()
        )

    def test_student_form_does_not_expose_sensitive_fields(self):

        form = StudentForm()

        self.assertNotIn(
            "user",
            form.fields
        )

        self.assertNotIn(
            "assigned_trainer",
            form.fields
        )

        self.assertNotIn(
            "active",
            form.fields
        )

        self.assertNotIn(
            "joined_date",
            form.fields
        )

    def test_student_form_invalid_age(self):

        form = StudentForm(data={
            "name": "Jaya",
            "email": "jaya@test.com",
            "age": 10,
            "department": self.department.id,
        })

        self.assertFalse(
            form.is_valid()
        )

    def test_student_form_empty_name(self):

        form = StudentForm(data={
            "name": "   ",
            "email": "jaya@test.com",
            "age": 22,
            "department": self.department.id,
        })

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "name",
            form.errors
        )

    def test_enrollment_marks_cannot_exceed_100(self):

        student = Student.objects.create(
            name="Jaya",
            email="jaya@test.com",
            age=22,
            department=self.department
        )

        enrollment = Enrollment(
            student=student,
            course=self.course,
            marks=150
        )

        with self.assertRaises(
            ValidationError
        ):
            enrollment.full_clean()

    def test_enrollment_marks_cannot_be_negative(self):

        student = Student.objects.create(
            name="Jaya",
            email="jaya@test.com",
            age=22,
            department=self.department
        )

        enrollment = Enrollment(
            student=student,
            course=self.course,
            marks=-10
        )

        with self.assertRaises(
            ValidationError
        ):
            enrollment.full_clean()

    def test_register_form_valid(self):

        form = RegisterForm(data={
            "username": "newuser",
            "email": "new@test.com",
            "password1": "Test@12345",
            "password2": "Test@12345",
        })

        self.assertTrue(
            form.is_valid()
        )

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

        self.assertFalse(
            form.is_valid()
        )


# =========================================================
# MODEL TESTS
# =========================================================

class ModelTests(TestCase):

    def setUp(self):

        self.trainer = User.objects.create_user(
            username="trainer",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer,
            role="trainer",
            is_approved=True
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
            department=self.department,
            assigned_trainer=self.trainer
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            marks=85
        )

    def test_student_str(self):

        self.assertEqual(
            str(self.student),
            "Jaya"
        )

    def test_department_str(self):

        self.assertEqual(
            str(self.department),
            "CSE"
        )

    def test_course_str(self):

        self.assertEqual(
            str(self.course),
            "Python"
        )

    def test_enrollment_str(self):

        self.assertEqual(
            str(self.enrollment),
            "Jaya - Python"
        )

    def test_feedback_create(self):

        feedback = Feedback.objects.create(
            trainer=self.trainer,
            student=self.student,
            enrollment=self.enrollment,
            rating=5,
            comments="Excellent"
        )

        self.assertEqual(
            feedback.rating,
            5
        )

    def test_marks_history_create(self):

        history = MarksHistory.objects.create(
            student=self.student,
            enrollment=self.enrollment,
            previous_marks=85,
            new_marks=95,
            updated_by=self.trainer,
            reason="Internal Test"
        )

        self.assertEqual(
            history.new_marks,
            95
        )

    def test_feedback_rating_range(self):

        feedback = Feedback(
            trainer=self.trainer,
            student=self.student,
            enrollment=self.enrollment,
            rating=6,
            comments="Invalid rating"
        )

        with self.assertRaises(
            ValidationError
        ):
            feedback.full_clean()


# =========================================================
# STUDENT ACCESS / AUTHORIZATION TESTS
# =========================================================

class StudentAuthorizationTests(TestCase):

    def setUp(self):

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.student_user = User.objects.create_user(
            username="student1",
            password="Test@12345",
            email="student1@test.com"
        )

        UserProfile.objects.create(
            user=self.student_user,
            role="student"
        )

        self.other_student_user = User.objects.create_user(
            username="student2",
            password="Test@12345",
            email="student2@test.com"
        )

        UserProfile.objects.create(
            user=self.other_student_user,
            role="student"
        )

        self.student = Student.objects.create(
            user=self.student_user,
            name="Student One",
            email="student1@test.com",
            age=22,
            department=self.department
        )

        self.other_student = Student.objects.create(
            user=self.other_student_user,
            name="Student Two",
            email="student2@test.com",
            age=23,
            department=self.department
        )

    def test_student_can_view_own_profile(self):

        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                args=[self.student.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_student_cannot_view_other_student_profile(self):

        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                args=[self.other_student.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_student_cannot_edit_student(self):

        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "edit_student",
                args=[self.student.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_student_cannot_delete_student(self):

        self.client.login(
            username="student1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "delete_student",
                args=[self.student.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )


# =========================================================
# TRAINER AUTHORIZATION TESTS
# =========================================================

class TrainerAuthorizationTests(TestCase):

    def setUp(self):

        self.department = Department.objects.create(
            name="IT",
            description="Information Technology"
        )

        self.course = Course.objects.create(
            course_name="Django",
            code="DJ101",
            duration="3 Months"
        )

        self.trainer1 = User.objects.create_user(
            username="trainer1",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer1,
            role="trainer",
            is_approved=True
        )

        self.trainer2 = User.objects.create_user(
            username="trainer2",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer2,
            role="trainer",
            is_approved=True
        )

        self.student1 = Student.objects.create(
            name="Student One",
            email="one@test.com",
            age=22,
            department=self.department,
            assigned_trainer=self.trainer1
        )

        self.student2 = Student.objects.create(
            name="Student Two",
            email="two@test.com",
            age=23,
            department=self.department,
            assigned_trainer=self.trainer2
        )

        self.enrollment1 = Enrollment.objects.create(
            student=self.student1,
            course=self.course,
            marks=80
        )

        self.enrollment2 = Enrollment.objects.create(
            student=self.student2,
            course=self.course,
            marks=70
        )

    def test_trainer_can_view_assigned_student(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                args=[self.student1.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_trainer_cannot_view_unassigned_student(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                args=[self.student2.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_trainer_cannot_edit_unassigned_student(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "edit_student",
                args=[self.student2.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_trainer_cannot_update_unassigned_student_marks(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "update_marks",
                args=[self.enrollment2.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_trainer_cannot_delete_student(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "delete_student",
                args=[self.student1.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_trainer_can_access_assigned_marks_history(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "marks_history",
                args=[self.student1.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_trainer_cannot_access_unassigned_marks_history(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "marks_history",
                args=[self.student2.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )


# =========================================================
# FEEDBACK AUTHORIZATION TESTS
# =========================================================

class FeedbackAuthorizationTests(TestCase):

    def setUp(self):

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.course = Course.objects.create(
            course_name="Python",
            code="PY201",
            duration="3 Months"
        )

        self.trainer1 = User.objects.create_user(
            username="trainer1",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer1,
            role="trainer",
            is_approved=True
        )

        self.trainer2 = User.objects.create_user(
            username="trainer2",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer2,
            role="trainer",
            is_approved=True
        )

        self.student1 = Student.objects.create(
            name="Student One",
            email="one@test.com",
            age=22,
            department=self.department,
            assigned_trainer=self.trainer1
        )

        self.student2 = Student.objects.create(
            name="Student Two",
            email="two@test.com",
            age=23,
            department=self.department,
            assigned_trainer=self.trainer2
        )

        self.enrollment1 = Enrollment.objects.create(
            student=self.student1,
            course=self.course,
            marks=80
        )

        self.enrollment2 = Enrollment.objects.create(
            student=self.student2,
            course=self.course,
            marks=75
        )

        self.feedback = Feedback.objects.create(
            trainer=self.trainer1,
            student=self.student1,
            enrollment=self.enrollment1,
            rating=5,
            comments="Excellent"
        )

    def test_trainer_can_edit_own_feedback(self):

        self.client.login(
            username="trainer1",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "edit_feedback",
                args=[self.feedback.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_trainer_cannot_edit_other_trainer_feedback(self):

        self.client.login(
            username="trainer2",
            password="Test@12345"
        )

        response = self.client.get(
            reverse(
                "edit_feedback",
                args=[self.feedback.id]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )


# =========================================================
# ADMIN AUTHORIZATION TESTS
# =========================================================

class AdminAuthorizationTests(TestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username="admin",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.admin,
            role="admin"
        )

        self.trainer = User.objects.create_user(
            username="trainer",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer,
            role="trainer",
            is_approved=True
        )

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.student = Student.objects.create(
            name="Student",
            email="student@test.com",
            age=22,
            department=self.department,
            assigned_trainer=self.trainer
        )

    def test_admin_can_delete_student(self):

        self.client.login(
            username="admin",
            password="Test@12345"
        )

        response = self.client.post(
            reverse(
                "delete_student",
                args=[self.student.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            Student.objects.filter(
                id=self.student.id
            ).exists()
        )

    def test_trainer_cannot_access_audit_logs(self):

        self.client.login(
            username="trainer",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("audit_log_list")
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_admin_can_access_audit_logs(self):

        self.client.login(
            username="admin",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("audit_log_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )


# =========================================================
# VIEW TESTS
# =========================================================

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

        self.course = Course.objects.create(
            course_name="Python",
            code="PY102",
            duration="3 Months"
        )

        self.student = Student.objects.create(
            name="Test Student",
            email="test@student.com",
            age=21,
            department=self.department
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            marks=80
        )

    def test_student_list_requires_login(self):

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_student_list_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )

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

        self.assertEqual(
            response.status_code,
            200
        )

    def test_add_student_page_authenticated(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("add_student")
        )

        self.assertEqual(
            response.status_code,
            200
        )

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

        self.assertEqual(
            response.status_code,
            200
        )

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

        self.assertEqual(
            response.status_code,
            200
        )

    def test_student_search(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {
                "search": "Test Student"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Test Student"
        )

    def test_department_filter(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {
                "department": self.department.id
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_active_filter(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {
                "active": "yes"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_result_filter(self):

        self.client.login(
            username="admin_test",
            password="Test@12345"
        )

        response = self.client.get(
            reverse("student_list"),
            {
                "result": "pass"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
# =========================================================
# RETASK ADDITIONAL TESTS
# =========================================================

class RetaskAdditionalTests(TestCase):

    def setUp(self):

        self.department = Department.objects.create(
            name="CSE",
            description="Computer Science"
        )

        self.course = Course.objects.create(
            course_name="Python",
            code="PY301",
            duration="3 Months"
        )

        self.admin = User.objects.create_user(
            username="retask_admin",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.admin,
            role="admin",
            is_approved=True
        )

        self.trainer = User.objects.create_user(
            username="retask_trainer",
            password="Test@12345"
        )

        UserProfile.objects.create(
            user=self.trainer,
            role="trainer",
            is_approved=True
        )

        self.student_user = User.objects.create_user(
            username="retask_student",
            password="Test@12345",
            email="retaskstudent@test.com"
        )

        UserProfile.objects.create(
            user=self.student_user,
            role="student",
            is_approved=True
        )

        self.student = Student.objects.create(
            user=self.student_user,
            department=self.department,
            assigned_trainer=self.trainer,
            name="Retask Student",
            email="retaskstudent@test.com",
            age=22
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            marks=80
        )

    def test_audit_log_action_choices_are_valid(self):

        valid_actions = {
            choice[0]
            for choice in AuditLog.ACTION_CHOICES
        }

        for action in [
            "LOGIN",
            "LOGOUT",
            "FAILED_LOGIN",
            "CREATE",
            "UPDATE",
            "DELETE",
            "MARKS_UPDATE",
            "FEEDBACK",
        ]:

            self.assertIn(
                action,
                valid_actions
            )

    def test_audit_log_create_action(self):

        log = AuditLog.objects.create(
            user=self.admin,
            action="CREATE",
            description="Created test record"
        )

        self.assertEqual(
            log.action,
            "CREATE"
        )

    def test_custom_404_page(self):

        response = self.client.get(
            "/this-url-does-not-exist/"
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_registration_page_available(self):

        response = self.client.get(
            reverse("register")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_password_validation(self):

        form = RegisterForm(
            data={
                "username": "weakuser",
                "email": "weak@test.com",
                "password1": "password",
                "password2": "password",
            }
        )

        self.assertFalse(
            form.is_valid()
        )

    def test_student_relationship_with_department(self):

        self.assertEqual(
            self.student.department,
            self.department
        )

    def test_student_relationship_with_trainer(self):

        self.assertEqual(
            self.student.assigned_trainer,
            self.trainer
        )

    def test_enrollment_relationship_with_course(self):

        self.assertEqual(
            self.enrollment.course,
            self.course
        )

    def test_enrollment_unique_student_course(self):

        duplicate = Enrollment(
            student=self.student,
            course=self.course,
            marks=70
        )

        with self.assertRaises(
            ValidationError
        ):
            duplicate.full_clean()

    def test_feedback_rating_validation(self):

        feedback = Feedback(
            trainer=self.trainer,
            student=self.student,
            enrollment=self.enrollment,
            rating=10,
            comments="Invalid rating"
        )

        with self.assertRaises(
            ValidationError
        ):
            feedback.full_clean()