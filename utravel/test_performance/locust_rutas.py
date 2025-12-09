from locust import HttpUser, task, between
import random
import threading

#PRUEBAS DE API DE LOCUST DE RUTAS


TOKEN_GLOBAL = None #variable vacio donde se almacena el token
TOKEN_LOCK = threading.Lock() #evita que el token se genere simultaneamente (solo permite 1) solo 1 hilo

# --- Usuarios Locust que prueban Lugares ---
class LugaresUser(HttpUser):
    wait_time = between(1, 3)
    lugar_creado_id = None

    def on_start(self):
        global TOKEN_GLOBAL
        self.headers = {}
        if TOKEN_GLOBAL is None:
            with TOKEN_LOCK:
                if TOKEN_GLOBAL is None:
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json().get("access")
                        print("TOKEN GENERADO OK (LUGARES)")
        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"} if TOKEN_GLOBAL else {}

    @task(3)
    def listar_lugares(self):
        self.client.get("/lugares/", headers=self.headers)

    @task(1)
    def crear_lugar(self):
        payload = {
            "lug_nombre": f"Lugar {random.randint(1000, 9999)}",
            "lug_descripcion": "Lugar de prueba Locust",
            "lug_ciudad": 1  # Asume que existe ciudad con ID 1
        }
        response = self.client.post("/lugares/", json=payload, headers=self.headers)
        if response.status_code in (200, 201):
            try:
                self.lugar_creado_id = response.json().get("lug_id")
            except:
                pass

    @task(1)
    def obtener_lugar(self):
        if self.lugar_creado_id:
            self.client.get(f"/lugares/{self.lugar_creado_id}/", headers=self.headers)

    @task(1)
    def actualizar_lugar(self):
        if self.lugar_creado_id:
            payload = {
                "lug_nombre": f"Lugar Actualizado {random.randint(1000, 9999)}",
                "lug_descripcion": "Actualizado por Locust"
            }
            self.client.put(f"/lugares/{self.lugar_creado_id}/", json=payload, headers=self.headers)


# --- Usuarios Locust que prueban Usuarios ---
class UsuariosUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        global TOKEN_GLOBAL
        self.headers = {}
        if TOKEN_GLOBAL is None:
            with TOKEN_LOCK:
                if TOKEN_GLOBAL is None:
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json().get("access")
                        print("TOKEN GENERADO OK (USUARIOS)")
        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"} if TOKEN_GLOBAL else {}

    @task(3)
    def listar_usuarios(self):
        self.client.get("/usuarios/", headers=self.headers)

    @task(1)
    def crear_usuario(self):
        payload = {
            "usu_nombre": f"Usuario{random.randint(10000, 99999)}",
            "usu_email": f"user{random.randint(1000, 9999)}@test.com",
            "usu_telefono": "3001234567"
        }
        self.client.post("/usuarios/", json=payload, headers=self.headers)

    @task(1)
    def obtener_usuario(self):
        self.client.get("/usuarios/1/", headers=self.headers)


# --- Usuarios Locust que prueban Tipo de Experiencia ---
class TipoExperienciaUser(HttpUser):
    wait_time = between(1, 3)
    tipoexp_creado_id = None

    def on_start(self):
        global TOKEN_GLOBAL
        self.headers = {}
        if TOKEN_GLOBAL is None:
            with TOKEN_LOCK:
                if TOKEN_GLOBAL is None:
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json().get("access")
                        print("TOKEN GENERADO OK (TIPO EXPERIENCIA)")
        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"} if TOKEN_GLOBAL else {}

    @task(3)
    def listar_tipoexp(self):
        self.client.get("/tipo_exp/", headers=self.headers)

    @task(1)
    def crear_tipoexp(self):
        payload = {
            "tipexp_descripcion": f"Tipo Experiencia {random.randint(1000, 9999)}"
        }
        response = self.client.post("/tipo_exp/", json=payload, headers=self.headers)
        if response.status_code in (200, 201):
            try:
                self.tipoexp_creado_id = response.json().get("tipexp_id")
            except:
                pass

    @task(1)
    def obtener_tipoexp(self):
        if self.tipoexp_creado_id:
            self.client.get(f"/tipo_exp/{self.tipoexp_creado_id}/", headers=self.headers)

    @task(1)
    def buscar_por_nombre_tipoexp(self):
        self.client.get("/tipo_exp/Aventura/", headers=self.headers)


# --- Usuarios Locust que prueban Rutas Turísticas ---
class RutasUser(HttpUser):
    wait_time = between(1, 3)
    ruta_creada_id = None

    def on_start(self):
        global TOKEN_GLOBAL
        self.headers = {}
        if TOKEN_GLOBAL is None:
            with TOKEN_LOCK:
                if TOKEN_GLOBAL is None:
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json().get("access")
                        print("TOKEN GENERADO OK (RUTAS)")
        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"} if TOKEN_GLOBAL else {}

    @task(3)
    def listar_rutas(self):
        self.client.get("/api/utravel/rutas/", headers=self.headers)

    @task(1)
    def crear_ruta(self):
        payload = {
            "rut_nombre": f"Ruta Locust {random.randint(10000, 99999)}",
            "rut_descripcion": "Ruta creada en prueba de carga",
            "rut_duracion": "2h"
        }
        response = self.client.post("/api/utravel/rutas/crear/", json=payload, headers=self.headers)
        if response.status_code in (200, 201):
            try:
                self.ruta_creada_id = response.json().get("rut_id")
            except:
                pass

    @task(1)
    def obtener_ruta_aleatorio(self):
        # Intenta obtener una ruta aleatoria (1-10)
        ruta_id = random.randint(1, 10)
        self.client.get(f"/api/utravel/rutas/{ruta_id}/", headers=self.headers)

    @task(1)
    def actualizar_ruta(self):
        if self.ruta_creada_id:
            payload = {
                "rut_nombre": f"Ruta Actualizada {random.randint(10000, 99999)}",
                "rut_descripcion": "Cambio de prueba",
                "rut_duracion": "3h"
            }
            self.client.put(f"/api/utravel/rutas/{self.ruta_creada_id}/actualizar/", 
                          json=payload, headers=self.headers)

