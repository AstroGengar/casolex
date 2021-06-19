from django.db import models
from django.contrib.auth.models import User
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
    descripcion = models.TextField(null=False, default='lorem')
    estado = models.CharField(max_length=2, choices=ESTADO_CONSULTA, default=REVISION)

    def __str__(self):
        return str(self.tipo + ' ' + self.cliente.rut + ' ' + self.estado)
