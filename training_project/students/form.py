from django import forms 
from .models import Student, StudentProfile

# student form 
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields="__all__"

        exclude=['age','active_status']

        widgets = {
            "course": forms.CheckboxSelectMultiple(),
        }

    def clean_age(self):
        age=self.cleaned_data['age']
        if age<18 or age>60: 
            raise forms.ValidationError("age must be between 18 to 60")
        return age
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Only Gmail addresses are allowed.")

        return email
    def clean_marks(self):
            marks=self.cleaned_data['marks']
            if marks<0 or marks>100: 
                raise forms.ValidationError("marks must be between 0 to 100")
            return marks

# student profile form
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        fields = [
            "phone",
            "address",
            "DoB",
        ]
    
