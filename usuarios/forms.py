from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario

class RegistroUsuarioForm(UserCreationForm):
    
    # Redefinimos username con una etiqueta más amigable
    username = forms.CharField(
        required=True,
        label="Nombre",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    # Campo de email
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
        })
    )
    
    # Campo de teléfono personalizado
    telefono = forms.CharField(
        required=True, 
        label="Número Telefónico",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
        # Campo opcional para código de gerente
    codigo_gerente = forms.CharField(
        required=False,
        label="Código de Gerente (opcional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Si tienes un código especial'
        })
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telefono' , 'codigo_gerente']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos estilos a los campos de contraseña
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
        
    def clean_email(self):
        """Validamos que el email no esté repetido"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
        
    def clean_username(self):
        """Validamos que el nombre de usuario no esté repetido"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username
        
    def clean_telefono(self):
        """Validamos el formato del teléfono"""
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            telefono_limpio = ''.join(filter(str.isdigit, telefono))
            if len(telefono_limpio) < 10:
                raise forms.ValidationError("El número de teléfono debe tener al menos 10 dígitos.")
        return telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['username']  # Guardamos el nombre también en first_name

        if commit:
            user.save()
            # Creamos el perfil del usuario con el teléfono
            try:
                PerfilUsuario.objects.create(
                    usuario=user, 
                    telefono=self.cleaned_data['telefono']
                )
            except Exception as e:
                # Si hay error creando el perfil, eliminamos el usuario
                user.delete()
                raise forms.ValidationError(f"Error al crear el perfil: {str(e)}")

        return user