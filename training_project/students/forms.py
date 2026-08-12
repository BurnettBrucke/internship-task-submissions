from .models import Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Student
from .models import MarksHistory


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name.strip():
            raise forms.ValidationError("Name cannot be empty")

        return name

    def clean_course(self):
        course = self.cleaned_data["course"]

        if not course.strip():
            raise forms.ValidationError("Course cannot be empty")

        return course

    def clean_age(self):
        age = self.cleaned_data["age"]

        if age < 16 or age > 60:
            raise forms.ValidationError("Age must be between 16 and 60")

        return age

    def clean_marks(self):
        marks = self.cleaned_data["marks"]

        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100")

        return marks
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_password1(self):

        password = self.cleaned_data.get("password1")
        username = self.data.get("username", "")
        email = self.data.get("email", "")

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one digit."
            )

        if not any(not char.isalnum() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        if username and username.lower() in password.lower():
            raise forms.ValidationError(
                "Password must not contain your username."
            )

        if email and email.lower() in password.lower():
            raise forms.ValidationError(
                "Password must not contain your email."
            )

        return password

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter Username"
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter Email"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter Password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm Password"
        })

    
     
class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            "student",
            "rating",
            "comments",
            "visible_to_student"
        ]

        widgets = {

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5
                }
            ),

            "comments": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "student": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "visible_to_student": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }

class MarksHistoryForm(forms.ModelForm):

    class Meta:
        model = MarksHistory

        fields = [
            "new_marks",
            "reason"
        ]

        widgets = {

            "new_marks": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

        }
        