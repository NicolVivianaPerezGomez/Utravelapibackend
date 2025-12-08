import pytest
from utravel.service.lugares_service import LugaresServices
from utravel.models import Ciudad, CategoriaLugar, Lugares


@pytest.mark.django_db
def test_lugar_creation():
    service = LugaresServices()

    # Crear una ciudad
    ciudad = Ciudad.objects.create(
        ciu_descripcion="Bogotá",
        ciudad_status="1"
    )

    # Crear categoría de lugar
    categoria = CategoriaLugar.objects.create(
        catlug_descripcion="Parque"
    )

    # Datos del lugar
    data = {
        "lug_nombre": "Parque Simón Bolívar",
        "lug_descripcion": "Parque principal de Bogotá",
        "lug_ubicacion": "Bogotá centro",
        "catlug_id": categoria,
        "ciu_id": ciudad
    }

    lugar = service.create_lugares(**data)

    assert lugar.lug_status == "1"
    assert lugar.lug_nombre == "Parque Simón Bolívar"


@pytest.mark.django_db
def test_lugar_deactivate():
    service = LugaresServices()

    ciudad = Ciudad.objects.create(
        ciu_descripcion="Medellín",
        ciudad_status="1"
    )

    categoria = CategoriaLugar.objects.create(
        catlug_descripcion="Museo"
    )

    lugar = service.create_lugares(
        lug_nombre="Museo de Antioquia",
        lug_descripcion="Museo principal",
        lug_ubicacion="Centro Medellín",
        catlug_id=categoria,
        ciu_id=ciudad
    )

    lugar_id = lugar.lug_id

    # Verificar que exista
    assert service.get_lugares_id(lugar_id) is not None

    # Desactivar
    result = service.deactivate_lugares(lugar_id)
    assert result is True

    # Verificar estado actualizado
    lugar_actualizado = service.get_lugares_id(lugar_id)
    assert lugar_actualizado.lug_status == "0"
