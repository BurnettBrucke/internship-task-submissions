from .models import AuditLog


def create_audit_log(
    *,
    user,
    action,
    object_name,
    description,
    request,
):

    AuditLog.objects.create(
        user=user,
        action=action,
        object_name=object_name,
        description=description,
        ip_address=request.META.get(
            "REMOTE_ADDR",
            "Unknown",
        ),
    )