from django.shortcuts import render
from django.http import JsonResponse


def index(req):
    return JsonResponse('hello', safe=False)