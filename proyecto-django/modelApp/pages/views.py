import django
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from core.models import *
from core.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from core.decorators import *


# Create your views here.


def home_page(request):
    context = {}

    return render(request, 'pages/home_contenido.html' ,context)

def contacto(request):
    return render(request, 'pages/contacto.html')

def register_page(request):
    form = CreateUserForm()
    form_cliente = ClienteForm()

    if request.method == 'POST':
        form_cliente = CreateUserForm(request.POST)
        form_datos = ClienteForm(request.POST)
        if form_cliente.is_valid():
            user = form_cliente.save()
            # obtener datos extra
            apellido_paterno = request.POST.get('apellido_paterno')
            apellido_materno = request.POST.get('apellido_materno')
            numero = request.POST.get('numero')
            rut = request.POST.get('rut')
            user_name = form_cliente.cleaned_data.get('username')
               
            group = Group.objects.get(name='cliente')
            user.groups.add(group)
            Cliente.objects.create(
                usuario=user,
                nombre=user.username,
                email=user.email,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                numero=numero,
                rut=rut,
            )

            messages.success(request, 'Cuenta creada exitosamente '+ user_name)
    
    
    context = {'form': form, 'formCliente': form_cliente}
    return render(request, 'pages/register_page.html', context)

@usuario_identificado
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Usuario o contraseña incorrecto')

    context = {}
    return render(request, 'pages/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login') 

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['cliente'])
def user_page(request):
    solicitudes = request.user.cliente.cliente.all()
    print(solicitudes)
    context = {'solicitudes': solicitudes}
    return render(request, 'pages/user.html', context)
    
@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['cliente'])
def pagos_page(request):
    context = {}
    return render(request, 'pages/pagos.html', context)

@usuarios_permitiado(roles_permitidos=['admin', 'abogados', 'tecnico'])
def listar_solicitudes(request):

    
    solicitudes = Solicitud.objects.all()

    context = {'solicitudes':solicitudes}

    return render(request, 'pages/listar_solicitudes.html', context)