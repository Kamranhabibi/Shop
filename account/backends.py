# backends.py - نسخه کامل
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    بکند سفارشی برای احراز هویت با فیلد username
    (اگر بخوای validation اضافه یا لاگینگ داشته باشی)
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None

        # اینجا میتونی هر منطقی که خواستی اضافه کنی
        # مثلاً لاگینگ، محدودیت تلاش، و غیره

        try:
            # پیدا کردن کاربر با username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # میتونی لاگ کنی که کاربر پیدا نشد
            return None

        # بررسی رمز عبور
        if user.check_password(password) and self.user_can_authenticate(user):
            # میتونی اینجا لاگ کنی که احراز هویت موفق بوده
            return user

        # میتونی لاگ کنی که رمز اشتباه بوده
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None