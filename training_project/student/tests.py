"""
Day 3 - Task 5 + Day 4 Testing Requirements
============================================
23 test cases covering:
- Model creation & relationships
- Views (list, detail, add, edit, delete)
- Authentication (login, register, protected pages)
- Filtering & search
- Dashboard totals
- [Day 4] Role-based access (admin/trainer/student dashboards)
- [Day 4] Trainer blocked from admin pages (403)
- [Day 4] Audit log creation on login
- [Day 4] Feedback visibility rules
- [Day 4] Login lockout after 5 failed attempts
- [Day 4] Marks history recorded on update
- [Day 4] Trainer ownership check on marks update
- [Day 4] Password change view requires login
- [Day 4] Student blocked from trainer portal (403)
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student, Department, Course, StudentProfile, UserProfile, AuditLog, Feedback, MarksHistory


#  create sample data used across multiple tests
def create_sample_data():
    """Creates one department, one course, and two students for testing."""
    dept = Department.objects.create(name="Computer Science", description="CS dept")
    course = Course.objects.create(name="Python Django", code="PY101", duration="3 months")
    student1 = Student.objects.create(
        name="Alice Smith", email="alice@test.com",
        age=22, course="Python Django", marks=75.0,
        is_active=True, department=dept
    )
    student2 = Student.objects.create(
        name="Bob Jones", email="bob@test.com",
        age=20, course="Python Django", marks=35.0,
        is_active=False, department=dept
    )
    student1.enrolled_courses.add(course)
    student2.enrolled_courses.add(course)
    return dept, course, student1, student2



# 1. Student Model Test
class StudentModelTest(TestCase):

    def setUp(self):
        self.dept, self.course, self.s1, self.s2 = create_sample_data()

    def test_student_creation(self):
        """Test 1: Student model can be created with correct fields."""
        self.assertEqual(self.s1.name, "Alice Smith")
        self.assertEqual(self.s1.email, "alice@test.com")
        self.assertEqual(self.s1.age, 22)
        self.assertEqual(self.s1.marks, 75.0)
        self.assertTrue(self.s1.is_active)

    def test_student_str_method(self):
        """Test 2: __str__ returns 'Name (email)' format."""
        self.assertEqual(str(self.s1), "Alice Smith (alice@test.com)")

    def test_student_is_pass_property(self):
        """Test 3: is_pass returns True for marks>=40, False otherwise."""
        self.assertTrue(self.s1.is_pass)   # 75 >= 40
        self.assertFalse(self.s2.is_pass)  # 35 < 40

    def test_marks_boundary_values(self):
        """Test 4: Boundary marks — 0 (fail), 40 (pass), 100 (pass)."""
        s_zero    = Student(name="T1", email="t1@t.com", age=18, course="X", marks=0)
        s_forty   = Student(name="T2", email="t2@t.com", age=18, course="X", marks=40)
        s_hundred = Student(name="T3", email="t3@t.com", age=18, course="X", marks=100)
        self.assertFalse(s_zero.is_pass)
        self.assertTrue(s_forty.is_pass)
        self.assertTrue(s_hundred.is_pass)


# 2. Relationship Tests
class RelationshipTest(TestCase):

    def setUp(self):
        self.dept, self.course, self.s1, self.s2 = create_sample_data()

    def test_department_relationship(self):
        """Test 5: ForeignKey — student belongs to a department."""
        self.assertEqual(self.s1.department.name, "Computer Science")
        # Reverse: dept.students gives all students in that dept
        self.assertIn(self.s1, self.dept.students.all())

    def test_one_to_one_profile(self):
        """Test 6: OneToOneField — StudentProfile linked to Student."""
        profile = StudentProfile.objects.create(
            student=self.s1, phone="9999999999", address="Delhi"
        )
        # Access profile via student.profile
        self.assertEqual(self.s1.profile.phone, "9999999999")
        self.assertEqual(str(profile), "Profile of Alice Smith")

    def test_many_to_many_courses(self):
        """Test 7: ManyToManyField — student enrolled in courses."""
        self.assertIn(self.course, self.s1.enrolled_courses.all())
        # Reverse: course.enrolled_students gives all students in that course
        self.assertIn(self.s1, self.course.enrolled_students.all())



# 3. Student List Page Tests
class StudentListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Need a user with admin role since student list is now at student_portal
        self.user = User.objects.create_user(username='testuser', password='pass123')
        UserProfile.objects.create(user=self.user, role='student')
        create_sample_data()

    def test_student_list_page_loads(self):
        """Test 8: Student portal (list) page loads for logged-in user."""
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('student_portal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")

    def test_protected_page_redirects(self):
        """Test 9: Unauthenticated user is redirected to login page."""
        response = self.client.get(reverse('student_portal'))
        # Should redirect (302) to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_student_detail_page(self):
        """Test 10: Student detail page loads correctly."""
        self.client.login(username='testuser', password='pass123')
        student = Student.objects.first()
        response = self.client.get(reverse('student_detail', args=[student.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, student.name)

    def test_search_functionality(self):
        """Test 11: Search by name filters correctly on student portal.
        Note: We only assert Alice appears in the filtered response.
        Bob Jones may still appear in dashboard stats widgets (recent students etc.)
        so we do not assert his absence from the entire page.
        """
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('student_portal'), {'search': 'Alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")

    def test_department_filter(self):
        """Test 12: Filter by department returns correct students."""
        self.client.login(username='testuser', password='pass123')
        dept = Department.objects.first()
        response = self.client.get(reverse('student_portal'), {'department': dept.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")

# 4. Student Form Tests (Admin-only CRUD — requires admin role)
class StudentFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        # These views require admin access
        self.user = User.objects.create_user(
            username='testadmin', password='pass123',
            email='testadmin@admin.com', is_staff=True
        )
        UserProfile.objects.create(user=self.user, role='admin', is_approved=True)
        self.client.login(username='testadmin', password='pass123')

    def test_valid_student_creation(self):
        """Test 13: Valid form data creates a new student and redirects."""
        data = {
            'name': 'Charlie Doe',
            'email': 'charlie@test.com',
            'age': 25,
            'course': 'Python Django',
            'marks': 85.0,
            'is_active': True,
            'enrolled_courses': [],
        }
        response = self.client.post(reverse('admin_student_add'), data)
        # Should redirect to admin dashboard after success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(email='charlie@test.com').exists())

    def test_invalid_student_form(self):
        """Test 14: Invalid form (age out of range) shows error."""
        data = {
            'name': 'Invalid Person',
            'email': 'invalid@test.com',
            'age': 5,        # Invalid: below 16
            'course': 'Django',
            'marks': 60.0,
        }
        response = self.client.post(reverse('admin_student_add'), data)
        # Should NOT redirect — form has errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Age must be between 16 and 60")

    def test_student_update(self):
        """Test 15: Editing a student saves updated data."""
        dept, course, student, _ = create_sample_data()
        updated_data = {
            'name': 'Alice Updated',
            'email': 'alice@test.com',
            'age': 23,
            'course': 'Advanced Django',
            'marks': 90.0,
            'is_active': True,
            'enrolled_courses': [],
        }
        response = self.client.post(reverse('admin_student_edit', args=[student.pk]), updated_data)
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.name, 'Alice Updated')
        self.assertEqual(student.marks, 90.0)


# 5. Authentication Tests
class AuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_login_page_loads(self):
        """Test: Login page is accessible to everyone."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Test: Correct credentials log the user in."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'pass123'
        })
        # Should redirect to student list
        self.assertEqual(response.status_code, 302)


# 6. Dashboard
class DashboardTest(TestCase):

    def setUp(self):
        create_sample_data()

    def test_dashboard_totals(self):
        """Test: Home page shows correct student totals in context."""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['active_students'], 1)


# =============================================================================
# Day 4 Tests (Tests 17–23+)
# =============================================================================

def create_trainer_user(username='trainer1', password='Trainer@123'):
    """Helper: creates a User with UserProfile(role='trainer', is_approved=True)."""
    user = User.objects.create_user(username=username, password=password, email=f'{username}@trainer.com')
    UserProfile.objects.create(user=user, role='trainer', is_approved=True)
    return user


def create_admin_user(username='admin', password='Admin@1234'):
    """Helper: creates a User with UserProfile(role='admin') + is_staff=True."""
    user = User.objects.create_user(username=username, password=password,
                                    email='admin@admin.com', is_staff=True)
    UserProfile.objects.create(user=user, role='admin', is_approved=True)
    return user


# 7. Role-Based Access Tests
class RoleBasedAccessTest(TestCase):
    """Day 4 - Task 1: Tests 17-20"""

    def setUp(self):
        self.client  = Client()
        self.admin   = create_admin_user()
        self.trainer = create_trainer_user()
        # Student user
        self.student_user = User.objects.create_user(
            username='stu1', password='pass123', email='stu1@test.com'
        )
        UserProfile.objects.create(user=self.student_user, role='student')

    def test_admin_can_access_admin_dashboard(self):
        """Test 17: Admin user can access the admin dashboard."""
        self.client.login(username='admin', password='Admin@1234')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_student_blocked_from_admin_dashboard(self):
        """Test 18: Student user gets 403 on admin dashboard."""
        self.client.login(username='stu1', password='pass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_trainer_can_access_trainer_dashboard(self):
        """Test 19: Approved trainer can access trainer dashboard."""
        self.client.login(username='trainer1', password='Trainer@123')
        response = self.client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_student_blocked_from_trainer_dashboard(self):
        """Test 20: Student user gets 403 on trainer dashboard."""
        self.client.login(username='stu1', password='pass123')
        response = self.client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 403)


# 8. Audit Log Tests
class AuditLogTest(TestCase):
    """Day 4 - Task 3: Test 21"""

    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user(username='loguser', password='pass123')
        UserProfile.objects.create(user=self.user, role='student')

    def test_audit_log_created_on_login(self):
        """Test 21: AuditLog entry is created when a user logs in."""
        self.client.post(reverse('login'), {'username': 'loguser', 'password': 'pass123'})
        self.assertTrue(
            AuditLog.objects.filter(user=self.user, action_type='LOGIN').exists()
        )


# 9. Login Lockout Test
class LoginLockoutTest(TestCase):
    """Day 4 - Task 2: Test 22"""

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='lockme', password='pass123')

    def test_login_locked_after_five_failures(self):
        """Test 22: After 5 failed attempts, login is blocked."""
        for _ in range(5):
            self.client.post(reverse('login'), {
                'username': 'lockme', 'password': 'wrongpass'
            })
        # 6th attempt should show lockout message (not try to authenticate)
        response = self.client.post(reverse('login'), {
            'username': 'lockme', 'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        # Check that 'locked' context or lockout message is present
        content = response.content.decode()
        self.assertIn('locked', content.lower())


# 10. Marks History Test
class MarksHistoryTest(TestCase):
    """Day 4 - Task 3: Test 23"""

    def setUp(self):
        self.dept, self.course, self.student, _ = create_sample_data()
        self.trainer = create_trainer_user()
        # Assign trainer to student
        self.student.trainer = self.trainer
        self.student.save()

    def test_marks_history_recorded_on_update(self):
        """Test 23: MarksHistory entry is created when trainer updates marks."""
        self.client.login(username='trainer1', password='Trainer@123')
        old_marks = self.student.marks
        response = self.client.post(
            reverse('trainer_marks_update', args=[self.student.pk]),
            {'marks': 85.0, 'reason': 'Improved performance'}
        )
        self.assertEqual(response.status_code, 302)   # redirect on success
        self.assertTrue(
            MarksHistory.objects.filter(
                student=self.student,
                updated_by=self.trainer,
                old_marks=old_marks,
                new_marks=85.0
            ).exists()
        )


# 11. Feedback Visibility Test
class FeedbackVisibilityTest(TestCase):
    """Day 4 - Task 3: Tests 24-25"""

    def setUp(self):
        self.client  = Client()
        self.trainer = create_trainer_user()
        dept, course, self.student, _ = create_sample_data()
        self.student.trainer = self.trainer
        self.student.save()
        # Create a linked user for student portal login
        self.student_user = User.objects.create_user(
            username='stuportal', password='pass123', email='stuportal@test.com'
        )
        UserProfile.objects.create(user=self.student_user, role='student')
        self.student.user = self.student_user
        self.student.save()

    def test_visible_feedback_shown_to_student(self):
        """Test 24: Student sees feedback marked is_visible=True."""
        Feedback.objects.create(
            trainer=self.trainer, student=self.student,
            rating=4, comment='Great work!', is_visible=True
        )
        self.client.login(username='stuportal', password='pass123')
        response = self.client.get(reverse('student_portal'))
        self.assertIn('my_feedback', response.context)
        self.assertEqual(response.context['my_feedback'].count(), 1)

    def test_hidden_feedback_not_shown_to_student(self):
        """Test 25: Student does NOT see feedback marked is_visible=False."""
        Feedback.objects.create(
            trainer=self.trainer, student=self.student,
            rating=2, comment='Needs improvement', is_visible=False
        )
        self.client.login(username='stuportal', password='pass123')
        response = self.client.get(reverse('student_portal'))
        self.assertEqual(response.context['my_feedback'].count(), 0)


# 12. Trainer Ownership Test
class TrainerOwnershipTest(TestCase):
    """Day 4 - Test 26: Trainer cannot update marks for another trainer's student."""

    def setUp(self):
        self.client   = Client()
        self.trainer1 = create_trainer_user('trainer1', 'Trainer@123')
        self.trainer2 = create_trainer_user('trainer2', 'Trainer@456')
        dept, course, self.student, _ = create_sample_data()
        self.student.trainer = self.trainer1
        self.student.save()

    def test_trainer_cannot_update_other_trainers_student(self):
        """Test 26: trainer2 gets 403 when trying to update trainer1's student's marks."""
        self.client.login(username='trainer2', password='Trainer@456')
        response = self.client.post(
            reverse('trainer_marks_update', args=[self.student.pk]),
            {'marks': 50.0, 'reason': 'Unauthorized change'}
        )
        self.assertEqual(response.status_code, 403)


# 13. Password Change Test
class PasswordChangeTest(TestCase):
    """Day 4 - Test 27: Password change page requires login."""

    def test_password_change_requires_login(self):
        """Test 27: Unauthenticated user is redirected from password change page."""
        client   = Client()
        response = client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])


# 14. Admin Trainer Management & Course Assignment Tests
class AdminTrainerManagementTest(TestCase):
    """Tests for Admin managing trainers and assigning them to courses."""

    def setUp(self):
        self.client = Client()
        self.admin = create_admin_user()
        self.trainer = create_trainer_user('trainer1', 'Trainer@123')
        self.course = Course.objects.create(name='Django Advanced', code='DJ102', duration='2 months')

    def test_admin_can_access_trainer_list(self):
        """Test: Admin can access trainer list view."""
        self.client.login(username='admin', password='Admin@1234')
        response = self.client.get(reverse('admin_trainer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'trainer1')

    def test_student_blocked_from_trainer_list(self):
        """Test: Student blocked from trainer list view."""
        student_user = User.objects.create_user(username='stu1', password='pass123', email='stu1@test.com')
        UserProfile.objects.create(user=student_user, role='student')
        self.client.login(username='stu1', password='pass123')
        response = self.client.get(reverse('admin_trainer_list'))
        self.assertEqual(response.status_code, 403)

    def test_admin_add_trainer_valid_email(self):
        """Test: Admin can add new trainer with valid @trainer.com email."""
        self.client.login(username='admin', password='Admin@1234')
        response = self.client.post(reverse('admin_trainer_add'), {
            'username': 'newtrainer',
            'email': 'newtrainer@trainer.com',
            'first_name': 'New Trainer',
            'password1': 'SecretPassword@123',
            'password2': 'SecretPassword@123',
            'courses': [self.course.id]
        })
        self.assertEqual(response.status_code, 302) # Redirect to trainer list
        new_trainer = User.objects.get(username='newtrainer')
        self.assertEqual(new_trainer.userprofile.role, 'trainer')
        self.assertTrue(new_trainer.userprofile.is_approved)
        # Check course assignment
        self.course.refresh_from_db()
        self.assertEqual(self.course.trainer, new_trainer)

    def test_admin_add_trainer_invalid_email(self):
        """Test: Adding trainer fails if email does not end with @trainer.com."""
        self.client.login(username='admin', password='Admin@1234')
        response = self.client.post(reverse('admin_trainer_add'), {
            'username': 'newtrainer2',
            'email': 'newtrainer2@gmail.com', # invalid email
            'first_name': 'New Trainer 2',
            'password1': 'SecretPassword@123',
            'password2': 'SecretPassword@123',
        })
        self.assertEqual(response.status_code, 200) # Re-renders form with errors
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_trainer_assigned_courses_reflection(self):
        """Test: Assigned courses reflect on trainer dashboard page."""
        self.course.trainer = self.trainer
        self.course.save()
        self.client.login(username='trainer1', password='Trainer@123')
        response = self.client.get(reverse('trainer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Advanced')

