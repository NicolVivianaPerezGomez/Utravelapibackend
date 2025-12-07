from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utravel.api.serializers.serializer_tipoexperiencia import TipoExperienciaSerializer
from utravel.service.tipoexperiencia_service import TipoExperienciaService

#El rol de la capa API o Controller es la comunicación con el cliente, recibe valida usa el service
# y envia datos al cliente

class TExperienciaApi(APIView):

    #instanciando TipoExperienciaService

    service = TipoExperienciaService()

    #METODO PARA OBTENER LOS TIPOS DE EXPERIENCIA
    def get(self, request):
        experiencias = self.service.list_tpexp()
        serializer = TipoExperienciaSerializer(experiencias, many=True) #many: procesa una lista de objetos no solo uno
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #MÉTODO POST (CREAR)
    def post(self, request):

        serializer = TipoExperienciaSerializer(data=request.data) #datos serializados enviados por el cliente

        if not serializer.is_valid(): #is_valid() ejecuta las validaciones necesarias
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #devuelve que campos/validaciones que  estan mal
        
        try:
            experiencia = self.service.create_tpexp(**serializer.validated_data) #crear con datos ya validados 
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        out_serializer = TipoExperienciaSerializer(experiencia) #Serializar para converitr a JSON
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

#Buscar por el ID
class TExperienciaApiDetailId(APIView):

    service = TipoExperienciaService()

    #GET POR ID
    #traer objeto por id
    def get_object_id(self, id):
        return self.service.get_tpexp_id(id)
        
    #método para validar y enviar al cliente
    def get(self, request, id:int):
        experiencia = self.get_object_id(id)

        if not experiencia:
            return Response ({"detail": "Experiencia no encontrada."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = TipoExperienciaSerializer(experiencia) #validar y transformar a JSON
        return Response(serializer.data, status=status.HTTP_200_OK) #enviar al cliente
        
    #MÉTODO PARA ACTUALIZAR
    def put(self, request, id:int):

        experiencia = self.service.get_tpexp_id(id)

        if not experiencia:
            return Response ({"detail": "Experiencia no encontrada para actualizar."}, status=status.HTTP_404_NOT_FOUND)
            
        #pasar instancia al seriallizer
        serializer = TipoExperienciaSerializer(experiencia, data=request.data) #lleva el id y la info del cliente

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST) #devuelve que campos estan mal
            
        try:
            updated = self.service.update_tpexp(id, **serializer.validated_data) #actualziar info con el dicionario de la info validada
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_BAD_REQUEST)
            
        out_serializer = TipoExperienciaSerializer(updated) #converitr a JSON
        return Response(out_serializer.data, status=status.HTTP_200_OK) #Enviar la expe. actualizada al cliente
        
    #MÉTODO PARA DESACTIVAR
    def delete(self, request, id:int):
        deleted = self.service.desactivate_tpexp(id)

        if not deleted: #si no existe
            return Response({"detail:" "Experiencia no encontrada."},
                        status=status.HTTP_404_NOT_FOUND)
            
        #retorno al cliente
        return Response(status=status.HTTP_204_NO_CONTENT)
        
#FILTRAR POR NOMBRE
class TExperienciaApiDetailName(APIView):

    service = TipoExperienciaService()

    #GET POR NAME
    #traer objeto por nombre
    def get_object_name(self, name):
        return self.service.get_tpexp_name(name)
        
    #método para validar y enviar al cliente
    def get(self, request, name:str):
        experiencia = self.get_object_name(name)

        if not experiencia:
            return Response ({"detail": "Experiencia no encontrada."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = TipoExperienciaSerializer(experiencia) #validar y transformar a JSON
        return Response(serializer.data, status=status.HTTP_200_OK) #enviar al cliente

        
            

            






        




    