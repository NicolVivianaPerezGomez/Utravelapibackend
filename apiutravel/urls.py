from django.contrib import admin
from django.urls import path, include

from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),
    path('admin/', admin.site.urls),
    path('usuarios/', UsuarioApi.as_view(), name='usuarios-list-create'),
    path('usuarios/<int:id>/', UsuarioApi.as_view(), name='usuarios-detail'),
]

urlpatterns += [
    path('api/utravel/', include('utravel.urls')),
]

