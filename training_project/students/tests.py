from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    UserProfile,
    AuditLog,
    Student,
    Department,
    Course,
    TrainerAssignment,
    MarksHistory,
    Feedback,
)

# =========================================================
# Authentication Tests
# =========================================================

class AuthenticationTests(TestCase):

    def setUp(self):

        self.student_user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="Test@12345",
        )

        self.student_profile = UserProfile.objects.get(
            user=self.student_user
        )

        self.student_profile.role = (
            UserProfile.UserRole.STUDENT
        )

        self.student_profile.is_approved = True
        self.student_profile.save()

        self.department = Department.objects.create(
            name="Computer Science",
            description="Computer Science Department",
        )

        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student1@example.com",
            age=22,
            department=self.department,
            marks=75,
            joined_date=date.today(),
            is_active=True,
        )

    def test_student_can_login(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "student1",
                "password": "Test@12345",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertRedirects(
            response,
            reverse("student_dashboard"),
        )

    def test_invalid_login_is_rejected(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "student1",
                "password": "WrongPassword123!",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_failed_login_creates_audit_log(self):

        self.client.post(
            reverse("login"),
            {
                "username": "student1",
                "password": "WrongPassword123!",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.student_user,
                action=AuditLog.Action.FAILED_LOGIN,
            ).exists()
        )

    def test_successful_login_creates_audit_log(self):

        self.client.post(
            reverse("login"),
            {
                "username": "student1",
                "password": "Test@12345",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.student_user,
                action=AuditLog.Action.LOGIN,
            ).exists()
        )

    def test_logout_creates_audit_log(self):

        self.client.login(
            username="student1",
            password="Test@12345",
        )

        self.client.post(
            reverse("logout"),
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.student_user,
                action=AuditLog.Action.LOGOUT,
            ).exists()
        )


# =========================================================
# Authorization Tests
# =========================================================

class AuthorizationTests(TestCase):

    def setUp(self):

        # -------------------------------------------------
        # Department
        # -------------------------------------------------

        self.department = Department.objects.create(
            name="Computer Science",
            description="Computer Science Department",
        )

        # -------------------------------------------------
        # Admin User
        # -------------------------------------------------

        self.admin_user = User.objects.create_user(
            username="admin1",
            email="admin1@example.com",
            password="Admin@12345",
        )

        self.admin_profile = UserProfile.objects.get(
            user=self.admin_user
        )

        self.admin_profile.role = (
            UserProfile.UserRole.ADMIN
        )

        self.admin_profile.is_approved = True
        self.admin_profile.save()

        # -------------------------------------------------
        # Trainer User
        # -------------------------------------------------

        self.trainer_user = User.objects.create_user(
            username="trainer1",
            email="trainer1@example.com",
            password="Trainer@12345",
        )

        self.trainer_profile = UserProfile.objects.get(
            user=self.trainer_user
        )

        self.trainer_profile.role = (
            UserProfile.UserRole.TRAINER
        )

        self.trainer_profile.is_approved = True
        self.trainer_profile.save()

        # -------------------------------------------------
        # Student User
        # -------------------------------------------------

        self.student_user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="Student@12345",
        )

        self.student_profile = UserProfile.objects.get(
            user=self.student_user
        )

        self.student_profile.role = (
            UserProfile.UserRole.STUDENT
        )

        self.student_profile.is_approved = True
        self.student_profile.save()

        # -------------------------------------------------
        # Student Record
        # -------------------------------------------------

        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student1@example.com",
            age=22,
            department=self.department,
            marks=75,
            joined_date=date.today(),
            is_active=True,
        )

    # -----------------------------------------------------
    # Test 6
    # -----------------------------------------------------

    def test_admin_can_access_admin_dashboard(self):

        self.client.login(
            username="admin1",
            password="Admin@12345",
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    # -----------------------------------------------------
    # Test 7
    # -----------------------------------------------------

    def test_trainer_cannot_access_admin_dashboard(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # -----------------------------------------------------
    # Test 8
    # -----------------------------------------------------

    def test_student_cannot_access_admin_dashboard(self):

        self.client.login(
            username="student1",
            password="Student@12345",
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # -----------------------------------------------------
    # Test 9
    # -----------------------------------------------------

    def test_trainer_can_access_trainer_dashboard(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.get(
            reverse("trainer_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    # -----------------------------------------------------
    # Test 10
    # -----------------------------------------------------

    def test_student_can_access_student_dashboard(self):

        self.client.login(
            username="student1",
            password="Student@12345",
        )

        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )


# =========================================================
# Marks Security Tests
# =========================================================

class MarksSecurityTests(TestCase):

    def setUp(self):

        # -------------------------------------------------
        # Department
        # -------------------------------------------------

        self.department = Department.objects.create(
            name="Computer Science",
            description="Computer Science Department",
        )

        # -------------------------------------------------
        # Course
        # -------------------------------------------------

        self.course = Course.objects.create(
            course_name="Python Programming",
            code="PY101",
            duration="3 Months",
            is_active=True,
        )

        # -------------------------------------------------
        # Assigned Trainer
        # -------------------------------------------------

        self.trainer_user = User.objects.create_user(
            username="trainer1",
            email="trainer1@example.com",
            password="Trainer@12345",
        )

        self.trainer_profile = UserProfile.objects.get(
            user=self.trainer_user
        )

        self.trainer_profile.role = (
            UserProfile.UserRole.TRAINER
        )

        self.trainer_profile.is_approved = True
        self.trainer_profile.save()

        # -------------------------------------------------
        # Unassigned Trainer
        # -------------------------------------------------

        self.other_trainer = User.objects.create_user(
            username="trainer2",
            email="trainer2@example.com",
            password="Trainer@12345",
        )

        self.other_trainer_profile = UserProfile.objects.get(
            user=self.other_trainer
        )

        self.other_trainer_profile.role = (
            UserProfile.UserRole.TRAINER
        )

        self.other_trainer_profile.is_approved = True
        self.other_trainer_profile.save()

        # -------------------------------------------------
        # Student
        # -------------------------------------------------

        self.student_user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="Student@12345",
        )

        self.student_profile = UserProfile.objects.get(
            user=self.student_user
        )

        self.student_profile.role = (
            UserProfile.UserRole.STUDENT
        )

        self.student_profile.is_approved = True
        self.student_profile.save()

        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student1@example.com",
            age=22,
            department=self.department,
            marks=75,
            joined_date=date.today(),
            is_active=True,
        )

        # -------------------------------------------------
        # Trainer Assignment
        # -------------------------------------------------

        self.assignment = TrainerAssignment.objects.create(
            trainer=self.trainer_user,
            student=self.student,
            course=self.course,
        )

    # -----------------------------------------------------
    # Test 11
    # Assigned trainer can update marks
    # -----------------------------------------------------

    def test_assigned_trainer_can_update_marks(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                kwargs={
                    "student_id": self.student.pk,
                    "course_id": self.course.pk,
                },
            ),
            {
                "new_marks": 85,
                "reason": "Improved performance",
            },
        )

        self.assertRedirects(
            response,
            reverse("trainer_dashboard"),
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.marks,
            85,
        )

    # -----------------------------------------------------
    # Test 12
    # Unassigned trainer cannot update marks
    # -----------------------------------------------------

    def test_unassigned_trainer_cannot_update_marks(self):

        self.client.login(
            username="trainer2",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                kwargs={
                    "student_id": self.student.pk,
                    "course_id": self.course.pk,
                },
            ),
            {
                "new_marks": 90,
                "reason": "Unauthorized update",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.marks,
            75,
        )

    # -----------------------------------------------------
    # Test 13
    # Student cannot update marks
    # -----------------------------------------------------

    def test_student_cannot_update_marks(self):

        self.client.login(
            username="student1",
            password="Student@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                kwargs={
                    "student_id": self.student.pk,
                    "course_id": self.course.pk,
                },
            ),
            {
                "new_marks": 95,
                "reason": "Student direct update",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.marks,
            75,
        )

    # -----------------------------------------------------
    # Test 14
    # Marks above 100 are rejected
    # -----------------------------------------------------

    def test_marks_above_100_are_rejected(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                kwargs={
                    "student_id": self.student.pk,
                    "course_id": self.course.pk,
                },
            ),
            {
                "new_marks": 101,
                "reason": "Invalid marks",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.marks,
            75,
        )

        self.assertEqual(
            MarksHistory.objects.count(),
            0,
        )

    # -----------------------------------------------------
    # Test 15
    # Marks below 0 are rejected
    # -----------------------------------------------------

    def test_marks_below_0_are_rejected(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                kwargs={
                    "student_id": self.student.pk,
                    "course_id": self.course.pk,
                },
            ),
            {
                "new_marks": -1,
                "reason": "Invalid marks",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.marks,
            75,
        )

        self.assertEqual(
            MarksHistory.objects.count(),
            0,
        )


# =========================================================
# Feedback Workflow Tests
# =========================================================

class FeedbackWorkflowTests(TestCase):

    def setUp(self):

        # -------------------------------------------------
        # Department
        # -------------------------------------------------

        self.department = Department.objects.create(
            name="Computer Science",
            description="Computer Science Department",
        )

        # -------------------------------------------------
        # Courses
        # -------------------------------------------------

        self.course = Course.objects.create(
            course_name="Python Programming",
            code="PY101",
            duration="3 Months",
            is_active=True,
        )

        self.other_course = Course.objects.create(
            course_name="Django Development",
            code="DJ101",
            duration="3 Months",
            is_active=True,
        )

        # -------------------------------------------------
        # Trainer 1
        # -------------------------------------------------

        self.trainer_user = User.objects.create_user(
            username="trainer1",
            email="trainer1@example.com",
            password="Trainer@12345",
        )

        self.trainer_profile = UserProfile.objects.get(
            user=self.trainer_user
        )

        self.trainer_profile.role = (
            UserProfile.UserRole.TRAINER
        )

        self.trainer_profile.is_approved = True
        self.trainer_profile.save()

        # -------------------------------------------------
        # Trainer 2
        # -------------------------------------------------

        self.other_trainer = User.objects.create_user(
            username="trainer2",
            email="trainer2@example.com",
            password="Trainer@12345",
        )

        self.other_trainer_profile = UserProfile.objects.get(
            user=self.other_trainer
        )

        self.other_trainer_profile.role = (
            UserProfile.UserRole.TRAINER
        )

        self.other_trainer_profile.is_approved = True
        self.other_trainer_profile.save()

        # -------------------------------------------------
        # Student
        # -------------------------------------------------

        self.student_user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="Student@12345",
        )

        self.student_profile = UserProfile.objects.get(
            user=self.student_user
        )

        self.student_profile.role = (
            UserProfile.UserRole.STUDENT
        )

        self.student_profile.is_approved = True
        self.student_profile.save()

        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student1@example.com",
            age=22,
            department=self.department,
            marks=75,
            joined_date=date.today(),
            is_active=True,
        )

        # -------------------------------------------------
        # Trainer Assignment
        # -------------------------------------------------

        self.assignment = TrainerAssignment.objects.create(
            trainer=self.trainer_user,
            student=self.student,
            course=self.course,
        )

    # -----------------------------------------------------
    # Test 16
    # Assigned trainer can add feedback
    # -----------------------------------------------------

    def test_assigned_trainer_can_add_feedback(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "add_feedback",
                kwargs={
                    "student_id": self.student.pk,
                },
            ),
            {
                "rating": 5,
                "feedback": "Excellent performance.",
            },
        )

        self.assertRedirects(
            response,
            reverse("trainer_dashboard"),
        )

        self.assertTrue(
            Feedback.objects.filter(
                trainer=self.trainer_user,
                student=self.student,
                course=self.course,
            ).exists()
        )
    # -----------------------------------------------------
    # Test 17
    # Unassigned trainer cannot add feedback
    # -----------------------------------------------------

    def test_unassigned_trainer_cannot_add_feedback(self):

        self.client.login(
            username="trainer2",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "add_feedback",
                kwargs={
                    "student_id": self.student.pk,
                },
            ),
            {
                "rating": 5,
                "feedback": "Unauthorized feedback.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            Feedback.objects.filter(
                trainer=self.other_trainer,
                student=self.student,
            ).exists()
        )

    # -----------------------------------------------------
    # Test 18
    # Trainer can edit own feedback
    # -----------------------------------------------------

    def test_trainer_can_edit_own_feedback(self):

        feedback = Feedback.objects.create(
            trainer=self.trainer_user,
            student=self.student,
            course=self.course,
            rating=3,
            feedback="Average performance.",
            is_visible=True,
        )

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "edit_feedback",
                kwargs={
                    "feedback_id": feedback.pk,
                },
            ),
            {
                "rating": 5,
                "feedback": "Excellent performance.",
            },
        )

        self.assertRedirects(
            response,
            reverse("trainer_dashboard"),
        )

        feedback.refresh_from_db()

        self.assertEqual(
            feedback.rating,
            5,
        )

        self.assertEqual(
            feedback.feedback,
            "Excellent performance.",
        )

    # -----------------------------------------------------
    # Test 19
    # Trainer cannot edit another trainer's feedback
    # -----------------------------------------------------

    def test_trainer_cannot_edit_other_trainers_feedback(self):

        feedback = Feedback.objects.create(
            trainer=self.other_trainer,
            student=self.student,
            course=self.course,
            rating=4,
            feedback="Feedback from another trainer.",
            is_visible=True,
        )

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "edit_feedback",
                kwargs={
                    "feedback_id": feedback.pk,
                },
            ),
            {
                "rating": 5,
                "feedback": "Unauthorized edit.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        feedback.refresh_from_db()

        self.assertEqual(
            feedback.rating,
            4,
        )

    # -----------------------------------------------------
    # Test 20
    # Student can view visible feedback
    # -----------------------------------------------------

    def test_student_can_view_visible_feedback(self):

        feedback = Feedback.objects.create(
            trainer=self.trainer_user,
            student=self.student,
            course=self.course,
            rating=5,
            feedback="Excellent performance.",
            is_visible=True,
        )

        self.client.login(
            username="student1",
            password="Student@12345",
        )

        response = self.client.get(
            reverse("student_feedback")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Excellent performance.",
        )

    # -----------------------------------------------------
    # Test 21
    # Student cannot view hidden feedback
    # -----------------------------------------------------

    def test_student_cannot_view_hidden_feedback(self):

        Feedback.objects.create(
            trainer=self.trainer_user,
            student=self.student,
            course=self.course,
            rating=5,
            feedback="Private trainer feedback.",
            is_visible=False,
        )

        self.client.login(
            username="student1",
            password="Student@12345",
        )

        response = self.client.get(
            reverse("student_feedback")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertNotContains(
            response,
            "Private trainer feedback.",
        )

    # -----------------------------------------------------
    # Test 22
    # Rating below 1 is rejected
    # -----------------------------------------------------

    def test_feedback_rating_below_1_is_rejected(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "add_feedback",
                kwargs={
                    "student_id": self.student.pk,
                },
            ),
            {
                "rating": 0,
                "feedback": "Invalid rating.",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Feedback.objects.count(),
            0,
        )

    # -----------------------------------------------------
    # Test 23
    # Rating above 5 is rejected
    # -----------------------------------------------------

    def test_feedback_rating_above_5_is_rejected(self):

        self.client.login(
            username="trainer1",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "add_feedback",
                kwargs={
                    "student_id": self.student.pk,
                },
            ),
            {
                "rating": 6,
                "feedback": "Invalid rating.",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            Feedback.objects.count(),
            0,
        )


# =========================================================
# User Account Status Tests
# =========================================================

class UserAccountStatusTests(TestCase):

    def setUp(self):

        # -------------------------------------------------
        # Admin User
        # -------------------------------------------------

        self.admin_user = User.objects.create_user(
            username="admin_status",
            email="admin_status@example.com",
            password="Admin@12345",
        )

        self.admin_profile = UserProfile.objects.get(
            user=self.admin_user
        )

        self.admin_profile.role = (
            UserProfile.UserRole.ADMIN
        )

        self.admin_profile.is_approved = True
        self.admin_profile.save()

        # -------------------------------------------------
        # Test User
        # -------------------------------------------------

        self.test_user = User.objects.create_user(
            username="status_user",
            email="status_user@example.com",
            password="User@12345",
        )

        self.test_profile = UserProfile.objects.get(
            user=self.test_user
        )

        self.test_profile.role = (
            UserProfile.UserRole.STUDENT
        )

        self.test_profile.is_approved = True
        self.test_profile.save()

    # -----------------------------------------------------
    # Admin can deactivate an active user
    # -----------------------------------------------------

    def test_admin_can_deactivate_user(self):

        self.assertTrue(
            self.test_user.is_active
        )

        self.client.login(
            username="admin_status",
            password="Admin@12345",
        )

        response = self.client.post(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.test_user.pk,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("user_management"),
        )

        self.test_user.refresh_from_db()

        self.assertFalse(
            self.test_user.is_active
        )

    # -----------------------------------------------------
    # Admin can activate an inactive user
    # -----------------------------------------------------

    def test_admin_can_activate_user(self):

        self.test_user.is_active = False
        self.test_user.save(
            update_fields=["is_active"]
        )

        self.client.login(
            username="admin_status",
            password="Admin@12345",
        )

        response = self.client.post(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.test_user.pk,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("user_management"),
        )

        self.test_user.refresh_from_db()

        self.assertTrue(
            self.test_user.is_active
        )

    # -----------------------------------------------------
    # Status change creates audit log
    # -----------------------------------------------------

    def test_status_change_creates_audit_log(self):

        self.client.login(
            username="admin_status",
            password="Admin@12345",
        )

        self.client.post(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.test_user.pk,
                },
            )
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.admin_user,
                action=AuditLog.Action.STATUS_CHANGE,
                object_name="User Account",
            ).exists()
        )

    # -----------------------------------------------------
    # Trainer cannot change user status
    # -----------------------------------------------------

    def test_trainer_cannot_change_user_status(self):

        trainer = User.objects.create_user(
            username="status_trainer",
            email="status_trainer@example.com",
            password="Trainer@12345",
        )

        trainer_profile = UserProfile.objects.get(
            user=trainer
        )

        trainer_profile.role = (
            UserProfile.UserRole.TRAINER
        )

        trainer_profile.is_approved = True
        trainer_profile.save()

        self.client.login(
            username="status_trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.test_user.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.test_user.refresh_from_db()

        self.assertTrue(
            self.test_user.is_active
        )

    # -----------------------------------------------------
    # Student cannot change user status
    # -----------------------------------------------------

    def test_student_cannot_change_user_status(self):

        self.client.login(
            username="status_user",
            password="User@12345",
        )

        response = self.client.post(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.admin_user.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # -----------------------------------------------------
    # GET request cannot change user status
    # -----------------------------------------------------

    def test_get_request_cannot_change_user_status(self):

        self.client.login(
            username="admin_status",
            password="Admin@12345",
        )

        response = self.client.get(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.test_user.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.test_user.refresh_from_db()

        self.assertTrue(
            self.test_user.is_active
        )

    # -----------------------------------------------------
    # Admin cannot change own account status
    # -----------------------------------------------------

    def test_admin_cannot_change_own_status(self):

        self.client.login(
            username="admin_status",
            password="Admin@12345",
        )

        response = self.client.post(
            reverse(
                "toggle_user_status",
                kwargs={
                    "user_id": self.admin_user.pk,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("user_management"),
        )

        self.admin_user.refresh_from_db()

        self.assertTrue(
            self.admin_user.is_active
        )

        self.assertFalse(
            AuditLog.objects.filter(
                user=self.admin_user,
                action=AuditLog.Action.STATUS_CHANGE,
            ).exists()
        )