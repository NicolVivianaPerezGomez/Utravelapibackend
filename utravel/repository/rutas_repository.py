from typing import Optional
from django.db.models import QuerySet
from utravel.models import RutaTuristica

class RutaRepository:

    model = RutaTuristica

    def list_active(self) -> QuerySet[RutaTuristica]:
        return self.model.objects.filter(rut_estado="1")

    def get_by_id(self, id: int) -> Optional[RutaTuristica]:
        return self.model.objects.filter(rut_id=id).first()

    def create(self, **data) -> RutaTuristica:
        return self.model.objects.create(**data)

    def update(self, id: int, **data) -> Optional[RutaTuristica]:
        ruta = self.model.objects.filter(rut_id=id).first()
        if not ruta:
            return None

        for field, value in data.items():
            setattr(ruta, field, value)

        ruta.save()
        return ruta

    def desactivate(self, id: int) -> bool:
        deleted = self.model.objects.filter(rut_id=id).update(rut_estado="0")
        return deleted > 0
