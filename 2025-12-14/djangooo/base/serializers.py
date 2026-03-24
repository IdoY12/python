from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product


# ── Existing serializer (kept as-is) ─────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


# ── Category ──────────────────────────────────────────────────────────────────
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'priority', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


# ── Product (read) ────────────────────────────────────────────────────────────
class ProductSerializer(serializers.ModelSerializer):
    # Nested category object in GET responses
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'desc', 'price', 'image', 'createdTime', 'category']
        read_only_fields = ['id', 'createdTime']


# ── Product (write) ───────────────────────────────────────────────────────────
# Separate write serializer so we accept category as a plain FK integer (id)
# while reads return the full nested object via ProductSerializer above.
class ProductWriteSerializer(serializers.ModelSerializer):
    # category is optional (nullable in the model)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    # image is optional
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['desc', 'price', 'image', 'category']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value


# ── Image upload (standalone, not tied to a product) ─────────────────────────
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()