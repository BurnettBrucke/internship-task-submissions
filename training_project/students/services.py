from django.db.models import Avg, Max, Q

from .models import Student, Department, Course


def get_dashboard_data():

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        active_status=True
    ).count()

    total_departments = Department.objects.count()

    total_courses = Course.objects.count()

    average_marks = Student.objects.aggregate(
        average=Avg('marks')
    )['average']

    highest_marks = Student.objects.aggregate(
        highest=Max('marks')
    )['highest']

    highest_student = None

    if highest_marks is not None:
        highest_student = Student.objects.filter(
            marks=highest_marks
        ).first()

    recent_students = Student.objects.order_by(
        '-joined_date'
    )[:5]

    return {
        'total_students': total_students,
        'active_students': active_students,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'average_marks': average_marks,
        'highest_marks': highest_marks,
        'highest_student': highest_student,
        'recent_students': recent_students,
    }


def get_filtered_students(params):

    students = Student.objects.all()

    # Search
    search = params.get('search')

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        )

    # Department filter
    department = params.get('department')

    if department:
        students = students.filter(
            department_id=department
        )

    # Course filter
    course = params.get('course')

    if course:
        students = students.filter(
            courses__id=course
        )

    # Active status filter
    active_status = params.get('active_status')

    if active_status == 'active':
        students = students.filter(
            active_status=True
        )

    elif active_status == 'inactive':
        students = students.filter(
            active_status=False
        )

    # Pass / Fail filter
    status = params.get('status')

    if status == 'pass':
        students = students.filter(
            marks__gte=40
        )

    elif status == 'fail':
        students = students.filter(
            marks__lt=40
        )

    return students.distinct()