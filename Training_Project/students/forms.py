from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'age',
            'course',
            'marks',
            'joined_date',
            'active',
        ]

    def clean_name(self):
        name = self.cleaned_data['name']

        if not name.strip():
            raise forms.ValidationError("Name cannot be empty.")

        return name

    def clean_course(self):
        course = self.cleaned_data['course']

        if not course.strip():
            raise forms.ValidationError("Course cannot be empty.")

        return course

    def clean_age(self):
        age = self.cleaned_data['age']

        if age < 16 or age > 60:
            raise forms.ValidationError("Age must be between 16 and 60.")

        return age

    def clean_marks(self):
        marks = self.cleaned_data['marks']

        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")

        return marks
