from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import os

from .models import Student, StudentProfile, UserProfile


@transaction.atomic
def create_student_account(
    name,
    email,
    age,
    active,
    department,
    request,
):
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


def send_student_activation_email(student, request):

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