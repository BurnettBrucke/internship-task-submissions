from django.contrib import admin
from .models import Student, Department, Course, StudentProfile, TrainerProfile, UserProfile,AuditLog


admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(StudentProfile)
admin.site.register(UserProfile)
admin.site.register(TrainerProfile)
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'action']
    ordering = ['-created_at']
