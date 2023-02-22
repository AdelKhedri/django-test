from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True, verbose_name="email")
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="phone number")
    is_report = models.BooleanField(default=True, verbose_name="is reported")
    reported_time = models.DateTimeField(blank=False, null=True, verbose_name="time report")
    is_active = models.BooleanField(default=False)

    def is_report_time(self):
        if self.is_report and self.reported_time < timezone.now():
            return True
    
    def __str__(self):
        return self.username

class Profiel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_image/', null=True, blank=True, verbose_name="Profiel Image")
    hide_profile = models.BooleanField(default=True, verbose_name='Hide email')
    point = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
