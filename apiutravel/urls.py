from django.contrib import admin
from django.urls import path, include

# Importaciones de tus APIs
from utravel.api.login_api import LoginApi
from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi
from utravel.api.usuario_api import UsuarioApi
from utravel.api.ciudad_api import CiudadesApi, CiudadApiDetailName, CiudadApiDetailId
from utravel.api.tipoexperiencia_api import TExperienciaApi, TExperienciaApiDetailId, TExperienciaApiDetailName
from utravel.api.rutas_api import RutaListCreateView, RutaRetrieveUpdateDestroyView
from utravel.api.resena_api import ResenaApi, ResenaDetailId

# JWT importaciones
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Media
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # JWT routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Admin
    path('admin/', admin.site.urls),

    # Rutas lugares
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),

    # Rutas ussuarios
    path('usuarios/', UsuarioApi.as_view(), name='usuarios-list-create'),
    path('usuarios/<int:id>/', UsuarioApi.as_view(), name='usuarios-detail'),
    path("api/login/", LoginApi.as_view(), name="login"),

    #Rutas de ciudades
    path('ciudades/', CiudadesApi.as_view(), name='ciudades-all-create'), #listar y crear
    path('ciudades/<int:id>/', CiudadApiDetailId.as_view(), name='ciudades-details'), #Actulizar, desactivar y filtrar por id
    path('ciudades/<str:name>/', CiudadApiDetailName.as_view(), name='ciudades-names'), #filtrar por nombre 

    #Rutas de Tipo de experiencia 
    path('tipo_exp/', TExperienciaApi.as_view(), name='tipoexperiencias-all-create'), #listar y crear
    path('tipo_exp/<int:id>/', TExperienciaApiDetailId.as_view(), name='tipoexperiencias-details'), #Actulizar, desactivar y filtrar por id
    path('tipo_exp/<str:name>/', TExperienciaApiDetailName.as_view(), name='tipoexperiencias-names'), #filtrar por nombre 

    # Rutas de RutaTuristica
    path('api/utravel/rutas/', RutaListCreateView.as_view(), name='rutas-list-create'),
    path('api/utravel/rutas/crear/', RutaListCreateView.as_view(), name='rutas-crear'),
    path('api/utravel/rutas/<int:id>/', RutaRetrieveUpdateDestroyView.as_view(), name='rutas-detail'),
    path('api/utravel/rutas/<int:id>/actualizar/', RutaRetrieveUpdateDestroyView.as_view(), name='rutas-actualizar'),
    path('api/utravel/rutas/<int:id>/eliminar/', RutaRetrieveUpdateDestroyView.as_view(), name='rutas-eliminar'),

    #Rutas de Reseña
    path('resenas/', ResenaApi.as_view(), name='resenas-all-create'), #listar y crear
    path('resenas/<int:id>/', ResenaDetailId.as_view(), name='tipoexperiencias-details'), #Actulizar, desactivar y filtrar por id

]

#Usuario para pedir tokens
""" {
        "username": "root",
        "password":"1234"
    }
""" 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)