from .models import Vote, Survey, Product
from django.db.models.signals import post_save
from django.dispatch import receiver

#from django.core.mail import send_mail


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