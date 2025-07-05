from django.db import models  # Importa las herramientas para crear modelos en Django

# ---------------------------
# MODELO: Plato
# ---------------------------
class Plato(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del plato
    descripcion = models.TextField(blank=True)  # Descripción (opcional)
    precio = models.DecimalField(max_digits=10, decimal_places=0)  # Precio del plato (sin decimales)
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True)  # Imagen opcional, se guarda en 'media/platos/'

    def __str__(self):
        return self.nombre  # Muestra el nombre del plato cuando se imprime el objeto

# ---------------------------
# MODELO: Restaurante
# ---------------------------
class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del restaurante
    direccion = models.CharField(max_length=200)  # Dirección del restaurante

    def __str__(self):
        return self.nombre  # Muestra el nombre cuando se imprime el restaurante

# ---------------------------
# MODELO: Mesa
# ---------------------------
class Mesa(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)  # Mesa vinculada a un restaurante
    numero = models.IntegerField()  # Número identificador de la mesa
    capacidad = models.IntegerField()  # Cantidad de personas que caben en la mesa

    def __str__(self):
        return f"Mesa {self.numero} (capacidad : {self.capacidad})"

# ---------------------------
# MODELO: Reserva
# ---------------------------
class Reserva(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)  # La mesa que se reserva
    nombre_cliente = models.CharField(max_length=100)  # Nombre del cliente
    fecha = models.DateField()  # Fecha de la reserva
    hora = models.TimeField()  # Hora de la reserva
    pedido = models.TextField(blank=True, null=True)  # Texto con resumen del pedido (opcional)
    cantidad_personas = models.IntegerField()  # Número de personas para la reserva
    platos = models.ManyToManyField(Plato, through='PlatoReserva')  # Relación con platos mediante tabla intermedia

    def __str__(self):
        return f"Reservas de {self.nombre_cliente} - Mesa {self.mesa.numero}"

# ---------------------------
# MODELO: PlatoReserva (tabla intermedia entre Plato y Reserva)
# ---------------------------
class PlatoReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)  # A qué reserva pertenece
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)  # Qué plato se reservó
    cantidad = models.PositiveIntegerField()  # Cuántas unidades del plato pidió

    def __str__(self):
        return f"{self.plato.nombre} x {self.cantidad} para {self.reserva.nombre_cliente}"
