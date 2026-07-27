from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'marks', 'department', 'courses', 'is_active']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }

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


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
