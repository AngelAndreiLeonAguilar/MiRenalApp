from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Opinion
from apps.usuarios.models import Perfil # No olvides esta importación
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def foro(request):
    # --- 1. Lógica para GUARDAR nuevos comentarios ---
    if request.method == 'POST':
        # Verificamos si el usuario está bloqueado antes de dejarlo publicar
        if request.user.perfil.esta_bloqueado:
            # Si está bloqueado, lo regresamos al foro sin guardar nada
            return redirect('foro')

        comentario_texto = request.POST.get('comentario')
        estrellas_valor = request.POST.get('estrellas')
        
        if comentario_texto:
            Opinion.objects.create(
                usuario=request.user,
                comentario=comentario_texto,
                estrellas=estrellas_valor
            )
            return redirect('foro')

    # --- 2. Lógica para MOSTRAR y FILTRAR ---
    filtro = request.GET.get('ordenar', 'reciente')
    
    if filtro == 'estrellas':
        query = Opinion.objects.all().order_by('-estrellas', '-fecha_creacion')
    elif filtro == 'likes':
        query = Opinion.objects.annotate(total_likes=Count('likes')).order_by('-total_likes', '-fecha_creacion')
    else:
        query = Opinion.objects.all().order_by('-fecha_creacion')

    # --- 3. Paginación ---
    paginator = Paginator(query, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/foro.html', {
        'opiniones': page_obj, 
        'filtro_actual': filtro
    })

# --- FUNCIONES DE ADMINISTRADOR (STAFF) ---

@user_passes_test(lambda u: u.is_staff)
def eliminar_comentario(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id)
    opinion.delete()
    return redirect('foro')

@user_passes_test(lambda u: u.is_staff)
def alternar_bloqueo(request, usuario_id):
    # Buscamos el perfil del usuario mediante su ID de usuario
    perfil = get_object_or_404(Perfil, user_id=usuario_id)
    perfil.esta_bloqueado = not perfil.esta_bloqueado
    perfil.save()
    return redirect('foro')

# --- LIKES Y DISLIKES (Tus funciones originales) ---

@login_required
def dar_like(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    if request.user in opinion.likes.all():
        opinion.likes.remove(request.user)
    else:
        opinion.likes.add(request.user)
        opinion.dislikes.remove(request.user)
    return redirect('foro')

@login_required
def dar_dislike(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    if request.user in opinion.dislikes.all():
        opinion.dislikes.remove(request.user)
    else:
        opinion.dislikes.add(request.user)
        opinion.likes.remove(request.user)
    return redirect('foro')