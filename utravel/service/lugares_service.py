from typing import Optional
from utravel.models import CategoriaLugar, Ciudad, Lugares
from utravel.repository.lugares_repository import LugaresRepository
from django.db.models import QuerySet

class LugaresServices:
    """ 1.Constructor e inyección de repository """
    def __init__(self, repository: Optional[LugaresRepository] = None) -> None:
        # Si no me pasan repository instancio una 
        self.repository = repository or LugaresRepository()

    """ 2.Consultas tipo read (retorno de datos) """
    # Retornar todos los lugares
    def list_lugares(self) -> QuerySet[Lugares]:
        return self.repository.listLugares().filter(lug_status="1").select_related('catlug_id', 'ciu_id')

    
    # Retornar por id
    def get_lugares_id(self, id:int) -> Optional[Lugares]:
        return self.repository.get_by_id(id)
    
    # Retornar por nombre
    def get_lugares_name(self, name:str) -> Optional[Lugares]:
        return self.repository.get_by_name(name)
    
    """ 3. Create """
    def create_lugares(self, **data) -> Lugares:

        # Validar que ningun campo este vacio
        required_campos= ["lug_nombre", "lug_descripcion", "lug_ubicacion", "catlug_id", "ciu_id"]
        for campo in required_campos:
            if not data.get(campo): # Si el valor existe o esta vacio
                raise ValueError(f"El campo '{campo}' es obligatorio.") # Raise: detine el codigo y muestra el error
            
        # Validar estado
        data.setdefault("lug_status", "1")

        # Obtiene los objetos desde los datos validados del serializer (no el ID)
        categoria = data["catlug_id"]
        ciudad = data["ciu_id"]

        # Validar que el lugar no este duplicado en una misma ciudad
        if Lugares.objects.filter(lug_nombre__iexact=data["lug_nombre"],ciu_id=data["ciu_id"]).exists():
            raise ValueError("Ya existe un lugar con ese nombre en esta ciudad.")
        
        # Crea el lugar
        return self.repository.create(**data)
    
    """ 4. Update """
    def update_lugares(self, id:int, **data) -> Optional[Lugares]:

        # Obtener el lugar
        lugares = self.repository.get_by_id(id)
        if not lugares:
            raise ValueError("Lugar no encontrado. No se puede actualizar")
        
        # Leer los valores que vienen del data 
        nombre = data.get("lug_nombre")
        status = data.get("lug_status")
        
        # Validar el estado sea 1
        if status != "1":
            raise ValueError("El registro está inactivo. No se puede actualizar")

        # Obtener el lugar antes de validar los duplicados
        lugar = self.repository.get_by_id(id)
        if not lugar:
            return None # No esxiste, no se puede actualizar
        
        # Validar duplicado (si mandan nombre)
        if nombre:
            lugar_existente = Lugares.objects.filter(lug_nombre__iexact=nombre, ciu_id=lugar.ciu_id).exclude(pk=id).first()

        if lugar_existente:
            raise ValueError("Ya existe un lugar registrado con ese nombre en esta ciudad.")

        # Validar categoria
        if "catlug_id" in data:
            if not CategoriaLugar.objects.filter(pk=data["catlug_id"].pk).exists():
                raise ValueError("La categoría no existe.")

        # Validar ciudad
        if "ciu_id" in data:
            if not Ciudad.objects.filter(pk=data["ciu_id"].pk).exists():
                raise ValueError("La ciudad no existe.")

        # Si pasa todo, se actualiza
        return self.repository.update(id, **data)
    
    
    """ 5. Desactivar """
    def deactivate_lugares(self, id:int) -> bool:
        return self.repository.deactivate(id)