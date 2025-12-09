from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ..models import RutaTuristica
from .serializers.serializers_rutas import RutaTuristicaSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utravel.models import RutaTuristica
from utravel.api.serializers.serializers_rutas import RutaTuristicaSerializer


class RutaListCreateView(APIView):

    def get(self, request):
        rutas = RutaTuristica.objects.filter(rut_estado="1")
        serializer = RutaTuristicaSerializer(rutas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RutaTuristicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(rut_estado="1")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RutaRetrieveUpdateDestroyView(APIView):

    lookup_field = "id"  

    def get_object(self, id):
        try:
            return RutaTuristica.objects.get(rut_id=id, rut_estado="1")
        except RutaTuristica.DoesNotExist:
            return None

    def get(self, request, id):
        ruta = self.get_object(id)
        if not ruta:
            return Response({"error": "Ruta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RutaTuristicaSerializer(ruta)
        return Response(serializer.data)

    def put(self, request, id):
        ruta = self.get_object(id)
        if not ruta:
            return Response({"error": "Ruta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RutaTuristicaSerializer(ruta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ruta = self.get_object(id)
        if not ruta:
            return Response({"error": "Ruta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        ruta.rut_estado = "0"
        ruta.save()
        return Response({"mensaje": "Ruta desactivada correctamente"})
        # return Response(status=status.HTTP_204_NO_CONTENT)