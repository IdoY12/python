from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView   # --> Login

urlpatterns = [
    path('hello', views.index),
    path('ido_was_here', views.ido_was_here),
    path('test', views.test),
    path('login',TokenObtainPairView.as_view() ),
    # Adding the signup endpoint here
    path('signup', views.register_user),
]
