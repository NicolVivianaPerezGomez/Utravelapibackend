import pytest
from utravel.service.ciudad_service import CiudadService

#PRUEBAS UNITARIAS CIUDAD - PYTEST
#pruebas para crear ciudad

@pytest.mark.django_db #mark para usar la db
def test_ciudad_creation():
    service = CiudadService()
    data = {"ciu_descripcion":"Villavicencio"}
    ciudad = service.create_ciudad(**data)

    #condiciones de aporbación de la prueba
    assert ciudad.ciudad_status == 1 #condicion si tiene 1 default 
    assert ciudad.ciu_descripcion == "Villavicencio" #condicion si se cumple pasa el test
 
@pytest.mark.django_db                                                    #si funciona bien debe de tener registrado "villavicencio" 
def test_ciudad_detelete():

    service = CiudadService()

    # Crear ciudad de prueba
    ciudad = service.create_ciudad(
        ciu_descripcion="Villavicencio",
    )

    ciudad_id = ciudad.ciu_id
    
    #verificar que exista
    ciudad = service.get_ciudad_id(ciudad_id)
    assert ciudad is not None

    #desacticar y verificar que si suceda
    result = service.desactivate_ciudad(ciudad_id)
    assert result is True

    #Verificar si el estado ahora es 0
    ciudad_actualizada = service.get_ciudad_id(ciudad_id)
    assert ciudad_actualizada.ciudad_status == "0"