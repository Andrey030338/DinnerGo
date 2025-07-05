# Importa las herramientas de formularios de Django
from django import forms

# Importa el modelo Reserva, sobre el cual se va a construir el formulario
from .models import Reserva


# Crea un formulario basado en el modelo Reserva
class ReservaForm(forms.ModelForm):
    # Esta clase interna define la configuración del formulario
    class Meta:
        model = Reserva  # Indica que el formulario se basa en el modelo Reserva
        fields = ['nombre_cliente', 'fecha', 'hora', 'cantidad_personas', 'pedido']
        # Lista de campos del modelo que se incluirán en el formulario

        widgets = {
            # Personaliza el campo 'fecha' con un input tipo "date" (calendario)
            'fecha': forms.DateInput(attrs={'type': 'date'}),

            # Personaliza el campo 'hora' con un input tipo "time" (selector de hora)
            'hora': forms.TimeInput(attrs={'type': 'time'}),

            # Personaliza el campo 'pedido' para que sea un textarea con 3 filas de alto
            'pedido': forms.Textarea(attrs={'rows': 3}),
        }
