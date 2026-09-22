from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Student,
    Department,
    Course,
    StudentProfile,
    UserProfile
)


class StudentPortalTests(TestCase):

    def setUp(self):

        # Create Department
        self.department = Department.objects.create(
            name='Computer Science',
            description='Computer Science Department'
        )

        self.department2 = Department.objects.create(
            name='Information Technology',
            description='Information Technology Department'
        )

        # Create Courses
        self.course = Course.objects.create(
            course_name='Python Django',
            code='PD101',
            duration='6 Months',
            active_status=True
        )

        self.course2 = Course.objects.create(
            course_name='Python FastAPI',
            code='FA101',
            duration='4 Months',
            active_status=True
        )

        # Create Student
        self.student = Student.objects.create(
            name='Kalyani',
            email='kalyani@gmail.com',
            age=22,
            department=self.department,
            marks=85,
            joined_date='2026-09-01',
            active_status=True
        )

        self.student.courses.add(self.course)

        # Create another student
        self.student2 = Student.objects.create(
            name='Riya',
            email='riya@gmail.com',
            age=24,
            department=self.department2,
            marks=35,
            joined_date='2026-08-20',
            active_status=False
        )

        self.student2.courses.add(self.course2)

        # Create Test User
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword123'
        )
        
        UserProfile.objects.create(
            user=self.user,
            role='admin',
            is_approved=True
        )


    # -------------------------------------------------
    # 1. Student List Page
    # -------------------------------------------------

    def test_student_list_page(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list')
        )

        self.assertEqual(response.status_code, 200)


    # -------------------------------------------------
    # 2. Student Detail Page
    # -------------------------------------------------

    def test_student_detail_page(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse(
                'student_detail',
                args=[self.student.pk]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kalyani')


    # -------------------------------------------------
    # 3. Dashboard Page
    # -------------------------------------------------

    def test_dashboard_page(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
           reverse('dashboard')
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse('admin_dashboard')
        )


    # -------------------------------------------------
    # 4. Successful Login
    # -------------------------------------------------

    def test_successful_login(self):

        response = self.client.post(
            reverse('login'),
            {
                'email': 'testuser@gmail.com',
                'password': 'testpassword123'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse('admin_dashboard')
        )


    # -------------------------------------------------
    # 5. Invalid Login
    # -------------------------------------------------

    def test_invalid_login(self):

        response = self.client.post(
            reverse('login'),
            {
                'email': 'testuser@gmail.com',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'Invalid email or password.'
        )


    # -------------------------------------------------
    # 6. Protected Student List
    # -------------------------------------------------

    def test_student_list_requires_login(self):

        response = self.client.get(
            reverse('student_list')
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse('login') + '?next=' +
            reverse('student_list')
        )


    # -------------------------------------------------
    # 7. Protected Dashboard
    # -------------------------------------------------

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse('login') + '?next=' +
            reverse('dashboard')
        )


    # -------------------------------------------------
    # 8. Create Student
    # -------------------------------------------------

    def test_create_student(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.post(
            reverse('add_student'),
            {
                'name': 'Neha',
                'email': 'neha@gmail.com',
                'age': 21,
                'department': self.department.pk,
                'courses': [self.course.pk],
                'marks': 75,
                'joined_date': '2026-09-05',
                'active_status': True,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Student.objects.filter(
                email='neha@gmail.com'
            ).exists()
        )


    # -------------------------------------------------
    # 9. Invalid Student Form
    # -------------------------------------------------

    def test_invalid_student_form(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.post(
            reverse('add_student'),
            {
                'name': '',
                'email': 'invalid-email',
                'age': 10,
                'department': self.department.pk,
                'courses': [self.course.pk],
                'marks': 150,
                'joined_date': '2026-09-05',
                'active_status': True,
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Student.objects.filter(
                email='invalid-email'
            ).exists()
        )


    # -------------------------------------------------
    # 10. Update Student
    # -------------------------------------------------

    def test_update_student(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.post(
            reverse(
                'edit_student',
                args=[self.student.pk]
            ),
            {
                'name': 'Kalyani Updated',
                'email': 'kalyani@gmail.com',
                'age': 23,
                'department': self.department.pk,
                'courses': [self.course.pk],
                'marks': 90,
                'joined_date': '2026-09-01',
                'active_status': True,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.name,
            'Kalyani Updated'
        )

        self.assertEqual(
            self.student.marks,
            90
        )


    # -------------------------------------------------
    # 11. Delete Student
    # -------------------------------------------------

    def test_delete_student(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.post(
            reverse(
                'delete_student',
                args=[self.student.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Student.objects.filter(
                pk=self.student.pk
            ).exists()
        )


    # -------------------------------------------------
    # 12. Department Filter
    # -------------------------------------------------

    def test_department_filter(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'department': self.department.pk
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Kalyani')

        self.assertNotContains(response, 'Riya')


    # -------------------------------------------------
    # 13. Course Filter
    # -------------------------------------------------

    def test_course_filter(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'course': self.course.pk
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Kalyani')

        self.assertNotContains(response, 'Riya')


    # -------------------------------------------------
    # 14. Active Status Filter
    # -------------------------------------------------

    def test_active_status_filter(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'active_status': 'active'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Kalyani')

        self.assertNotContains(response, 'Riya')


    # -------------------------------------------------
    # 15. Pass Filter
    # -------------------------------------------------

    def test_pass_filter(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'status': 'pass'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Kalyani')

        self.assertNotContains(response, 'Riya')


    # -------------------------------------------------
    # 16. Fail Filter
    # -------------------------------------------------

    def test_fail_filter(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'status': 'fail'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Riya')

        self.assertNotContains(response, 'Kalyani')


    # -------------------------------------------------
    # 17. Student Search
    # -------------------------------------------------

    def test_student_search(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'search': 'Kalyani'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Kalyani')

        self.assertNotContains(response, 'Riya')


    # -------------------------------------------------
    # 18. One-to-One Student Profile
    # -------------------------------------------------

    def test_student_profile_one_to_one(self):

        profile = StudentProfile.objects.create(
            student=self.student,
            phone='9876543210',
            address='Indore',
            date_of_birth='2003-09-28'
        )

        self.assertEqual(
            profile.student,
            self.student
        )

        self.assertEqual(
            self.student.profile,
            profile
        )


    # -------------------------------------------------
    # 19. Many-to-Many Courses
    # -------------------------------------------------

    def test_student_many_to_many_courses(self):

        self.student.courses.add(self.course2)

        self.assertEqual(
            self.student.courses.count(),
            2
        )

        self.assertIn(
            self.course2,
            self.student.courses.all()
        )


    # -------------------------------------------------
    # 20. Dashboard Totals
    # -------------------------------------------------

    def test_dashboard_totals(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse('admin_dashboard')
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '2')

        # -------------------------------------------------
    # 21. Admin Dashboard Direct Access
    # -------------------------------------------------

    def test_admin_dashboard_access(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 200)


    # -------------------------------------------------
    # 22. Student Form Invalid Age
    # -------------------------------------------------

    def test_student_form_invalid_age(self):

        from .forms import StudentForm

        form = StudentForm(data={
            'name': 'Test Student',
            'email': 'teststudent@gmail.com',
            'age': 10,
            'department': self.department.pk,
            'courses': [self.course.pk],
            'marks': 75,
            'joined_date': '2026-09-05',
            'active_status': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)


    # -------------------------------------------------
    # 23. Student Form Invalid Marks
    # -------------------------------------------------

    def test_student_form_invalid_marks(self):

        from .forms import StudentForm

        form = StudentForm(data={
            'name': 'Test Student',
            'email': 'teststudent2@gmail.com',
            'age': 21,
            'department': self.department.pk,
            'courses': [self.course.pk],
            'marks': 150,
            'joined_date': '2026-09-05',
            'active_status': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('marks', form.errors)


    # -------------------------------------------------
    # 24. Student Cannot Access Admin Dashboard
    # -------------------------------------------------

    def test_student_cannot_access_admin_dashboard(self):

        student_user = User.objects.create_user(
            username='studentuser',
            email='studentuser@gmail.com',
            password='studentpassword123'
        )

        UserProfile.objects.create(
            user=student_user,
            role='student',
            student=self.student,
            is_approved=True
        )

        self.client.login(
            username='studentuser',
            password='studentpassword123'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 403)


    # -------------------------------------------------
    # 25. Student Dashboard Access
    # -------------------------------------------------

    def test_student_dashboard_access(self):

        student_user = User.objects.create_user(
            username='studentdashboard',
            email='studentdashboard@gmail.com',
            password='studentpassword123'
        )

        UserProfile.objects.create(
            user=student_user,
            role='student',
            student=self.student,
            is_approved=True
        )

        self.client.login(
            username='studentdashboard',
            password='studentpassword123'
        )

        response = self.client.get(
            reverse('student_dashboard')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kalyani')

        # -------------------------------------------------
    # 26. Logout
    # -------------------------------------------------

    def test_logout(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('logout')
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('login')
        )


    # -------------------------------------------------
    # 27. Failed Login Increments Attempt Count
    # -------------------------------------------------

    def test_failed_login_increments_attempt_count(self):

        response = self.client.post(
            reverse('login'),
            {
                'email': 'testuser@gmail.com',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.user.profile.refresh_from_db()

        self.assertEqual(
            self.user.profile.failed_login_attempts,
            1
        )


    # -------------------------------------------------
    # 28. Search With Department Filter
    # -------------------------------------------------

    def test_search_with_department_filter(self):

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

        response = self.client.get(
            reverse('student_list'),
            {
                'search': 'Kalyani',
                'department': self.department.pk
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kalyani')
        self.assertNotContains(response, 'Riya')


    # -------------------------------------------------
    # 29. Trainer Cannot Access Admin Dashboard
    # -------------------------------------------------

    def test_trainer_cannot_access_admin_dashboard(self):

        trainer_user = User.objects.create_user(
            username='traineruser',
            email='traineruser@gmail.com',
            password='trainerpassword123'
        )

        UserProfile.objects.create(
            user=trainer_user,
            role='trainer',
            is_approved=True
        )

        self.client.login(
            username='traineruser',
            password='trainerpassword123'
        )

        response = self.client.get(
            reverse('admin_dashboard')
        )

        self.assertEqual(response.status_code, 403)


    # -------------------------------------------------
    # 30. Student Cannot Create Student
    # -------------------------------------------------

    def test_student_cannot_create_student(self):

        student_user = User.objects.create_user(
            username='studentcreate',
            email='studentcreate@gmail.com',
            password='studentpassword123'
        )

        UserProfile.objects.create(
            user=student_user,
            role='student',
            student=self.student,
            is_approved=True
        )

        self.client.login(
            username='studentcreate',
            password='studentpassword123'
        )

        response = self.client.get(
            reverse('add_student')
        )

        self.assertEqual(response.status_code, 403)