from rest_framework import serializers
from utravel.models import Lugares

class LugaresSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='catlug_id.catlug_descripcion', read_only=True)
    ciudad = serializers.CharField(source='ciu_id.ciu_descripcion', read_only=True)
    lug_imagen = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Lugares
        fields = [
            "lug_id",
            "lug_nombre",
            "lug_descripcion",
            "lug_ubicacion",
            "lug_latitud",
            "lug_longitud",
            "lug_status",
            "categoria",
            "ciudad",
            "lug_imagen",
        ]


