from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utravel.api.serializers.serializer_usuario import UsuarioSerializer
from utravel.service.usuario_service import UsuarioService


#HTTP
class UsuarioApi(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UsuarioService()

    #lista por id 
    def get(self, request, id=None):
        if id:
            usuario = self.service.obtener_id(id)
            if not usuario:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Si NO viene id → lista
        usuarios = self.service.listar_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #CREAR 
    def post(self, request, id=None):
        try:
            usuario = self.service.crear_usuario(request.data)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #ACTUALIZAR
    def put(self, request, id=None):
        if not id:
            return Response({"error": "Debes enviar un ID para actualizar"},status=status.HTTP_400_BAD_REQUEST)

        usuario = self.service.actualizar_usuario(id, request.data)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #ELIMINAR
    def delete(self, request, id=None):
        if not id:
            return Response({"error": "Debes enviar un ID para desactivar"},status=status.HTTP_400_BAD_REQUEST)

        ok = self.service.desactivar_usuario(id)
        if not ok:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"mensaje": "Usuario desactivado correctamente"}, status=status.HTTP_200_OK)
    