from django.db import models
from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#code


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'apellido_paterno', 'apellido_materno', 'numero']

        widgets = {
            'rut':forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno':forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno':forms.TextInput(attrs={'class': 'form-control'}),
            'numero':forms.TextInput(attrs={'class': 'form-control'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class SolicitudUserForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['tipo','descripcion']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('cliente', None)
        super(SolicitudUserForm, self).__init__(*args, **kwargs)
        

class SolicitudForm(forms.ModelForm):

    class Meta:
        model = Solicitud
        fields = ['estado']
        # estado = forms.ChoiceField(choices=ESTADO_CONSULTA)
    

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = PresupuestoCliente
        fields = ['valor']


class ContratoForm(forms.ModelForm):
    class Meta:
        model = ContratoCliente
        fields = ['archivo', 'estado']