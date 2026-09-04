from django import forms
from .models import Student
import re

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "name",
            "email",
            "age" ,
            "course",
            "marks",
            "active"
        ]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Name cannot be empty."
            )

        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise forms.ValidationError(
                "Name can contain only letters and spaces."
            )

        return name
    def clean_course(self):
        course = self.cleaned_data["course"]

        if not course.strip():
            raise forms.ValidationError(
                "Course cannot be empty."
            )
        return course

    def clean_age(self):
        age = self.cleaned_data["age"]

        if age > 60 or age< 16:
            raise forms.ValidationError(
                "Age must be between 16 and 60"
            )
        return age
    def clean_marks(self):
        marks = self.cleaned_data["marks"]

        if marks <0 or marks > 100:
            raise forms.ValidationError(
                "Marks must be between 0 - 100"
            )
        return marks

    