from django.urls import path
from .views import recibir_datos, predecir_movimiento

urlpatterns = [
    path('recibir_datos/', recibir_datos, name='recibir_datos'),
    path('predecir_movimiento/', predecir_movimiento, name='predecir_movimiento'),
]