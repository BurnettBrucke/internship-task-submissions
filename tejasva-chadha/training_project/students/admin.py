from django.contrib import admin
from .models import Student, Department, Course, StudentProfile, AuditLog, Feedback, MarksHistory

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'student'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'code', 'duration', 'active_status')
    list_filter = ('active_status', 'duration')
    search_fields = ('course_name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'department', 'display_courses', 'marks', 'joined_date', 'active_status')
    list_filter = ('active_status', 'department', 'courses', 'joined_date')
    search_fields = ('name', 'email')
    inlines = (StudentProfileInline,)

    def display_courses(self, obj):
        return ", ".join([c.course_name for c in obj.courses.all()])
    display_courses.short_description = 'Courses'

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'phone', 'date_of_birth')
    search_fields = ('student__name', 'phone')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'affected_object', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'description', 'affected_object')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'trainer', 'course', 'rating', 'is_visible', 'created_at')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('student__name', 'trainer__username', 'comments')


@admin.register(MarksHistory)
class MarksHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'previous_marks', 'new_marks', 'updater', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('student__name', 'updater__username', 'reason')


