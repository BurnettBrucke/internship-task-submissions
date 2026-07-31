from django import forms
from django.utils import timezone
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'course', 'marks', 'joined_date', 'active_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. john@example.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 20 (between 16 & 60)'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python Programming'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 85 (between 0 & 100)'}),
            'joined_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active_status': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'name': {
                'required': 'Name cannot be empty.',
            },
            'course': {
                'required': 'Course cannot be empty.',
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

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if not course or not course.strip():
            raise forms.ValidationError("Course cannot be empty.")
        return course

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 16 or age > 60:
                raise forms.ValidationError("Age must be between 16 and 60.")
        return age

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0 or marks > 100:
                raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks
