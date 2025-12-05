from typing import Optional
from utravel.models import Lugares
from django.db.models import QuerySet

class LugaresRepository:
    """ Declarar una referencia a la clase NO al objeto"""
    model = Lugares

    """ Creación de metodos """

    """ 1. Crear lugar """
    def create (self, **data) -> Lugares:
        # Paso diccionario que crea y guarda la instancia
        return Lugares.objects.create(**data)
    
    """ 2. Actualizar lugar """
    def update(self, id: int, **data) -> Optional[Lugares]:
        # Busqueda del lugar por id, devuelve el primer resultado
        lugares_obj = Lugares.objects.filter(pk=id).first()

        # Si el id no existe, devuelvo un Null
        if not lugares_obj:
            return None
        
        # Si lo encuentro
        for field,value in data.items():
            setattr(lugares_obj, field, value)

        # Salvo valores y devuelvo el valor actualizado
        lugares_obj.save()
        return lugares_obj
    
    """ 3. Eliminar por estado """
    def deactivate(self, id: int) -> bool:
        deleted = Lugares.objects.filter(pk=id).update(lug_status = "0")
        return deleted > 0
    
    """ 4. Listar todos los lugares """
    def listLugares(self) -> QuerySet[Lugares]:# QuerySet: conjunto de objetos que viene de la db
        return(
            self.model.objects # Modelo de lugares
            .filter(lug_status="1")  # Filtra solomlos lugares activos
            .select_related('catlug_id', 'ciu_id') # Hace un JOIN, para traer la categoria y la ciudad 
        )
    
    """ 5. Retornar lugar por id """
    def get_by_id(self, id: int) -> Optional[Lugares]:
        return self.model.objects.filter(pk=id, lug_status="1").select_related('catlug_id', 'ciu_id').first()
    
    """ 6. Retornar lugar por nombre """
    def get_by_name(self, name: str) -> Optional[Lugares]:
        return self.model.objects.filter(lug_nombre=name, lug_status="1").select_related('catlug_id', 'ciu_id').first()

