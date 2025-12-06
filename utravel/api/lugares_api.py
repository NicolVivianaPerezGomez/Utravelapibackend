from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utravel.api.serializers.serializars_lugares import LugaresSerializer
from utravel.service.lugares_service import LugaresServices


class LugaresApiLC(APIView):
    service = LugaresServices()

    def get(self,request):
        lugares = self.service.list_lugares()
        serializer = LugaresSerializer(lugares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """ Metodo crear un nuevo lugar"""
    def post(self, request):
        serializer = LugaresSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Si esta bien se crea el lugar si no mandamos un 400
        try:
            lugar = self.service.create_lugares(**serializer.validated_data)
        except ValueError as e:
            # Reglas de negocio
            return Response({"detail":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        out_serializer = LugaresSerializer(lugar)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
    

class LugaresDetailApi(APIView):
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
    
    def put(self, request, id:int):
        lugares = self.service.get_lugares_id(id)
        if not lugares:
            return Response ({"detail": "Lugar no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Pasar instancia al serializer (clave)
        serializer = LugaresSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            update = self.service.update_lugares(id, **serializer.validated_data)
        except ValueError as e:
            # Reglas de negocio: Inactivo
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        out_serializer = LugaresSerializer(update)
        return Response(out_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id:int):
        deleted = self.service.deactivate_lugares(id)
        if not deleted:
            return Response({"detail": "Lugar no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
