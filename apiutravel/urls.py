from django.contrib import admin
from django.urls import path, include
from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),
]

# Rutas adicionales
urlpatterns += [
    path('api/utravel/', include('utravel.urls')),
]
