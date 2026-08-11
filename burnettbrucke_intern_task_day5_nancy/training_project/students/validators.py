import re

from django.core.exceptions import ValidationError


class ComplexityValidator:
    """Requires at least one uppercase letter, one lowercase letter, one
    digit, and one special character. Used alongside Django's built-in
    validators (minimum length, common-password check, and similarity to
    username/email) in AUTH_PASSWORD_VALIDATORS."""

    def validate(self, password, user=None):
        missing = []
        if not re.search(r'[A-Z]', password):
            missing.append("one uppercase letter")
        if not re.search(r'[a-z]', password):
            missing.append("one lowercase letter")
        if not re.search(r'\d', password):
            missing.append("one digit")
        if not re.search(r'[^\w\s]', password):
            missing.append("one special character")

        if missing:
            raise ValidationError(
                "Password must contain at least %(missing)s.",
                code='password_missing_complexity',
                params={'missing': ', '.join(missing)},
            )

    def get_help_text(self):
        return (
            "Your password must include at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character."
        )
