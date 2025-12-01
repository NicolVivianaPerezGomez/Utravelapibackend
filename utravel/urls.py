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
