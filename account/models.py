# account/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')

        if '@' in username and '.' in username:
            username = self.normalize_email(username)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='نام کاربری (ایمیل یا شماره موبایل)'
    )
    email = models.EmailField(unique=True, null=True, blank=True , verbose_name= 'ایمیل')
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True  , verbose_name= 'شماره موبایل')
    first_name = models.CharField(max_length=150, blank=True , verbose_name= 'نام')
    last_name = models.CharField(max_length=150, blank=True , verbose_name= 'نام خانوادگی')
    is_admin = models.BooleanField(default=False , verbose_name= 'مدیر')
    is_staff = models.BooleanField(default=False , verbose_name= 'کارمند')
    is_active = models.BooleanField(default=True , verbose_name= 'فعال')
    is_superuser = models.BooleanField(default=False , verbose_name= 'مالک')
    date_join = models.DateTimeField(auto_now_add=True , verbose_name= 'تاریخ عضویت')

    # ✅ این دو خط را اضافه کن (مهمترین بخش)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_groups',  # این خط را اضافه کن
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_permissions',  # این خط را اضافه کن
        related_query_name='custom_user'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ' کاربر'
        verbose_name_plural = 'حساب ها'

    def save(self, *args, **kwargs):
        if '@' in self.username and '.' in self.username:
            self.email = self.username
            self.phone = None
        elif re.match(r'^09[0-9]{9}$', self.username):
            self.phone = self.username
            self.email = None
        else:
            raise ValueError('Username must be either an email or a phone number')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username