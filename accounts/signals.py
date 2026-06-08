from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

#automatic profile creation for new users.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs): 
    '''automaticlly create a profile for a new user when they are created.'''
    if created:
        Profile.objects.create(user=instance)
        print("پروفایل برای کاربر {instance.username} ساخته شد.") # این خط برای دیباگ

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    '''When the user is saved, save theier profile as well.'''
    if hasattr(instance, 'profile'):
        instance.profile.save()
    