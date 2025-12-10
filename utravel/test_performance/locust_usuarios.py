from locust import HttpUser, task, between
import random
import string
import threading

# PRUEBAS DE DESEMPEÑO PARA USUARIOS

TOKEN_GLOBAL = None
TOKEN_LOCK = threading.Lock()  # Evita que varios hilos generen token al mismo tiempo

# Generar datos aleatorios
def texto_aleatorio(longitud=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))

# Clase principal de la prueba
class UsuariosSimulados(HttpUser):
    wait_time = between(1, 3)
    usuario_creado_id = None

    def on_start(self):
        global TOKEN_GLOBAL
        self.headers = {}

        if TOKEN_GLOBAL is None:
            with TOKEN_LOCK:
                if TOKEN_GLOBAL is None:
                    # Solicitar token JWT
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json()["access"]
                        print("TOKEN GENERADO OK (USUARIOS)")
                    else:
                        print("ERROR TOKEN USUARIOS:", response.status_code, response.text)
                        return

        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"}

    # Listar usuarios
    @task(3)
    def listar_usuarios(self):
        response = self.client.get("/usuarios/", headers=self.headers)
        print("GET /usuarios/ status:", response.status_code)

    # Crear usuario
    @task(1)
    def crear_usuario(self):
        nombre = texto_aleatorio(4)
        data = {
            "usu_nombre": f"Test{nombre}",
            "usu_apellido": f"User{nombre}",
            "usu_correo": f"{nombre}@example.com",
            "usu_contraseña": "123456",
            "usu_usunombre": f"user{nombre}",
            "usu_status": "1",
            "ciu_id": 1,      # Debe existir en DB
            "tipousu_id": 1   # Debe existir en DB
        }

        response = self.client.post("/usuarios/", headers=self.headers, json=data)
        print("POST /usuarios/ status:", response.status_code, response.text)

        if response.status_code in (200, 201):
            try:
                self.usuario_creado_id = response.json().get("usu_id")
            except:
                pass

    # Buscar usuario por id
    @task(1)
    def buscar_por_id(self):
        if self.usuario_creado_id:
            response = self.client.get(f"/usuarios/{self.usuario_creado_id}/", headers=self.headers)
            print(f"GET /usuarios/{self.usuario_creado_id}/ status:", response.status_code)

    # Actualizar usuario
    @task(1)
    def actualizar_usuario(self):
        if not self.usuario_creado_id:
            return

        nombre = texto_aleatorio(4)
        data = {
            "usu_nombre": f"Actualizado{nombre}",
            "usu_apellido": f"User{nombre}",
            "usu_correo": f"{nombre}@example.com",
            "usu_usunombre": f"user{nombre}",
            "usu_status": "1",
            "ciu_id": 1,
            "tipousu_id": 1
        }

        response = self.client.put(f"/usuarios/{self.usuario_creado_id}/", headers=self.headers, json=data)
        print(f"PUT /usuarios/{self.usuario_creado_id}/ status:", response.status_code)

    # Desactivar usuario
    @task(1)
    def eliminar_usuario(self):
        if self.usuario_creado_id:
            response = self.client.delete(f"/usuarios/{self.usuario_creado_id}/", headers=self.headers)
            print(f"DELETE /usuarios/{self.usuario_creado_id}/ status:", response.status_code)


""" 1. Estar en la carpeta de teest perfomance 
    2. Ejecuto: locust -f locust_usuarios.py --host=http://127.0.0.1:8000

"""