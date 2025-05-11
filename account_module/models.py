from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars',verbose_name='آواتار', null=True, blank=True)
    mobile = models.CharField(max_length=100, verbose_name='شماره همراه', null=True, blank=True)
    email_active_code = models.CharField(max_length=300, verbose_name='کد فعالسازی کاربر', null=True, blank=True)
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=False)