from django.db.models import Avg, Q
from django.db import transaction
from .models import Student, Department, Course, AuditLog, Feedback, MarksHistory


def get_dashboard_stats():
    """
    Computes dashboard analytics for the Student Training Portal.
    """
    students_qs = Student.objects.all()
    
    total_students = students_qs.count()
    active_students = students_qs.filter(active_status=True).count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()
    
    avg_result = students_qs.aggregate(avg=Avg('marks'))['avg']
    avg_marks = round(avg_result, 1) if avg_result is not None else 0.0
    
    highest_scoring_student = students_qs.order_by('-marks', 'name').first()
    recently_joined_students = (
        students_qs.select_related('department')
        .prefetch_related('courses')
        .order_by('-joined_date', '-id')[:5]
    )
    
    return {
        'total_students': total_students,
        'active_students': active_students,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'avg_marks': avg_marks,
        'highest_scoring_student': highest_scoring_student,
        'recently_joined_students': recently_joined_students,
    }


def filter_students(params):
    """
    Filters student records based on request query parameters.
    Params supported:
      - q: search query for student name, email, department, or course name
      - department: department ID filter
      - course: course ID filter
      - active_status: 'active' or 'inactive'
      - pass_fail_status: 'pass' (marks >= 50) or 'fail' (marks < 50)
    """
    qs = Student.objects.select_related('department').prefetch_related('courses').all()
    
    q_search = params.get('q', '').strip()
    if q_search:
        qs = qs.filter(
            Q(name__icontains=q_search) |
            Q(email__icontains=q_search) |
            Q(course__icontains=q_search) |
            Q(courses__course_name__icontains=q_search) |
            Q(department__name__icontains=q_search)
        )
    
    dept_id = params.get('department', '').strip()
    if dept_id and dept_id.isdigit():
        qs = qs.filter(department_id=int(dept_id))
        
    course_id = params.get('course', '').strip()
    if course_id and course_id.isdigit():
        qs = qs.filter(courses__id=int(course_id))
        
    active_param = params.get('active_status', '').strip().lower()
    if active_param == 'active':
        qs = qs.filter(active_status=True)
    elif active_param == 'inactive':
        qs = qs.filter(active_status=False)
        
    pass_fail_param = params.get('pass_fail_status', '').strip().lower()
    if pass_fail_param == 'pass':
        qs = qs.filter(marks__gte=50)
    elif pass_fail_param == 'fail':
        qs = qs.filter(marks__lt=50)
        
    return qs.distinct().order_by('-joined_date', '-id')


def get_trainer_dashboard_stats(trainer_user):
    """
    Computes summary metrics and retrieves assigned courses & students for a trainer.
    """
    assigned_courses = Course.objects.filter(assigned_trainer=trainer_user)
    students = Student.objects.filter(courses__in=assigned_courses).distinct().order_by('name')
    
    total_courses = assigned_courses.count()
    total_students = students.count()
    
    avg_result = students.aggregate(avg=Avg('marks'))['avg']
    avg_marks = round(avg_result, 1) if avg_result is not None else 0.0
    
    stats = {
        'total_courses': total_courses,
        'total_students': total_students,
        'avg_marks': avg_marks,
    }
    
    return {
        'assigned_courses': assigned_courses,
        'students': students,
        'stats': stats,
    }


def get_student_dashboard_data(user):
    """
    Retrieves student record, enrolled courses, and profile completion percentage.
    """
    student = getattr(user, 'student', None)
    if not student:
        return {'student': None, 'courses': [], 'profile_completion': 0}
        
    courses = student.courses.all()
    profile_completion = calculate_profile_completion(student)
    
    return {
        'student': student,
        'courses': courses,
        'profile_completion': profile_completion,
    }


def calculate_profile_completion(student):
    """
    Calculates profile completion percentage based on phone, address, and date of birth.
    """
    profile = getattr(student, 'profile', None)
    if not profile:
        return 0
    filled = 0
    if profile.phone:
        filled += 1
    if profile.address:
        filled += 1
    if profile.date_of_birth:
        filled += 1
    return int((filled / 3.0) * 100)


@transaction.atomic
def update_student_marks(student, course, new_marks, updater_user, reason="Marks updated", ip_address=None):
    """
    Updates student's marks, creates a MarksHistory entry, and logs an AuditLog.
    """
    old_marks = student.marks
    student.marks = new_marks
    student.save()

    marks_history = MarksHistory.objects.create(
        student=student,
        course=course,
        previous_marks=old_marks,
        new_marks=new_marks,
        updater=updater_user,
        reason=reason
    )

    course_info = f" in course '{course.course_name}'" if course else ""
    updater_role = getattr(getattr(updater_user, 'profile', None), 'role', 'User').capitalize()
    
    AuditLog.objects.create(
        user=updater_user,
        action='marks_update',
        affected_object=f"Student: {student.name}",
        description=f"{updater_role} {updater_user.username} updated marks for {student.name}{course_info} from {old_marks} to {new_marks}.",
        ip_address=ip_address
    )

    return student, marks_history


@transaction.atomic
def create_feedback(student, trainer_user, course, rating, comments, is_visible=True, ip_address=None):
    """
    Creates a new Feedback record and logs an AuditLog entry.
    """
    feedback = Feedback.objects.create(
        student=student,
        trainer=trainer_user,
        course=course,
        rating=rating,
        comments=comments,
        is_visible=is_visible
    )

    AuditLog.objects.create(
        user=trainer_user,
        action='feedback_creation',
        affected_object=f"Student: {student.name}",
        description=f"Trainer {trainer_user.username} created feedback for {student.name} in course '{course.course_name}'.",
        ip_address=ip_address
    )

    return feedback


def can_user_view_student(user, student):
    """
    Helper to check if a user is permitted to view a specific student's details.
    - Superusers and Admins: Yes
    - Trainers: Yes if assigned to at least one course of the student
    - Student: Yes if viewing their own profile
    """
    if user.is_superuser or getattr(getattr(user, 'profile', None), 'role', None) == 'admin':
        return True
    if getattr(getattr(user, 'profile', None), 'role', None) == 'trainer':
        return student.courses.filter(assigned_trainer=user).exists()
    if getattr(getattr(user, 'profile', None), 'role', None) == 'student':
        student_obj = getattr(user, 'student', None)
        return student_obj is not None and student_obj.id == student.id
    return False


def can_user_edit_student(user, student):
    """
    Helper to check if a user is permitted to edit a specific student.
    - Superusers and Admins: Full edit permission
    - Trainers: Marks edit permission only if assigned to at least one course of the student
    """
    if user.is_superuser or getattr(getattr(user, 'profile', None), 'role', None) == 'admin':
        return True
    if getattr(getattr(user, 'profile', None), 'role', None) == 'trainer':
        return student.courses.filter(assigned_trainer=user).exists()
    return False

