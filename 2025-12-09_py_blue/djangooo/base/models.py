from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    priority = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Priority: {self.priority})"

class Product(models.Model):
    desc = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True,blank=True,default='/placeholder.png')
    createdTime = models.DateTimeField(auto_now_add=True)
    
    # The Foreign Key: linking each product to a category
    # on_delete=models.CASCADE means if a category is deleted, its products are also deleted.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.desc} - {self.price} NIS"

class User(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    age = models.DecimalField(max_digits=3, decimal_places=0)
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.age}"