from django.db import models

class TipoUsuario(models.Model):
    tipousu_id = models.AutoField(primary_key=True)
    tipousu_turista = models.BooleanField(default=False)  # 2
    tipousu_empresa = models.BooleanField(default=False)   # 1

    def __str__(self):
        if self.tipousu_empresa:
            return "Empresa"  # 1
        elif self.tipousu_turista:
            return "Turista"  # 2
        return "Sin Tipo"


class Ciudad(models.Model):
    ciu_id = models.AutoField(primary_key=True)
    ciu_descripcion = models.CharField(max_length=200, unique=True)
    ciudad_status = models.CharField(max_length=1, default="1")

    def __str__(self):
        return self.ciu_descripcion
    


class CategoriaLugar(models.Model):
    catlug_id = models.AutoField(primary_key=True)
    catlug_descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.catlug_descripcion


class Usuario(models.Model):
    usu_id = models.AutoField(primary_key=True)
    usu_nombre = models.CharField(max_length=100)
    usu_apellido = models.CharField(max_length=100)
    usu_correo = models.EmailField(unique=True)
    usu_contraseña = models.CharField(max_length=100)
    usu_usunombre = models.CharField(max_length=100, unique=True)
    usu_status = models.CharField(
    max_length=10, choices=[("1", "Activo"), ("0", "Inactivo")], default="1")
    ciu_id = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    tipousu_id = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usu_nombre} {self.usu_apellido}"


class TipoExperiencia(models.Model):
    tipexp_id = models.AutoField(primary_key=True)
    tipexp_descripcion = models.CharField(max_length=200)
    tipexp_status = models.CharField(max_length=1, default="1")

    def __str__(self):
        return self.tipexp_descripcion


class PreferenciaUsuario(models.Model):
    prefusu_id = models.AutoField(primary_key=True)
    prefusu_tipoExperiencia = models.CharField(max_length=100)
    usu_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Preferencias {self.prefusu_id} de Usuario {self.usu_id}"


class Lugares(models.Model):
    lug_id = models.AutoField(primary_key=True)
    lug_nombre = models.CharField(max_length=100)
    lug_descripcion = models.CharField(max_length=300)
    lug_ubicacion = models.CharField(max_length=200)
    lug_latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lug_longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lug_status = models.CharField(max_length=1, default="1")
    lug_imagen = models.ImageField(upload_to='lugares/', null=True, blank=True) 
    catlug_id = models.ForeignKey(CategoriaLugar, on_delete=models.CASCADE)
    ciu_id = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.lug_nombre

class CiudadLugares(models.Model):
    ciulug_id = models.AutoField(primary_key=True)
    lug_id = models.ForeignKey(Lugares, on_delete=models.CASCADE)
    ciu_id = models.ForeignKey(Ciudad, on_delete=models.CASCADE)


class LugarCategoria(models.Model):
    lugcat_id = models.AutoField(primary_key=True)
    catlug_id = models.ForeignKey(CategoriaLugar, on_delete=models.CASCADE)
    lug_id = models.ForeignKey(Lugares, on_delete=models.CASCADE)


class RutaTuristica(models.Model):
    rut_id = models.AutoField(primary_key=True)
    rut_nombre = models.CharField(max_length=150)
    rut_descripcion = models.TextField()
    rut_duracion = models.CharField(max_length=100)
    rut_estado = models.CharField(max_length=1, default="1")
    rut_imagen = models.ImageField(upload_to='rutas/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.rut_nombre


class OrdenLugares(models.Model):
    logrut_id = models.AutoField(primary_key=True)
    lugrut_orden = models.IntegerField()
    rut_id = models.ForeignKey(RutaTuristica, on_delete=models.CASCADE)
    lug_id = models.ForeignKey(Lugares, on_delete=models.CASCADE)


class Reseña(models.Model):
    res_id = models.AutoField(primary_key=True)
    res_calificacion = models.IntegerField()
    res_comentario = models.TextField()
    res_fecha = models.DateField()
    res_visible = models.BooleanField(default=True)
    usu_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    lug_id = models.ForeignKey(Lugares, on_delete=models.CASCADE)
    res_status = models.CharField(max_length=1, default="1")

    def __str__(self):
        return f"Reseña de {self.usu_id} en {self.lug_id}"


  
