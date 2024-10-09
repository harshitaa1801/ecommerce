from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

