from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Photo

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_photo(req):
    image = req.FILES.get('image')
    if not image:
        return Response({'error': 'No image provided'}, status=400)
    photo = Photo.objects.create(user=req.user, image=image)
    return Response({'id': photo.id, 'image': photo.image.url}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_photos(req):
    photos = Photo.objects.filter(user=req.user)
    data = [{'id': p.id, 'image': p.image.url, 'uploaded_at': p.uploaded_at} for p in photos]
    return Response(data)