from django.db import models
from django.conf import settings
from PIL import Image

# Create your models here.
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