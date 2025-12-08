from locust import HttpUser, task, between
import random
import string
import threading


#PRUEBAS DE DESEMEPEÑO (TIEMPO DE RESPUESTA) CON LOCUST
"""Evalue el rendimiento de una app simulando a miles de usuarios usandola al mismo tiempo para 
ver el tiempo de respuesta de esta"""


TOKEN_GLOBAL = None #variable vacio donde se almacena el token
TOKEN_LOCK = threading.Lock() #evita que el token se genere simultaneamente (solo permite 1) solo 1 hilo


# Genera datos
def texto_aleatorio(longitud=10):
    letras = string.ascii_letters + " "
    return ''.join(random.choice(letras) for _ in range(longitud))


def coordenada_lat():
    return round(random.uniform(-90, 90), 6)

def coordenada_lon():
    return round(random.uniform(-180, 180), 6)


# Clase principal de la prueba
class LugaresSimulados(HttpUser):

    wait_time = between(1, 3)   # delay entre peticiones
    lugar_creado_id = None      # almacena el ID recién creado

    # Se guarda el token global
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
                        TOKEN_GLOBAL = response.json()["access"]
                        print("TOKEN GENERADO OK (LUGARES)")
                    else:
                        print("ERROR TOKEN LUGARES:", response.status_code, response.text)
                        return

        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"}

    # Lista los lugares
    @task(3)
    def listar_lugares(self):
        self.client.get("/lugares/", headers=self.headers)

    # Crea el lugar
    @task(1)
    def crear_lugar(self):

        payload = {
            "lug_nombre": f"Lugar {texto_aleatorio(6)}",
            "lug_descripcion": f"Descripción {texto_aleatorio(15)}",
            "lug_ubicacion": f"Calle {random.randint(1, 50)} # {random.randint(1, 50)}",
            "lug_latitud": coordenada_lat(),
            "lug_longitud": coordenada_lon(),
            "lug_status": "1",
            "catlug_id": 1,   
            "ciu_id": 1       
        }

        response = self.client.post(
            "/lugares/",
            headers=self.headers,
            data=payload   # Lugares usa FormParser
        )

        if response.status_code in (200, 201):
            try:
                self.lugar_creado_id = response.json().get("lug_id")
            except:
                pass

    # Busca por id
    @task(1)
    def buscar_por_id(self):
        if self.lugar_creado_id:
            self.client.get(f"/lugares/{self.lugar_creado_id}/", headers=self.headers)

    # Actualiza el lugar
    @task(1)
    def actualizar_lugar(self):

        if not self.lugar_creado_id:
            return

        payload = {
            "lug_nombre": f"Lugar {texto_aleatorio(5)}",
            "lug_descripcion": f"Actualizado {texto_aleatorio(12)}",
        }

        self.client.put(
            f"/lugares/{self.lugar_creado_id}/",
            headers=self.headers,
            data=payload
        )

    # Desactiva el lugar
    @task(1)
    def eliminar_lugar(self):
        if self.lugar_creado_id:
            self.client.delete(
                f"/lugares/{self.lugar_creado_id}/",
                headers=self.headers
            )

""" 1. Estar en la carpeta de teest perfomance 
    2. Ejecuto: locust -f locust_lugares.py --host=http://127.0.0.1:8000
"""
