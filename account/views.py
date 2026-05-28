from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .forms import CustomUserCreationForm, CustomUserLoginForm




class Signup_view(View):
    def get(self , request):
        form = CustomUserCreationForm()

        return render(request , 'account/signup.html',{'form':form})

    def post(self , request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'به سامانه خوش آمدید {user.first_name or user.username}!')
            return redirect('/')
        else:
            for field , errors in form.errors.items():
                for error in errors :
                    messages.error(request ,f'{field}: {error}')

        return render(request, 'account/signup.html', {'form': form})



def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید {user.first_name or user.username}!')


                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('/')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
        else:
            messages.error(request, 'لطفا اطلاعات معتبر وارد کنید')
    else:
        form = CustomUserLoginForm
    return render(request, 'account/login.html', {'form':form})




def logout_view(request):
    logout(request)
    messages.info(request, 'شما از حساب خود خارج شدید')
    return redirect('/')




@login_required(login_url='login')
def home_view(request):
    return render(request, 'account/home.html', {
        'user': request.user
    })