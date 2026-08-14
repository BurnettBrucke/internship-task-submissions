from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:

        model = Feedback

        fields = (
            "rating",
            "feedback",
        )

        widgets = {

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5,
                }
            ),

            "feedback": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter your feedback...",
                }
            ),
        }

    def clean_rating(self):

        rating = self.cleaned_data["rating"]

        if rating < 1 or rating > 5:

            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating