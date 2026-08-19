from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    Student,
    Department,
    Course,
    Feedback,
    MarksHistory,
    Enrollment,
)


# =========================================================
# STUDENT FORM
# =========================================================

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "department",
            "name",
            "email",
            "age",
        ]

        widgets = {
            "department": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Student Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Email",
                }
            ),

            "age": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 16,
                    "max": 60,
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

    def clean_age(self):

        age = self.cleaned_data.get("age")

        if age < 16 or age > 60:

            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )

        return age


# =========================================================
# DEPARTMENT FORM
# =========================================================

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department

        fields = [
            "name",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Department Name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter Department Description",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data.get("name")

        if not name or not name.strip():

            raise forms.ValidationError(
                "Department name cannot be empty."
            )

        return name.strip()


# =========================================================
# COURSE FORM
# =========================================================

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course

        fields = [
            "course_name",
            "code",
            "duration",
            "active",
        ]

        widgets = {
            "course_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Course Name",
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Course Code",
                }
            ),

            "duration": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Duration",
                }
            ),

            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_course_name(self):

        name = self.cleaned_data.get(
            "course_name"
        )

        if not name or not name.strip():

            raise forms.ValidationError(
                "Course name cannot be empty."
            )

        return name.strip()

    def clean_code(self):

        code = self.cleaned_data.get(
            "code"
        )

        if not code or not code.strip():

            raise forms.ValidationError(
                "Course code cannot be empty."
            )

        return code.strip().upper()


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

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

        if User.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_password1(self):

        password = self.cleaned_data.get(
            "password1"
        )

        username = self.data.get(
            "username",
            ""
        )

        email = self.data.get(
            "email",
            ""
        )

        if not password:
            return password

        if len(password) < 8:

            raise forms.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not any(
            char.isupper()
            for char in password
        ):

            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not any(
            char.islower()
            for char in password
        ):

            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not any(
            char.isdigit()
            for char in password
        ):

            raise forms.ValidationError(
                "Password must contain at least one digit."
            )

        if not any(
            not char.isalnum()
            for char in password
        ):

            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        if (
            username
            and username.lower()
            in password.lower()
        ):

            raise forms.ValidationError(
                "Password must not contain your username."
            )

        if (
            email
            and email.lower()
            in password.lower()
        ):

            raise forms.ValidationError(
                "Password must not contain your email."
            )

        return password

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            "username"
        ].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter Username",
        })

        self.fields[
            "email"
        ].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter Email",
        })

        self.fields[
            "password1"
        ].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter Password",
        })

        self.fields[
            "password2"
        ].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm Password",
        })


# =========================================================
# FEEDBACK FORM
# =========================================================

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            "enrollment",
            "rating",
            "comments",
            "visible_to_student",
        ]

        widgets = {
            "enrollment": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5,
                    "step": 1,
                }
            ),

            "comments": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter feedback",
                }
            ),

            "visible_to_student": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(
        self,
        *args,
        user=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        self.user = user

        self.fields[
            "enrollment"
        ].queryset = Enrollment.objects.none()

        if (
            user
            and hasattr(user, "profile")
            and user.profile.role == "trainer"
        ):

            self.fields[
                "enrollment"
            ].queryset = (
                Enrollment.objects
                .filter(
                    student__assigned_trainer=user
                )
                .select_related(
                    "student",
                    "course"
                )
                .order_by(
                    "student__name",
                    "course__course_name"
                )
            )

        elif (
            user
            and hasattr(user, "profile")
            and user.profile.role == "admin"
        ):

            self.fields[
                "enrollment"
            ].queryset = (
                Enrollment.objects
                .select_related(
                    "student",
                    "course"
                )
                .order_by(
                    "student__name",
                    "course__course_name"
                )
            )

    def clean_enrollment(self):

        enrollment = self.cleaned_data.get(
            "enrollment"
        )

        if not enrollment:

            raise forms.ValidationError(
                "Please select an enrollment."
            )

        if (
            self.user
            and hasattr(self.user, "profile")
            and self.user.profile.role == "trainer"
        ):

            if (
                enrollment.student.assigned_trainer
                != self.user
            ):

                raise forms.ValidationError(
                    "You can give feedback only to your assigned students."
                )

        return enrollment

    def clean_rating(self):

        rating = self.cleaned_data.get(
            "rating"
        )

        if rating is None:

            raise forms.ValidationError(
                "Rating is required."
            )

        if rating < 1 or rating > 5:

            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

    def clean_comments(self):

        comments = self.cleaned_data.get(
            "comments"
        )

        if (
            not comments
            or not comments.strip()
        ):

            raise forms.ValidationError(
                "Comments cannot be empty."
            )

        return comments.strip()


# =========================================================
# MARKS HISTORY FORM
# =========================================================

class MarksHistoryForm(forms.ModelForm):

    class Meta:
        model = MarksHistory

        fields = [
            "enrollment",
            "new_marks",
            "reason",
        ]

        widgets = {
            "enrollment": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "new_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                    "step": "0.01",
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter reason",
                }
            ),
        }

    def clean_new_marks(self):

        marks = self.cleaned_data[
            "new_marks"
        ]

        if marks < 0 or marks > 100:

            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks