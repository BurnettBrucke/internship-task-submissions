from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Student,
    Course,
    Feedback,
    CourseMark,
)
# ============================================================
# STUDENT FORM
# ============================================================

class StudentForm(forms.ModelForm):

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 5,
        }),
        required=False
    )

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
            'active',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter age',
            }),

            'department': forms.Select(attrs={
                'class': 'form-control',
                'size': 3,
            }),

            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter marks',
            }),

            'joined_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

        }

    def clean_name(self):
        name = self.cleaned_data['name']

        if not name.strip():
            raise forms.ValidationError(
                "Name cannot be empty."
            )

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


# ============================================================
# TRAINER FORM
# ============================================================

class TrainerForm(forms.ModelForm):
    """
    Form used by Admin to Add and Edit Trainers.

    Admin can manage:
    - Trainer name
    - Email
    - Multiple course assignment
    """

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
                'size': '5',
            }
        ),
        help_text="Hold Ctrl and select multiple courses."
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter trainer name',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter trainer email',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['courses'].initial = Course.objects.filter(
                trainer=self.instance
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(
                "Email is required."
            )

        existing_user = User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        )

        if existing_user.exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    def save(self, commit=True):
        trainer = super().save(commit=False)

        # Trainer accounts created by Admin
        # will receive password functionality separately.
        if not trainer.pk:
            trainer.set_unusable_password()

        if commit:
            trainer.save()

        return trainer

# ============================================================
# COURSE FORM
# ============================================================

class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['trainer'].queryset = User.objects.filter(
            profile__role='trainer'
        ).order_by('username')
    class Meta:
        model = Course
        fields = [
            'course_name',
            'code',
            'duration',
            'active',
            'students',
            'trainer',
        ]
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course code'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 3 Months'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'students': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
            'trainer': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
        }


# ============================================================
# REGISTRATION FORM
# ============================================================

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('trainer', 'Trainer'),
    ]

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
        })
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')

        if password2:
            from django.contrib.auth import password_validation

            password_validation.validate_password(
                password2,
                self.instance
            )

        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

# ============================================================
# TASK 3 - FEEDBACK FORMS
# ============================================================

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'rating',
            'comment',
            'is_visible',
        ]

        widgets = {
            'rating': forms.Select(
                choices=[
                    (1, '1 - Very Poor'),
                    (2, '2 - Poor'),
                    (3, '3 - Average'),
                    (4, '4 - Good'),
                    (5, '5 - Excellent'),
                ],
                attrs={
                    'class': 'form-select'
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter feedback...'
                }
            ),

            'is_visible': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')

        if rating is None:
            raise forms.ValidationError(
                "Rating is required."
            )

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating


# ============================================================
# TASK 3 - MARKS UPDATE FORM
# ============================================================

class MarksUpdateForm(forms.ModelForm):
    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter reason for marks update...'
            }
        ),
        required=True
    )

    class Meta:
        model = CourseMark
        fields = [
            'marks',
        ]

        widgets = {
            'marks': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter marks',
                    'min': 0,
                    'max': 100
                }
            ),
        }

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')

        if marks is None:
            raise forms.ValidationError(
                "Marks are required."
            )

        if marks < 0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks