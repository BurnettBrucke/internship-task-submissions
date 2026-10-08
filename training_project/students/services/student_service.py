import os

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from ..models import (
    Student,
    StudentProfile,
    UserProfile,
    Enrollment,
)


@transaction.atomic
def create_student_account(
    name,
    email,
    age,
    active,
    department,
    request,
):
    """
    Create the complete student account.

    This service creates:
    - Django User
    - UserProfile
    - Student
    - StudentProfile

    The operation is atomic so that a partial account is not
    created if one of the database operations fails.
    """

    user = User.objects.create_user(
        username=email,
        email=email,
    )

    user.set_unusable_password()
    user.save()

    UserProfile.objects.create(
        user=user,
        role=UserProfile.Role.STUDENT,
        status=UserProfile.Status.APPROVED,
    )

    student = Student.objects.create(
        user=user,
        name=name,
        email=email,
        age=age,
        active=active,
        department=department,
    )

    StudentProfile.objects.create(
        student=student,
    )

    send_student_activation_email(
        student,
        request,
    )

    return student


def enroll_student_in_courses(student, courses):
    """
    Create enrollments for a student.

    Existing enrollments are ignored so this function can safely
    be reused by views or a future API.
    """

    existing_course_ids = set(
        Enrollment.objects.filter(
            student=student,
            course__in=courses,
        ).values_list(
            "course_id",
            flat=True,
        )
    )

    new_enrollments = [
        Enrollment(
            student=student,
            course=course,
        )
        for course in courses
        if course.id not in existing_course_ids
    ]

    if new_enrollments:
        Enrollment.objects.bulk_create(
            new_enrollments
        )

    return new_enrollments


def update_student_courses(student, selected_courses):
    """
    Synchronize a student's course enrollments.

    Courses no longer selected are removed and missing courses
    are added.
    """

    selected_course_ids = {
        course.id
        for course in selected_courses
    }

    Enrollment.objects.filter(
        student=student
    ).exclude(
        course_id__in=selected_course_ids
    ).delete()

    existing_course_ids = set(
        Enrollment.objects.filter(
            student=student,
            course_id__in=selected_course_ids,
        ).values_list(
            "course_id",
            flat=True,
        )
    )

    new_enrollments = [
        Enrollment(
            student=student,
            course=course,
        )
        for course in selected_courses
        if course.id not in existing_course_ids
    ]

    if new_enrollments:
        Enrollment.objects.bulk_create(
            new_enrollments
        )

    return new_enrollments


def send_student_activation_email(student, request):
    """
    Generate and send the student password-setup email.

    Kept in the student service because activation is part of
    the student-account creation workflow.
    """

    uid = urlsafe_base64_encode(
        force_bytes(student.user.pk)
    )

    token = default_token_generator.make_token(
        student.user
    )

    activation_path = reverse(
        "set_student_password",
        kwargs={
            "uidb64": uid,
            "token": token,
        },
    )

    activation_url = request.build_absolute_uri(
        activation_path
    )

    subject = "Set Your Student Account Password"

    text_content = f"""
Hello {student.name},

Your student account has been created successfully.

Please use the link below to set your password:

{activation_url}

After setting your password, you can log in to the Student Management System.

Regards,
Student Management System
"""

    html_content = f"""
<html>
    <body>
        <h2>Welcome, {student.name}!</h2>

        <p>
            Your student account has been created successfully.
        </p>

        <p>
            Please click the link below to set your password:
        </p>

        <p>
            <a href="{activation_url}">
                Set Your Password
            </a>
        </p>

        <p>
            After setting your password, you can log in
            to the Student Management System.
        </p>

        <p>
            Regards,<br>
            Student Management System
        </p>
    </body>
</html>
"""

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=os.getenv("EMAIL_USER"),
        to=[student.email],
    )

    email_message.attach_alternative(
        html_content,
        "text/html",
    )

    email_message.send()