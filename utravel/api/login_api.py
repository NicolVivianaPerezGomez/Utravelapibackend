from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # ✅ Importar AllowAny
from utravel.service.usuario_service import UsuarioService

class LoginApi(APIView):
    permission_classes = [AllowAny]  # ✅ Permitir acceso sin token
    service = UsuarioService()

    def post(self, request):
        correo = request.data.get("usu_correo")
        contraseña = request.data.get("usu_contraseña")

        if not correo or not contraseña:
            return Response(
                {"error": "Correo y contraseña son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            tokens = self.service.login(correo, contraseña)
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            # Devolver siempre 400 para errores de login
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





