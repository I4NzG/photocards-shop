# myApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('update/', views.user_update, name='update'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
