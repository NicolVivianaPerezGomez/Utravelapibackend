from typing import Optional
from utravel.repository.ciudad_repository import CiudadRepository
from utravel.models import Ciudad
from django.db.models import QuerySet
import re #para expresiones regulares

class CiudadService:

    #Contructor con inyeción del repository de ciudad con none = no retorna nada
    def __init__(self, repository: Optional[CiudadRepository] = None) -> None:

        self.repository = repository or CiudadRepository() #Si no me pasan un repository instancio uno

    #Consultas de lectura ---------------------------------

    #listar todas las ciudades
    def list_ciudades(self) -> QuerySet[Ciudad]: #QuerySet devuelve una lista de ciudades
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

        name = data.get("ciu_descripcion") #trayendo dato del diccionario con clave: ciu_descripcion
        existing = self.repository.get_by_name(name)

        #validar que este activo
        if existing and existing.ciudad_status == 1:
            raise ValueError("Ya existe una ciudad con ese nombre")
        
        #Reactivar si esta inactivo
        if existing and existing.ciudad_status == 0:
            existing.ciudad_status = 1
            return self.repository.update(existing.id, **data)
        
        #validación de expreisiones regulares
        if name:
            if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", name):
                raise ValueError("El nombre de la ciudad solo puede contener letras y espacios")
            
        #Estado por default del status
        data.setdefault("ciudad_status", 1)
        
        #Creación de la ciudad
        return self.repository.create(**data)
    
    #UPDATE
    def update_ciudad(self, id:int, **data) -> Optional[Ciudad]:

        ciudad = self.repository.get_by_id(id) #traer la ciudad
        name = data.get("ciu_descripcion") #trayendo dato del diccionario con clave: ciu_descripcion
        status = data.get("ciudad_status")

        #validar que exista ciudad
        if not ciudad: #si existe
            raise ValueError("Ciudad no encontrada, no es posible actualizar")

        #validar que el status sea 1
        if ciudad.ciudad_status != "1":
            raise ValueError("El registro está inactivo. No se puede actualizar")
        
        #validar nombre/descripcion (único)
        if name and name != ciudad.ciu_descripcion: #si la info de la ciudad y en la bd ya existe un registro igual
            existing = self.repository.get_by_name(name)
            if existing:
                raise ValueError("Ya existe una ciudad registrada con ese nombre")

        #validación de expreisiones regulares
        if name:
            if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", name):
                raise ValueError("El nombre de la ciudad solo puede contener letras y espacios")
            
        #Establecer status
        if status is None:
            data["ciudad_status"] = ciudad.ciudad_status #si no hay calor nuevo dejar el que ya tenia

        
        return self.repository.update(id, **data)
    
    #DELETE LÓGICO
    def desactivate_ciudad(self, id: int) -> bool:
        obj = self.repository.get_by_id(id)

        if not obj: #no existe el registro/objeto
            return False
        
        return self.repository.desactivate(id)
        
    

        


