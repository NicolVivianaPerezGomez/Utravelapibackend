from django.contrib import admin
from django.urls import path, include

# Importaciones de tus APIs
from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi
from utravel.api.usuario_api import UsuarioApi

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas lugares
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),

    # Rutas ussuarios
    path('usuarios/', UsuarioApi.as_view(), name='usuarios-list-create'),
    path('usuarios/<int:id>/', UsuarioApi.as_view(), name='usuarios-detail'),
]

# Rutas adicionales 
urlpatterns += [
    path('api/utravel/', include('utravel.urls')),
]

