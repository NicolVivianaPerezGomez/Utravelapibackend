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
from django.urls import path, include

from utravel.api.lugares_api import LugaresApiLC, LugaresDetailApi

urlpatterns = [
    path('admin/', admin.site.urls),
    # Lista y creación
    path('lugares/', LugaresApiLC.as_view(), name="lugares-all-create"),
    # Actualizar, desactivar y detalle por id
    path('lugares/<int:id>/', LugaresDetailApi.as_view(), name="lugares-details"),
]

urlpatterns += [
    path('api/utravel/', include('utravel.urls')),
]

