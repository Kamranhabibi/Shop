from django.urls import path
from .views import Home

app_name = 'home'
#create url

urlpatterns = [
    path('',Home.as_view() ,name='home' )
]