import re
from django.core.exceptions import ValidationError


class StrongPasswordValidator:
    """
    Validates that the password contains:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """

    def validate(self, password, user=None):

        if len(password) < 8:
            raise ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise ValidationError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\];']", password):
            raise ValidationError(
                "Password must contain at least one special character."
            )

    def get_help_text(self):
        return (
            "Your password must contain at least 8 characters, "
            "including uppercase, lowercase, digit and special character."
        )