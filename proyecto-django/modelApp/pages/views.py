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
from django.db.models import Q


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
            print(user.email)
            # obtener datos extra
            apellido_paterno = request.POST.get('apellido_paterno')
            apellido_materno = request.POST.get('apellido_materno')
            numero = request.POST.get('numero')
            rut = request.POST.get('rut')
               
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

            messages.success(request, 'Cuenta creada exitosamente')
    
    
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
def user_page(request, action):
    # Main page de los clientes
    # Agregar: Presupuesto, contratos, causas
    context = {}
    user = request.user
    cliente = Cliente.objects.get(usuario=user)
    notificacion = NotificacionCliente.objects.all().filter(cliente=cliente)

    context['notifiaciones'] = notificacion

    if action == 'soli':
        context['nombre'] = 'Solicitud'
        try:
            solicitud = Solicitud.objects.all().filter(cliente=cliente)
            context["solicitudes"] = solicitud

        except:
            context["solicitudes"] = None

    elif action == 'presu':
        context['nombre'] = 'Presupuestos'
        try:
            presupuesto = PresupuestoCliente.objects.filter(Q(solicitud__cliente = cliente))
            context['presupuestos'] = presupuesto
        except:
            context['presupuestos'] = None
    elif action == 'contr':
        context['nombre'] = 'Contratos'
        try:
            contrato = ContratoCliente.objects.filter(Q(presupuesto__solicitud__cliente = cliente))
            context["contratos"] = contrato
        except:
            context["contratos"] = None
    elif action == 'inicio':
        context['nombre'] = 'Inicio'
        try:
            solicitud = Solicitud.objects.all().filter(cliente=cliente)
            context["solicitudes"] = solicitud

        except:
            context["solicitudes"] = None
        try:
            presupuesto = PresupuestoCliente.objects.filter(Q(solicitud__cliente = cliente))
            context['presupuestos'] = presupuesto
        except:
            context['presupuestos'] = None
        try:
            contrato = ContratoCliente.objects.filter(Q(presupuesto__solicitud__cliente = cliente))
            context["contratos"] = contrato
        except:
            context["contratos"] = None
    elif action == 'caus':
        context['nombre'] = 'Causas'


    return render(request, 'pages/user.html', context)

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['cliente'])
def ver_solicitud(request, pk):
    solicitud = Solicitud.objects.get(id=pk)
    context = {'solicitud': solicitud}
    try:
        presupuesto = PresupuestoCliente.objects.get(solicitud=solicitud)
        context['presupuesto'] = presupuesto
    except:
        context['presupuesto'] = 'sin presupuesto'

    try:
        contrato = ContratoCliente.objects.get(presupuesto=presupuesto)
        context['contrato'] = contrato
        if request.method == 'POST':
            contrato.estado = 'FM'
            contrato.save()

        print(contrato.estado)
    except:
         context['contrato'] = 'sin contrato'

    return render(request, 'pages/ver_solicitud.html', context)


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


# Parte de Tecnico
@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogado', 'tecnico'])
def funcionario(request, action):
    context = {}
    solicitud = Solicitud.objects.all()
    presupuesto = PresupuestoCliente.objects.all()
    contrato = ContratoCliente.objects.all()

    context["solicitudes"] = solicitud
    context['presupuestos'] = presupuesto
    context["contratos"] = contrato
    
    if action == 'inicio':
        context['nombre'] = 'Inicio'
    elif action == 'soli':
        context['nombre'] = 'Solicitudes'
    elif action == 'presu':
        context['nombre'] = 'Presupuestos'
    elif action == 'contr':
        context['nombre'] = 'Contratos'
    elif action == 'caus':
        context['nombre'] = 'Causas'

    return render(request, 'pages/funcionario.html', context)

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogado', 'tecnico'])
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
@usuarios_permitiado(roles_permitidos=['admin', 'tecnico'])
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
                datos = form.save()
                NotificacionCliente.objects.create(
                    cliente = datos.solicitud.cliente,
                    informacion = 'Se ha modificado presupuesto'
                )
                messages.info(request, 'Presupuesto creado con exito')
            else:
                messages.error(request, 'Presupuesto rechazado')
    except:
        form = PresupuestoForm()
        if request.method == 'POST':
            form = PresupuestoForm(request.POST)
            if form.is_valid():
                form.instance.solicitud = solicitud
                datos = form.save()
                NotificacionCliente.objects.create(
                    cliente = datos.solicitud.cliente,
                    informacion = 'Se ha creado presupuesto'
                )
                messages.info(request, 'Presupuesto creado con exito')
            else:
                messages.error(request, 'Presupuesto rechazado')

   
    
    context = {'form': form}
    return render(request, 'pages/presupuesto.html', context)

# Parte de abogados
@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogado'])
def listar_presupuesto(request):
    presupuestos = PresupuestoCliente.objects.all()


    context = {'presupuestos': presupuestos}
    return render(request, 'pages/listar_presupuestos.html', context)

@login_required(login_url='login')
@usuarios_permitiado(roles_permitidos=['admin', 'abogado'])
def contrato_page(request, pk):
    presupuesto = PresupuestoCliente.objects.get(id=pk)
    
    form = ContratoForm()

    try:
        contrato = ContratoCliente.objects.get(presupuesto = presupuesto)
        form = ContratoForm(instance=contrato)
        if request.method == 'POST':
            form = ContratoForm(request.POST, request.FILES, instance=contrato)
            if form.is_valid():
                datos = form.save()
                NotificacionCliente.objects.create(
                    cliente = datos.presupuesto.solicitud.cliente,
                    informacion = 'Contrato modificado'
                )

                messages.info(request, 'Aceptado')
            else:
                messages.error(request, 'Rechazado')
    except:
        contrato = 'no hay contrato'
        if request.method == 'POST':
            form = ContratoForm(request.POST, request.FILES)
            form.instance.presupuesto = presupuesto

            if form.is_valid():
                datos = form.save()
                NotificacionCliente.objects.create(
                    cliente = datos.presupuesto.solicitud.cliente,
                    informacion = 'Contrato creado'
                )
                messages.info(request, 'Aceptado')

            else:
                messages.error(request, 'Rechazado')

        
    context = {'presupuesto': presupuesto, 'contrato': contrato, 'form': form}
    return render(request, 'pages/contrato.html', context)