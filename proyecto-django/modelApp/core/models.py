from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
# Create your models here.

class Cliente(models.Model):
    usuario = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    rut = models.CharField(max_length=9, null=True)
    nombre = models.CharField(max_length=20, null=True)
    apellido_paterno = models.CharField(max_length=20, null=True)
    apellido_materno = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=254)
    numero = models.CharField(max_length=9)

    def __str__(self):
        return str(self.nombre + ' ' + self.apellido_paterno + ' ' + self.apellido_materno)


class Solicitud(models.Model):

    # Tipo de defensa 
    CORPORATIVO = 'CP'
    BANCA = 'BN'
    DEFENSA = 'DF'
    ADMINISTRATIVO = 'AD'
    INMOBILIARIO = 'IM'
    SEGUROS = 'SG'
    MEDIOAMBIENTE = 'MA'

    TIPO_SOLICITUD = [
        (CORPORATIVO, 'Corporativo'),
        (BANCA, 'Bancario'),
        (DEFENSA, 'Defensa'),
        (ADMINISTRATIVO, 'Administrativo'),
        (INMOBILIARIO, 'Inmobiliario'),
        (SEGUROS, 'Seguros'),
        (MEDIOAMBIENTE, 'Medioambiente'),
    ]
    # Estado de la solicitud
    REVISION = 'RV'
    APROBADO = 'AP'
    RECHAZADO = 'RC'

    ESTADO_CONSULTA = [
        (REVISION, 'Revisión'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    ]
    
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cliente')
    tipo = models.CharField(max_length=2, choices=TIPO_SOLICITUD, default=DEFENSA)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    descripcion = models.TextField(null=False, default='')
    estado = models.CharField(max_length=2, choices=ESTADO_CONSULTA, default=REVISION)

    def __str__(self):
        return str(self.tipo + ' ' + self.cliente.rut + ' ' + self.estado)

    class Meta:
        verbose_name = 'Solicitude'

class PresupuestoCliente(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='solicitud')
    valor = models.CharField(null=False, default='0', max_length=9)
    pagado = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.solicitud.cliente.rut + ' | ' + self.solicitud.tipo + ' | ' + self.valor)

    class Meta:
        verbose_name = 'Presupuesto'

class ContratoCliente(models.Model):
     
    REVISION = 'RV'
    FIRMADO = 'FM'
    RECHAZADO = 'RC'

    CONTRATO_ESTADO = [
        (REVISION, 'Revisión'),
        (FIRMADO, 'Firmado'),
        (RECHAZADO, 'Rechazado'),
    ]

    presupuesto = models.ForeignKey(PresupuestoCliente, on_delete=models.CASCADE, related_name='presupuesto')
    archivo = models.FileField()
    estado = models.CharField(max_length=2, choices=CONTRATO_ESTADO, default=REVISION)

    def __str__(self):
        return str(self.presupuesto.solicitud.cliente.rut + ' | ' + self.presupuesto.solicitud.tipo + ' | ' + self.estado)

    class Meta:
        verbose_name = 'Contrato'

class Causa(models.Model):
    INICIO = 'IN'
    PREPARACION = 'PR'
    JUICIO = 'JC'
    APELACION = 'AP'
    PRUEBA = 'PB'
    CITACION = 'CT'
    EXHORTO = 'EH'
    IMPUNE = 'IP'

    CAUSA_ESTADO = [
        (INICIO, 'Inicio'),
        (PREPARACION, 'Preparación'),
        (JUICIO, 'Juicio'),
        (APELACION, 'Apelación'),
        (PRUEBA,'Prueba'),
        (CITACION, 'Citación'),
        (EXHORTO, 'Exhorto'),
        (IMPUNE, 'Impune'),
    ]

    contrato = models.ForeignKey(ContratoCliente, on_delete=models.CASCADE, related_name='contrato')
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    tribunal = models.CharField(max_length=200, default='1º Juzgado Civil de Santiago')
    etapa = models.CharField(max_length=2, choices=CAUSA_ESTADO, default=INICIO)

    def __str__(self):
        return str(self.contrato.presupuesto.solicitud.cliente.nombre + ' ' + self.etapa)

    

class NotificacionCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    informacion = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return str(self.cliente.rut)

    class Meta:
        verbose_name = 'Notificacione'
    