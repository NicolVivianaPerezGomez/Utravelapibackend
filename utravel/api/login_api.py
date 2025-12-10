from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utravel.service.usuario_service import UsuarioService

class LoginApi(APIView):
    service = UsuarioService()

    def post(self, request):
        correo = request.data.get("usu_correo")
        contraseña = request.data.get("usu_contraseña")
        try:
            tokens = self.service.login(correo, contraseña)
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



