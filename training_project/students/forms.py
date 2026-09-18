from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Student, Feedback, TrainerProfile, Course
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'age',
            'department',
            'courses',
            'marks',
            'joined_date',
            'active_status'
        ]

    def clean_name(self):
        name = self.cleaned_data['name']

        if not name.strip():
            raise forms.ValidationError("Name cannot be empty.")

        return name

    def clean_age(self):
        age = self.cleaned_data['age']

        if age < 16 or age > 60:
            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )

        return age

    def clean_marks(self):
        marks = self.cleaned_data['marks']

        if marks < 0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email
    role = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('trainer', 'Trainer'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ),
        label='Register As'
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if not password:
            return password

        if len(password) < 8:
            raise forms.ValidationError(
                'Password must contain at least 8 characters.'
            )

        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                'Password must contain at least one uppercase letter.'
            )

        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                'Password must contain at least one lowercase letter.'
            )

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                'Password must contain at least one digit.'
            )

        if not any(not char.isalnum() for char in password):
            raise forms.ValidationError(
                'Password must contain at least one special character.'
            )

        if username and username.lower() in password.lower():
            raise forms.ValidationError(
                'Password must not contain your username.'
            )

        if email:
            email_username = email.split('@')[0]

            if email_username.lower() in password.lower():
                raise forms.ValidationError(
                    'Password must not contain your email.'
                )

        return password
    
class MarksUpdateForm(forms.ModelForm):

    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder': 'Enter reason for marks update...'
            }
        )
    )

    class Meta:
        model = Student
        fields = ['marks', 'reason']

    def clean_marks(self):
        marks = self.cleaned_data['marks']

        if marks < 0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            'course',
            'feedback',
            'rating',
            'is_visible'
        ]

        widgets = {
            'feedback': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter feedback for the student...'
                }
            ),

            'rating': forms.NumberInput(
                attrs={
                    'min': 1,
                    'max': 5
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        courses = kwargs.pop('courses', None)

        super().__init__(*args, **kwargs)

        if courses is not None:
            self.fields['course'].queryset = courses

    def clean_rating(self):

        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating
    
class TrainerForm(UserCreationForm):

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class TrainerEditForm(forms.ModelForm):

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]
