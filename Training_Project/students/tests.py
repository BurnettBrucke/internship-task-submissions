from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import (
    Student,
    Department,
    StudentProfile,
    Course,
    UserProfile,
    CourseMark,
    AuditLog,
)
from .forms import (
    StudentForm,
    RegistrationForm,
    FeedbackForm,
    MarksUpdateForm,
)

class StudentPortalTests(TestCase):

    def setUp(self):

        # =========================================================
        # 1. Create Admin User
        # =========================================================

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword'
        )

        UserProfile.objects.create(
            user=self.user,
            role='admin',
            is_approved=True
        )

        # =========================================================
        # 2. Create Trainer User
        # =========================================================

        self.trainer = User.objects.create_user(
            username='trainer',
            password='trainerpassword'
        )

        UserProfile.objects.create(
            user=self.trainer,
            role='trainer',
            is_approved=True
        )

        # =========================================================
        # 3. Create Student User
        # =========================================================

        self.student_user = User.objects.create_user(
            username='student',
            password='studentpassword'
        )

        UserProfile.objects.create(
            user=self.student_user,
            role='student',
            is_approved=True
        )

        # =========================================================
        # 4. Create Department
        # =========================================================

        self.department = Department.objects.create(
            name='Computer Science',
            description='Computer Science Department'
        )

        # =========================================================
        # 5. Create Student
        # =========================================================

        self.student = Student.objects.create(
            name='Rahul',
            email='rahul@gmail.com',
            age=22,
            marks=80,
            joined_date='2026-09-01',
            active=True,
            department=self.department
        )

        # Connect Student record with Student User
        self.student.user = self.student_user
        self.student.save()

        # =========================================================
        # 6. Create Course
        # =========================================================

        self.course = Course.objects.create(
            course_name='Django',
            code='DJ101',
            duration='3 Months',
            active=True
        )

    # =============================================================
    # 1. Student list loads
    # =============================================================

    def test_student_list_loads(self):

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('student_list')
        )

        self.assertEqual(response.status_code, 200)

    # =============================================================
    # 2. Student detail loads
    # =============================================================

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

    # =============================================================
    #  Student can access only their own data
    # =============================================================

    def test_student_cannot_access_other_student_data(self):

        # Create another student
        other_student_user = User.objects.create_user(
            username='otherstudent',
            password='otherpassword'
        )

        UserProfile.objects.create(
            user=other_student_user,
            role='student',
            is_approved=True
        )

        other_student = Student.objects.create(
            name='Amit',
            email='amit@gmail.com',
            age=23,
            marks=75,
            joined_date='2026-09-02',
            active=True,
            department=self.department,
            user=other_student_user
        )

        # Login as Rahul
        self.client.login(
            username='student',
            password='studentpassword'
        )

        # Try to access Amit's student detail
        response = self.client.get(
            reverse(
                'student_detail',
                args=[other_student.id]
            )
        )

        # Student should be blocked
        self.assertEqual(
            response.status_code,
            403
        )

    # Trainer can update marks only for assigned students
    def test_trainer_can_update_assigned_student_marks(self):

        # Assign student to course
        self.course.students.add(self.student)

        # Assign trainer to course
        self.course.trainer.add(self.trainer)

        # Login as trainer
        self.client.login(
            username='trainer',
            password='trainerpassword'
        )

        # Update marks
        response = self.client.post(
            reverse(
                'update_marks',
                args=[self.student.id, self.course.id]
            ),
            {
                'marks': 90,
                'reason': 'Improved performance'
            }
        )

        # Successful update should redirect
        self.assertEqual(
            response.status_code,
            302
        )

        # Verify marks were saved
        course_mark = CourseMark.objects.get(
            student=self.student,
            course=self.course
        )

        self.assertEqual(
            course_mark.marks,
            90
        )

        self.assertEqual(
            course_mark.updated_by,
            self.trainer
        )

    # Trainer cannot update marks for unassigned course
    def test_trainer_cannot_update_unassigned_student_marks(self):

        # Student is enrolled in the course
        self.course.students.add(self.student)

        # IMPORTANT:
        # Trainer is NOT assigned to this course

        # Login as trainer
        self.client.login(
            username='trainer',
            password='trainerpassword'
        )

        # Try to update marks
        response = self.client.post(
            reverse(
                'update_marks',
                args=[self.student.id, self.course.id]
            ),
            {
                'marks': 95,
                'reason': 'Unauthorized update'
            }
        )

        # Trainer should be blocked
        self.assertEqual(
            response.status_code,
            403
        )

        # No CourseMark should be created
        self.assertFalse(
            CourseMark.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    # Student cannot directly POST marks update
    def test_student_cannot_update_marks_directly(self):

        # Enroll student in the course
        self.course.students.add(self.student)

        # Assign trainer to the course
        self.course.trainer.add(self.trainer)

        # Login as student
        self.client.login(
            username='student',
            password='studentpassword'
        )

        # Student directly sends POST request
        response = self.client.post(
            reverse(
                'update_marks',
                args=[self.student.id, self.course.id]
            ),
            {
                'marks': 95,
                'reason': 'Unauthorized student update'
            }
        )

        # Student should be blocked
        self.assertEqual(
            response.status_code,
            403
        )

        # Marks should not be created
        self.assertFalse(
            CourseMark.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    # =============================================================
    # 3. Valid student creation
    # =============================================================

    def test_valid_student_creation(self):

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        data = {
            'name': 'Priya',
            'email': 'priya@gmail.com',
            'age': 21,
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

    # =============================================================
    # 4. Invalid student form
    # =============================================================

    def test_invalid_student_form(self):

        form = StudentForm(data={
            'name': '',
            'email': 'wrong-email',
            'age': 10,
            'marks': 150,
            'joined_date': '2026-09-01',
            'active': True,
        })

        self.assertFalse(form.is_valid())

    # =============================================================
    # 5. Student update
    # =============================================================

    def test_student_update(self):

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        data = {
            'name': 'Rahul Updated',
            'email': 'rahul_updated@gmail.com',
            'age': 23,
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

    # =============================================================
    # 6. Student delete
    # =============================================================

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

    # =============================================================
    # 7. Login page loads
    # =============================================================

    def test_login_page_loads(self):

        response = self.client.get(
            reverse('login')
        )

        self.assertEqual(response.status_code, 200)

    # =============================================================
    # 8. Successful login
    # =============================================================

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

        self.assertEqual(
            response.url,
            reverse('dashboard')
        )

    # =============================================================
    # 9. Protected page redirects unauthenticated user
    # =============================================================

    def test_protected_page_redirects(self):

        response = self.client.get(
            reverse('student_list')
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            '/login/',
            response.url
        )

    # =============================================================
    # 10. Department relationship
    # =============================================================

    def test_department_relationship(self):

        self.assertEqual(
            self.student.department,
            self.department
        )

        self.assertIn(
            self.student,
            self.department.students.all()
        )

    # =============================================================
    # 11. One-to-One StudentProfile
    # =============================================================

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

    # =============================================================
    # 12. Many-to-Many Course
    # =============================================================

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

    # =============================================================
    # 13. Student search
    # =============================================================

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

    # =============================================================
    # 14. Department filter
    # =============================================================

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

    # =============================================================
    # 15. Dashboard totals
    # =============================================================

    def test_dashboard_totals(self):

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('admin_dashboard')
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

    # =============================================================
    # 16. Admin can access admin dashboard
    # =============================================================

    def test_admin_dashboard_access(self):

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # =============================================================
    # 17. Trainer can access trainer dashboard
    # =============================================================

    def test_trainer_dashboard_access(self):

        self.client.login(
            username='trainer',
            password='trainerpassword'
        )

        response = self.client.get(
            reverse('trainer_dashboard')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # =============================================================
    # 18. Student can access student dashboard
    # =============================================================

    def test_student_dashboard_access(self):

        self.client.login(
            username='student',
            password='studentpassword'
        )

        response = self.client.get(
            reverse('student_dashboard')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # =============================================================
    # 19. Student is blocked from admin dashboard
    # =============================================================

    def test_student_blocked_from_admin_dashboard(self):

        self.client.login(
            username='student',
            password='studentpassword'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(
            response.status_code,
            403
        )

    # =============================================================
    # 20. Trainer is blocked from admin dashboard
    # =============================================================

    def test_trainer_blocked_from_admin_dashboard(self):

        self.client.login(
            username='trainer',
            password='trainerpassword'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(
            response.status_code,
            403
        )

    # Registration form accepts valid data
    def test_registration_form_valid_data(self):

        form = RegistrationForm(data={
            'username': 'newstudent',
            'email': 'newstudent@gmail.com',
            'role': 'student',
            'password1': 'StrongPass@123',
            'password2': 'StrongPass@123',
        })

        self.assertTrue(form.is_valid())


    # Registration form rejects weak password
    def test_registration_form_rejects_weak_password(self):

        form = RegistrationForm(data={
            'username': 'newstudent',
            'email': 'newstudent@gmail.com',
            'role': 'student',
            'password1': '123',
            'password2': '123',
        })

        self.assertFalse(form.is_valid())

    # Registration rejects duplicate email
    def test_registration_rejects_duplicate_email(self):

        form = RegistrationForm(data={
            'username': 'anotheruser',
            'email': 'testuser@gmail.com',
            'role': 'student',
            'password1': 'StrongPass@123',
            'password2': 'StrongPass@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    # Account is blocked after 5 failed login attempts
    def test_login_blocked_after_five_failed_attempts(self):

        for _ in range(5):
            self.client.post(
                reverse('login'),
                {
                    'username': 'testuser',
                    'password': 'wrongpassword'
                }
            )

        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'testpassword'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Too many failed login attempts'
        )

    # Registration rejects mismatched passwords
    def test_registration_rejects_mismatched_passwords(self):

        form = RegistrationForm(data={
            'username': 'mismatchuser',
            'email': 'mismatch@gmail.com',
            'role': 'student',
            'password1': 'StrongPass@123',
            'password2': 'DifferentPass@123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    # Registration rejects password same as username
    def test_registration_rejects_password_same_as_username(self):

        form = RegistrationForm(data={
            'username': 'sameuser',
            'email': 'sameuser@gmail.com',
            'role': 'student',
            'password1': 'sameuser',
            'password2': 'sameuser',
        })

        self.assertFalse(form.is_valid())

    # Registration rejects password same as email
    def test_registration_rejects_password_same_as_email(self):

        form = RegistrationForm(data={
            'username': 'emailuser',
            'email': 'emailuser@gmail.com',
            'role': 'student',
            'password1': 'emailuser@gmail.com',
            'password2': 'emailuser@gmail.com',
        })

        self.assertFalse(form.is_valid())

    # 25. Successful login creates audit log
    def test_successful_login_creates_audit_log(self):

        self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'testpassword'
            }
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.user,
                action='User Login'
            ).exists()
        )


    # 26. Failed login creates audit log
    def test_failed_login_creates_audit_log(self):

        self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )

        self.assertTrue(
            AuditLog.objects.filter(
                action='Failed Login'
            ).exists()
        )


    # 27. Successful logout creates audit log
    def test_logout_creates_audit_log(self):

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        self.client.post(reverse('logout'))

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.user,
                action='User Logout'
            ).exists()
        )


    # 28. Marks update creates audit log
    def test_marks_update_creates_audit_log(self):

        self.course.students.add(self.student)
        self.course.trainer.add(self.trainer)

        self.client.login(
            username='trainer',
            password='trainerpassword'
        )

        self.client.post(
            reverse(
                'update_marks',
                args=[self.student.id, self.course.id]
            ),
            {
                'marks': 90,
                'reason': 'Improved performance'
            }
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.trainer,
                action='Marks Updated'
            ).exists()
        )


    # 29. Feedback creation creates audit log
    def test_feedback_creation_creates_audit_log(self):

        self.course.students.add(self.student)
        self.course.trainer.add(self.trainer)

        self.client.login(
            username='trainer',
            password='trainerpassword'
        )

        self.client.post(
            reverse(
                'add_feedback',
                args=[self.student.id, self.course.id]
            ),
            {
                'rating': 5,
                'comment': 'Excellent performance',
                'is_visible': True
            }
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.trainer,
                action='Feedback Created'
            ).exists()
        )


    # 30. Student cannot see hidden feedback
    def test_student_cannot_see_hidden_feedback(self):

        from .models import Feedback

        self.course.students.add(self.student)
        self.course.trainer.add(self.trainer)

        Feedback.objects.create(
            student=self.student,
            trainer=self.trainer,
            course=self.course,
            rating=4,
            comment='Private feedback',
            is_visible=False
        )

        self.client.login(
            username='student',
            password='studentpassword'
        )

        response = self.client.get(
            reverse('student_detail', args=[self.student.id])
        )

        self.assertNotContains(
            response,
            'Private feedback'
        )