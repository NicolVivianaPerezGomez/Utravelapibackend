from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import RutaTuristica
from .serializers  import RutaTuristicaSerializer
from .service.utravel_service import RutaService


service = RutaService()


@api_view(['GET'])
def listar_rutas(request):
    rutas = service.list_rutas()
    serializer = RutaTuristicaSerializer(rutas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_ruta(request):
    serializer = RutaTuristicaSerializer(data=request.data)
    if serializer.is_valid():
        # Use service to centralize creation logic
        try:
            obj = service.create_ruta(**serializer.validated_data)
        except ValueError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

        out = RutaTuristicaSerializer(obj)
        return Response(out.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_ruta(request, id):
    ruta = service.get_ruta_id(id)
    if not ruta or ruta.rut_estado != "1":
        return Response({"error": "Ruta no encontrada o inactiva."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RutaTuristicaSerializer(ruta)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def actualizar_ruta(request, id):
    ruta = service.get_ruta_id(id)
    if not ruta or ruta.rut_estado != "1":
        return Response({"error": "Ruta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    partial = request.method == 'PATCH'
    serializer = RutaTuristicaSerializer(ruta, data=request.data, partial=partial)
    if serializer.is_valid():
        try:
            obj = service.update_ruta(id, **serializer.validated_data)
        except ValueError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

        out = RutaTuristicaSerializer(obj)
        return Response(out.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_ruta(request, id):
    ruta = service.get_ruta_id(id)
    if not ruta or ruta.rut_estado != "1":
        return Response({"error": "Ruta no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    deactivated = service.desactivate_ruta(id)
    if not deactivated:
        return Response({"error": "No fue posible desactivar la ruta."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"mensaje": "Ruta desactivada correctamente."})
