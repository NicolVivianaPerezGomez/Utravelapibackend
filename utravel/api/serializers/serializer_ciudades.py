from rest_framework import serializers
from utravel.models import Ciudad

#hace validacion, convierte a JSON al modelo y del modelo a JSON

class CiudadesSerializer(serializers.ModelSerializer): #Crea un serializer que hereda de serialaziers funciones para hacer validaciones, mapear campos y crear o actualizar instancias

    #campos que neceseita validar
    class Meta:
        model = Ciudad #que modelo usar
        fields = [ #campos que envian y reciben en formato JSON con validaciones
            "ciu_id",
            "ciu_descripcion",
            "ciudad_status"
        ]


    
