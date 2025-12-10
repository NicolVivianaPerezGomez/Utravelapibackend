from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utravel.api.serializers.serializer_usuario import UsuarioSerializer
from utravel.service.usuario_service import UsuarioService


class UsuarioApi(APIView):
    permission_classes = [IsAuthenticated]   # Exigir autenticación

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UsuarioService()

    # LISTAR TODOS O POR ID
    def get(self, request, id=None):
        if id is not None:
            usuario = self.service.obtener_id(id)
            if not usuario:
                return Response(
                    {"error": "Usuario no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)

        usuarios = self.service.listar_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

 
    # CREAR USUARIO
    def post(self, request, id=None):
        try:
            usuario = self.service.crear_usuario(request.data)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    # ACTUALIZAR USUARIO POR ID
    def put(self, request, id=None):
        if not id:
            return Response(
                {"error": "Debes enviar un ID para actualizar"},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = self.service.actualizar_usuario(id, request.data)

        if usuario is None:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DESACTIVAR USUARIO (DELETE)
    def delete(self, request, id=None):
        if id is None:
            return Response(
                {"error": "Debes enviar un ID para desactivar"},
                status=status.HTTP_400_BAD_REQUEST
            )

        exito = self.service.desactivar_usuario(id)

        if not exito:
            return Response(
                {"error": "Usuario no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"mensaje": "Usuario desactivado correctamente"},
            status=status.HTTP_200_OK
        )
