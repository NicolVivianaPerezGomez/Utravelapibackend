from typing import Optional
from utravel.repository.rutas_repository import RutaRepository
from utravel.models import RutaTuristica

class RutaService:

    def __init__(self, repository: Optional[RutaRepository] = None):
        self.repository = repository or RutaRepository()

    def list_rutas(self):
        return self.repository.list_active()

    def get_ruta(self, id: int):
        return self.repository.get_by_id(id)

    def create_ruta(self, **data):
        data.setdefault("rut_estado", "1")
        return self.repository.create(**data)

    def update_ruta(self, id: int, **data):
        return self.repository.update(id, **data)

    def delete_ruta(self, id: int):
        return self.repository.desactivate(id)
