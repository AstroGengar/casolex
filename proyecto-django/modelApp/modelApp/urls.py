"""modelApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('user/', user_page, name='user_page'),
    path('ingresar-solicitud', user_add_solicitud, name='user_add_solicitud'),
    path('pagos/', pagos_page, name='pagos_page'),
    path('contacto/', contacto, name='contacto'),
    path('listar-solicitudes/', listar_solicitudes, name='listar_solicitudes'),
    path('revisar-solicitud/<str:pk>/', revisar_solicitud, name='revisar_solicitud'),
    path('presupuesto-inicial/<str:pk>', presupuesto_inicial, name='presupuesto_inicial'),   
    path('contrato/<str:pk>', contrato_page, name='contrato_page'),
    
    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    