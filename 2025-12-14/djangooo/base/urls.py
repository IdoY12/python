from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('login',   views.MyTokenObtainPairView.as_view()),
    path('signup',  views.register_user),

    # ── Image upload ──────────────────────────────────────────────────────────
    path('upload-image', views.upload_image),         # POST  (multipart)

    # ── Products ──────────────────────────────────────────────────────────────
    path('products',        views.products_list_create),   # GET / POST
    path('products/<int:pk>', views.product_detail),       # GET / PUT / DELETE

    # ── Categories ────────────────────────────────────────────────────────────
    path('categories',      views.categories_list_create), # GET / POST

    # ── Orders ────────────────────────────────────────────────────────────────
    path('buy',       views.create_order),
    path('my-orders', views.get_my_orders),

    # ── Misc (original) ───────────────────────────────────────────────────────
    path('hello',        views.index),
    path('ido_was_here', views.ido_was_here),
    path('test',         views.test),
    path('private',      views.private_mem),
]