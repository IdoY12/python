from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction

from .models import Order, OrderItem, Product, Category
from .serializers import (
    RegisterSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductWriteSerializer,
    ImageUploadSerializer,
)


# ─────────────────────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────────────────────

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['waga'] = "baga"
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────────────────────────────────────
# Image upload  POST /api/upload-image
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """
    Accepts a single image file and returns its saved URL.
    The file is stored via Django's default MEDIA storage (configure MEDIA_ROOT
    and MEDIA_URL in settings.py).

    Request (multipart/form-data):
        image  — required, image file

    Response 201:
        { "url": "/media/..." }
    """
    serializer = ImageUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    image_file = serializer.validated_data['image']

    # Save directly under MEDIA_ROOT/uploads/
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile

    path = default_storage.save(f'uploads/{image_file.name}', ContentFile(image_file.read()))
    url = default_storage.url(path)

    return Response({'url': url}, status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────────────────────────────────────────
# Products   GET /api/products   POST /api/products
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def products_list_create(request):
    """
    GET  — returns all products with nested category object.
    POST — creates a new product (multipart/form-data).

    POST body:
        desc      — string, max 50 chars
        price     — decimal  e.g. "49.99"
        category  — integer (Category pk), optional
        image     — image file, optional

    Response 201:
        Full ProductSerializer output (nested category).
    """
    if request.method == 'GET':
        products = Product.objects.select_related('category').filter(uploaded_by=request.user)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    # POST
    write_serializer = ProductWriteSerializer(data=request.data)
    if not write_serializer.is_valid():
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    product = write_serializer.save(uploaded_by=request.user)

    # Return the full read representation (nested category)
    read_serializer = ProductSerializer(product, context={'request': request})
    return Response(read_serializer.data, status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────────────────────────────────────────
# Single product   GET/PUT/DELETE /api/products/<id>
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def product_detail(request, pk):
    """
    GET    — returns a single product.
    PUT    — updates the product (partial update supported).
    DELETE — deletes the product.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        write_serializer = ProductWriteSerializer(product, data=request.data, partial=True)
        if not write_serializer.is_valid():
            return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        updated = write_serializer.save()
        read_serializer = ProductSerializer(updated, context={'request': request})
        return Response(read_serializer.data)

    # DELETE
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────────────────────────────────────
# Categories   GET /api/categories   POST /api/categories
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def categories_list_create(request):
    """
    GET  — returns all active categories.
    POST — creates a new category.

    POST body:
        title     — string, max 100 chars (required)
        priority  — integer, default 1
        is_active — boolean, default true
    """
    if request.method == 'GET':
        categories = Category.objects.filter(is_active=True).order_by('priority')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────────────────────────────────────
# Orders (kept from original)
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    items = request.data.get('items', [])
    if not items:
        return Response({'error': 'No items provided'}, status=400)

    with transaction.atomic():
        order = Order.objects.create(user=request.user)
        for item in items:
            product = get_object_or_404(Product, id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.get('quantity', 1),
                price=product.price,
            )

    return Response({'order_id': order.id, 'status': order.status}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    orders = Order.objects.filter(user=request.user)
    data = [
        {
            'order_id': order.id,
            'status': order.status,
            'created_at': order.created_at,
            'items': [
                {'product': item.product.desc, 'quantity': item.quantity, 'price': item.price}
                for item in order.items.all()
            ],
        }
        for order in orders
    ]
    return Response(data)


# ─────────────────────────────────────────────────────────────────────────────
# Misc (kept from original)
# ─────────────────────────────────────────────────────────────────────────────

@api_view(['GET'])
def index(request):
    return Response('hello')

@api_view(['GET'])
def ido_was_here(request):
    return Response('ido_was_here')

@api_view(['GET'])
def test(request):
    return Response({'username': 'waga', 'age': 3})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def private_mem(request):
    user = request.user
    print(f"{user} this is 'def private_mem' in /private")
    return Response({'Welcome': user.email})