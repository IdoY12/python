from django.contrib import admin
# Import the specific classes from your models.py file
from .models import Product, Category

# Register each model to make it visible in the Admin panel
admin.site.register(Product)
admin.site.register(Category)