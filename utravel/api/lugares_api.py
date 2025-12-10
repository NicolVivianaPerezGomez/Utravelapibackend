from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

from utravel.api.serializers.serializars_lugares import LugaresSerializer
from utravel.service.lugares_service import LugaresServices
from rest_framework.parsers import MultiPartParser, FormParser



class LugaresApiLC(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    service = LugaresServices()

    def get(self, request):
    # Trae todos los lugares activos con relaciones cargadas
        lugares = self.service.list_lugares().select_related('catlug_id', 'ciu_id')
        serializer = LugaresSerializer(lugares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = LugaresSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Guarda imagen
        lugar = serializer.save()

        out_serializer = LugaresSerializer(lugar)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


class LugaresDetailApi(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    service = LugaresServices()

    """ Metodo recibe id """
    def get_object (self, id):
        return self.service.get_lugares_id(id)

    """ Metodo que llama al anterior para que haga la invocacion al service"""
    def get(self, request, id: int):
        lugares = self.get_object(id)
        if not lugares:
            return Response({"detail": "Lugar no encontrado"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = LugaresSerializer(lugares)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id: int):
        lugar = self.service.get_lugares_id(id)
        if not lugar:
            return Response({"detail": "Lugar no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LugaresSerializer(lugar, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
            updated_lugar = serializer.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(LugaresSerializer(updated_lugar).data, status=status.HTTP_200_OK)

    
    def delete(self, request, id:int):
        deleted = self.service.deactivate_lugares(id)
        if not deleted:
            return Response({"detail": "Lugar no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
