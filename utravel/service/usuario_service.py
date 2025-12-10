from typing import Optional, List
from utravel.models import Usuario, Ciudad, TipoUsuario
from utravel.repository.usuario_repository import UsuarioRepository
from django.contrib.auth.hashers import make_password

class UsuarioService:

    def __init__(self):
        self.repo = UsuarioRepository()

    # Crear y Registrar mi usuario 
    def crear_usuario(self, data: dict) -> Usuario:
        # Valido si el correo existe
        if self.repo.get_by_correo(data.get("usu_correo")):
            raise ValueError("El correo ya está registrado.")

        # Valido que el nombre sea diferente a uno registrado
        if self.repo.model.objects.filter(usu_usunombre=data.get("usu_usunombre")).exists():
            raise ValueError("El nombre de usuario ya existe.")

        # Convertir IDs a instancias de Ciudad y TipoUsuario
        ciudad = Ciudad.objects.get(ciu_id=data.get("ciu_id"))
        tipo = TipoUsuario.objects.get(tipousu_id=data.get("tipousu_id"))

        # Reemplazar los IDs por instancias
        data["ciu_id"] = ciudad
        data["tipousu_id"] = tipo

        # Hashear la contraseña
        data["usu_contraseña"] = make_password(data["usu_contraseña"])

        # Crear usuario usando el repo
        return self.repo.create(**data)
    
    # Actualizar usuario
    def actualizar_usuario(self, id: int, data: dict) -> Optional[Usuario]:
        usuario = self.repo.get_by_id(id)
        if not usuario:
            return None
        return self.repo.update(id, **data)

    # Desactivar
    def desactivar_usuario(self, id: int) -> bool:
        return self.repo.desactivate(id)

    # Listar usuarios
    def listar_usuarios(self) -> List[Usuario]:
        return self.repo.listarUsuarios()

    # Traer por ID
    def obtener_id(self, id: int) -> Optional[Usuario]:
        return self.repo.get_by_id(id)

    # Traer por correo
    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        return self.repo.get_by_correo(correo)
