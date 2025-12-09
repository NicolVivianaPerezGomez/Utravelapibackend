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

        self.headers = {} #diccionario vacio

        if TOKEN_GLOBAL is None: #si hay un token global salir porque solo debe haber 1
            with TOKEN_LOCK:  # candado que asegura que solo un hilo genere el token
                if TOKEN_GLOBAL is None: #validacion extra de si ya hay un token
                    response = self.client.post("/api/token/", json={
                        "username": "root",
                        "password": "1234"
                    })
                    if response.status_code == 200:
                        TOKEN_GLOBAL = response.json().get("access") #acces tiene el token POSTMAN ej
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

    #------------------------------------------------------------------------------

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

"""
CÓMO EJECUTAR LAS PRUEBAS DE CARGA CON LOCUST:

1. Abrir dos terminales en PowerShell

Terminal 1 - Ejecutar servidor Django:
    & ".envs\\Scripts\\python.exe" manage.py runserver

Terminal 2 - Ejecutar Locust:
    & ".envs\\Scripts\\python.exe" locust -f locustfile.py --host=http://127.0.0.1:8000

"""
