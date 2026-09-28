from django import forms
from .models import (student,department,Course,Feedback,CourseMark,)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }
        ))

    role = forms.ChoiceField(
        choices=[
            ("student", "Student"),
            ("trainer", "Trainer"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )
    department = forms.ModelChoiceField(
        queryset=department.objects.all(), # type: ignore
        required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "role",
            "department",
        ]
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter username"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password"
        })

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password1")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if password:
            validate_password(
                password,
                user=User(
                    username=username,
                    email=email
                )
            )

        return cleaned_data



class BootstrapLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )


class BootstrapPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter current password"
            }
        )
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password"
            }
        )
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password"
            }
        )
    )

class AssignTrainerForm(forms.Form):

    trainer = forms.ModelChoiceField(
        queryset=User.objects.filter(
            userprofile__role="trainer"
        ),
        empty_label="Select Trainer"
    )

class StudentForm(forms.ModelForm):


    class Meta:
        model = student

        fields = [
            "name",
            "email",
            "age",
            "course",
            "marks",
            "active",
            "department",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "age": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "course": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100
                }
            ),

            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "department": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data.get("name")

        if not name or not name.strip():
            raise forms.ValidationError(
                "Name cannot be empty."
            )

        return name.strip()

    def clean_course(self):

        course = self.cleaned_data.get("course")

        if not course or not course.strip():
            raise forms.ValidationError(
                "Course cannot be empty."
            )

        return course.strip()

    def clean_age(self):

        age = self.cleaned_data.get("age")

        if age is not None and not 16 <= age <= 60:
            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )

        return age

    def clean_marks(self):

        marks = self.cleaned_data.get("marks")

        if marks is not None and not 0 <= marks <= 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks

class MarksUpdateForm(forms.ModelForm):

    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter reason for marks update"
            }
        ),
        label="Reason for update"
    )

    class Meta:
        model = CourseMark
        fields = ["marks"]
        widgets = {
            "marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "placeholder": "Enter marks (0-100)"
                }
            )
        }

    def clean_marks(self):
        marks = self.cleaned_data.get("marks")

        if marks is None:
            raise forms.ValidationError(
                "Marks are required."
            )

        if not 0 <= marks <= 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")

        if not reason or not reason.strip():
            raise forms.ValidationError(
                "Please provide a reason for the marks update."
            )

        return reason.strip()

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [
            "rating",
            "comment",
            "is_visible",
        ]

        widgets = {
            "rating": forms.Select(
                choices=[
                    (1, "1 - Poor"),
                    (2, "2 - Below Average"),
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
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter feedback for the student"
                }
            ),

            "is_visible": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")

        if rating is None:
            raise forms.ValidationError(
                "Please select a rating."
            )

        if not 1 <= rating <= 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get("comment")

        if not comment or not comment.strip():
            raise forms.ValidationError(
                "Feedback comment cannot be empty."
            )

        return comment.strip()

class AuditLogFilterForm(forms.Form):

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search user or description"
            }
        )
    )

    action_type = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All Actions"),
            ("CREATE", "Create"),
            ("UPDATE", "Update"),
            ("DELETE", "Delete"),
            ("LOGIN", "Login"),
            ("LOGOUT", "Logout"),
            ("FAILED", "Failed"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date"
            }
        )
    )

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date"
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()

        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")

        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(
                "Start date cannot be after end date."
            )

        return cleaned_data



    

    