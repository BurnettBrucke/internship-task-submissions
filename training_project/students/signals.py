from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile for new users and ensure
    existing users also have one.
    """
    profile, created_profile = UserProfile.objects.get_or_create(
        user=instance
    )

    profile.save()