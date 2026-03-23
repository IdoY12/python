from django.urls import path
from . import views

urlpatterns = [
    path('photos/upload', views.upload_photo),
    path('my-photos', views.my_photos),
]