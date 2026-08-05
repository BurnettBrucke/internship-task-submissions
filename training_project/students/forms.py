from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student  
        fields = "__all__"

        widgets = {
            "active_status": forms.CheckboxInput(
                attrs={"class": "form-check-input"}),
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get("age")

        if age < 16 or age > 60:
            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )
        return age

    def clean_marks(self):
        marks = self.cleaned_data.get("marks")

        if marks < 0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )
        return marks

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if not course:
            raise forms.ValidationError("Course cannot be empty.")
        return course
    

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