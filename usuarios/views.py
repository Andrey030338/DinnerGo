# Importamos funciones de Django para autenticación y manejo de sesiones
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect  # Para renderizar páginas o redirigir
from .forms import RegistroUsuarioForm  # Nuestro formulario de registro personalizado
from django.contrib import messages  # Para mostrar mensajes (como "registro exitoso")
from django.core.signing import Signer, BadSignature
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import PerfilUsuario
from usuarios.models import PerfilUsuario
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import json
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

# Vista principal del sitio, renderiza la plantilla del home
def home(request):
    return render(request, 'usuarios/home.html')

# Vista para registrar un nuevo usuario
def registrar_usuario(request):
    if request.method == 'POST':
        # Si se envió el formulario (POST), lo llenamos con los datos enviados
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            print("✅ Formulario válido")
            
            # Solo obtenemos los datos limpios del formulario según tu formulario real
            datos_usuario = {
                'nombre': form.cleaned_data.get('nombre', ''),  # Campo "Nombre" de tu formulario
                'email': form.cleaned_data.get('email', ''),   # Campo "Correo Electrónico"
                'telefono': form.cleaned_data.get('telefono', ''),  # Campo "Número Telefónico"  
                'password': form.cleaned_data.get('password1', ''),  # Campo "Contraseña"
                'codigo_gerente': form.cleaned_data.get('codigo_gerente'), # Campo del codigo del gerente
            }
            print("💾 Código gerente guardado:", datos_usuario['codigo_gerente'])

            
            # Usamos el email como username si no hay campo username específico
            datos_usuario['username'] = datos_usuario['email']
            
            # Verificamos que no exista ya un usuario con ese email (que usamos como username)
            if User.objects.filter(username=datos_usuario['email']).exists():
                messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                return render(request, 'usuarios/registro.html', {'form': form})
            
            if User.objects.filter(email=datos_usuario['email']).exists():
                messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                return render(request, 'usuarios/registro.html', {'form': form})
            
            try:
                print("📨 Enviando correo de verificación...")
                # Enviamos el correo con los datos del usuario (sin guardarlo aún)
                enviar_correo_verificacion_registro(datos_usuario)
                print("✅ Correo de verificación enviado")
                
                # Guardamos temporalmente los datos en la sesión (opcional, para reenvío)
                request.session['datos_registro_pendiente'] = datos_usuario
                
                messages.success(request, f'¡Te hemos enviado un correo de verificación a {datos_usuario["email"]}! Debes verificar tu correo antes de que se cree tu cuenta.')
                
            except Exception as e:
                print("❌ Error al enviar el correo:", e)
                messages.error(request, 'Hubo un problema al enviar el correo de verificación. Inténtalo de nuevo.')
            
            return render(request, 'usuarios/verificacion_pendiente.html', {
                'email': datos_usuario['email'],
                'es_registro_nuevo': True
            })
        else:    
            print("❌ Formulario inválido:", form.errors)
    else:
        # Si no es POST, solo mostramos el formulario vacío
        form = RegistroUsuarioForm()
    
    # Renderizamos la plantilla de registro con el formulario
    return render(request, 'usuarios/registro.html', {'form': form})    

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre') # Obtenemos el campo "nombre" que estás usando como username
        password = request.POST['password']

        user = authenticate(request, username=nombre, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name}!')

            # 🔐 Verificamos si el usuario es Gerente
            if user.groups.filter(name='Gerente').exists():
                return redirect('panel_gerente')  # Redirige al panel de gerente
            else:
                return redirect('home')  # Redirige al home normal si no es gerente
        else:
            messages.error(request, 'Nombre o contraseña incorrectos')

    return render(request, 'usuarios/login.html')  

# Vista para cerrar sesión
def logout_view(request):
    logout(request)  # Cerramos la sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('home')  # Redirigimos al inicio


#inicio verificacion de correo
signer = Signer()

def enviar_correo_verificacion_registro(datos_usuario):
    """
    Envía correo de verificación con los datos del usuario sin guardarlo aún
    """
    signer = Signer()
    # Firmamos los datos completos del usuario
    token = signer.sign(json.dumps(datos_usuario))
    host = 'localhost:8000'
    link = f"http://{host}/verificar-correo-registro/{token}/"

    subject = "Verifica tu correo para completar el registro"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = datos_usuario['email']

    text_content = f"Hola {datos_usuario.get('nombre', 'Usuario')}, confirma tu correo para completar tu registro: {link}"
    html_content = render_to_string('usuarios/email_verificacion_registro.html', {
        'nombre': datos_usuario.get('nombre', 'Usuario'),
        'link': link
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Vista para verificar correo desde registro
def verificar_correo_registro(request, token):
    try:
        signer = Signer()
        datos_usuario = json.loads(signer.unsign(token))

        if User.objects.filter(email=datos_usuario['email']).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return redirect('login')

        if User.objects.filter(username=datos_usuario['username']).exists():
            messages.error(request, 'Este nombre de usuario ya está registrado.')
            return redirect('registro')

        user = User.objects.create_user(
            username=datos_usuario['username'],
            email=datos_usuario['email'],
            password=datos_usuario['password'],
            first_name=datos_usuario.get('nombre', datos_usuario['username']),
            is_active=True
        )

        # Crear el perfil
        PerfilUsuario.objects.create(
            usuario=user,
            telefono=datos_usuario['telefono']
        )

        # Asignar rol
        codigo = datos_usuario.get('codigo_gerente', '')
        grupo_nombre = 'Gerente' if codigo == 'DG-Admin2025' else 'Mesero'

        try:
            grupo = Group.objects.get(name=grupo_nombre)
            user.groups.add(grupo)
            print(f"✅ Usuario asignado al grupo: {grupo_nombre}")
        except Group.DoesNotExist:
            print(f"⚠️ El grupo '{grupo_nombre}' no existe.")

        messages.success(request, '¡Tu cuenta ha sido verificada exitosamente! Ahora puedes iniciar sesión.')
        return redirect('login')

    except BadSignature:
        messages.error(request, 'El enlace de verificación no es válido o ha expirado.')
        return redirect('registro')
    except KeyError as e:
        messages.error(request, f'Datos de verificación incompletos: {str(e)}')
        return redirect('registro')
    except Exception as e:
        messages.error(request, f'Error al verificar la cuenta: {str(e)}')
        return redirect('registro')




# Vista de verificación de correo antigua (para usuarios ya existentes)
def verificar_correo(request, token):
    """
    Para usuarios que ya existen pero necesitan verificar correo
    """
    try:
        user_id = signer.unsign(token)
        user = User.objects.get(pk=user_id)
        perfil = PerfilUsuario.objects.get(usuario=user)
        perfil.verificado = True
        perfil.save()
        
        login(request, user)
        messages.success(request, '¡Correo verificado exitosamente!')
        
        return render(request, "usuarios/verificacion_exitosa.html", {
            "usuario": user,
            "mensaje": "Tu correo ha sido verificado correctamente."
        })
    except (BadSignature, User.DoesNotExist, PerfilUsuario.DoesNotExist):
        return render(request, "usuarios/verificacion_invalida.html")

def perfil_usuario(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para acceder a tu perfil.')
        return redirect('login')
    
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        if not perfil.verificado:
            return render(request, 'usuarios/verificacion_pendiente.html')
    except PerfilUsuario.DoesNotExist:
        return render(request, 'usuarios/verificacion_pendiente.html')

    return render(request, 'usuarios/perfil.html')

def reenviar_verificacion_registro(request):
    """
    Reenvía el correo de verificación usando los datos guardados en la sesión
    """
    if request.method == 'POST':
        if 'datos_registro_pendiente' in request.session:
            datos_usuario = request.session['datos_registro_pendiente']
            try:
                enviar_correo_verificacion_registro(datos_usuario)
                messages.success(request, 'Correo de verificación reenviado exitosamente.')
            except Exception as e:
                messages.error(request, 'Error al reenviar el correo. Inténtalo de nuevo.')
        else:
            messages.error(request, 'No hay datos de registro pendientes. Intenta registrarte nuevamente.')
    
    return render(request, 'usuarios/reenviar_verificacion.html')


#ROLES
def es_gerente(user):
    return user.groups.filter(name='Gerente').exists()

@login_required
@user_passes_test(es_gerente)
def crear_empleado(request): #CREAR EMPLEADO
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=nombre).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
        else:
            nuevo_usuario = User.objects.create_user(username=nombre, email=correo, password=password)
            grupo = Group.objects.get(name=rol)
            nuevo_usuario.groups.add(grupo)
            messages.success(request, f'Empleado {nombre} creado con rol {rol}.')
            return redirect('crear_empleado')

    grupos = Group.objects.all()
    return render(request, 'usuarios/crear_empleado.html', {'grupos': grupos})


@login_required
@user_passes_test(es_gerente)
def ver_empleados(request):
    empleados = User.objects.exclude(groups__name='Gerente')
    return render(request, 'usuarios/ver_empleados.html', {'empleados': empleados})




#Panel del Gerente
@login_required
@user_passes_test(es_gerente)
def panel_gerente(request):
    return render(request, 'usuarios/panel_gerente.html')

