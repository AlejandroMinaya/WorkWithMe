from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    # Dashboard
    template = loader('index.html')
    context = {}
    return HttpResponse("index")

def add(request):
    return HttpResponse("klk")

def edit(request):
    return HttpResponse("hola")
