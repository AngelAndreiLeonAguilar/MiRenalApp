from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegistroForm, UserUpdateForm, PerfilUpdateForm
from .models import Perfil  # 🔹 Importamos el modelo Perfil
from .decorators import medico_required  # 🔹 Importamos el decorador que creamos
from django.contrib.auth.decorators import login_required  # 🔹 Para proteger vistas de usuarios logueados

# Página principal
def home(request):
    return render(request, "home.html")

# Registro de usuarios
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()  # guarda el nuevo usuario
            # 🔹 Crear perfil automáticamente como paciente
            Perfil.objects.create(user=usuario, tipo="paciente")
            return redirect("login")  # redirige al login después de registrarse
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})

# Logout personalizado
def custom_logout(request):
    logout(request)  # Cierra la sesión
    return redirect("home")  # Redirige al home como invitado

# Panel exclusivo para médicos
@medico_required
def panel_medico(request):
    return render(request, "usuarios/panel_medico.html")

# Vista de perfil del usuario autenticado
@login_required
def mi_perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    return render(request, "usuarios/mi_perfil.html", {"perfil": perfil})

# Página "Quiénes somos"
def quienes_somos(request):
    return render(request, "quienes_somos.html")

# Página "Profesionales de la salud"
def profesionales(request):
    return render(request, "profesionales.html")

# 1. Página informativa del Sector Salud (Acceso libre)
def sector_salud_info(request):
    # Aquí puedes pasar datos estáticos si lo deseas, o simplemente renderizar
    return render(request, "usuarios/sector_salud_info.html")

# 1. DEFINIR PRIMERO LA LÓGICA (Helper function)
def calcular_semaforo(imc, edad):
    # Lógica para Adultos [cite: 15-19]
    if edad < 60:
        if imc < 18.5: return "warning", "Bajo peso"
        if imc < 25.0: return "success", "Normal"
        if imc < 30.0: return "warning", "Sobrepeso"
        return "danger", "Obesidad"
    # Lógica para Adulto Mayor [cite: 20-25]
    else:
        if imc <= 23.0: return "warning", "Delgadez"
        if imc < 28.0: return "success", "Normal"
        if imc < 32.0: return "warning", "Sobrepeso"
        return "danger", "Obesidad"

# 2. USARLA DESPUÉS EN LA VISTA
def calculadora_imc(request):
    resultado = None
    if request.method == "POST":
        try:
            peso = float(request.POST.get('peso'))
            talla = float(request.POST.get('talla'))
            edad = int(request.POST.get('edad'))
            
            imc = peso / (talla ** 2) # [cite: 14]
            
            # Aquí ya no dará NameError porque está definida arriba
            color, categoria = calcular_semaforo(imc, edad)
            
            # Conductas sugeridas según documento [cite: 36]
            if color == "success": conducta = "Educación + control periódico."
            elif color == "warning": conducta = "Intervención educativa + re-tamizaje."
            else: conducta = "Valoración prioritaria (Nutrición + Médico)."

            resultado = {
                'imc': round(imc, 2),
                'categoria': categoria,
                'color': color,
                'conducta': conducta
            }
        except (TypeError, ValueError):
            resultado = {'error': "Ingresa valores válidos."}

    return render(request, "usuarios/calculadora.html", {"resultado": resultado})

#Test de riesgo nutricional
def test_riesgo_nutricional(request):
    resultado_test = None
    
    # Definimos las preguntas aquí para que el HTML sea más limpio [cite: 27, 28]
    preguntas = [
        {'id': 1, 'titulo': 'Pérdida de peso no intencional', 'desc': '¿Ha bajado de peso sin proponérselo?'},
        {'id': 2, 'titulo': 'Disminución del apetito', 'desc': '¿Tiene menos ganas de comer o saciedad temprana?'},
        {'id': 3, 'titulo': 'Cantidad de comida', 'desc': '¿Come porciones más pequeñas que antes?'},
        {'id': 4, 'titulo': 'Síntomas gastrointestinales', 'desc': 'Náusea, vómito, diarrea o mal sabor de boca.'},
        {'id': 5, 'titulo': 'Capacidad funcional', 'desc': 'Fatiga, pérdida de fuerza o dificultad para tareas.'},
        {'id': 6, 'titulo': 'Enfermedad aguda reciente', 'desc': 'Infección, fiebre o cirugía reciente.'},
        {'id': 7, 'titulo': 'Problemas del tratamiento', 'desc': 'Complicaciones que afecten su alimentación.'},
        {'id': 8, 'titulo': 'Señales físicas', 'desc': 'Cambios en ropa o cuerpo (pérdida muscular/edema).'}
    ]

    if request.method == "POST":
        # Sumamos los puntajes de los 8 ítems [cite: 31, 33]
        puntos = sum([int(request.POST.get(f'p{i}', 0)) for i in range(1, 9)])
        
        # Interpretación basada en el rango de puntos (0-24) [cite: 36]
        if puntos <= 4:
            nivel, clase, conducta = "Bajo", "success", "Educación + control periódico."
        elif puntos <= 9:
            nivel, clase, conducta = "Leve", "info", "Intervención educativa + re-tamizaje."
        elif puntos <= 14:
            nivel, clase, conducta = "Moderado", "warning", "Cita con nutrición clínica."
        else:
            nivel, clase, conducta = "Alto", "danger", "Valoración prioritaria (nutrición + médico)."
            
        resultado_test = {
            'puntos': puntos,
            'nivel': nivel,
            'clase': clase,
            'conducta': conducta
        }
        
    context = {
        "resultado": resultado_test,
        "preguntas": preguntas,
        "rango_puntaje": [0, 1, 2, 3] # Enviamos el rango como una lista
    }
    
    return render(request, "usuarios/test_riesgo.html", context)

def pacientes_familias(request):
    return render(request, 'usuarios/pacientes_familias.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'usuarios/editar_perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    return render(request, 'usuarios/editar_perfil.html', {
        'u_form': u_form,
        'p_form': p_form
    })