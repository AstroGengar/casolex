from django.db import models

# Create your models here.

class Cliente(models.Model):
    rut = models.CharField(max_length=9, null=False)
    nombre = models.CharField(max_length=20, null=False)
    apellido_paterno = models.CharField(max_length=20, null=False)
    apellido_materno = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=254)
    numero = models.CharField(max_length=9)

    def __str__(self):
        return self.nombre  + ' ' + self.apellido_paterno + ' ' + self.email

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
    rut = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPO_SOLICITUD, default=DEFENSA)

    def __str__(self):
        return self.tipo

class FormaPago(models.Model):
    pass

