from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer   # --> Login
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Order, OrderItem, Product
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(req):
    items = req.data.get('items', [])

    if not items:
        return Response({'error': 'No items provided'}, status=400)

    with transaction.atomic():
        order = Order.objects.create(user=req.user)

        for item in items:
            product = get_object_or_404(Product, id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.get('quantity', 1),
                price=product.price
            )

    return Response({'order_id': order.id, 'status': order.status}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(req):
    orders = Order.objects.filter(user=req.user)
    
    data = []
    for order in orders:
        data.append({
            'order_id': order.id,
            'status': order.status,
            'created_at': order.created_at,
            'items': [
                {
                    'product': item.product.desc,
                    'quantity': item.quantity,
                    'price': item.price,
                }
                for item in order.items.all()
            ]
        })

    return Response(data)


# return jwt to user
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom columns
        token['username'] = user.username
        token['email'] = user.email
        token['waga'] = "baga"
        # ...

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def index(req):
    return Response('hello')


@api_view(['GET'])
def ido_was_here(req):
    return Response('ido_was_here')

@api_view(['GET'])
def test(req):
    return Response({'username': 'waga', 'age': 3})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def private_mem(req):
    user = req.user
    print(f"{user} this is 'def private_mem' in /private")
    return Response({'Welcome': user.email})


# DRF create user in the table for us
@api_view(['POST'])
def register_user(request):
    # Initialize the serializer with the incoming data from the request
    serializer = RegisterSerializer(data=request.data)
    
    # Check if the data is valid (username exists, password length, etc.)
    if serializer.is_valid():
        # This triggers the 'create' method inside our Serializer
        serializer.save()
        
        # Return a success message with 201 Created status
        return Response(
            {"message": "User created successfully"}, 
            status=status.HTTP_201_CREATED
        )
    
    # If not valid, return the errors (e.g., "This username is already taken")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

