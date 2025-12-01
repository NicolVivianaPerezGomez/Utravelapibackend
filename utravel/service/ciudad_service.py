from typing import Optional
from utravel.repository.ciudad_repository import CiudadRepository
from utravel.models import Ciudad
from django.db.models import QuerySet

class CiudadService:

    #Contructor con inyeción del repository de ciudad con none = no retorna nada
    def __init__(self, repository: Optional[CiudadRepository] = None) -> None:

        self.repository = repository or CiudadRepository #Si no me pasan un repository instancio uno

    
    #Consultas de lectura ---------------------------------

    #listar todas las ciudades
    def list_ciudades(self) -> QuerySet[Ciudad]:
        return self.repository.listCiudades() #método del repository
    
    #listar por ID
    def get_ciudad_id(self, id:int)-> Optional[Ciudad]:
        return self.repository.get_by_id(id)
    
    #listar por nombre
    def get_ciudad_name(self, name:str)-> Optional[Ciudad]:
        return self.repository.get_by_name(name)
    
    #métodos CRUD ---------------------------------------

    #CREATE
    def create_ciudad(self, **data) -> Ciudad:

        #validar que el nombre/descripción no exista
        name = data.get("ciu_descripcion") #trayendo dato del diccionario con clave: ciu_descripcion

        #validar nombre/descripcion único
        if name and self.repository.get_by_name(name): #si la info de la ciudad y en la bd ya existe un registro igual
            raise ValueError("Ya existe una ciudad registrada con ese nombre") #Exepción
        
        #Estado por default
        data.setdefault("ciudad_status", 1)

        #Creación de la ciudad
        return self.repository.create(**data)
    
    #UPDATE
    def update_ciudad(self, id:int, **data) -> Optional[Ciudad]:

        name = data.get("ciu_descripcion") #trayendo dato del diccionario con clave: ciu_descripcion
        status = data.get("ciudad_status")

        #validar que el status sea 1
        if status != "1":
            raise ValueError("El registro está inactivo. No se puede actualizar")

        #validar nombre/descripcion existente
        if name and self.repository.get_by_name(name): #si la info de la ciudad y en la bd ya existe un registro igual
            raise ValueError("Ya existe una ciudad registrada con ese nombre")
        
        return self.repository.update(id, **data)
    
    #DELETE LÓGICO
    def desactivate_ciudad(self, id: int) -> bool:
        obj = self.repository.get_by_id(id)

        if not obj: #no existe el registro/objeto
            return False
        
        return self.repository.desactivate(id)
        
    

        


