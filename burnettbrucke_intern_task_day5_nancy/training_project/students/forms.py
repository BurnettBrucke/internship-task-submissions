from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Feedback, Student, UserProfile
from .security import is_locked_out, reset_attempts


BOOTSTRAP_INPUT = 'form-control'
BOOTSTRAP_SELECT = 'form-select'
BOOTSTRAP_CHECK = 'form-check-input'


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', BOOTSTRAP_INPUT)


class LockoutAwareAuthenticationForm(BootstrapAuthenticationForm):
    """Adds brute-force protection on top of Django's normal login form:
    if the account has racked up too many recent failures, block the
    attempt (and don't even touch the database) before authenticating.
    On a successful login the failure counter is reset."""

    def clean(self):
        username = self.cleaned_data.get('username')

        if username and is_locked_out(username):
            raise forms.ValidationError(
                "Too many failed login attempts. This account is temporarily "
                "locked -- please wait a few minutes and try again, or use "
                "'Forgot password?' to reset it.",
                code='account_locked',
            )

        cleaned_data = super().clean()

        if username and self.get_user() is not None:
            reset_attempts(username)

        return cleaned_data


class BootstrapPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', BOOTSTRAP_INPUT)


class BootstrapPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', BOOTSTRAP_INPUT)


class BootstrapSetPasswordForm(SetPasswordForm):
    """Used on the /reset/<uidb64>/<token>/ page to actually set the new
    password."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', BOOTSTRAP_INPUT)


class StudentForm(forms.ModelForm):
    """Full student record form -- used by Administrators only."""

    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'marks', 'department', 'courses', 'is_active']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.CheckboxInput)):
                continue
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', BOOTSTRAP_SELECT)
            else:
                field.widget.attrs.setdefault('class', BOOTSTRAP_INPUT)

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

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None and (marks < 0 or marks > 100):
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks


class TrainerMarksForm(forms.ModelForm):
    """Narrow form: trainers may only update marks, nothing else on the
    Student record -- plus a required reason, since every marks change must
    be explainable in the audit trail. Kept as a separate form (rather than
    reusing StudentForm with fields hidden) so there's no way to slip extra
    fields into a POST and have them accepted."""

    reason = forms.CharField(
        max_length=255,
        required=True,
        help_text="Why is this mark changing? (e.g. 'Resit exam', 'Grading correction')",
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_INPUT}),
    )

    class Meta:
        model = Student
        fields = ['marks']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': BOOTSTRAP_INPUT, 'step': '0.01'}),
        }

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None and (marks < 0 or marks > 100):
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course', 'rating', 'comment', 'is_visible_to_student']
        widgets = {
            'course': forms.Select(attrs={'class': BOOTSTRAP_SELECT}),
            'rating': forms.Select(
                choices=[(i, f"{i} - {label}") for i, label in [
                    (1, 'Poor'), (2, 'Below average'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')
                ]],
                attrs={'class': BOOTSTRAP_SELECT},
            ),
            'comment': forms.Textarea(attrs={'class': BOOTSTRAP_INPUT, 'rows': 3}),
            'is_visible_to_student': forms.CheckboxInput(attrs={'class': BOOTSTRAP_CHECK}),
        }

    def __init__(self, *args, trainer=None, student=None, **kwargs):
        super().__init__(*args, **kwargs)
        if trainer is not None:
            # A trainer may only leave feedback on courses they teach that
            # this particular student is actually enrolled in.
            qs = trainer.trainer_courses.all()
            if student is not None:
                qs = qs.filter(students=student)
            self.fields['course'].queryset = qs

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class RegisterForm(UserCreationForm):
    """Public self-registration. Always creates a 'Student' account -- there
    is no role field on this form, so a visitor cannot grant themselves
    Administrator/Trainer access. See TrainerRegisterForm for the separate,
    approval-gated trainer sign-up path."""

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': BOOTSTRAP_INPUT}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = BOOTSTRAP_INPUT
        self.fields['password1'].widget.attrs['class'] = BOOTSTRAP_INPUT
        self.fields['password2'].widget.attrs['class'] = BOOTSTRAP_INPUT

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # The post_save signal already created a UserProfile with the
            # default role of 'student' (auto-approved); nothing else to do.
        return user


class TrainerRegisterForm(RegisterForm):
    """Same as RegisterForm, but the resulting account is a Trainer that
    starts out *unapproved*. It can't use the trainer dashboard, update
    marks, or leave feedback until an Administrator approves it (see
    students.views.approve_trainer)."""

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.role = UserProfile.ROLE_TRAINER
            user.profile.is_approved = False
            user.profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT}),
            'bio': forms.Textarea(attrs={'class': BOOTSTRAP_INPUT, 'rows': 3}),
        }
