from django.contrib import admin
from .models import AuditLog
from .models import Student, Department, StudentProfile, Course, UserProfile


admin.site.register(Student)

admin.site.register(Department)

admin.site.register(StudentProfile)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'course_name',
        'code',
        'duration',
        'trainer',
        'active'
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'role')

    list_filter = ('role',)

    search_fields = ('user__username', 'user__email')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'description')
    ordering = ('-timestamp',)