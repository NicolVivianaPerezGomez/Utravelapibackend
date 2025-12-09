import requests

url = "http://127.0.0.1:8000/api/utravel/rutas/crear/"

files = {
    'rut_imagen': open('test_ruta_image.png', 'rb')
}

data = {
    'rut_nombre': 'Ruta con Imagen Test 2',
    'rut_descripcion': 'Descripción de prueba con imagen',
    'rut_duracion': '4h'
}

response = requests.post(url, files=files, data=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
