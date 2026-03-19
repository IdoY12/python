from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(req):
    return Response('hello from /users')


@api_view(['GET'])
def ido_was_here(req):
    return Response('ido_was_here in /users')