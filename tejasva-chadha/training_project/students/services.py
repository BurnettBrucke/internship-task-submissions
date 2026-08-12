from django.db.models import Avg, Q
from .models import Student, Department, Course

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
