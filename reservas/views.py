# Importa funciones útiles de Django para manejar vistas
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.urls import reverse

# Importa los modelos necesarios
from .models import Plato, Mesa, PlatoReserva, Reserva

# Importa el formulario de reservas
from .forms import ReservaForm

# Importa la clase encargada de crear la reserva (con validaciones)
from .servicios import GestorReserva


def hacer_reserva(request, mesa_id):
    # Busca la mesa por ID o muestra un error 404 si no existe
    mesa = get_object_or_404(Mesa, id=mesa_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST)  # Crea un formulario con los datos enviados por el cliente

        if form.is_valid():
            try:
                # Construye el texto del pedido con los platos seleccionados
                pedido_texto = ""
                for plato in Plato.objects.all():
                    cantidad = int(request.POST.get(f'plato_{plato.id}', 0))
                    if cantidad > 0:
                        pedido_texto += f"{plato.nombre} x {cantidad}\n"

                # Asigna ese texto al campo oculto 'pedido' del formulario
                form.cleaned_data['pedido'] = pedido_texto.strip()

                # Crea la reserva usando el gestor de reservas
                gestor = GestorReserva(mesa, form.cleaned_data)
                reserva = gestor.crear()

                # Registra los platos elegidos con sus cantidades en la tabla intermedia PlatoReserva
                for plato in Plato.objects.all():
                    cantidad = int(request.POST.get(f'plato_{plato.id}', 0))
                    if cantidad > 0:
                        PlatoReserva.objects.create(
                            reserva=reserva,
                            plato=plato,
                            cantidad=cantidad
                        )

                # Redirige a la página de "reserva exitosa"
                return redirect(reverse('reserva_exitosa', args=[reserva.id]))

            except ValidationError as e:
                # Si ocurre una validación (ej. demasiadas personas), muestra el error en el formulario
                form.add_error(None, e)

    else:
        form = ReservaForm()  # Si la petición no es POST, muestra un formulario vacío

    # Lista de todos los platos para mostrar en el formulario
    platos = Plato.objects.all()

    # Renderiza el formulario de reserva con la mesa y los platos disponibles
    return render(request, 'reservas/hacer_reserva.html', {
        'form': form,
        'mesa': mesa,
        'platos': platos
    })


def reserva_exitosa(request, reserva_id):
    # Obtiene la reserva por su ID o muestra error si no existe
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Obtiene todos los platos reservados para esta reserva
    platos_reservados = PlatoReserva.objects.filter(reserva=reserva)

    # Renderiza la plantilla de confirmación con los datos de la reserva
    return render(request, 'reservas/reserva_exitosa.html', {
        'nombre_cliente': reserva.nombre_cliente,
        'fecha': reserva.fecha,
        'hora': reserva.hora,
        'platos': platos_reservados,
        'reserva': reserva  
    })




def lista_mesas(request):
    # Obtiene todas las mesas del restaurante
    mesas = Mesa.objects.all()

    # Muestra la lista de mesas disponibles para reservar
    return render(request, 'reservas/lista_mesas.html', {'mesas': mesas})
