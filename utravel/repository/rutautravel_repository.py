from utravel.models import RutaTuristica
from typing import Optional
from django.db.models import QuerySet


class RutaTuristicaRepository:

	# referencia a la clase (no a la instancia)
	model = RutaTuristica

	# crear una ruta
	def create(self, **data) -> RutaTuristica:
		return self.model.objects.create(**data)

	# actualizar por id (devuelve el objeto o None si no existe)
	def update(self, id: int, **data) -> Optional[RutaTuristica]:
		obj = self.model.objects.filter(pk=id).first()
		if not obj:
			return None

		for field, value in data.items():
			setattr(obj, field, value)

		obj.save()
		return obj

	# borrado lógico
	def desactivate(self, id: int) -> bool:
		updated = self.model.objects.filter(pk=id).update(rut_estado="0")
		return updated > 0

	# listar sólo activas
	def listRutas(self) -> QuerySet[RutaTuristica]:
		return self.model.objects.filter(rut_estado="1")

	# buscar por id (sin filtrar estado)
	def get_by_id(self, id: int) -> Optional[RutaTuristica]:
		return self.model.objects.filter(pk=id).first()

	# buscar por nombre entre activas
	def get_by_name(self, name: str) -> Optional[RutaTuristica]:
		return self.model.objects.filter(rut_nombre=name, rut_estado="1").first()

