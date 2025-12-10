from utravel.models import Ciudad
from typing import Optional
from django.db.models import QuerySet

class CiudadRepository:

    #Declarando una referencia a la clase no al objeto
    model = Ciudad

    #crear una ciudad
    def create(self, **data) -> Ciudad: #recibir todos los datos por medio de un diccionario
        return Ciudad.objects.create(**data) #Crear una nueva ciudad, objects.create() viene del ORM Django crea un neuvo registro en la bd
    
    #actualizar una ciudad
    def update(self, id:int, **data) -> Optional[Ciudad]: #Optional es un tipo de dato que puede retornar un objeto o un None
        ciudad_object = Ciudad.objects.filter(pk=id).first() #filtra por id y obtiene el primer resultado

        #si no se encuentra
        if not ciudad_object:
            return None #None: tipo de dato void null o undefind no hay nada
        
        #si se encuentra
        for field, value in data.items():
            setattr(ciudad_object, field, value) #asignar campos dinamicamente del diccionario
        
        #salvar y retornar
        ciudad_object.save() #guarda los cambios del objeto en la bd
        return ciudad_object
    
    #eliminar lógico ciudad
    def desactivate(self, id:int) -> bool:
        deleted = Ciudad.objects.filter(pk=id).update(ciudad_status="0")
        return deleted > 0 #retorna True o False si algun registro fue actualizado por eso > 0 
    
    #listar todas las ciudades
    def listCiudades(self) -> QuerySet[Ciudad]:
        return(
            self.model.objects.filter(ciudad_status="1") #solo listar las que esten activas
        )
    
    #listar para
    def get_by_id(self, id:int) -> Optional[Ciudad]:
        return Ciudad.objects.filter(pk=id).first()
    
    def get_by_name(self, name:str) -> Optional[Ciudad]:
        return Ciudad.objects.filter(ciu_descripcion=name).first()


    
    



