from django.shortcuts import render
from core.models import *

# Create your views here.


def home_page(request):
    context = {}

    return render(request, 'pages/home.html' ,context)

def contacto(request):
    return render(request, 'pages/contacto.html')

def listar_solicitudes(request):

    
    solicitudes = Solicitud.objects.all()

    context = {'solicitudes':solicitudes}
    print(solicitudes)

    return render(request, 'pages/listar_solicitudes.html', context)