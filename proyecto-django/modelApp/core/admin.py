from django.contrib import admin
from .models import *

# Register your models here.
class AbogadoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'tipo', 'fecha', 'descripcion', 'estado']
    list_filter = ['estado']
    list_per_page = 10

admin.site.register(Cliente)
admin.site.register(Solicitud, AbogadoAdmin)
admin.site.register(PresupuestoCliente)
admin.site.register(ContratoCliente)
admin.site.register(NotificacionCliente)
admin.site.register(Causa)