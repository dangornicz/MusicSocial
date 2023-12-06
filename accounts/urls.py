from django.urls import path

import accounts
from . import views

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('register/', views.user_registration, name="user_registration"),
    path('logout/', views.user_logout, name="user_logout"),
]