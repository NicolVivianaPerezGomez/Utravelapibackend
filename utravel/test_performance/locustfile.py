from locust import HttpUser, task, between
import random


#PRUEBAS DE DESEMEPEÑO (TIEMPO DE RESPUESTA) CON LOCUST
"""Evalue el rendimiento de una app simulando a miles de usuarios usandola al mismo tiempo para 
ver el tiempo de respuesta de esta

pesos:
3 = se ejecuta más veces cada x tiempo
1 = se ejecuta menos veces cada x tiempo
"""

TOKEN_GLOBAL = None

class CiudadSimulada(HttpUser):

    wait_time = between(1,3) #tiempo de espera entre peticiones del usuario (crear, editar, listar)

    ciudad_creada_id = None #variable para almecenar el ID generado

    #método para generar JWT
    def on_start(self):

      global TOKEN_GLOBAL

      if TOKEN_GLOBAL is None:
          response = self.client.post("/api/token/", json={
              "username": "root",
              "password": "1234"
          })

          if response.status_code == 200:
              TOKEN_GLOBAL = response.json().get("access")
              print("TOKEN GENERADO OK")
          else:
              print("ERROR TOKEN: ", response.status_code, response.text)
              return
    
      self.headers = {"Authorization": f"Bearer {TOKEN_GLOBAL}"}
 
    @task(3)
    def listar(self):
        self.client.get("/ciudades/", headers=self.headers)

    @task(1) #decorador que indica que esta accion la eejcuta un usuario con un peso de 1 
    def crear_ciudad(self):

        ciu_descripcion= f"Ciudad de prueba {random.randint(100,999)}" #guarando un ejemplo de registro con un nombre con int random

        response = self.client.post("/ciudades/", json={ #método simulado POST con el dato
            "ciu_descripcion": ciu_descripcion},
            headers=self.headers
            )

        if response.status_code in (200, 201): #CODIGO DE OK o Created
            try:
                self.ciudad_creada_id = response.json().get("id") #response json: convertir JSON a diccionario y .get("id") extrae el ID
            except:
                pass #si no se puede igual pasa y continua 

    @task(1)
    def buscar_por_id(self):
        if self.ciudad_creada_id:
            self.client.get(f"/ciudades/{self.ciudad_creada_id}/", headers=self.headers)

    @task(1)
    def actualizar_ciudad(self):
        if self.ciudad_creada_id:
            self.client.put(f"/ciudades/{self.ciudad_creada_id}/", json={
                "ciu_descripcion": "Ciudad Actualizada"},
                headers=self.headers)

    @task(1)
    def buscar_por_nombre(self):
        self.client.get("/ciudades/Bogot%C3%A1/", headers=self.headers)


"""
Como ejecutar:

correr servido: py manage.py runserver
buscar en la terminar la carpeta test_performance
ejecutar locust -f locustfile.py --host=http://127.0.0.1:8000
abrir en la web http://localhost:8089
ejecutar prueba

"""