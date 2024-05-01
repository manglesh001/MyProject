from django.urls import path
from .views import custom_login, register, sign_out

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', sign_out, name='logout'),

]