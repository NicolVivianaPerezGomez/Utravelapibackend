#Esta capa de datos va a estar interactuando e inyectando a mi base de datos información a través del ORM que nos da python
#ORM es abstracción de bases de datos
#metodos que me van a permirir ese intercambio con la db

from django.db.models import QuerySet
from typing import Optional
from utravel.models import Usuario

class UsuarioRepository:
    #Declarando una referencia a la clase no al objeto 
    model = Usuario
    
    #Crear un Usuario
    def create(self, **data)->Usuario:
        return Usuario.objects.create(**data)
    
    #Actualizar un Usuario
    def update(self, id: int, **data) -> Optional[Usuario]:
        usuario_obj = Usuario.objects.filter(pk=id).first()
        if not usuario_obj:
            return None
        
        for field, value in data.items():
            setattr(usuario_obj, field, value)
        
        usuario_obj.save() 
        return usuario_obj

    
    #Aquí desactivo por status 
    def desactivate(self, id:int) -> bool:
         deleted = Usuario.objects.filter(pk=id).update(usu_status="0")
         return deleted > 0 # retorna true si un registro fue actualizado por eso > 0
    
    # Listar todos los usuarios
    def listarUsuarios(self) -> QuerySet [Usuario]:
        return(
            self.model.objects
            .select_related("tipousu_id")
            .all()
        )
    
#CONSULTAS
      # Consultar por ID
    def get_by_id(self, id: int) -> Optional[Usuario]:
        return Usuario.objects.filter(pk=id).first()

    # Consultar por correo
    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        return Usuario.objects.filter(usu_correo=correo).first()
