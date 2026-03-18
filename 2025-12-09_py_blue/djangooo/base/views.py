from django.shortcuts import render
from django.http import JsonResponse


def index(req):
    return JsonResponse('hello', safe=False)


def ido_was_here(req):
    return JsonResponse('ido_was_here', safe=False)