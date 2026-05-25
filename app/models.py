from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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