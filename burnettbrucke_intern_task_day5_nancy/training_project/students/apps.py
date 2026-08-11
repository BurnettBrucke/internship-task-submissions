from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'

    def ready(self):
        # Registers the post_save signal (auto-create UserProfile) and the
        # auth signal receivers (login/logout/failed-login auditing).
        import students.models  # noqa: F401
        import students.signals  # noqa: F401
