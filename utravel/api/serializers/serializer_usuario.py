from rest_framework import serializers
from utravel.models import Usuario

#Los serializadores permiten convertir datos complejos 
#como conjuntos de consultas e instancias de modelos a tipos nativos de Python 
#que luego pueden renderizarse fácilmente 
class UsuarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = [
            "usu_id",
            "usu_nombre",
            "usu_apellido",
            "usu_correo",
            "usu_contraseña",
            "usu_usunombre",
            "usu_status",
            "ciu_id",
            "tipousu_id",
        ]
