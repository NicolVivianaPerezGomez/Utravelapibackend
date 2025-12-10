from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

from utravel.api.serializers.serializer_resena import ResenaSerializer
from utravel.service.resenas_service import ResenasService
from rest_framework.parsers import MultiPartParser, FormParser


class ResenaApi(APIView):

    permission_classes = [IsAuthenticated]

    service = ResenasService()

    #METODO PARA LISTAR TODAS LAS RESEÑAS
    def get(self, request):

        reseñas = self.service.list_resenas()
        serializer = ResenaSerializer(reseñas, many=True) #con many permite validar muchos objetos y serializa todos JSON y validaciones
        return Response(serializer.data, status=status.HTTP_200_OK) #respuesta que muestra la consulta al terminar

    #METODO PARA CREAR RESEÑAS
    def post(self, request):

        serializer = ResenaSerializer(data=request.data) #datos serializados enviados por el cliente (request: datos que envia el usuario)

        if not serializer.is_valid(): #is_valid() ejecuta las validaciones necesarias
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #devuelve que campos/validaciones estan mal
        
        try: 
            resena = self.service.create_resena(**serializer.validated_data) # creando diccionario con informacion serializada (validada)
        
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        out_serializer = ResenaSerializer(resena) #Serializer para convertir datos a JSON
        return Response(out_serializer.data, status=status.HTTP_201_CREATED) #enviar datos creados al cliente
    
#BUSCAR CON EL ID
class ResenaDetailId(APIView):

    #permisos JWT
    permission_classes = [IsAuthenticated]

    service = ResenasService()

    #GET POR ID
    #traer objeto por id
    def get_object_id(self, id):
        return self.service.get_resenas_id(id)
        
    #método para validar y traer por ID
    def get(self, request, id:int):
            
        resena = self.get_object_id(id) #obtener resena

        if not resena:
            return Response ({"detail": "Reseña no eocontrada."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ResenaSerializer(resena) #serializar (validar y transformar)
        return Response(serializer.data, status=status.HTTP_200_OK) #enviar datos y respuesta ok
        
    #MÉTODO PARA ACTUALIZAR
    def put(self, request, id:int):

        resena = self.service.get_resenas_id(id)

        if not resena:
            return Response({"detail": "cliente no encontrado para actualizar."}, status=status.HTTP_404_NOT_FOUND)
            
            
        serializer = ResenaSerializer(resena, data=request.data) #informacion validada enviada por el cliente

        if not serializer.is_valid(): #si las validaciones fallan
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #devuelve que campos estan mal
            
        try:
            updated = self.service.update_resena(id, **serializer.validated_data) #actualizar con los datos serializados y validados 

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        out_serializer = ResenaSerializer(updated) #convertir a JSON

        return Response(out_serializer.data, status=status.HTTP_200_OK ) #enviar o mostrar datos actualizados al cliente

    #MÉTODO PARA DESACTIVAR        
    def delete(self, request, id:int):
        deleted = self.service.desativate_resena(id)

        if not deleted: #si no existe
            return Response({"detail:" "Reseña no encontrada."},
                        status=status.HTTP_404_NOT_FOUND)
            
        #retorno al cliente
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
                


        





