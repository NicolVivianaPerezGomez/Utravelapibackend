from rest_framework import serializers
from ...models import RutaTuristica


class RutaTuristicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = RutaTuristica
        fields = "__all__"
        read_only_fields = ("rut_estado",)

    # Validación: el nombre no puede repetirse entre rutas activas
    def validate_rut_nombre(self, value):
        # Comprueba unicidad entre rutas activas.
        queryset = RutaTuristica.objects.filter(
            rut_nombre=value,
            rut_estado="1"
        )

        # Si hay una instancia (update), exclúyela de la comprobación
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Ya existe una ruta con este nombre.")

        return value
