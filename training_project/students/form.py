from django import forms
from .models import Student , Enrollment , Feedback , Course , StudentProfile
from django.contrib.auth.forms import SetPasswordForm
import re
from django.contrib.auth import authenticate

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  

class StudentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
    queryset=Course.objects.filter(active_status=True),
    required=True,
    widget=forms.CheckboxSelectMultiple,
    label="Courses"
    )

    class Meta:
        model = Student
        fields = [
            "name",
            "email",
            "age" ,
            "active",
            "department",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Name cannot be empty."
            )

        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise forms.ValidationError(
                "Name can contain only letters and spaces."
            )

        return name

    def clean_age(self):
        age = self.cleaned_data["age"]

        if age > 60 or age< 16:
            raise forms.ValidationError(
                "Age must be between 16 and 60"
            )
        return age

class StudentPasswordSetForm(SetPasswordForm):
    pass

class LoginForm(forms.Form):

    login = forms.CharField(
        label="Email or Username",
        max_length=150
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        login_value = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if not login_value or not password:
            return cleaned_data

        user = None

        try:
            user = User.objects.get(email__iexact=login_value)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=login_value)
            except User.DoesNotExist:
                user = None

        if user:
            if hasattr(user, "profile") and user.profile.login_blocked:
                raise forms.ValidationError(
                    "This account is temporarily blocked because "
                    "of too many failed login attempts."
                )

            self.user = authenticate(
                username=user.username,
                password=password
            )

        else:
            self.user = None

        if self.user is None:
            raise forms.ValidationError(
                "Invalid login credentials."
            )

        return cleaned_data

class TrainerRegistrationForm(forms.Form):

    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    requested_course = forms.ModelChoiceField(queryset=Course.objects.filter(active_status = True) , required= True , label = "Course you want to teach")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        # Use Django's configured password validators
        from django.contrib.auth.password_validation import validate_password

        validate_password(password)

        return password

class MarkForm(forms.Form):

    marks = forms.IntegerField(
        min_value=0,
        max_value=100,
        label="Marks",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter marks (0-100)"
            }
        )
    )

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Why are you updating these marks?"
            }
        ),
        required=True,
        label="Reason for update"
    )
    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ["rating", "comment"]

        widgets = {
            "rating": forms.Select(
                choices=[
                    (1, "1 - Poor"),
                    (2, "2 - Needs Improvement"),
                    (3, "3 - Average"),
                    (4, "4 - Good"),
                    (5, "5 - Excellent"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Write your feedback..."
                }
            )
        }

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = [
            "phone",
            "address",
            "date_of_birth",
        ]

        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter phone number"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your address"
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course

        fields = [
            "course_name",
            "code",
            "duration",
            "duration_days",
            "active_status",
        ]

        widgets = {
            "course_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Python Programming"
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. PY101"
                }
            ),

            "duration": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 3 Months"
                }
            ),

            "duration_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "e.g. 90"
                }
            ),

            "active_status": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }