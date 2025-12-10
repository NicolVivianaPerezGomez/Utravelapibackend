from rest_framework import serializers
from utravel.models import Usuario, Lugares, Reseña

#hace validacion, convierte a JSON al modelo y del modelo a JSON

class ResenaSerializer(serializers.ModelSerializer):

    usu_id = serializers.PrimaryKeyRelatedField( #usu_id = campo a validad
        queryset=Usuario.objects.all(),          #PrimaryKeyRelatedField indicar relacion SOLO ID
    )                                            #Lista de usuarios donde se comprueba si el ID existe

    lug_id = serializers.PrimaryKeyRelatedField(
        queryset = Lugares.objects.all()
    )

    #campos que neceito validar
    class Meta:
        model = Reseña 
        fields = [ #campos que envian y reciben en formato JSON con validaciones
            "res_id",
            "res_calificacion",
            "res_comentario",
            "res_fecha",
            "res_visible",
            "usu_id",
            "lug_id",
            "res_status",
        ]

