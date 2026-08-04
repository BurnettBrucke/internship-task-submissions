# audit log function ke liye taki baar baar view mai audit log object create na krna pde just function call ho
from django.utils import timezone
from .models import AuditLog


def create_audit_log(request, user, action, description, object_name=''):
    ip = request.META.get("REMOTE_ADDR")
    AuditLog.objects.create(
        user=user,
        action=action,
        object_name=object_name,
        description=description,
        ip_address=ip,
    )


def ensure_profile_and_student(user):
    
    # Local imports to avoid circular import issues with models.py
    from .models import UserProfile, Student, StudentProfile

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": "ADMIN" if user.is_superuser else "STUDENT"},
    )

    if profile.role == "STUDENT" and not hasattr(user, "student"):
        student = Student.objects.create(
            user=user,
            name=user.get_full_name() or user.username,
            email=user.email or f"{user.username}@example.com",
            marks=0,
            join_date=timezone.now().date(),
            active_status="fail",
        )
        StudentProfile.objects.create(student=student)

    return profile
