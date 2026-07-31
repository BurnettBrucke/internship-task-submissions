# audit log function ke liye taki baar baar view mai audit log object create na krna pde just function call ho
from .models import AuditLog

def create_audit_log(request,user,action,description,object_name=''):
    ip=request.META.get("REMOTE_ADDR")
    AuditLog.objects.create(
        user=user,
        action=action,
        object_name=object_name,
        description=description,
        ip_address=ip
    )