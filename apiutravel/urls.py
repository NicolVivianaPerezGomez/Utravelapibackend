from django.contrib import admin
from django.urls import path, include

# Importaciones de tus APIs
from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi
from utravel.api.usuario_api import UsuarioApi
from utravel.api.ciudad_api import CiudadesApi, CiudadApiDetailName, CiudadApiDetailId

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas lugares
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),

    # Rutas ussuarios
    path('usuarios/', UsuarioApi.as_view(), name='usuarios-list-create'),
    path('usuarios/<int:id>/', UsuarioApi.as_view(), name='usuarios-detail'),

    #Rutas de ciudades
    path('ciudades/', CiudadesApi.as_view(), name='ciudades-all-create'), #listar y crear
    path('ciudades/<int:id>/', CiudadApiDetailId.as_view(), name='ciudades-details'), #Actulizar, desactivar y filtrar por id
    path('ciudades/<str:name>/', CiudadApiDetailName.as_view(), name='ciudades-names'), #filtrar por nombre 
]

# Rutas adicionales 
urlpatterns += [
    path('api/utravel/', include('utravel.urls')),
]

