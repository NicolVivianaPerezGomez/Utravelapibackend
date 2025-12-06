from typing import Optional, List
from utravel.models import Usuario
from utravel.repository.usuario_repository import UsuarioRepository

class UsuarioService:

    def __init__(self):
        self.repo = UsuarioRepository()

    # Crear y Registrar mi usuario 
    def crear_usuario(self, data: dict) -> Usuario:
        # Valido si el correo existe
        if self.repo.get_by_correo(data.get("usu_correo")):
            raise ValueError("El correo ya está registrado.")

        #Valido que el nombre sea difetente a uno registrado
        if self.repo.model.objects.filter(usu_usunombre=data.get("usu_usunombre")).exists():
            raise ValueError("El nombre de usuario ya existe.")
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

    #Traer por ID
    def obtener_id(self, id: int) -> Optional[Usuario]:
        return self.repo.get_by_id(id)

    #Traer por correo
    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        return self.repo.get_by_correo(correo)
