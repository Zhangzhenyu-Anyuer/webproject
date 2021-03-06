from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.

class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11,verbose_name='手机号')


    class Meta:
        db_table = 'edu_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

