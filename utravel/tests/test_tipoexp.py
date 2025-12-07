import pytest
from utravel.service.tipoexperiencia_service import TipoExperienciaService

#PRUEBAS UNITARIAS TIPO EXPERIENCIA - PYTEST

#pruebas para crear tipo de experiencia
@pytest.mark.django_db #mark para usar la db
def test_tpexperiencia_creation():
    service = TipoExperienciaService()
    data = {"tipexp_descripcion":"Adrenalina"}
    experiencia = service.create_tpexp(**data)

    #condiciones de aporbación de la prueba
    assert experiencia.tipexp_status == 1 
    assert experiencia.tipexp_descripcion == "Adrenalina" 
    
