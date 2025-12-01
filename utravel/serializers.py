from rest_framework import serializers
from .models import RutaTuristica


class RutaTuristicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = RutaTuristica
        fields = "__all__"

    # Validación: el nombre no puede repetirse entre rutas activas
    def validate_rut_nombre(self, value):
        queryset = RutaTuristica.objects.filter(
            rut_nombre=value,
            rut_estado="1"
        )
        # cuando instance es None, es creación; si existe ruta activa con ese nombre, fallar
        if queryset.exists() and self.instance is None:
            raise serializers.ValidationError("Ya existe una ruta con este nombre.")
        return value
