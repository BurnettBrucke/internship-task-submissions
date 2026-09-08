from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
import os

def send_mail(student):
    dashbord_path = reverse(
        "student_detail" , 
        kwargs={"id": student.id}
    )
    dashboard_url = f"http://127.0.0.1:8000{dashbord_path}"

    subject = "Welcome to the Student Management System"

    text_content = f"""
Hello {student.name},

Your student account has been successfully created.

You can access your student dashboard here:

{dashboard_url}

Regards,
Student Management System
"""

    html_content = f"""
    <html>
        <body>
            <h2>Welcome, {student.name}!</h2>

            <p>
                Your student account has been successfully created.
            </p>

            <p>
                You can access your student dashboard using the link below:
            </p>

            <a href="{dashboard_url}">
                Open Student Dashboard
            </a>

            <p>
                Regards,<br>
                Student Management System
            </p>
        </body>
    </html>
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=os.getenv("EMAIL_USER"),
        to=[student.email],
    )

    email.attach_alternative(
        html_content,
        "text/html"
    )

    email.send()