from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    UserProfile,
    Department,
    Course,
    Student,
    Enrollment,
    TrainerCourse,
    MarkHistory,
    Feedback,
    AuditLog,
)


# ============================================================
# COMMON TEST SETUP
# ============================================================

class StudentPortalTestSetup(TestCase):

    def setUp(self):

        # -------------------------------------------------
        # ADMIN
        # -------------------------------------------------

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


        # -------------------------------------------------
        # TRAINER
        # -------------------------------------------------

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


        # -------------------------------------------------
        # SECOND TRAINER
        # -------------------------------------------------

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


        # -------------------------------------------------
        # STUDENT USER
        # -------------------------------------------------

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


        # -------------------------------------------------
        # DEPARTMENT
        # -------------------------------------------------

        self.department = Department.objects.create(
            name="Information Technology",
            description="IT Department",
        )


        # -------------------------------------------------
        # COURSES
        # -------------------------------------------------

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


        # -------------------------------------------------
        # STUDENT
        # -------------------------------------------------

        self.student = Student.objects.create(
            user=self.student_user,
            name="Test Student",
            email="student@test.com",
            age=22,
            department=self.department,
            active=True,
        )


        # -------------------------------------------------
        # ENROLLMENT
        # -------------------------------------------------

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            marks=70,
        )


        # -------------------------------------------------
        # TRAINER ASSIGNMENT
        # -------------------------------------------------

        TrainerCourse.objects.create(
            trainer=self.trainer,
            course=self.course,
        )

        TrainerCourse.objects.create(
            trainer=self.other_trainer,
            course=self.other_course,
        )


# ============================================================
# 1 - 3 AUTHENTICATION TESTS
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
            reverse("dashboard"),
        )

        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )


    # 2
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


    # 3
    def test_failed_login_increments_attempt_counter(self):

        self.client.post(
            reverse("login"),
            {
                "login": "trainer",
                "password": "WrongPassword@123",
            },
        )

        profile = self.trainer.profile

        self.assertEqual(
            profile.failed_login_attempts,
            1,
        )


# ============================================================
# 4 - 10 AUTHORIZATION TESTS
# ============================================================

class AuthorizationTests(StudentPortalTestSetup):

    # 6
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


    # 7
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
                "reason": "Updated test marks",
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


    # 8
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


    # 9
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


    # 10
    def test_student_can_only_view_own_student_detail(self):

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


# ============================================================
# 11 - 15 MARKS TESTS
# ============================================================

class MarksTests(StudentPortalTestSetup):

    # 11
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


    # 12
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

        self.assertEqual(
            history.reason,
            "Improved performance",
        )


    # 13
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


    # 14
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


    # 15
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


# ============================================================
# 16 - 20 FEEDBACK TESTS
# ============================================================

class FeedbackTests(StudentPortalTestSetup):

    # 16
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


    # 17
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


    # 18
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


    # 19
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

        self.assertEqual(
            feedback.comment,
            "Great improvement.",
        )


    # 20
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


# ============================================================
# 21 - 25 TRAINER / MODEL TESTS
# ============================================================

class TrainerManagementTests(StudentPortalTestSetup):

    # 21
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


    # 22
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


    # 23
    def test_enrollment_unique_student_course(self):

        with self.assertRaises(Exception):

            Enrollment.objects.create(
                student=self.student,
                course=self.course,
                marks=90,
            )


    # 24
    def test_trainer_course_assignment_is_unique(self):

        with self.assertRaises(Exception):

            TrainerCourse.objects.create(
                trainer=self.trainer,
                course=self.course,
            )


    # 25
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