from rest_framework import serializers
from utravel.models import Usuario, Ciudad, TipoUsuario
from django.contrib.auth.hashers import make_password

class UsuarioSerializer(serializers.ModelSerializer):
    # Estos campos ahora aceptan IDs y los convierten a instancias automáticamente
    ciu_id = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())
    tipousu_id = serializers.PrimaryKeyRelatedField(queryset=TipoUsuario.objects.all())

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
        extra_kwargs = {
            "usu_contraseña": {"write_only": True},  # No mostrar contraseña en GET
        }

    # Al crear, convertimos la contraseña a hash
    def create(self, validated_data):
        validated_data["usu_contraseña"] = make_password(validated_data["usu_contraseña"])
        return super().create(validated_data)
