from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def api_view (request ,*args, **kwargs):
    #request= instance de http request
    data= {
        'name':'fleurette',
        'language':'python',
    }
    return JsonResponse(data)