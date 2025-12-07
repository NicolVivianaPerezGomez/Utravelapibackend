import pytest
from utravel.service.ciudad_service import CiudadService

#PRUEBAS UNITARIAS CIUDAD
#pruebas para crear ciudad

@pytest.mark.django_db #mark para usar la db
def test_ciudad_creation():
    service = CiudadService()
    data = {"ciu_descripcion":"Villavicencio"}
    ciudad = service.create_ciudad(**data)

    #condiciones de aporbación de la prueba
    assert ciudad.ciudad_status == 1 #condicion si tiene 1 default 
    assert ciudad.ciu_descripcion == "Villavicencio" #condicion si se cumple pasa el test
                                                     #si funciona bien debe de tener registrado "villavicencio" 