
from os import name
from django.contrib import admin
from django.urls import path
from pages.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Para cualquiera
    path('', home_page, name='home'),
    path('contacto/', contacto, name='contacto'),
    # Para ususarios
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('user/<action>/', user_page, name='user_page'),
    path('ingresar-solicitud', user_add_solicitud, name='user_add_solicitud'),
    path('ver-solicitud/<str:pk>', ver_solicitud, name='ver_solicitud'),
    path('pagar/<str:pk>', pagar_page, name='pagar_page'),
    # parte tecnico
    path('func/<action>/', funcionario, name='funcionario'),
    path('listar-solicitudes/', listar_solicitudes, name='listar_solicitudes'),
    path('revisar-solicitud/<str:pk>/', revisar_solicitud, name='revisar_solicitud'),
    path('presupuesto-inicial/<str:pk>', presupuesto_inicial, name='presupuesto_inicial'),   
    path('add-presupuesto/', add_presupuesto_page, name='add_presupuesto_pages'),
    path('contrato/<str:pk>', contrato_page, name='contrato_page'),

    path('causa/<str:pk>', ver_causa, name='ver_causa'),
    path('add-contrato/', add_contrato, name='add_contrato'),
    path('ingresos/', ver_ingresos, name='ver_ingresos'),
    
    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = "Administración Lex"
admin.site.index_title = "Modulos de administración"
admin.site.site_title = "Abogados Lex"