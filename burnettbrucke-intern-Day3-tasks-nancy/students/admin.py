from django.contrib import admin

from .models import Course, Department, Student, StudentProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration_weeks', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'department', 'marks', 'joined_date', 'is_active')
    list_filter = ('is_active', 'department', 'courses')
    search_fields = ('name', 'email')
    filter_horizontal = ('courses',)
    inlines = [StudentProfileInline]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'phone', 'date_of_birth')
    search_fields = ('student__name', 'phone')
