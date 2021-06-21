import django
from django.contrib.auth import authenticate
from django.http import request
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
# Parte de los clientes
@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['cliente'])
def user_page(request):
    # Main page de los clientes
    solicitudes = request.user.cliente.cliente.all()
    print(solicitudes)
    context = {'solicitudes': solicitudes}
    return render(request, 'pages/user.html', context)

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['cliente'])
def user_add_solicitud(request):
    # Ingresar solicitud de un cliente
    forms = SolicitudUserForm()
        
    if request.method == 'POST':
        cliente = request.user.cliente
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        
        try:
            Solicitud.objects.create(
                cliente=cliente,
                tipo=tipo,
                descripcion=descripcion
            )
            messages.info(request, 'Solicitud creada con exito')
        except Exception as e:
            messages.info(request, 'Solicitud no pudo ser creada')

    context = {'forms': forms}
    return render(request, 'pages/ingresar_solicitud.html', context)
    
@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['cliente'])
def pagos_page(request):
    context = {}
    return render(request, 'pages/pagos.html', context)


# Parte de Admin
@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogados', 'tecnico'])
def listar_solicitudes(request):

    solicitudes = Solicitud.objects.all()

    context = {'solicitudes':solicitudes}

    return render(request, 'pages/listar_solicitudes.html', context)

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogados', 'tecnico'])
def revisar_solicitud(request, pk):
    solicitud = Solicitud.objects.get(id=pk)
    form = SolicitudForm(instance=solicitud)
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Solicitud actualizada con exito')
            else:
                messages.error(request, 'No se pudo actualizar la información')
        except Exception as e:
            print(e)

    context = {'form': form, 'solicitud': solicitud}
    return render(request, 'pages/revisar_solicitud.html', context)


@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogados', 'tecnico'])
def presupuesto_inicial(request, pk):
    solicitud = Solicitud.objects.get(id=pk)
    form = PresupuestoForm()
    try:
        presupuesto = PresupuestoCliente.objects.get(solicitud=solicitud)
        form = PresupuestoForm(instance=presupuesto)
        if request.method == 'POST':
            form = PresupuestoForm(request.POST, instance=presupuesto)
            if form.is_valid():
                form.instance.solicitud = solicitud
                form.save()
                messages.info(request, 'Presupuesto creado con exito')
            else:
                messages.error(request, 'Presupuesto rechazado')
    except:
        form = PresupuestoForm()
        if request.method == 'POST':
            form = PresupuestoForm(request.POST)
            if form.is_valid():
                form.instance.solicitud = solicitud
                form.save()
                messages.info(request, 'Presupuesto creado con exito')
            else:
                messages.error(request, 'Presupuesto rechazado')

   
    
    context = {'form': form}
    return render(request, 'pages/presupuesto.html', context)

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogados'])
def contrato_page(request, pk):
    presupuesto = PresupuestoCliente.objects.get(id=pk)
    
    form = ContratoForm()
    try:
        contrato = ContratoCliente.objects.get(presupuesto = presupuesto)
        form = ContratoForm(instance=contrato)
        if request.method == 'POST':
            form = ContratoForm(request.POST, instance=contrato)
            if form.is_valid():
                form.save()
    except:
        contrato = 'no hay contrato'
        if request.method == 'POST':
            form = ContratoForm(request.POST, request.FILES)
            form.instance.presupuesto = presupuesto

            if form.is_valid():
                form.save()
                messages.info(request, 'Aceptado')

            else:
                messages.error(request, 'rechazado')

        
    context = {'presupuesto': presupuesto, 'contrato': contrato, 'form': form}
    return render(request, 'pages/contrato.html', context)