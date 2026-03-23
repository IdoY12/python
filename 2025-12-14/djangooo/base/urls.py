from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView   # --> Login

urlpatterns = [
    path('hello', views.index),
    path('ido_was_here', views.ido_was_here),
    path('test', views.test),
    path('private', views.private_mem),
    path('buy', views.create_order),
    path('my-orders', views.get_my_orders),
    # path('login',TokenObtainPairView.as_view() ),
    path('login',views.MyTokenObtainPairView.as_view() ),
    # Adding the signup endpoint here
    path('signup', views.register_user),
]
