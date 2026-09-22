from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (
    AuditLog,
    Course,
    Department,
    Enrollment,
    Feedback,
    MarkHistory,
    Student,
    StudentProfile,
    TrainerCourse,
    UserProfile,
)


# ============================================================
# COMMON TEST SETUP
# ============================================================


class StudentPortalTestSetup(TestCase):

    def setUp(self):
        # -----------------------------------------------------
        # ADMIN
        # -----------------------------------------------------

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="Admin@12345",
        )

        UserProfile.objects.create(
            user=self.admin,
            role=UserProfile.Role.ADMIN,
            status=UserProfile.Status.APPROVED,
        )

        # -----------------------------------------------------
        # TRAINER
        # -----------------------------------------------------

        self.trainer = User.objects.create_user(
            username="trainer",
            email="trainer@test.com",
            password="Trainer@12345",
        )

        UserProfile.objects.create(
            user=self.trainer,
            role=UserProfile.Role.TRAINER,
            status=UserProfile.Status.APPROVED,
        )

        # -----------------------------------------------------
        # SECOND TRAINER
        # -----------------------------------------------------

        self.other_trainer = User.objects.create_user(
            username="trainer2",
            email="trainer2@test.com",
            password="Trainer@12345",
        )

        UserProfile.objects.create(
            user=self.other_trainer,
            role=UserProfile.Role.TRAINER,
            status=UserProfile.Status.APPROVED,
        )

        # -----------------------------------------------------
        # STUDENT USER
        # -----------------------------------------------------

        self.student_user = User.objects.create_user(
            username="student",
            email="student@test.com",
            password="Student@12345",
        )

        UserProfile.objects.create(
            user=self.student_user,
            role=UserProfile.Role.STUDENT,
            status=UserProfile.Status.APPROVED,
        )

        # -----------------------------------------------------
        # DEPARTMENT
        # -----------------------------------------------------

        self.department = Department.objects.create(
            name="Information Technology",
            description="IT Department",
        )

        self.other_department = Department.objects.create(
            name="Computer Science",
            description="CS Department",
        )

        # -----------------------------------------------------
        # COURSES
        # -----------------------------------------------------

        self.course = Course.objects.create(
            course_name="Python",
            code="PY101",
            duration="3 Months",
            duration_days=90,
            active_status=True,
        )

        self.other_course = Course.objects.create(
            course_name="Django",
            code="DJ101",
            duration="3 Months",
            duration_days=90,
            active_status=True,
        )

        # -----------------------------------------------------
        # STUDENT
        # -----------------------------------------------------

        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student@test.com",
            age=22,
            department=self.department,
            active=True,
        )

        StudentProfile.objects.create(
            student=self.student,
            phone="9876543210",
            address="Indore",
        )

        # -----------------------------------------------------
        # ENROLLMENT
        # -----------------------------------------------------

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            marks=70,
        )

        # -----------------------------------------------------
        # TRAINER ASSIGNMENT
        # -----------------------------------------------------

        TrainerCourse.objects.create(
            trainer=self.trainer,
            course=self.course,
        )

        TrainerCourse.objects.create(
            trainer=self.other_trainer,
            course=self.other_course,
        )


# ============================================================
# AUTHENTICATION TESTS
# 1 - 7
# ============================================================


class AuthenticationTests(StudentPortalTestSetup):

    # 1
    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "Trainer@12345",
            },
        )

        self.assertRedirects(
            response,
            reverse("home"),
        )

        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )

    # 2
    def test_login_with_email(self):
        response = self.client.post(
            reverse("login"),
            {
                "login": "trainer@test.com",
                "password": "Trainer@12345",
            },
        )

        self.assertRedirects(
            response,
            reverse("home"),
        )

        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )

    # 3
    def test_invalid_password_does_not_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "WrongPassword@123",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertIsNone(
            self.client.session.get("_auth_user_id")
        )

    # 4
    def test_invalid_login_creates_failed_login_audit(self):
        self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "WrongPassword@123",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                action=AuditLog.Action.FAILED_LOGIN,
                user=self.trainer,
            ).exists()
        )

    # 5
    def test_failed_login_increments_attempt_counter(self):
        self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "WrongPassword@123",
            },
        )

        self.trainer.profile.refresh_from_db()

        self.assertEqual(
            self.trainer.profile.failed_login_attempts,
            1,
        )

    # 6
    def test_five_failed_attempts_block_account(self):
        for _ in range(5):
            self.client.post(
                reverse("login"),
                {
                    "login": "trainer",
                    "password": "WrongPassword@123",
                },
            )

        self.trainer.profile.refresh_from_db()

        self.assertEqual(
            self.trainer.profile.failed_login_attempts,
            5,
        )

        self.assertTrue(
            self.trainer.profile.login_blocked
        )

    # 7
    def test_successful_login_resets_failed_attempts(self):
        profile = self.trainer.profile

        profile.failed_login_attempts = 3
        profile.login_blocked = False
        profile.save()

        response = self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "Trainer@12345",
            },
        )

        self.assertRedirects(
            response,
            reverse("home"),
        )

        profile.refresh_from_db()

        self.assertEqual(
            profile.failed_login_attempts,
            0,
        )

        self.assertFalse(
            profile.login_blocked
        )


# ============================================================
# AUTHORIZATION TESTS
# 8 - 14
# ============================================================


class AuthorizationTests(StudentPortalTestSetup):

    # 8
    def test_blocked_account_cannot_login(self):
        profile = self.trainer.profile

        profile.login_blocked = True
        profile.failed_login_attempts = 5
        profile.save()

        response = self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "Trainer@12345",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            self.client.session.get("_auth_user_id")
        )

    # 9
    def test_student_cannot_update_marks(self):
        self.client.login(
            username="student",
            password="Student@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 80,
                "reason": "Unauthorized update",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.enrollment.refresh_from_db()

        self.assertEqual(
            self.enrollment.marks,
            70,
        )

    # 10
    def test_unapproved_trainer_cannot_update_marks(self):
        profile = self.trainer.profile

        profile.status = UserProfile.Status.PENDING
        profile.save()

        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 80,
                "reason": "Updated test marks",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # 11
    def test_trainer_cannot_update_another_trainers_course(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        other_enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.other_course,
            marks=60,
        )

        response = self.client.post(
            reverse(
                "update_marks",
                args=[other_enrollment.id],
            ),
            {
                "marks": 90,
                "reason": "Unauthorized update",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        other_enrollment.refresh_from_db()

        self.assertEqual(
            other_enrollment.marks,
            60,
        )

    # 12
    def test_student_cannot_view_another_student(self):
        another_user = User.objects.create_user(
            username="student2",
            email="student2@test.com",
            password="Student@12345",
        )

        UserProfile.objects.create(
            user=another_user,
            role=UserProfile.Role.STUDENT,
            status=UserProfile.Status.APPROVED,
        )

        another_student = Student.objects.create(
            user=another_user,
            name="Another Student",
            email="student2@test.com",
            age=21,
            department=self.department,
            active=True,
        )

        self.client.login(
            username="student",
            password="Student@12345",
        )

        response = self.client.get(
            reverse(
                "student_detail",
                args=[another_student.id],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # 13
    def test_unauthenticated_user_cannot_access_student_list(self):
        response = self.client.get(
            reverse("students_list")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('students_list')}",
        )

    # 14
    def test_unauthenticated_user_cannot_access_dashboard(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )


# ============================================================
# MARKS TESTS
# 15 - 20
# ============================================================


class MarksTests(StudentPortalTestSetup):

    # 15
    def test_assigned_trainer_can_update_marks(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 85,
                "reason": "Improved performance",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "student_detail",
                args=[self.student.id],
            ),
        )

        self.enrollment.refresh_from_db()

        self.assertEqual(
            self.enrollment.marks,
            85,
        )

    # 16
    def test_mark_history_is_created(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 85,
                "reason": "Improved performance",
            },
        )

        history = MarkHistory.objects.get(
            enrollment=self.enrollment
        )

        self.assertEqual(
            history.previous_marks,
            70,
        )

        self.assertEqual(
            history.new_marks,
            85,
        )

        self.assertEqual(
            history.updated_by,
            self.trainer,
        )

    # 17
    def test_marks_update_creates_audit_log(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 90,
                "reason": "Final assessment",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.trainer,
                action=AuditLog.Action.MARKS_UPDATE,
            ).exists()
        )

    # 18
    def test_reason_is_required_for_marks_update(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 90,
                "reason": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.enrollment.refresh_from_db()

        self.assertEqual(
            self.enrollment.marks,
            70,
        )

    # 19
    def test_mark_history_stores_multiple_updates(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 80,
                "reason": "First update",
            },
        )

        self.client.post(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            ),
            {
                "marks": 90,
                "reason": "Final update",
            },
        )

        history = MarkHistory.objects.filter(
            enrollment=self.enrollment
        ).order_by("updated_at")

        self.assertEqual(
            history.count(),
            2,
        )

        self.assertEqual(
            history.first().new_marks,
            80,
        )

        self.assertEqual(
            history.last().new_marks,
            90,
        )

    # 20
    def test_get_update_marks_page_for_assigned_trainer(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.get(
            reverse(
                "update_marks",
                args=[self.enrollment.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )


# ============================================================
# FEEDBACK TESTS
# 21 - 26
# ============================================================


class FeedbackTests(StudentPortalTestSetup):

    # 21
    def test_trainer_can_create_feedback(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "create_feedback",
                args=[self.enrollment.id],
            ),
            {
                "rating": 5,
                "comment": "Excellent progress.",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "student_detail",
                args=[self.student.id],
            ),
        )

        self.assertTrue(
            Feedback.objects.filter(
                trainer=self.trainer,
                student=self.student,
                course=self.course,
            ).exists()
        )

    # 22
    def test_feedback_creates_audit_log(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        self.client.post(
            reverse(
                "create_feedback",
                args=[self.enrollment.id],
            ),
            {
                "rating": 4,
                "comment": "Good work.",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.trainer,
                action=AuditLog.Action.FEEDBACK_CREATE,
            ).exists()
        )

    # 23
    def test_trainer_cannot_create_feedback_for_other_course(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        other_enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.other_course,
            marks=50,
        )

        response = self.client.post(
            reverse(
                "create_feedback",
                args=[other_enrollment.id],
            ),
            {
                "rating": 5,
                "comment": "Unauthorized feedback.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # 24
    def test_trainer_can_edit_own_feedback(self):
        feedback = Feedback.objects.create(
            student=self.student,
            trainer=self.trainer,
            course=self.course,
            rating=3,
            comment="Needs improvement.",
        )

        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "edit_feedback",
                args=[feedback.id],
            ),
            {
                "rating": 5,
                "comment": "Great improvement.",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "student_detail",
                args=[self.student.id],
            ),
        )

        feedback.refresh_from_db()

        self.assertEqual(
            feedback.rating,
            5,
        )

    # 25
    def test_trainer_cannot_edit_another_trainers_feedback(self):
        feedback = Feedback.objects.create(
            student=self.student,
            trainer=self.other_trainer,
            course=self.other_course,
            rating=3,
            comment="Original feedback.",
        )

        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "edit_feedback",
                args=[feedback.id],
            ),
            {
                "rating": 5,
                "comment": "Unauthorized edit.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # 26
    def test_feedback_rating_is_validated(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.post(
            reverse(
                "create_feedback",
                args=[self.enrollment.id],
            ),
            {
                "rating": 10,
                "comment": "Invalid rating.",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            Feedback.objects.filter(
                trainer=self.trainer,
                student=self.student,
                course=self.course,
            ).exists()
        )


# ============================================================
# TRAINER / MODEL TESTS
# 27 - 31
# ============================================================


class TrainerManagementTests(StudentPortalTestSetup):

    # 27
    def test_admin_can_delete_trainer_without_history(self):
        self.client.login(
            username="admin",
            password="Admin@12345",
        )

        trainer_id = self.trainer.id

        response = self.client.post(
            reverse(
                "delete_trainer",
                args=[trainer_id],
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_dashboard"),
        )

        self.assertFalse(
            User.objects.filter(
                id=trainer_id
            ).exists()
        )

    # 28
    def test_trainer_deletion_creates_audit_log(self):
        self.client.login(
            username="admin",
            password="Admin@12345",
        )

        trainer_id = self.trainer.id

        self.client.post(
            reverse(
                "delete_trainer",
                args=[trainer_id],
            )
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.admin,
                action=AuditLog.Action.DELETE,
                description__icontains="trainer",
            ).exists()
        )

    # 29
    def test_enrollment_unique_student_course(self):
        with self.assertRaises(Exception):
            Enrollment.objects.create(
                student=self.student,
                course=self.course,
                marks=90,
            )

    # 30
    def test_trainer_course_assignment_is_unique(self):
        with self.assertRaises(Exception):
            TrainerCourse.objects.create(
                trainer=self.trainer,
                course=self.course,
            )

    # 31
    def test_admin_can_assign_course_to_trainer(self):
        self.client.login(
            username="admin",
            password="Admin@12345",
        )

        response = self.client.post(
            reverse(
                "assign_trainer_course",
                args=[self.other_trainer.id],
            ),
            {
                "course": self.course.id,
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "trainer_detail",
                args=[self.other_trainer.id],
            ),
        )

        self.assertTrue(
            TrainerCourse.objects.filter(
                trainer=self.other_trainer,
                course=self.course,
            ).exists()
        )


# ============================================================
# DASHBOARD / VIEW TESTS
# 32 - 35
# ============================================================


class DashboardTests(StudentPortalTestSetup):

    # 32
    def test_student_dashboard_requires_student_role(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # 33
    def test_student_dashboard_loads_for_student(self):
        self.client.login(
            username="student",
            password="Student@12345",
        )

        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Test Student",
        )

    # 34
    def test_admin_dashboard_loads_for_admin(self):
        self.client.login(
            username="admin",
            password="Admin@12345",
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    # 35
    def test_trainer_dashboard_loads_for_approved_trainer(self):
        self.client.login(
            username="trainer",
            password="Trainer@12345",
        )

        response = self.client.get(
            reverse("trainer_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Python",
        )