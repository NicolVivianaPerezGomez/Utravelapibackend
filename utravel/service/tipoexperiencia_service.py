from django.db.models import QuerySet
from typing import Optional
from utravel.models import TipoExperiencia
from utravel.repository.tipoexperiencia_repository import TipoExperienciaRepository

class TipoExperienciaService:

   #Creando el constructor y haciendo inyección del repositorio
    def __init__(self, repository: Optional[TipoExperienciaRepository] = None) -> None:

        self.repository = repository or TipoExperienciaRepository #Si no me pasan en repository instancio uno

    #CONSULTAS DE LECTURA ------------------------

    #listar todas los tipos de exp.
    def list_tpexp(self) -> QuerySet[TipoExperiencia]:
        return self.repository.listTpExperiencias()
    
    #listar por ID
    def get_tpexp_id(self, id:int) -> Optional[TipoExperiencia]:
        return self.repository.get_by_id(id)
    
    #listar por nombre
    def get_tpexp_name(self, name:str) -> Optional[TipoExperiencia]:
        return self.repository.get_by_name(name)
    
    #MÉTODOS CRUD --------------------------------

    #Create
    def create_tpexp(self, **data) -> TipoExperiencia:

        name = data.get("tipexp_descripcion")

        #Validar nombre/descripción existente
        if name and self.repository.get_by_name(name):
            raise ValueError("Ya existe un Tipo de experiencia con ese nombre")
        
        #Estado por default
        data.setdefault("tipexp_status", 1)

        #Creación del tipo de exp.
        return self.repository.create(**data)
    
    #Update
    def update_tpexp(self, id:int, **data) -> Optional[TipoExperiencia]:

        name = data.get("tipexp_descripcion")
        status = data.get("tipexp_status")

        #validar que el status sea 1
        if status != "1":
            raise ValueError("El registro esta inactivo, no se puede Actualizar")
        
        #Validar nombre/descripción existente
        if name and self.repository.get_by_name(name):
            raise ValueError("Ya existe un Tipo de experiencia con ese nombre")
        
        return self.repository.update(id, **data)
    
    #Delete lógico
    def desactivate_tpexp(self, id: int) -> bool:
        obj = self.repository.get_by_id(id)

        if not obj: #no existe el registro/objeto
            return False
        
        return self.repository.desactivate(id)
    


    