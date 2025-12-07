from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utravel.api.serializers.serializer_ciudades import CiudadesSerializer
from utravel.service.ciudad_service import CiudadService

#El rol de la capa API o Controller es la comunicación con el cliente, recibe valida usa el service
# y envia datos al cliente

class CiudadesApi(APIView):

    #instanciando CiudadService
    service = CiudadService()

    #METODO PARA RETORNAR/ENVIAR TODAS LAS CIUDADES
    def get(self, request):
        ciudades = self.service.list_ciudades() #trayendo el metodo de listar
        serializer = CiudadesSerializer(ciudades, many=True) #many: procesa una lista de objetos no solo uno, serializer: el que valida y pasa a JSON
        return Response(serializer.data, status=status.HTTP_200_OK) #Respuesta del API con dara serializada: información con status ok
    
    #METODO PARA CREAR
    def post(self, request):
        
        serializer = CiudadesSerializer(data=request.data) #datos serializados enviados por el cliente

        if not serializer.is_valid(): #is_valid() ejecuta las validaciones necesarias
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #devuelve que campos/validaciones estan mal
        
        try:
            ciudad = self.service.create_ciudad(**serializer.validated_data) #Crear con un diccioanrio "**" con la información validada
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        out_serializer = CiudadesSerializer(ciudad) #Serializer para convertir a JSON
        return Response(out_serializer.data, status=status.HTTP_201_CREATED) #enviar datos creados al cliente
    

#BUSAR CON EL ID
class CiudadApiDetailId(APIView):

    service = CiudadService()

    #GET POR ID
    #traer el objeto por nombre
    def get_object_id(self, id):
        return self.service.get_ciudad_id(id)

    #método de validar y enviar al cliente
    def get(self, request, id: int):
        ciudad = self.get_object_id(id)

        if not ciudad: #si no existe 
            return Response ({"detail": "Ciudad no eocontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CiudadesSerializer(ciudad) #serializar (validar y transformar)
        return Response(serializer.data, status=status.HTTP_200_OK) #enviar al cliente
    
    #MÉTODO PARA ACTUALIZAR
    def put(self, request, id:int):

        ciudad = self.service.get_ciudad_id(id)

        if not ciudad:
            return Response({"detail": "cliente no encontrado para actualizar."}, status=status.HTTP_404_NOT_FOUND)
        
        #pasar instancia al seriallizer
        serializer = CiudadesSerializer(ciudad, data=request.data) #request representa toda la info que envia el cliente al servidor

        if not serializer.is_valid(): #las validaciones son incorrectas
            return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST) #devuelve que campos estan mal
        
        try:
            updated = self.service.update_ciudad(id, **serializer.validated_data) #actualziar info con el dicionario de la info validada

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_BAD_REQUEST)
        
        out_serializer = CiudadesSerializer(updated) #convertir a JSON

        return Response(out_serializer.data, status=status.HTTP_200_OK) #Enviar la ciudad actualizada al cliente
    
    #METODO PARA DESACTIVAR
    def delete(self, request, id:int):
        deleted = self.service.desactivate_ciudad(id)

        if not deleted: #si no existe
            return Response({"detail:" "CIudad no encontrada."},
                            status=status.HTTP_404_NOT_FOUND)
        
        #retorno al cliente 
        return Response(status=status.HTTP_204_NO_CONTENT)


#FILTRAR POR NOMBRE
class CiudadApiDetailName(APIView):

    service = CiudadService();

    #FILTRAR POR NOMBRE
    #traer el objeto por nombre
    def get_object_name(self, name):
        return self.service.get_ciudad_name(name)

        
    #método de validar y enviar
    def get(self, request, name: str):
        ciudad = self.get_object_name(name)

        if not ciudad: #si no existe 
            return Response ({"detail": "Ciudad no eocontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CiudadesSerializer(ciudad) #serializar (validar y transformar)
        return Response(serializer.data, status=status.HTTP_200_OK) #enviar al cliente
    
