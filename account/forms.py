# yourapp/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را دوباره وارد کنید'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل یا شماره موبایل'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        import re

        # بررسی ایمیل
        is_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username)
        # بررسی شماره موبایل ایران
        is_phone = re.match(r'^09[0-9]{9}$', username)

        if not (is_email or is_phone):
            raise forms.ValidationError('نام کاربری باید ایمیل معتبر یا شماره موبایل 11 رقمی باشد')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('رمزهای عبور مطابقت ندارند')

        if len(password1) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        # استخراج ایمیل یا شماره موبایل از username
        username = self.cleaned_data['username']
        import re

        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            user.email = username
        elif re.match(r'^09[0-9]{9}$', username):
            user.phone = username

        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='نام کاربری (ایمیل یا شماره موبایل)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@gmail.com یا 09123456789'
        })
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
    )

    error_messages = {
        'invalid_login': 'نام کاربری یا رمز عبور اشتباه است',
        'inactive': 'این حساب کاربری غیرفعال شده است',
    }