"""
URL configuration for apiutravel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import path
from .views import (
    listar_rutas,
    crear_ruta,
    obtener_ruta,
    actualizar_ruta,
    eliminar_ruta
)

urlpatterns = [
    path("rutas/", listar_rutas, name="listar_rutas"),
    path("rutas/crear/", crear_ruta, name="crear_ruta"),
    path("rutas/<int:id>/", obtener_ruta, name="obtener_ruta"),
    path("rutas/<int:id>/actualizar/", actualizar_ruta, name="actualizar_ruta"),
    path("rutas/<int:id>/eliminar/", eliminar_ruta, name="eliminar_ruta"),
]

