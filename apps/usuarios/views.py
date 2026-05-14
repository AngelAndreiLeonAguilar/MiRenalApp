from django.shortcuts import render, redirect, get_object_or_404 # Agregado get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # Agregado User
from .forms import RegistroForm, UserUpdateForm, PerfilUpdateForm
from .models import Perfil, Opinion 
from .decorators import medico_required
from django.core.paginator import Paginator
from django.db.models import Count # Opcional: puedes moverlo aquí arriba también

# --- VISTAS PÚBLICAS ---

def home(request):
    return render(request, "home.html")

def quienes_somos(request):
    return render(request, "quienes_somos.html")

def profesionales(request):
    return render(request, "profesionales.html")

def pacientes_familias(request):
    return render(request, 'usuarios/pacientes_familias.html')

# --- AUTENTICACIÓN Y PERFIL ---

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})

def custom_logout(request):
    logout(request)
    return redirect("home")

@login_required
def mi_perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    return render(request, "usuarios/mi_perfil.html", {"perfil": perfil})

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
    return render(request, 'usuarios/editar_perfil.html', {'u_form': u_form, 'p_form': p_form})

# --- FORO COMUNITARIO ---

def foro(request):
    # 1. Lógica para GUARDAR (Solo si está autenticado)
    if request.method == 'POST':
        if request.user.is_authenticated:
            comentario_texto = request.POST.get('comentario')
            estrellas_valor = request.POST.get('estrellas', 5)
            
            if comentario_texto:
                Opinion.objects.create(
                    usuario=request.user,
                    comentario=comentario_texto,
                    estrellas=estrellas_valor
                )
                return redirect('foro')
        else:
            # Si intenta publicar sin estar logueado, al login
            return redirect('login')

    # 2. Lógica para MOSTRAR (Para todo el mundo)
    filtro = request.GET.get('ordenar', 'reciente')
    query = Opinion.objects.all().select_related('usuario__perfil')
    
    # Lógica de ordenamiento
    filtro = request.GET.get('ordenar', 'reciente')
    if filtro == 'estrellas':
        query = query.order_by('-estrellas')
    elif filtro == 'likes':
        from django.db.models import Count
        query = query.annotate(total_likes=Count('likes')).order_by('-total_likes')
    else:
        query = query.order_by('-fecha_creacion')

    # AGREGAR PAGINACIÓN (10 opiniones por página)
    paginator = Paginator(query, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'usuarios/foro.html', {
        'opiniones': page_obj, # Enviamos el objeto paginado
        'filtro_actual': filtro
    })

# --- SECTOR SALUD Y HERRAMIENTAS ---

def sector_salud_info(request):
    return render(request, "usuarios/sector_salud_info.html")

@medico_required
def panel_medico(request):
    return render(request, "usuarios/panel_medico.html")

def calculadora_imc(request):
    resultado = None
    if request.method == "POST":
        try:
            peso = float(request.POST.get('peso'))
            talla = float(request.POST.get('talla'))
            edad = int(request.POST.get('edad'))
            imc = round(peso / (talla ** 2), 2)
            
            # Lógica según puntos de corte del PDF
            if edad < 60: # Adultos [cite: 15]
                if imc < 18.5: res = ('Bajo peso', 'warning', 'Valoración nutricional programada') # [cite: 16, 36]
                elif imc < 25: res = ('Normal', 'success', 'Educación + control periódico') # [cite: 17, 36]
                elif imc < 30: res = ('Sobrepeso', 'danger', 'Intervención educativa') # [cite: 18, 36]
                else: res = ('Obesidad', 'danger', 'Cita con nutrición clínica') # [cite: 19, 36]
            else: # Adulto Mayor [cite: 20]
                if imc <= 23.0: res = ('Delgadez', 'warning', 'Valoración nutricional programada') # [cite: 21, 36]
                elif imc < 28.0: res = ('Normal', 'success', 'Educación + control periódico') # [cite: 22, 36]
                elif imc < 32.0: res = ('Sobrepeso', 'danger', 'Intervención educativa') # [cite: 23, 36]
                else: res = ('Obesidad', 'danger', 'Cita con nutrición clínica') # [cite: 25, 36]

            resultado = {
                'imc': imc,
                'categoria': res[0],
                'color': res[1],
                'conducta': res[2]
            }
        except:
            resultado = {'error': "Datos inválidos"}
            
    return render(request, "usuarios/calculadora.html", {"resultado": resultado})

# ESTA ES LA FUNCIÓN QUE FALTABA
def test_riesgo_nutricional(request):
    resultado_test = None
    # Definición de los 8 ítems según el documento oficial 
    preguntas = [
        {'id': 1, 'titulo': 'Pérdida de peso', 'desc': '¿Ha bajado de peso sin proponérselo?'},
        {'id': 2, 'titulo': 'Apetito', 'desc': '¿Tiene menos ganas de comer o saciedad temprana?'},
        {'id': 3, 'titulo': 'Ingesta', 'desc': '¿Come menos que antes (porciones más pequeñas)?'},
        {'id': 4, 'titulo': 'Síntomas GI', 'desc': 'Náusea, vómito, diarrea o mal sabor de boca.'},
        {'id': 5, 'titulo': 'Capacidad funcional', 'desc': 'Fatiga, pérdida de fuerza o menos actividad.'},
        {'id': 6, 'titulo': 'Enfermedad reciente', 'desc': 'Infección, hospitalización o cirugía reciente.'},
        {'id': 7, 'titulo': 'Problemas tratamiento', 'desc': 'Cambios o complicaciones del tratamiento renal.'},
        {'id': 8, 'titulo': 'Señales físicas', 'desc': 'Cambios visibles que sugieran pérdida muscular.'},
    ]

    if request.method == "POST":
        # Suma de puntos (0-24 total) 
        puntos = sum([int(request.POST.get(f'p{i}', 0)) for i in range(1, 9)])
        
        # Interpretación diagnóstica basada en el protocolo 
        if puntos <= 4:
            nivel, clase, conducta = "Bajo", "success", "Educación + control periódico"
        elif puntos <= 9:
            nivel, clase, conducta = "Leve", "info", "Intervención educativa + re-tamizaje"
        elif puntos <= 14:
            nivel, clase, conducta = "Moderado", "warning", "Cita con nutrición clínica"
        else:
            nivel, clase, conducta = "Alto", "danger", "Valoración prioritaria (nutrición + médico)"
            
        resultado_test = {
            'puntos': puntos,
            'nivel': nivel,
            'clase': clase, # Cambiado de 'color' a 'clase' para coincidir con tu HTML
            'conducta': conducta
        }
        
    return render(request, "usuarios/test_riesgo.html", {
        "resultado": resultado_test, 
        "preguntas": preguntas,
        "rango_puntaje": range(4) # Esto genera los números [0, 1, 2, 3] 
    })
    
@login_required
def dar_like(request, pk):
    opinion = get_object_or_404(Opinion, pk=pk)
    if request.user in opinion.likes.all():
        opinion.likes.remove(request.user)
    else:
        opinion.likes.add(request.user)
        opinion.dislikes.remove(request.user) # Quitar dislike si da like
    return redirect('foro')

@login_required
def dar_dislike(request, pk):
    opinion = get_object_or_404(Opinion, pk=pk)
    if request.user in opinion.dislikes.all():
        opinion.dislikes.remove(request.user)
    else:
        opinion.dislikes.add(request.user)
        opinion.likes.remove(request.user) # Quitar like si da dislike
    return redirect('foro')

@login_required
def eliminar_comentario(request, opinion_id):
    # Solo el staff o el dueño pueden borrarlo
    opinion = get_object_or_404(Opinion, id=opinion_id)
    if request.user.is_staff or opinion.usuario == request.user:
        opinion.delete()
    return redirect('foro')

@login_required
def alternar_bloqueo(request, usuario_id):
    # Solo administradores pueden bloquear
    if not request.user.is_staff:
        return redirect('foro')
    
    usuario_a_bloquear = get_object_or_404(User, id=usuario_id)
    perfil = usuario_a_bloquear.perfil
    perfil.esta_bloqueado = not perfil.esta_bloqueado
    perfil.save()
    return redirect('foro')