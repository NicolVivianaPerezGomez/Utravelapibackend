from typing import Optional
from utravel.models import Reseña
from django.db.models import QuerySet

class ResenasRepository:

    model = Reseña
    
    #MÉTODO DE CREAR RESEÑA
    def create (self, **data) -> Reseña: #recibe un diccionario y retorna un objeto Reseña

        return Reseña.objects.create(**data) #método del ORM para crear registro en la bd
    
    #MÉTODO PARA ACTUALIZAR UNA RESEÑA
    def update(self, id:int, **data) -> Optional[Reseña]: #Optional : puede retornas un objeto o un None

        reseña_obj = Reseña.objects.filter(pk=id).first()

        if not reseña_obj: #si no existe
            return None
        
        for field, value in data.items(): #Si existe
            setattr(reseña_obj, field, value) #asignar campos dinamicamente del diccionario

        reseña_obj.save() #guardar cambios
        return reseña_obj #retornas objeto
    
    #MPETODO PARA ELININAR - DESACTIVAR
    def desactivate(self, id:int) -> bool:
        deleted = Reseña.objects.filter(pk=id).update(res_status = "0")
        return deleted > 0 #retorna True o False si algun registro fue actualizado por eso > 0
    
    #LISTAR TODOS LAS RESEÑAS
    def listarResenas(self) -> QuerySet[Reseña]: # QuerySet: conjunto de objetos que viene de la db
        return(
            self.model.objects.filter(res_status="1")
            .select_related('usu_id', 'lug_id') #select_related cargar tablas relacionadas (JOIN)
        )
    
    def listarResenaCalificacion(self, calificacion:int) -> QuerySet[Reseña]:
        return self.model.objects.filter(res_calificacion=calificacion, res_status="1")
    
    def get_by_id(self, id:int) -> Optional[Reseña]:
        return self.model.objects.filter(pk=id).select_related('usu_id', 'lug_id').first()
