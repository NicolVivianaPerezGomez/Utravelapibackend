from django.urls import path
from ..service import views

urlpatterns = [
    path('rutas/', views.listar_rutas, name='listar_rutas'),
    path('rutas/crear/', views.crear_ruta, name='crear_ruta'),
    path('rutas/<int:id>/', views.obtener_ruta, name='obtener_ruta'),
    path('rutas/<int:id>/actualizar/', views.actualizar_ruta, name='actualizar_ruta'),
    path('rutas/<int:id>/eliminar/', views.eliminar_ruta, name='eliminar_ruta'),
]
