from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import (
    Student,
    Feedback,
)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "marks": forms.NumberInput(attrs={"class": "form-control"}),
            "joined_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "department": forms.Select(attrs={"class": "form-select"}),
            "courses": forms.SelectMultiple(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name.strip():
            raise forms.ValidationError(
                "Name cannot be empty."
            )

        return name

    def clean_age(self):
        age = self.cleaned_data["age"]

        if age < 16 or age > 60:
            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )

        return age

    def clean_marks(self):
        marks = self.cleaned_data["marks"]

        if marks < 0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
        )

        return email

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )


class MarksUpdateForm(forms.Form):

    new_marks = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 0,
                "max": 100,
            }
        ),
    )

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter the reason for updating marks...",
            }
        )
    )

    def clean_new_marks(self):

        marks = self.cleaned_data["new_marks"]

        if marks < 0 or marks > 100:

            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks


class FeedbackForm(forms.ModelForm):

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
                "max": 5,
            }
        ),
    )

    feedback = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter your feedback...",
            }
        )
    )

    class Meta:
        model = Feedback
        fields = (
            "rating",
            "feedback",
        )

    def clean_rating(self):

        rating = self.cleaned_data.get("rating")

        if rating is None:
            raise forms.ValidationError(
                "Rating is required."
            )

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating 


class AuditLogFilterForm(forms.Form):

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search username, object or description...",
            }
        ),
    )

    action = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All Actions"),
            ("LOGIN", "Login"),
            ("LOGOUT", "Logout"),
            ("FAILED_LOGIN", "Failed Login"),
            ("CREATE", "Create"),
            ("UPDATE", "Update"),
            ("DELETE", "Delete"),
            ("MARKS_UPDATE", "Marks Update"),
            ("FEEDBACK", "Feedback"),
            ("STATUS_CHANGE", "Status Change"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
    )