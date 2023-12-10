from django.db import models

# Create your models here.
class Resultado(models.Model):
    tablero = models.JSONField()  # Almacena el estado del tablero en formato JSON
    movimiento_maquina = models.IntegerField()  # Almacena el movimiento de la máquina
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Registra la fecha y hora de la creación del registro

    def __str__(self):
        return f'Resultado #{self.id}'