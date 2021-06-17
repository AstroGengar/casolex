from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cliente(models.Model):
    usuario = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    rut = models.CharField(max_length=9, null=False)
    nombre = models.CharField(max_length=20, null=False)
    apellido_paterno = models.CharField(max_length=20, null=False)
    apellido_materno = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=254)
    numero = models.CharField(max_length=9)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.rut)

class Solicitud(models.Model):
    
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
    
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cliente')
    tipo = models.CharField(max_length=2, choices=TIPO_SOLICITUD, default=DEFENSA)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    descripcion = models.TextField(null=True)

    def __str__(self):
        return str(self.cliente)
