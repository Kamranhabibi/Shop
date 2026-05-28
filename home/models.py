from django.conf import settings
from django.db import models


# Create your models here.

class Category(models.Model):

    builder = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='سازنده')
    title = models.CharField(max_length=30 , verbose_name= 'عنوان')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title
