from django.contrib import admin
from django.urls import path, include
from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi
from utravel.api.usuario_api import UsuarioApi

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas lugares
    # Lista y creación
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    # Actualizar, desactivar por id
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),

    # Rutas usuarios
    path('usuarios/', UsuarioApi.as_view(), name='usuarios-list-create'),
    path('usuarios/<int:id>/', UsuarioApi.as_view(), name='usuarios-detail'),
]

# Rutas adicionales
urlpatterns += [
    path('api/utravel/', include('utravel.urls')),
]
