from rest_framework import serializers
from utravel.models import CategoriaLugar, Ciudad, Lugares

class LugaresSerializer(serializers.ModelSerializer):

    
    catlug_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoriaLugar.objects.all(),
    )

    ciu_id = serializers.PrimaryKeyRelatedField(
        queryset=Ciudad.objects.all()
    )

    lug_imagen = serializers.ImageField(
        required=False, allow_null=True
    )

    """ Campos que nececito """
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
            "catlug_id",
            "ciu_id", 
            "lug_imagen",  
        ]
