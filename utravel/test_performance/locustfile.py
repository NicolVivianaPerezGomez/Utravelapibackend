from locust import HttpUser, task, between
import random
import string
import threading


#PRUEBAS DE DESEMEPEÑO (TIEMPO DE RESPUESTA) CON LOCUST CIUDADES
"""Evalue el rendimiento de una app simulando a miles de usuarios usandola al mismo tiempo para 
ver el tiempo de respuesta de esta

pesos:
3 = se ejecuta más veces cada x tiempo
1 = se ejecuta menos veces cada x tiempo
"""

TOKEN_GLOBAL = None #variable vacio donde se almacena el token
TOKEN_LOCK = threading.Lock() #evita que el token se genere simultaneamente (solo permite 1) solo 1 hilo


class CiudadSimulada(HttpUser): #HttpUser usuario virtual con peticion http

    wait_time = between(1,3) #tiempo de espera entre peticiones del usuario (crear, editar, listar)

    ciudad_creada_id = None #variable para almecenar el ID generado

    #MÉTODO PARA OBTENER EL TOKEN
    def on_start(self):
        global TOKEN_GLOBAL

        self.headers = {}

        if TOKEN_GLOBAL is None: #si hay un token global salir porque solo debe haber 1
            with TOKEN_LOCK:  # candado que asegura que solo un hilo genere el token
                if TOKEN_GLOBAL is None: #validacion extra de si ya hay un token
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json().get("access")
                        print("TOKEN GENERADO OK")
                    else:
                        print("ERROR TOKEN:", response.status_code, response.text)
                        return

        self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"}

 
    #MÉTODO PARA PROBAR LISTAR CIUDADES
    @task(3) #decorador que indica que esta accion la eejcuta un usuario con un peso de 1 
    def listar(self):
        self.client.get("/ciudades/", headers=self.headers) #client hace referencia al cliente
        #headers es propio del get header: cabeceras personalizadas como ej tokens

    #metodo para generar nombre aleatorio
    def nombre_valido(self, longitud=8): #8 caracteres por defecto 
        letras = string.ascii_letters + " " #ascii_letters cadena de texto con minusculas y mayusuclas
                                            #" " espacios entre ellas
                                            #String: modulo para trabajar con cad. de texto

        return ''.join(random.choice(letras) for _ in range(longitud)) #bucle donde no importa el indice _ que retorna una cadena de texto '' con el método random.choice() que genera conjuntos de caracteres random

    #MÉTODO PARA PROBAR CREAR CIUDADES
    @task(1) 
    def crear_ciudad(self):

        ciu_descripcion = f"Ciudad {self.nombre_valido(5)}"#guarando un ejemplo de registro con un nombre con método de random string

        response = self.client.post("/ciudades/", json={ #método simulado POST con el dato
            "ciu_descripcion": ciu_descripcion
            }, headers=self.headers)
        
        if response.status_code in (200, 201): #CODIGO DE OK o Created
            try:
                self.ciudad_creada_id = response.json().get("ciu_id") #response json: convertir JSON a diccionario y .get("id") extrae el ID
            except:
                pass #si no se puede igual pasa y continua 

    #MÉTODO PARA PROBAR BUSCAR POR ID
    @task(1)
    def buscar_por_id(self):
        if self.ciudad_creada_id:
            self.client.get(f"/ciudades/{self.ciudad_creada_id}/", headers=self.headers)

    #MÉTODO PARA PROBAR ACTUALIZAR 
    @task(1)
    def actualizar_ciudad(self):

        new_description = f"Ciudad {self.nombre_valido(5)}" #nuevo nombre random

        if self.ciudad_creada_id:
            self.client.put(f"/ciudades/{self.ciudad_creada_id}/", json={
                "ciu_descripcion": new_description},
                headers=self.headers)
 
    #MÉTODO PARA PROBAR BUSCAR POR NOMBRE
    @task(1)
    def buscar_por_nombre(self):
        self.client.get("/ciudades/Bogot%C3%A1/", headers=self.headers)


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


"""
CÓMO EJECUTAR LAS PRUEBAS DE CARGA CON LOCUST:

1. Abre dos terminales en PowerShell

Terminal 1 - Ejecutar servidor Django:
    & ".envs\\Scripts\\python.exe" manage.py runserver

Terminal 2 - Ejecutar Locust:
    & ".envs\\Scripts\\python.exe" -m locust -f utravel/test_performance/locustfile.py --host=http://127.0.0.1:8000

2. Abre en tu navegador:
    http://localhost:8089/

3. En la interfaz de Locust configura:
    - Number of users: 50-100
    - Spawn rate: 5-10
    - Luego presiona "Start swarming"

4. Observa las métricas en tiempo real:
    - Response times (tiempo de respuesta promedio)
    - RPS (Requests Per Second)
    - Failures (errores)
    - Charts (gráficos de rendimiento)

COMPARACIÓN CON TESTS UNITARIOS:
- Tests Unitarios (pytest/Django TestCase): Verifican CORRECCIÓN (¿funciona?)
- Locust: Verifica RENDIMIENTO bajo CONCURRENCIA (¿aguanta muchos usuarios?)
- Juntos: Tests = Calidad, Locust = Escalabilidad
"""
