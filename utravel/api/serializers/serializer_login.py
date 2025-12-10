from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    usu_correo = serializers.EmailField()
    usu_contraseña = serializers.CharField(write_only=True)
