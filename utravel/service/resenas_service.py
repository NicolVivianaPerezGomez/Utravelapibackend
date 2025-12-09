from typing import Optional
from utravel.models import Reseña, Lugares, Usuario
from utravel.repository.resena_repository import ResenasRepository
from django.db.models import QuerySet

class ResenasService:

    #constructor e inyeccion del repositorio - hacer instancia de un objeto
    def __init__(self, repository: Optional[ResenasRepository] = None) -> None:
        self.repository = repository or ResenasRepository() #Si no me pasan un repository instancio uno

    #LISTAR TODAS LAS RESEÑAS

    def list_resenas(self) -> QuerySet[Reseña]:
        return self.repository.listarResenas()
    
    #LISTAR TODOS POR CALIFICACION

    def list_resenas_calificacion(self) -> QuerySet[Reseña]:
        return self.repository.listarResenaCalificacion()
    
    #RETORNAR POR ID
    def get_resenas_id(self, id:int) -> Optional[Reseña]:
        return self.repository.get_by_id(id)
    
    # CREAR RESEÑAS

    def create_resena(self, **data) -> Reseña:

        id = data.get("res_id")

        existing = self.repository.get_by_id(id)

        #validar que ningun campo este vacio
        required_campos = ["res_calificacion", "res_comentario", "res_fecha", "res_visible"]
        for campo in required_campos:
            if not data.get(campo): #si el valor no existe o esta vacio
                raise ValueError(f"el campo '{campo}' es obligatorio") #raise detiene el codigo y muestra el mensaje
            
        #validar que este activo
        if existing and existing.res_status == "1":
            raise ValueError("Ya existe la reseña")
        
        #Reactivar si esta inactivo
        if existing and existing.res_status == "0":
            existing.res_status = 1
            return self.repository.update(existing.res_id, **data)
        
        #Estado por default del status 
        data.setdefault("res_status", 1)

        #Crear la reseña
        return self.repository.create(**data)
    
    def update_resena(self, id:int, **data) -> Optional[Reseña]:

        resena = self.repository.get_by_id(id)
        status = data.get("res_status")
        
        #validar que existe
        if not resena:
            raise ValueError("Reseña no encontrada. No se puede actualizar")
        
        #validar que este activo
        if resena.res_status != "1":
            raise ValueError("El registro de reseña esta inactivo, no se puede actualizar")
        
        #Establecer status
        if status is None:
            data["res_status"] = resena.res_status #si no hay valor nuevo dejar el que ya tenia

        #validar lugar

        if "lug_id" in data: #existe el campo
            if not Lugares.objects.filter(pk=data["lug_id"].pk).exists(): #si existe el lugar en la bd 
                raise ValueError("La ciudad no existe.")
            
        if "usu_id" in data:
            if not Usuario.objects.filter(pk=data["usu_id"].pk).exists(): #si existe el usuario en la bd 
                raise ValueError("El usuario no existe.")
            
        return self.repository.update(id, **data)
    
    #DELETE LÓGICO

    def desativate_resena(self, id:int) -> bool:
        obj = self.repository.get_by_id(id)

        if not obj:
            return False
        
        return self.repository.desactivate(id)
        
        
