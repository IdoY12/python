from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.index),
    path('ido_was_here', views.ido_was_here),
    path('test', views.test),
]
