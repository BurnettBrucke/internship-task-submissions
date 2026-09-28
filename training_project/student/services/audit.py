from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from ..models import AuditLog, CourseMark, MarksHistory
from ..utils import get_client_ip



def create_audit_log(
    request,
    action_type,
    description,
    affected_object=None,
    action=None,
):
    """
    Create a centralized audit log entry.
    """

    content_type = None
    object_id = None

    if affected_object is not None:
        content_type = ContentType.objects.get_for_model( 
            affected_object
        )
        object_id = affected_object.pk

    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action or action_type,
        action_type=action_type,
        description=description,
        content_type=content_type,
        object_id=object_id,
        ip_address=get_client_ip(request),
    )


