from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class UserProfile(models.Model):

    class Role(models.TextChoices):
        ADMIN ="ADMIN" , "Administrator"
        TRAINER = "TRAINER" , "Trainer"
        STUDENT = "STUDENT" , "Student"

    class Status(models.TextChoices):
        PENDING = "PENDING" , "Pending"
        APPROVED = "APPROVED" , "Approved"
        REJECTED = "REJECTED" , "Rejected"

    user = models.OneToOneField(
        User ,  on_delete= models.CASCADE,
        related_name= "profile"
    )

    role = models.CharField(
        max_length = 20 , choices = Role.choices
    )
    status = models.CharField(
        max_length = 20  , choices= Status.choices , default = Status.APPROVED #may be need to be change later
    )
    requested_course = models.ForeignKey("Course",on_delete = models.SET_NULL,null=True,blank=True,related_name="trainer_requests")

    failed_login_attempts = models.PositiveBigIntegerField(default=0)

    login_blocked = models.BooleanField(default = False)

    login_blocked_at = models.DateTimeField(null = True , blank = True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.role}"


class Course(models.Model):
    course_name = models.CharField(max_length= 100)
    code = models.CharField(max_length = 20)
    duration = models.CharField(max_length = 50)
    duration_days = models.PositiveIntegerField(default=30)
    active_status = models.BooleanField(default= True)
    def __str__(self):
        return f"{self.course_name} ({self.code})"


class Department(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    def __str__(self):
        return self.name

class Student(models.Model):

    user = models.OneToOneField(
        User , on_delete= models.CASCADE, related_name = "student" , null= True , blank = True, 
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    joined_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students",
        null = True,
        blank = True
    )

    def __str__(self):
        return self.name
    @property
    def profile_completion_data(self):
    
        total = 7
        completed = 0
    
        # Student model fields
        if self.name and self.name.strip():
            completed += 1
    
        if self.email and self.email.strip():
            completed += 1
    
        if self.age is not None:
            completed += 1
    
        if self.department_id is not None:
            completed += 1
    
        # StudentProfile fields
        try:
            profile = self.profile
    
            if profile.phone and profile.phone.strip():
                completed += 1
    
            if profile.address and profile.address.strip():
                completed += 1
    
            if profile.date_of_birth is not None:
                completed += 1
    
        except StudentProfile.DoesNotExist:
            pass
        
        percentage = round((completed / total) * 100)
    
        return {
            "completed": completed,
            "total": total,
            "percentage": percentage,
        }
    
class StudentProfile(models.Model):
    student = models.OneToOneField( 
         Student, on_delete=models.CASCADE, related_name="profile" ) 
    phone = models.CharField(max_length=15 , blank = True) 
    address = models.TextField(blank = True) 
    date_of_birth = models.DateField(null=True, blank = True) 

    def __str__(self): 
        return f"{self.student.name}'s Profile"

    
class Enrollment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    enrolled_at = models.DateField(
        default=timezone.localdate
    )

    marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course"
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"

    @property
    def progress_percentage(self):

        today = timezone.localdate()

        total_days = self.course.duration_days

        if total_days <= 0:
            return 0

        days_passed = (today - self.enrolled_at).days

        progress = (days_passed / total_days) * 100

        return min(max(round(progress), 0), 100)
    @property
    def end_date(self):

        from datetime import timedelta

        return self.enrolled_at + timedelta(
            days=self.course.duration_days
        )    
    
class TrainerCourse(models.Model):
    trainer = models.ForeignKey(
        User , on_delete=models.CASCADE , related_name="trainer_courses"
    )

    course = models.ForeignKey(
        Course , on_delete = models.CASCADE, related_name = "trainer_assignments"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trainer" , "course"],
                name = "unique_trainer_course"
            )
        ]
    def __str__(self):
        return f"{self.trainer.email} - {self.course.course_name}"

class MarkHistory(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="mark_history"
    )

    previous_marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    new_marks = models.PositiveIntegerField()

    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="mark_updates"
    )

    reason = models.TextField()

    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.enrollment.student.name} - "
            f"{self.enrollment.course.course_name} - "
            f"{self.new_marks}"
        )


class Feedback(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="feedback"
    )

    trainer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="given_feedback"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="feedback"
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField()

    visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.course.course_name} - "
            f"{self.rating}/5"
        )

class AuditLog(models.Model):

    class Action(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        FAILED_LOGIN = "FAILED_LOGIN", "Failed Login"
        CREATE = "CREATE", "Create"
        UPDATE = "UPDATE", "Update"
        DELETE = "DELETE", "Delete"
        MARKS_UPDATE = "MARKS_UPDATE", "Marks Update"
        FEEDBACK_CREATE = "FEEDBACK_CREATE", "Feedback Create"
        ACCOUNT_STATUS_CHANGE = (
            "ACCOUNT_STATUS_CHANGE",
            "Account Status Change",
        )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=30,
        choices=Action.choices,
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    # Generic relation to the affected object
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    affected_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        username = self.user.username if self.user else "System"

        return (
            f"{username} - "
            f"{self.get_action_display()} - "
            f"{self.timestamp}"
        )