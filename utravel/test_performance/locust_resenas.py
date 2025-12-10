from locust import HttpUser, task, between
import random
import string
import threading
from datetime import datetime, timedelta

TOKEN_GLOBAL = None
TOKEN_LOCK = threading.Lock() 


# GENERAR DATOS ALEATORIOS
def texto_aleatorio(longitud=20):
    letras = string.ascii_letters + " "
    return ''.join(random.choice(letras) for _ in range(longitud))

def fecha_aleatoria():
    dias = random.randint(0, 365)
    fecha = datetime.now() - timedelta(days=dias)
    return fecha.strftime("%Y-%m-%d")


class ResenasSimuladas(HttpUser):

    wait_time = between(1, 3)
    resena_creada_id = None

   #OBTENER TOKEN
    def on_start(self):
        """Autenticación global solo una vez"""
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
                        print("TOKEN GENERADO OK (RESEÑAS)")
                    else:
                        print("ERROR TOKEN RESEÑAS:", response.status_code, response.text)
                        return
        
        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"}

    # LISTAR RESEÑAS
    @task(3)
    def listar_resenas(self):
        self.client.get("/resenas/", headers=self.headers)

    # CREAR RESEÑA
    @task(2)
    def crear_resena(self):

        payload = {
            "res_calificacion": random.randint(1, 5),
            "res_comentario": texto_aleatorio(50),
            "res_fecha": fecha_aleatoria(),
            "res_visible": random.choice([True, False]),
            "usu_id": 1,     
            "lug_id": 1      
        }

        response = self.client.post(
            "/resenas/",
            headers=self.headers,
            json=payload
        )

        if response.status_code in (200, 201):
            try:
                self.resena_creada_id = response.json().get("res_id")
            except:
                pass

    # BUSCAR POR ID
    @task(1)
    def buscar_por_id(self):
        if self.resena_creada_id:
            self.client.get(
                f"/resenas/{self.resena_creada_id}/",
                headers=self.headers
            )

    # ACTUALIZAR RESEÑA
    @task(1)
    def actualizar_resena(self):
        if not self.resena_creada_id:
            return
        
        payload = {
            "res_comentario": f"UPDATE -> {texto_aleatorio(30)}",
            "res_calificacion": random.randint(1, 5),
            "res_fecha": fecha_aleatoria(),
            "res_visible": True,
            "usu_id": 1,
            "lug_id": 1
        }

        self.client.put(
            f"/resenas/{self.resena_creada_id}/",
            headers=self.headers,
            json=payload
        )

    # DESACTIVAR RESEÑA (DELETE LÓGICO)
    @task(1)
    def eliminar_resena(self):
        if self.resena_creada_id:
            self.client.delete(
                f"/resenas/{self.resena_creada_id}/",
                headers=self.headers
            )
