from django.contrib import admin
# Register your models here
from .models import (
    TipoUsuario, Ciudad, CategoriaLugar, Usuario, TipoExperiencia,
    PreferenciaUsuario, Lugares, CiudadLugares, LugarCategoria,
    RutaTuristica, OrdenLugares, Reseña
)


#El inline me permite mostrar dentro del panel de administración los objetos relacionados con otro modelo
#Por ejemplo en Lugares, puedo ver y agregar Reseñas ahí mismo.
class ReseñaInline(admin.TabularInline):
    model = Reseña
    extra = 1
    fields = ("res_calificacion", "res_comentario", "res_visible", "res_fecha")
    readonly_fields = ("res_fecha",)


class OrdenLugaresInline(admin.TabularInline):
    model = OrdenLugares
    extra = 1
    fields = ("lug_id", "lugrut_orden")



@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("tipousu_id", "tipousu_turista", "tipousu_empresa")
    list_filter = ("tipousu_turista", "tipousu_empresa")


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    search_fields = ("ciu_descripcion",)
    list_display = ("ciu_id", "ciu_descripcion")


@admin.register(CategoriaLugar)
class CategoriaLugarAdmin(admin.ModelAdmin):
    search_fields = ("catlug_descripcion",)
    list_display = ("catlug_id", "catlug_descripcion")


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("usu_id", "usu_nombre", "usu_apellido", "usu_correo", "ciu_id", "tipousu_id")
    search_fields = ("usu_nombre", "usu_apellido", "usu_correo", "usu_usunombre")
    list_filter = ("ciu_id", "tipousu_id")


@admin.register(TipoExperiencia)
class TipoExperienciaAdmin(admin.ModelAdmin):
    search_fields = ("tipexp_descripcion",)
    list_display = ("tipexp_id", "tipexp_descripcion")


@admin.register(PreferenciaUsuario)
class PreferenciaUsuarioAdmin(admin.ModelAdmin):
    list_display = ("prefusu_id", "prefusu_tipoExperiencia", "usu_id")
    list_filter = ("prefusu_tipoExperiencia",)


@admin.register(Lugares)
class LugaresAdmin(admin.ModelAdmin):
    list_display = ("lug_id", "lug_nombre", "ciu_id", "catlug_id")
    search_fields = ("lug_nombre", "lug_descripcion")
    list_filter = ("ciu_id", "catlug_id")
    inlines = [ReseñaInline]


@admin.register(CiudadLugares)
class CiudadLugaresAdmin(admin.ModelAdmin):
    list_display = ("ciulug_id", "lug_id", "ciu_id")


@admin.register(LugarCategoria)
class LugarCategoriaAdmin(admin.ModelAdmin):
    list_display = ("lugcat_id", "catlug_id", "lug_id")


@admin.register(RutaTuristica)
class RutaTuristicaAdmin(admin.ModelAdmin):
    list_display = ("rut_id", "rut_nombre", "rut_duracion")
    search_fields = ("rut_nombre", "rut_descripcion")
    inlines = [OrdenLugaresInline]


@admin.register(OrdenLugares)
class OrdenLugaresAdmin(admin.ModelAdmin):
    list_display = ("logrut_id", "lug_id", "rut_id", "lugrut_orden")
    list_filter = ("rut_id",)


@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ("res_id", "res_calificacion", "res_visible", "usu_id", "lug_id", "res_fecha")
    list_filter = ("res_visible", "res_calificacion")
    search_fields = ("res_comentario",)
