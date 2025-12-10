from rest_framework import serializers
from utravel.models import Lugares

class LugaresSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='catlug_id.catlug_descripcion', read_only=True)
    ciudad = serializers.CharField(source='ciu_id.ciu_descripcion', read_only=True)
    lug_imagen = serializers.SerializerMethodField()

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

    def get_lug_imagen(self, obj):
        request = self.context.get('request')
        if obj.lug_imagen:
            return request.build_absolute_uri(obj.lug_imagen.url) if request else obj.lug_imagen.url
        return None
