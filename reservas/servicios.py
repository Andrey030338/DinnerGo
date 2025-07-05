from .models import Reserva  # Importa el modelo de Reserva
from django.core.exceptions import ValidationError  # Excepción que se lanza si algo no es válido
from datetime import datetime  # manejo de fechas (aun no se usa))

# -------------------------------
# CLASE: ValidadorReserva
# -------------------------------
class ValidadorReserva:
    """
    Clase encargada de validar si una reserva es válida según ciertas reglas.
    """

    def __init__(self, mesa, datos):
        self.mesa = mesa        # Objeto de la mesa a reservar
        self.datos = datos      # Diccionario con los datos del formulario (nombre, fecha, hora, etc.)

    def validar(self):
        # Verifica si el número de personas excede la capacidad de la mesa
        if self.datos['cantidad_personas'] > self.mesa.capacidad:
            raise ValidationError("La cantidad de personas excede la capacidad de la mesa.")

# -------------------------------
# CLASE: GestorReserva
# -------------------------------
class GestorReserva:
    """
    Clase que se encarga de crear reservas, asegurándose primero de validarlas.
    """

    def __init__(self, mesa, datos):
        self.mesa = mesa      # Objeto Mesa
        self.datos = datos    # Datos del formulario de reserva

    def crear(self):
        # Primero valida los datos antes de guardar la reserva
        ValidadorReserva(self.mesa, self.datos).validar()

        # Crea un objeto Reserva con los datos proporcionados
        reserva = Reserva(
            nombre_cliente = self.datos['nombre_cliente'],
            fecha = self.datos['fecha'],
            hora = self.datos['hora'],
            cantidad_personas = self.datos['cantidad_personas'],
            mesa = self.mesa
        )

        # Guarda la reserva en la base de datos
        reserva.save()

        # Devuelve el objeto reserva creado
        return reserva
