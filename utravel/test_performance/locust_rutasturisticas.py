import random
from locust import HttpUser, task, between
from threading import Lock

# Token global y lock
TOKEN_GLOBAL = None
TOKEN_LOCK = Lock()

class RutasUser(HttpUser):
    wait_time = between(1, 3)
    ruta_creada_id = None

    def on_start(self):
        global TOKEN_GLOBAL
        if TOKEN_GLOBAL is None:
            with TOKEN_LOCK:
                if TOKEN_GLOBAL is None:
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        try:
                            TOKEN_GLOBAL = response.json().get("access")
                            print("TOKEN GENERADO OK (RUTAS)")
                        except Exception as e:
                            print(f"Error al obtener token: {e}")
                    else:
                        print(f"Error al generar token: {response.status_code}")
        # Asignamos headers si el token existe
        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"} if TOKEN_GLOBAL else {}

    @task(3)
    def listar_rutas(self):
        with self.client.get("/api/utravel/rutas/", headers=self.headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Falló listar rutas: {response.status_code}")

    @task(1)
    def crear_ruta(self):
        payload = {
            "rut_nombre": f"Ruta Locust {random.randint(10000, 99999)}",
            "rut_descripcion": "Ruta creada en prueba de carga",
            "rut_duracion": "2h"
        }
        with self.client.post("/api/utravel/rutas/crear/", json=payload, headers=self.headers, catch_response=True) as response:
            if response.status_code in (200, 201):
                try:
                    self.ruta_creada_id = response.json().get("rut_id")
                except Exception:
                    self.ruta_creada_id = None
            else:
                response.failure(f"No se pudo crear ruta: {response.status_code}")

    @task(1)
    def obtener_ruta_aleatorio(self):
        ruta_id = random.randint(1, 10)
        with self.client.get(f"/api/utravel/rutas/{ruta_id}/", headers=self.headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"No se pudo obtener ruta {ruta_id}: {response.status_code}")

    @task(1)
    def actualizar_ruta(self):
        if self.ruta_creada_id:
            payload = {
                "rut_nombre": f"Ruta Actualizada {random.randint(10000, 99999)}",
                "rut_descripcion": "Cambio de prueba",
                "rut_duracion": "3h"
            }
            with self.client.put(f"/api/utravel/rutas/{self.ruta_creada_id}/actualizar/",
                                 json=payload, headers=self.headers, catch_response=True) as response:
                if response.status_code not in (200, 204):
                    response.failure(f"No se pudo actualizar ruta {self.ruta_creada_id}: {response.status_code}")
