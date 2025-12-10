import pytest
from django.contrib.auth.hashers import check_password
from utravel.models import Usuario, Ciudad, TipoUsuario
from utravel.service.usuario_service import UsuarioService

@pytest.mark.django_db
class TestUsuarioService:

    @pytest.fixture
    def ciudad(self):
        return Ciudad.objects.create(ciu_descripcion="Bogotá")

    @pytest.fixture
    def tipo_empresa(self):
        return TipoUsuario.objects.create(tipousu_empresa=True)

    @pytest.fixture
    def tipo_turista(self):
        return TipoUsuario.objects.create(tipousu_turista=True)

    @pytest.fixture
    def service(self):
        return UsuarioService()

    def test_crear_usuario_exitoso(self, service, ciudad, tipo_empresa):
        data = {
            "usu_nombre": "Artemis",
            "usu_apellido": "Pérez",
            "usu_correo": "arte@example.com",
            "usu_contraseña": "123456",
            "usu_usunombre": "arte123",
            "usu_status": "1",
            "ciu_id": ciudad.ciu_id,
            "tipousu_id": tipo_empresa.tipousu_id
        }

        usuario = service.crear_usuario(data)

        # Comprobamos que se creó el usuario
        assert usuario.usu_id is not None
        assert usuario.usu_nombre == "Artemis"
        assert usuario.usu_correo == "arte@example.com"

        # La contraseña debe estar hasheada
        assert check_password("123456", usuario.usu_contraseña)

        # Las relaciones ForeignKey funcionan
        assert usuario.ciu_id == ciudad
        assert usuario.tipousu_id == tipo_empresa

    def test_crear_usuario_correo_existente(self, service, ciudad, tipo_empresa):
        # Crear un usuario previo
        Usuario.objects.create(
            usu_nombre="Prueba",
            usu_apellido="Test",
            usu_correo="existente@example.com",
            usu_contraseña="123",
            usu_usunombre="usuario1",
            usu_status="1",
            ciu_id=ciudad,
            tipousu_id=tipo_empresa
        )

        data = {
            "usu_nombre": "Artemis",
            "usu_apellido": "Pérez",
            "usu_correo": "existente@example.com",  # correo duplicado
            "usu_contraseña": "123456",
            "usu_usunombre": "arte123",
            "usu_status": "1",
            "ciu_id": ciudad.ciu_id,
            "tipousu_id": tipo_empresa.tipousu_id
        }

        with pytest.raises(ValueError) as excinfo:
            service.crear_usuario(data)
        assert "El correo ya está registrado." in str(excinfo.value)

    def test_crear_usuario_nombre_usuario_existente(self, service, ciudad, tipo_empresa):
        # Crear un usuario previo
        Usuario.objects.create(
            usu_nombre="Prueba",
            usu_apellido="Test",
            usu_correo="correo@test.com",
            usu_contraseña="123",
            usu_usunombre="arte123",  # nombre duplicado
            usu_status="1",
            ciu_id=ciudad,
            tipousu_id=tipo_empresa
        )

        data = {
            "usu_nombre": "Artemis",
            "usu_apellido": "Pérez",
            "usu_correo": "nuevo@example.com",
            "usu_contraseña": "123456",
            "usu_usunombre": "arte123",  # duplicado
            "usu_status": "1",
            "ciu_id": ciudad.ciu_id,
            "tipousu_id": tipo_empresa.tipousu_id
        }

        with pytest.raises(ValueError) as excinfo:
            service.crear_usuario(data)
        assert "El nombre de usuario ya existe." in str(excinfo.value)
