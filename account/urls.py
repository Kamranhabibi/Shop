
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.Signup_view.as_view(), name='signup'),

    path('logout',views.logout_view,name='logout'),
    path('login',views.login_view,name='login'),

]