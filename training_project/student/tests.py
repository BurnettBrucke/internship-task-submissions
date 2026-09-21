from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    UserProfile,
    student,
    department,
    Course,
    AuditLog,
    Feedback,
    CourseMark,
    MarksHistory,
)


class ProjectTestCase(TestCase):

    def setUp(self):
        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

        self.admin = User.objects.create_user(
            username="admin_test",
            password="Admin@12345"
        )

        self.trainer = User.objects.create_user(
            username="trainer_test",
            password="Trainer@12345"
        )

        self.trainer2 = User.objects.create_user(
            username="trainer2_test",
            password="Trainer@12345"
        )

        self.student_user = User.objects.create_user(
            username="student_test",
            password="Student@12345"
        )

        self.student_user2 = User.objects.create_user(
            username="student2_test",
            password="Student@12345"
        )

        # -------------------------------------------------
        # USER PROFILES
        # -------------------------------------------------

        UserProfile.objects.create(
            user=self.admin,
            role="admin",
            is_approved=True,
            is_active=True
        )

        UserProfile.objects.create(
            user=self.trainer,
            role="trainer",
            is_approved=True,
            is_active=True
        )

        UserProfile.objects.create(
            user=self.trainer2,
            role="trainer",
            is_approved=True,
            is_active=True
        )

        UserProfile.objects.create(
            user=self.student_user,
            role="student",
            is_approved=True,
            is_active=True
        )

        UserProfile.objects.create(
            user=self.student_user2,
            role="student",
            is_approved=True,
            is_active=True
        )

        # -------------------------------------------------
        # DEPARTMENT
        # -------------------------------------------------

        self.department = department.objects.create(
            name="Computer Science"
        )

        # -------------------------------------------------
        # STUDENTS
        # -------------------------------------------------

        self.student1 = student.objects.create(
            user=self.student_user,
            name="Student One",
            email="student1@test.com",
            age=22,
            course="Python",
            marks=70,
            active=True,
            department=self.department
        )

        self.student2 = student.objects.create(
            user=self.student_user2,
            name="Student Two",
            email="student2@test.com",
            age=23,
            course="Django",
            marks=80,
            active=True,
            department=self.department
        )

        # -------------------------------------------------
        # COURSE
        # -------------------------------------------------

        self.course = Course.objects.create(
            course_name="Django Development",
            code="DJ101",
            duration=3,
            active_status=True,
            trainer=self.trainer
        )

        self.course.students.add(self.student1)

        # Second course for unauthorized trainer tests
        self.course2 = Course.objects.create(
            course_name="Python Development",
            code="PY101",
            duration=3,
            active_status=True,
            trainer=self.trainer2
        )

        self.course2.students.add(self.student2)

        # -------------------------------------------------
        # CLIENT
        # -------------------------------------------------

        self.client = Client()

    # =====================================================
    # 23. ROLE DASHBOARDS
    # =====================================================

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(
            username="admin_test",
            password="Admin@12345"
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(response.status_code, 200)

    def test_trainer_can_access_trainer_dashboard(self):
        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse("trainer_dashboard")
        )

        self.assertEqual(response.status_code, 200)

    def test_student_can_access_student_dashboard(self):
        self.client.login(
            username="student_test",
            password="Student@12345"
        )

        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(response.status_code, 200)

    # =====================================================
    # 24. ADMIN PAGE PROTECTION
    # =====================================================

    def test_student_blocked_from_audit_logs(self):
        self.client.login(
            username="student_test",
            password="Student@12345"
        )

        response = self.client.get(
            reverse("audit_log_list")
        )

        self.assertIn(response.status_code, [302, 403])

    def test_trainer_blocked_from_audit_logs(self):
        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse("audit_log_list")
        )

        self.assertIn(response.status_code, [302, 403])

    # =====================================================
    # 25. STUDENT OWN DATA
    # =====================================================

    def test_student_can_view_own_detail(self):
        self.client.login(
            username="student_test",
            password="Student@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                kwargs={"pk": self.student1.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_student_cannot_view_other_student(self):
        self.client.login(
            username="student_test",
            password="Student@12345"
        )

        response = self.client.get(
            reverse(
                "student_detail",
                kwargs={"pk": self.student2.pk}
            )
        )

        self.assertIn(response.status_code, [302, 403, 404])

    # =====================================================
    # 26. TRAINER ASSIGNMENT
    # =====================================================

    def test_assigned_trainer_can_update_marks(self):
        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_unassigned_trainer_cannot_update_marks(self):
        self.client.login(
            username="trainer2_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            )
        )

        self.assertIn(response.status_code, [302, 403, 404])

    # =====================================================
    # 27. UNAUTHORIZED DIRECT POST
    # =====================================================

    def test_student_cannot_update_marks_using_post(self):
        self.client.login(
            username="student_test",
            password="Student@12345"
        )

        response = self.client.post(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            ),
            {
                "marks": 95,
                "reason": "Unauthorized update"
            }
        )

        self.assertIn(response.status_code, [302, 403, 404])

        # Marks must remain unchanged
        self.student1.refresh_from_db()

        self.assertEqual(
            self.student1.marks,
            70
        )

    def test_unassigned_trainer_cannot_post_marks(self):
        self.client.login(
            username="trainer2_test",
            password="Trainer@12345"
        )

        response = self.client.post(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            ),
            {
                "marks": 90,
                "reason": "Unauthorized"
            }
        )

        self.assertIn(response.status_code, [302, 403, 404])

    # =====================================================
    # 28. REGISTRATION / PASSWORD VALIDATION
    # =====================================================

    def test_registration_rejects_password_mismatch(self):

        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password1": "StrongPassword@123",
                "password2": "DifferentPassword@123",
                "role": "student",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            User.objects.filter(
                username="newuser"
            ).exists()
        )

    def test_registration_rejects_existing_username(self):

        response = self.client.post(
            reverse("register"),
            {
                "username": "student_test",
                "email": "newemail@test.com",
                "password1": "StrongPassword@123",
                "password2": "StrongPassword@123",
                "role": "student",
            }
        )

        self.assertEqual(response.status_code, 200)

        # Only original user should exist
        self.assertEqual(
            User.objects.filter(
                username="student_test"
            ).count(),
            1
        )

    def test_registration_rejects_invalid_email(self):

        response = self.client.post(
            reverse("register"),
            {
                "username": "invalid_email_user",
                "email": "not-an-email",
                "password1": "StrongPassword@123",
                "password2": "StrongPassword@123",
                "role": "student",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            User.objects.filter(
                username="invalid_email_user"
            ).exists()
        )

    # =====================================================
    # 29. AUDIT LOGS
    # =====================================================

    def test_successful_login_creates_audit_log(self):

        before = AuditLog.objects.count()

        self.client.post(
            reverse("login"),
            {
                "username": "student_test",
                "password": "Student@12345"
            }
        )

        after = AuditLog.objects.count()

        self.assertGreater(
            after,
            before
        )

    def test_failed_login_creates_audit_log(self):

        before = AuditLog.objects.count()

        self.client.post(
            reverse("login"),
            {
                "username": "student_test",
                "password": "WrongPassword"
            }
        )

        after = AuditLog.objects.count()

        self.assertGreater(
            after,
            before
        )

    def test_audit_log_records_user(self):

        self.client.post(
            reverse("login"),
            {
                "username": "student_test",
                "password": "Student@12345"
            }
        )

        log = AuditLog.objects.order_by("-created_at").first()

        self.assertIsNotNone(log)

        self.assertEqual(
            log.user,
            self.student_user
        )

    # =====================================================
    # 30. FEEDBACK VISIBILITY
    # =====================================================

    def test_assigned_trainer_can_create_feedback(self):

        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse(
                "feedback_create",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_unassigned_trainer_cannot_create_feedback(self):

        self.client.login(
            username="trainer2_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse(
                "feedback_create",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            )
        )

        self.assertIn(
            response.status_code,
            [302, 403, 404]
        )

    # =====================================================
    # 31. TEMPLATE RENDERING
    # =====================================================

    def test_student_dashboard_uses_base_template(self):

        self.client.login(
            username="student_test",
            password="Student@12345"
        )

        response = self.client.get(
            reverse("student_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "<html",
            html=False
        )

    def test_trainer_dashboard_renders(self):

        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse("trainer_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_admin_dashboard_renders(self):

        self.client.login(
            username="admin_test",
            password="Admin@12345"
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # =====================================================
    # 32. MARKS VALIDATION
    # =====================================================

    def test_marks_cannot_be_above_100(self):

        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.post(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            ),
            {
                "marks": 101,
                "reason": "Invalid marks"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_marks_cannot_be_below_zero(self):

        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.post(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            ),
            {
                "marks": -1,
                "reason": "Invalid marks"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_valid_marks_are_accepted(self):

        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.post(
            reverse(
                "update_course_marks",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            ),
            {
                "marks": 90,
                "reason": "Performance improvement"
            }
        )

        self.assertIn(
            response.status_code,
            [200, 302]
        )

    # =====================================================
    # MARKS HISTORY
    # =====================================================

    def test_marks_history_page_accessible(self):

        self.client.login(
            username="trainer_test",
            password="Trainer@12345"
        )

        response = self.client.get(
            reverse(
                "marks_history",
                kwargs={
                    "course_id": self.course.pk,
                    "student_id": self.student1.pk,
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        ) 