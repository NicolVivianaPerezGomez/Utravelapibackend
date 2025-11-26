from utravel.models import TipoExperiencia
from typing import Optional
from django.db.models import QuerySet

class TipoExperienciaRepository:

    #Referencia a la clase no al objeto
    model = TipoExperiencia

    #Crear un tipo de exp.
    def create(self, **data) -> TipoExperiencia:
        return TipoExperiencia.objects.create(**data)
    
    #Actualizar un tipo de exp.
    def update(self, id:int, **data) -> Optional[TipoExperiencia]:
        tpexp_object = TipoExperiencia.objects.filter(pk=id).first()

        #si no se encuentra en el filtro
        if not tpexp_object:
            return None #tipo de dato que dice nada, como undefined o null
        
        #si se encuentra en el filtro
        for field, value in data.items():
            setattr(tpexp_object, field, value)
        
        #Salvar y retornar
        tpexp_object.save()
        return tpexp_object
    
    #Eliminado lógico de tipo exp.
    def desactivate(self, id:int) -> bool:
        deleted = TipoExperiencia.objects.filter(pk=id).update(tipexp_status="0")
        return deleted > 0 # retorna true si un registro fue actualizado por eso > 0
    
    #Listar todos los t.experiencia
    def listTpExperiencias(self) -> QuerySet[TipoExperiencia]:
        return(
            self.model.objects.filter(tipexp_status="1")
        )
    
    #Buscar por  id
    def get_by_id(self, id:int) -> Optional[TipoExperiencia]:
        return TipoExperiencia.objects.filter(pk=id).first()
    
    #Buscar por nombre
    def get_by_name(self, name:str) -> Optional[TipoExperiencia]:
        return TipoExperiencia.objects.filter(tipexp_descripcion=name).first()
    