import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexityValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("The password must be at least 8 characters long."),
                code='password_too_short'
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_uppercase'
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("The password must contain at least one lowercase letter."),
                code='password_no_lowercase'
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("The password must contain at least one digit."),
                code='password_no_digit'
            )
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError(
                _("The password must contain at least one special character."),
                code='password_no_special'
            )
        if user:
            if password == user.username:
                raise ValidationError(
                    _("Password must not match username."),
                    code='password_matches_username'
                )
            if hasattr(user, 'email') and password == user.email:
                raise ValidationError(
                    _("Password must not match email."),
                    code='password_matches_email'
                )

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters and contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character."
        )
