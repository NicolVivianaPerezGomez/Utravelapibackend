from rest_framework import serializers
from utravel.models import TipoExperiencia

class TipoExperienciaSerializer(serializers.ModelField):
    class Meta:
        model = TipoExperiencia
        fields = [
            "tipexp_id",
            "tipexp_descripcion",
            "tipexp_status"
        ]

