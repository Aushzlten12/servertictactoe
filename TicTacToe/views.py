from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import numpy as np
import tensorflow as tf  # Importa tensorflow directamente
import json

# MAÑANA LO DESPLEGAMOS EN HEROKU O PYTHONANYWHERE
@api_view(["POST"])
def predecir_movimiento(request):
    if request.method == "POST":
        # Obtener datos del cuerpo de la solicitud
        estado_tablero = request.data.get("tablero", [])

        # Convertir el estado del tablero a un arreglo de entrada para la predicción
        entrada_prediccion = [
            0 if c == "X" else 1 if c == "O" else 2 for c in estado_tablero
        ]

        # Construir la ruta completa a los archivos del modelo
        ruta_modelo_json = os.path.join(
            settings.BASE_DIR, "archivos_modelo", "model.json"
        )
        ruta_modelo_h5 = os.path.join(settings.BASE_DIR, "archivos_modelo", "model.h5")

        # Cargar el modelo previamente guardado
        with open(ruta_modelo_json, 'r') as json_file:
            model_json = json_file.read()
            modelo = tf.keras.models.model_from_json(model_json)
        modelo.load_weights(ruta_modelo_h5)

        # Generar posibles movimientos
        posibles_movimientos = generar_posibles_movimientos(estado_tablero)

        # Inicializar variables para el mejor movimiento y su probabilidad asociada
        mejor_movimiento = None
        mejor_probabilidad = 2

        # Calcular la probabilidad para cada posible movimiento
        for movimiento in posibles_movimientos:
            entrada_movimiento = [
                0 if c == "X" else 1 if c == "O" else 2 for c in movimiento
            ]
            prediccion = modelo.predict(np.array([entrada_movimiento]))
            probabilidad = prediccion[0][0]

            # Actualizar si encontramos un mejor movimiento
            if probabilidad < mejor_probabilidad:
                mejor_movimiento = entrada_movimiento
                mejor_probabilidad = probabilidad

        posicion_predicha = encontrar_cambio(entrada_prediccion, mejor_movimiento)

        # Crear o actualizar un objeto modelo (ajusta esto según tu modelo y lógica)
        # resultado = Resultado(tablero=estado_tablero, movimiento_maquina=posicion_predicha)
        # resultado.save()

        return Response({"posicion": posicion_predicha}, status=status.HTTP_200_OK)

    return Response(
        {"mensaje": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )



def encontrar_cambio(entrada_actual, movimiento):
    # Verifica que las listas tengan la misma longitud
    if len(entrada_actual) != len(movimiento):
        raise ValueError("Las listas deben tener la misma longitud")

    # Itera sobre los elementos de las listas y encuentra el cambio
    for i in range(len(entrada_actual)):
        if entrada_actual[i] != movimiento[i]:
            return i

    # Si no se encuentra ningún cambio
    return None


def generar_posibles_movimientos(estado_tablero):
    posibles_movimientos = []

    for i, c in enumerate(estado_tablero):
        if c == "-":
            movimiento = estado_tablero.copy()
            movimiento[i] = "X"  # Asumiendo que 'X' es el símbolo de la máquina
            posibles_movimientos.append(movimiento)

    return posibles_movimientos


@api_view(["POST"])
def recibir_datos(request):
    if request.method == "POST":
        # Lógica para recibir datos aquí
        # Puedes acceder a los datos del cuerpo de la solicitud con request.data
        datos_recibidos = request.data

        # Puedes hacer lo que necesites con los datos recibidos
        # Por ejemplo, almacenarlos en la base de datos, realizar alguna operación, etc.

        return Response({"status": "success"}, status=status.HTTP_200_OK)

    return Response(
        {"mensaje": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )