from .models import Profile, Vote, Survey, Product
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
#from django.core.mail import send_mail

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
    if hasattr(instance, 'proflie'):
        instance.profile.save()
    
    
@receiver(post_save, sender=Vote)
def updaate_choice_votes(sender, instance, created, **kwargs):
    if created:
        choice = instance.choice
        choice.votes += 1
        choice.save()

#@receiver(post_save, sender=Survey)
#def notify_admin_new_survey(sender, instance, created, **kwargs):
#    if created:
#        '''sent email to admin'''
#        send_mail(
#            'new_survey',
#            f'The new survey is created {instance.question}',
#            'admin@site.com',
#           ['admin@site.com'],
#        )

#@receiver(post_save, sender=Product)
#def log_product_change(sender, instance, **kwargs):
#    if instance.pk:
#        old = Product.objects.get(pk=instance.pk)
#        if old.price != instance.price:
#            print(f"قیمت محصول {instance.name} از {old.price} به {instance.price} تغییر کرد")