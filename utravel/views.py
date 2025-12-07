from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import RutaTuristica
from .api.serializers.serializers_rutas import RutaTuristicaSerializer


@api_view(['GET'])
def listar_rutas(request):
    rutas = RutaTuristica.objects.filter(rut_estado="1")
    serializer = RutaTuristicaSerializer(rutas, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def crear_ruta(request):

    if request.method == 'GET':
        return Response({
            "detalle": "Este endpoint se usa para crear rutas. "
                       "Envía un POST con rut_nombre, rut_descripcion y rut_duracion."
        }, status=status.HTTP_200_OK)

    serializer = RutaTuristicaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(rut_estado="1")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_ruta(request, id):
    try:
        ruta = RutaTuristica.objects.get(rut_id=id, rut_estado="1")
    except RutaTuristica.DoesNotExist:
        return Response(
            {"error": "Ruta no encontrada o inactiva."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = RutaTuristicaSerializer(ruta)
    return Response(serializer.data)

@api_view(['PUT'])
def actualizar_ruta(request, id):
    try:
        ruta = RutaTuristica.objects.get(rut_id=id, rut_estado="1")
    except RutaTuristica.DoesNotExist:
        return Response({"error": "Ruta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RutaTuristicaSerializer(ruta, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_ruta(request, id):
    try:
        ruta = RutaTuristica.objects.get(rut_id=id, rut_estado="1")
    except RutaTuristica.DoesNotExist:
        return Response({"error": "Ruta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    ruta.rut_estado = "0"
    ruta.save()

    return Response({"mensaje": "Ruta desactivada correctamente."})

