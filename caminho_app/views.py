from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AlgoritmoForm
from caminho_app.algoritmos.aprofundamentoProgressivo import busca_aprofundamento_progressivo
from caminho_app.algoritmos.aStar import a_estrela
from caminho_app.algoritmos.custoUniforme import custo_uniforme
from caminho_app.algoritmos.procuraSofrega import procura_sofrega
from caminho_app.algoritmos.ler_distancias_csv import ler_distancias_csv, ler_heuristica_faro

def processar_algoritmo(request):
    if request.method == 'POST':
        form = AlgoritmoForm(request.POST)
        if form.is_valid():
            request.session['algoritmo_form_data'] = form.cleaned_data
            return redirect(reverse('processar_algoritmo'))
    else:
        form = AlgoritmoForm()

    resultado = None
    form_data = request.session.pop('algoritmo_form_data', None)

    if form_data:
        algoritmo = form_data['algoritmo']
        origem = form_data['origem'].strip().lower()

        # Define destino automático para A* e Sôfrega
        if algoritmo in ['a_estrela', 'sofrega']:
            destino = 'faro'
        else:
            destino = form_data['destino'].strip().lower()

        grafo = ler_distancias_csv('distancesCities.csv')

        if origem not in grafo or destino not in grafo:
            resultado = "Cidade não encontrada no grafo."
        else:
            if algoritmo == 'aprofundamento':
                caminho = busca_aprofundamento_progressivo(grafo, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({len(caminho) - 1} passos)"
                else:
                    resultado = "Caminho não encontrado com Aprofundamento Agressivo."

            elif algoritmo == 'custo_uniforme':
                caminho, custo = custo_uniforme(grafo, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({custo:.1f} km)"
                else:
                    resultado = "Caminho não encontrado com Custo Uniforme."

            elif algoritmo == 'a_estrela':
                heuristica = ler_heuristica_faro('distancesFaro.csv')
                caminho, custo = a_estrela(grafo, heuristica, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({custo:.1f} km)"
                else:
                    resultado = "Caminho não encontrado com A*."

            elif algoritmo == 'sofrega':
                heuristica = ler_heuristica_faro('distancesFaro.csv')
                caminho = procura_sofrega(grafo, heuristica, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({len(caminho) - 1} passos)"
                else:
                    resultado = "Caminho não encontrado com Procura Sôfrega."

    return render(request, 'caminho_app/index.html', {'form': form, 'resultado': resultado})
