
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
    path('pagos/', pagos_page, name='pagos_page'),
    path('ver-solicitud/<str:pk>', ver_solicitud, name='ver_solicitud'),
    # parte tecnico
    path('func/<action>/', funcionario, name='funcionario'),
    path('listar-solicitudes/', listar_solicitudes, name='listar_solicitudes'),
    path('revisar-solicitud/<str:pk>/', revisar_solicitud, name='revisar_solicitud'),
    path('presupuesto-inicial/<str:pk>', presupuesto_inicial, name='presupuesto_inicial'),   
    path('add-presupuesto/', add_presupuesto_page, name='add_presupuesto_pages'),
    path('listar-presupuestos/', listar_presupuesto, name='listar_presupuesto'),
    path('contrato/<str:pk>', contrato_page, name='contrato_page'),
    
    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = "Administración Lex"
admin.site.index_title = "Modulos de administración"
admin.site.site_title = "Abogados Lex"