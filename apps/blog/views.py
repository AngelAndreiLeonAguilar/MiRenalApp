from django.shortcuts import render, redirect, get_object_or_404
from .models import Opinion
from django.contrib.auth.decorators import login_required

@login_required
def foro(request):
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        estrellas = request.POST.get('estrellas')
        
        # Guardamos la opinión vinculada al usuario logueado (como 'Nol')
        Opinion.objects.create(
            usuario=request.user,
            comentario=comentario,
            estrellas=estrellas
        )
        return redirect('foro')

    # Obtenemos todas las opiniones, las más recientes primero
    opiniones = Opinion.objects.all().order_by('-fecha_creacion')
    return render(request, 'blog/foro.html', {'opiniones': opiniones})

@login_required
def dar_like(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    if request.user in opinion.likes.all():
        opinion.likes.remove(request.user)
    else:
        opinion.likes.add(request.user)
        opinion.dislikes.remove(request.user) # Evita tener like y dislike al mismo tiempo
    return redirect('foro')

@login_required
def dar_dislike(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    if request.user in opinion.dislikes.all():
        opinion.dislikes.remove(request.user)
    else:
        opinion.dislikes.add(request.user)
        opinion.likes.remove(request.user) # Quita el like si existía
    return redirect('foro')