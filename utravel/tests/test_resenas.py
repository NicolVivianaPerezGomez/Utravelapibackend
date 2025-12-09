import pytest
from utravel.service.resenas_service import ResenasService
from utravel.models import Reseña, Usuario, Lugares, Ciudad, LugarCategoria, TipoUsuario


@pytest.mark.django_db
def test_resena_creation():

    service = ResenasService()

    #crear una ciudad
    ciudad = Ciudad.objects.create(
        ciu_nombre="Bogotá",
        ciu_descripcion="Capital de Colombia",
        ciu_status="1"
    )

    #crear un Tipo de usuario
    tipo_usu = TipoUsuario.objects.create(
        tipousu_turista=True,
        tipo_empresa=False
    )

    # Crear categoría
    categoria = LugarCategoria.objects.create(
        catlug_nombre="Parque",
        catlug_descripcion="Lugar natural",
        catlug_status="1"
    )

    #crear un usuario
    usuario = Usuario.objects.create(
        usu_nombre="Pedro",
        usu_apellido="Ramirez",
        usu_correo="pedro@gmail.com",
        usu_contraseña="12345",
        usu_usunombre="Pedroo",
        ciu_id=ciudad,
        tipousu_id=tipo_usu
    )

    # Crear lugar
    lugar = Lugares.objects.create(
        lug_nombre="Parque Simón Bolívar",
        lug_descripcion="Parque gigante",
        lug_ubicacion="Bogotá",
        lug_latitud=4.6583,
        lug_longitud=-74.093,
        lug_status="1",
        catlug_id=categoria,
        ciu_id=ciudad
    )

    #datos de la reseña
    data = Reseña.objects.create(
        res_calificacion = 5,
        res_comentario = "me encata este lugar",
        res_fecha = "10/20/25",
        res_visible = True,
        usu_id = usuario,
        lug_id = lugar 
    )

    resena = service.create_resena(**data)

    assert resena.res_status == "1"


