from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(req):
    return Response('hello')


@api_view(['GET'])
def ido_was_here(req):
    return Response('ido_was_here')

@api_view(['GET'])
def test(req):
    return Response({'username': 'waga', 'age': 3})

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