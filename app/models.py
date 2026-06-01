from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from PIL import Image

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="product name:")
    description = models.TextField(verbose_name="descriptions:")
    launch_date = models.DateField(verbose_name="date")
    create_at = models.DateTimeField(auto_now=True, verbose_name="Record date")
    
    def __str__(self):
        return self.name
    
class Survey(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="product")
    question = models.CharField(max_length=255, verbose_name="question")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="rocord date")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return f"{self.product.name}: {self.question[:64]}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "poll"
        verbose_name_plural = "polls"

class Choice(models.Model):
    '''Options of poll'''
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="poll")
    choice_text = models.CharField(max_length=255, verbose_name="text")
    votes = models.IntegerField(default=0, verbose_name="vote number")

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="Option")
    voted_at = models.DateTimeField(auto_now_add=True, verbose_name="vote time")

    class Meta:
#        unique_together = ["user", "choice"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'choice'], name='unique_user_choice')
        ]
        verbose_name = "vote"
        verbose_name_plural = "votes"

    def __str__(self):
        return f"{self.user.username} voted for {self.choice.choice_text}"
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    '''additional information'''
    bio = models.TextField(max_length=256, verbose_name='bio', blank=True, null=True)
    birth_date = models.DateField(verbose_name='birth_date', blank=True, null=True)
    phone = models.CharField(verbose_name='phone', max_length=15, blank=True, null=True)
    website = models.URLField(verbose_name='website', blank=True, null=True)
    avatar = models.ImageField(default='avatar/default.jpg',#default avatar
                                upload_to='avatar/',#dir to store the image
                                blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"profile user: {self.user.username}"

    def save(self, *args, **kwargs):
        #save the profile first
        super().save(*args, **kwargs)

        if self.avatar and not self.avatar.name.endswith('default.jpg'):
            try:          
                #resize the image
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    #create a thumbnail
                    img.thumbnail(output_size)
                    #and overwrite the larger image
                    img.save(self.avatar.path)
            except FileNotFoundError:
                pass

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"