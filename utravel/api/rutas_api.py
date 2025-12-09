from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ..models import RutaTuristica
from .serializers.serializers_rutas import RutaTuristicaSerializer


class RutaListCreateView(generics.ListCreateAPIView):
    """
    GET: List all active rutas (rut_estado='1').
    POST: Create a new ruta (sets rut_estado='1' by default).
    """
    serializer_class = RutaTuristicaSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return RutaTuristica.objects.filter(rut_estado="1")

    def get(self, request, *args, **kwargs):
        """List all active rutas."""
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create a new ruta with rut_estado='1'."""
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(rut_estado="1")


class RutaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific ruta by ID (rut_id).
    PUT/PATCH: Update a ruta (full or partial update).
    DELETE: Logically delete a ruta (sets rut_estado='0').
    """
    serializer_class = RutaTuristicaSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'rut_id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return RutaTuristica.objects.filter(rut_estado="1")

    def get(self, request, *args, **kwargs):
        """Retrieve a specific ruta."""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update a ruta (full update)."""
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Partial update a ruta."""
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Logically delete a ruta (set rut_estado='0')."""
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Logical delete: set rut_estado to '0' instead of removing the record."""
        instance.rut_estado = "0"
        instance.save()

