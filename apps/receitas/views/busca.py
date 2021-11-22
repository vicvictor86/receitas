from receitas.models import Receita
from django.shortcuts import render

def busca(request):
    """Busca uma receita e a renderiza no site"""
    lista_receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas' : lista_receitas
    }
    
    return render(request, 'receitas/buscar.html', dados)