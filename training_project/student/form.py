from django import forms
from .models import student


class StudentForm(forms.ModelForm):

    class Meta:
        model = student
        fields = [
            "name",
            "email",
            "age",
            "course",
            "marks",
            "active",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name or not name.strip():
            raise forms.ValidationError("Name cannot be empty.")

        return name.strip()

    def clean_course(self):
        course = self.cleaned_data.get("course")

        if not course or not course.strip():
            raise forms.ValidationError("Course cannot be empty.")

        return course.strip()

    def clean_age(self):
        age = self.cleaned_data.get("age")

        if age is not None and not 16 <= age <= 60:
            raise forms.ValidationError(
                "Age must be between 16 and 60."
            )

        return age

    def clean_marks(self):
        marks = self.cleaned_data.get("marks")

        if marks is not None and not 0 <= marks <= 100:
            raise forms.ValidationError(
                "Marks must be between 0 and 100."
            )

        return marks