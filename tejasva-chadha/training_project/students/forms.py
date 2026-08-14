from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Feedback, Course, Enrollment


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'name', 'email', 'age', 'department', 'courses', 'joined_date', 'active_status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. john@example.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 20 (between 16 & 60)'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'courses': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox-group'}),
            'joined_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active_status': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'name': {
                'required': 'Name cannot be empty.',
            },
            'email': {
                'required': 'Email cannot be empty.',
                'invalid': 'Email must be valid.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'joined_date' not in self.initial:
            self.initial['joined_date'] = timezone.localdate()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 16 or age > 60:
                raise forms.ValidationError("Age must be between 16 and 60.")
        return age


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'e.g. user@example.com'})
    )
    role = forms.ChoiceField(
        choices=(('student', 'Student'), ('trainer', 'Trainer')),
        initial='student',
        required=False,
        label="Role Type",
        widget=forms.Select()
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("A user with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password1')
        
        if password:
            if username and password == username:
                self.add_error('password1', "Password must not match username.")
            if email and password == email:
                self.add_error('password1', "Password must not match email.")
        return cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course', 'rating', 'comments', 'is_visible']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your feedback here...'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if trainer and student:
            self.fields['course'].queryset = student.courses.filter(assigned_trainer=trainer)


class MarksUpdateForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Course Context"
    )
    new_marks = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 85 (0 - 100)'}),
        label="New Marks"
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for updating marks...'}),
        label="Reason"
    )

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            if trainer and getattr(getattr(trainer, 'profile', None), 'role', None) == 'trainer':
                self.fields['course'].queryset = student.courses.filter(assigned_trainer=trainer)
            else:
                self.fields['course'].queryset = student.courses.all()
