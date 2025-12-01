from typing import Optional
from utravel.repository.utravel_repository import RutaTuristicaRepository
from utravel.models import RutaTuristica
from django.db.models import QuerySet


class RutaService:

    def __init__(self, repository: Optional[RutaTuristicaRepository] = None) -> None:
        self.repository = repository or RutaTuristicaRepository()

    # Lectura ----------------------------------------------------------------
    def list_rutas(self) -> QuerySet[RutaTuristica]:
        return self.repository.listRutas()

    def get_ruta_id(self, id: int) -> Optional[RutaTuristica]:
        return self.repository.get_by_id(id)

    def get_ruta_name(self, name: str) -> Optional[RutaTuristica]:
        return self.repository.get_by_name(name)

    # CRUD -------------------------------------------------------------------
    def create_ruta(self, **data) -> RutaTuristica:
        name = data.get('rut_nombre')
        if name and self.get_ruta_name(name):
            raise ValueError('Ya existe una ruta con este nombre.')

        data.setdefault('rut_estado', '1')
        return self.repository.create(**data)

    def update_ruta(self, id: int, **data) -> Optional[RutaTuristica]:
        obj = self.repository.get_by_id(id)
        if not obj:
            return None

        # no permitir actualizar si está inactiva
        status = data.get('rut_estado')
        if status is not None and status != '1':
            raise ValueError('El registro está inactivo. No se puede actualizar')

        # si se intenta cambiar el nombre, valida duplicado entre activas (excluyendo la misma ruta)
        name = data.get('rut_nombre')
        if name:
            existing = self.repository.get_by_name(name)
            if existing and existing.pk != obj.pk:
                raise ValueError('Ya existe una ruta con este nombre.')

        return self.repository.update(id, **data)

    def desactivate_ruta(self, id: int) -> bool:
        obj = self.repository.get_by_id(id)
        if not obj:
            return False
        return self.repository.desactivate(id)
