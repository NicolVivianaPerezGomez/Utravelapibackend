from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status

from .models import RutaTuristica
from .api.serializers.serializers_rutas import RutaTuristicaSerializer


@api_view(['GET'])
def listar_rutas(request):
    rutas = RutaTuristica.objects.filter(rut_estado="1")
    serializer = RutaTuristicaSerializer(rutas, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def crear_ruta(request):

    if request.method == 'GET':
        return Response({
            "detalle": "Este endpoint se usa para crear rutas. "
                       "Envía un POST multipart/form-data con rut_nombre, rut_descripcion, rut_duracion y opcional rut_imagen."
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

@api_view(['PUT', 'PATCH'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def actualizar_ruta(request, id):
    try:
        ruta = RutaTuristica.objects.get(rut_id=id, rut_estado="1")
    except RutaTuristica.DoesNotExist:
        return Response({"error": "Ruta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
    # allow partial updates with PATCH
    partial = True if request.method == 'PATCH' else False

    serializer = RutaTuristicaSerializer(ruta, data=request.data, partial=partial)
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

