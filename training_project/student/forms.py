from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Student, Department, Course, UserProfile, Feedback, MarksHistory


# ──────────────────────────────────────────────────────────────────────────────
# Student ModelForm  (Admin only — full CRUD)
# ──────────────────────────────────────────────────────────────────────────────
class StudentForm(forms.ModelForm):

    class Meta:
        model  = Student
        fields = ['name', 'email', 'age', 'course', 'marks',
                  'is_active', 'department', 'enrolled_courses', 'trainer']
        widgets = {
            'enrolled_courses': forms.CheckboxSelectMultiple(),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("Email cannot be empty.")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            raise forms.ValidationError("Age is required.")
        if age < 16 or age > 60:
            raise forms.ValidationError("Age must be between 16 and 60.")
        return age

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is None:
            raise forms.ValidationError("Marks are required.")
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks

    def clean_course(self):
        """Course cannot be empty."""
        course = self.cleaned_data.get('course', '').strip()
        if not course:
            raise forms.ValidationError("Course cannot be empty.")
        return course


# ──────────────────────────────────────────────────────────────────────────────
# Student Self-Edit Form  (Students only — edit own profile, no marks/dept)
# ──────────────────────────────────────────────────────────────────────────────
class StudentSelfEditForm(forms.ModelForm):
    """Students can only edit their name, age and course — not marks or status."""

    class Meta:
        model  = Student
        fields = ['name', 'age', 'course']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 16 or age > 60):
            raise forms.ValidationError("Age must be between 16 and 60.")
        return age

    def clean_course(self):
        course = self.cleaned_data.get('course', '').strip()
        if not course:
            raise forms.ValidationError("Course cannot be empty.")
        return course


# ──────────────────────────────────────────────────────────────────────────────
# Student Registration Form  (Public — creates both User + Student)
# ──────────────────────────────────────────────────────────────────────────────
class StudentRegistrationForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to also collect student-specific fields.
    On save(), creates a Django User + a linked Student record +
    a UserProfile with role='student'.
    """
    email      = forms.EmailField(required=True,  help_text="Required. Use your personal email.")
    first_name = forms.CharField(max_length=100,  required=True,  label="Full Name")
    age        = forms.IntegerField(required=True, label="Age")
    course     = forms.CharField(max_length=100,  required=True, label="Course (e.g. Python Django)")

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

    # ── Validation ────────────────────────────────────────────────────────────
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 16 or age > 60):
            raise forms.ValidationError("Age must be between 16 and 60.")
        return age

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name', '').strip()
        if not name:
            raise forms.ValidationError("Full name cannot be empty.")
        return name

    def save(self, commit=True):
        """Create User, then create the linked Student record and UserProfile."""
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            # Create the Student linked to this user
            Student.objects.create(
                user   = user,
                name   = self.cleaned_data['first_name'],
                email  = self.cleaned_data['email'],
                age    = self.cleaned_data['age'],
                course = self.cleaned_data['course'],
                marks  = 0,        # Admin will assign marks later
                is_active = True,
            )
            # Day 4 - Task 1: Create UserProfile with role='student'
            UserProfile.objects.create(user=user, role='student', is_approved=True)
        return user


# ──────────────────────────────────────────────────────────────────────────────
# Trainer Registration Form  (Day 4 - Task 1)
# Creates a User + UserProfile(role='trainer', is_approved=False)
# An admin must approve the trainer before they can access the trainer portal.
# ──────────────────────────────────────────────────────────────────────────────
class TrainerRegistrationForm(UserCreationForm):
    """
    Registration form for new trainers.
    Trainers start unapproved (is_approved=False) and must be
    activated by an administrator before they can log in to the
    trainer portal.
    """
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True, label="Full Name")

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            # is_approved=False → trainer cannot access portal until admin approves
            UserProfile.objects.create(user=user, role='trainer', is_approved=False)
        return user


# ──────────────────────────────────────────────────────────────────────────────
# Marks Update Form  (Admin only — just the marks field)
# ──────────────────────────────────────────────────────────────────────────────
class MarksUpdateForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['marks']

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is None:
            raise forms.ValidationError("Marks are required.")
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks


# ──────────────────────────────────────────────────────────────────────────────
# Marks Update With Reason Form  (Day 4 - Task 3: Trainer/Admin)
# Updates marks AND records the change in MarksHistory.
# The view is responsible for saving the history record after this form saves.
# ──────────────────────────────────────────────────────────────────────────────
class MarksWithReasonForm(forms.Form):
    """
    A plain Form (not ModelForm) so the view can explicitly read old marks,
    create a MarksHistory entry, and then update the student record.
    """
    marks  = forms.FloatField(
        min_value=0, max_value=100,
        label="New Marks",
        widget=forms.NumberInput(attrs={'step': '0.5'}),
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Reason for Change",
    )

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is None:
            raise forms.ValidationError("Marks are required.")
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks


# ──────────────────────────────────────────────────────────────────────────────
# Department Form  (Admin only)
# ──────────────────────────────────────────────────────────────────────────────
class DepartmentForm(forms.ModelForm):
    class Meta:
        model  = Department
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Department name cannot be empty.")
        return name


# ──────────────────────────────────────────────────────────────────────────────
# Course Form  (Admin only)
# ──────────────────────────────────────────────────────────────────────────────
class CourseForm(forms.ModelForm):
    class Meta:
        model  = Course
        fields = ['name', 'code', 'duration', 'is_active', 'trainer']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Course name cannot be empty.")
        return name

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip().upper()
        if not code:
            raise forms.ValidationError("Course code cannot be empty.")
        return code


# ──────────────────────────────────────────────────────────────────────────────
# Feedback Form  (Day 4 - Task 3: Trainer only)
# Trainers add/edit feedback for their assigned students.
# ──────────────────────────────────────────────────────────────────────────────
class FeedbackForm(forms.ModelForm):
    """
    Used by trainers to leave feedback on a student.
    The trainer and student fields are set by the view (not the form),
    so only comment, rating, course, and is_visible are shown.
    """
    class Meta:
        model  = Feedback
        fields = ['course', 'rating', 'comment', 'is_visible']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update({'class': 'form-select'})
        self.fields['rating'].widget.attrs.update({'class': 'form-select'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write your feedback here...'})
        self.fields['is_visible'].widget.attrs.update({'class': 'form-check-input'})

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None or not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


# ──────────────────────────────────────────────────────────────────────────────
# Account Activation Form  (Day 4 - Task 2: Admin only)
# Admin can toggle is_approved on a UserProfile (activate/deactivate trainers)
# and also toggle User.is_active (deactivate any account).
# ──────────────────────────────────────────────────────────────────────────────
class AccountActivationForm(forms.Form):
    """Simple form used in admin-portal to toggle account status."""
    is_active   = forms.BooleanField(required=False, label="Account Active")
    is_approved = forms.BooleanField(required=False, label="Trainer Approved")


# ──────────────────────────────────────────────────────────────────────────────
# Admin Trainer Forms
# ──────────────────────────────────────────────────────────────────────────────
class AdminTrainerAddForm(UserCreationForm):
    """
    Form used by Admin to create a new trainer.
    Enforces that email must end with @trainer.com.
    Automatically creates UserProfile with role='trainer' and is_approved=True.
    """
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True, label="Full Name")
    courses    = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Courses"
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap select/form-control classes
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email.endswith('@trainer.com'):
            raise forms.ValidationError("Trainer email must end with @trainer.com.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role='trainer', is_approved=True)
            # Assign selected courses
            for course in self.cleaned_data.get('courses', []):
                course.trainer = user
                course.save()
        return user


class AdminTrainerEditForm(forms.ModelForm):
    """
    Form used by Admin to edit trainer details.
    Enforces that email must end with @trainer.com.
    """
    email       = forms.EmailField(required=True)
    first_name  = forms.CharField(max_length=100, required=True, label="Full Name")
    is_approved = forms.BooleanField(required=False, label="Trainer Approved")
    courses     = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Courses"
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'is_active']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if user:
            if hasattr(user, 'userprofile'):
                initial['is_approved'] = user.userprofile.is_approved
            initial['courses'] = user.assigned_courses.all()
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_approved'].widget.attrs.update({'class': 'form-check-input'})

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email.endswith('@trainer.com'):
            raise forms.ValidationError("Trainer email must end with @trainer.com.")
        # Exclude current user from unique check
        qs = User.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if hasattr(user, 'userprofile'):
                profile = user.userprofile
                profile.is_approved = self.cleaned_data.get('is_approved', False)
                profile.save()
            # Clear previous course assignments for this trainer and assign new ones
            user.assigned_courses.update(trainer=None)
            for course in self.cleaned_data.get('courses', []):
                course.trainer = user
                course.save()
        return user
