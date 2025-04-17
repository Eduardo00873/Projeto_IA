from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AlgoritmoForm
from caminho_app.algoritmos.aprofundamentoProgressivo import busca_aprofundamento_progressivo
from caminho_app.algoritmos.aStar import a_estrela
from caminho_app.algoritmos.custoUniforme import custo_uniforme
from caminho_app.algoritmos.procuraSofrega import procura_sofrega
from caminho_app.algoritmos.ler_distancias_csv import ler_distancias_csv, ler_heuristica_faro
from django.shortcuts import render
from .forms import EscolherImagemForm
from caminho_app.detector import Matricula_detector, Ocr
from django.conf import settings
import os
import cv2
import pytesseract
import re
from ultralytics import YOLO

COORDENADAS = {
    'aveiro': (40.6405, -8.6538),
    'braga': (41.5454, -8.4265),
    'bragança': (41.8064, -6.7574),
    'beja': (38.0151, -7.8632),
    'castelo branco': (39.8222, -7.4917),
    'coimbra': (40.2110, -8.4292),
    'évora': (38.5711, -7.9096),
    'faro': (37.0194, -7.9304),
    'guarda': (40.5373, -7.2676),
    'leiria': (39.7436, -8.8071),
    'lisboa': (38.7169, -9.1399),
    'porto': (41.1496, -8.6109),
    'vila real': (41.3006, -7.7461),
}

def processar_algoritmo(request):
    resultado = None
    coordenadas_caminho = []
    marcadores_nomes = []
    interacoes = []
    form_data = request.session.pop('algoritmo_form_data', None)
    matricula_detectada = request.session.pop('matricula_detectada', None)

    if request.method == 'POST':
        form = AlgoritmoForm(request.POST)
        if form.is_valid():
            request.session['algoritmo_form_data'] = form.cleaned_data
            return redirect(reverse('processar_algoritmo'))
    else:
        if matricula_detectada:
            form = AlgoritmoForm(initial={'origem': matricula_detectada})
        else:
            form = AlgoritmoForm()

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
            caminho = None

            if algoritmo == 'aprofundamento':
                caminho, interacoes = busca_aprofundamento_progressivo(grafo, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({len(caminho) - 1} passos)"
                else:
                    resultado = "Caminho não encontrado com Aprofundamento Agressivo."

            elif algoritmo == 'custo_uniforme':
                caminho, custo, interacoes = custo_uniforme(grafo, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({custo:.1f} km)"
                else:
                    resultado = "Caminho não encontrado com Custo Uniforme."

            elif algoritmo == 'a_estrela':
                heuristica = ler_heuristica_faro('distancesFaro.csv')
                caminho, custo, interacoes = a_estrela(grafo, heuristica, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({custo:.1f} km)"
                else:
                    resultado = "Caminho não encontrado com A*."

            elif algoritmo == 'sofrega':
                heuristica = ler_heuristica_faro('distancesFaro.csv')
                caminho, interacoes = procura_sofrega(grafo, heuristica, origem, destino)
                if caminho:
                    resultado = f"Caminho: {' -> '.join(caminho)} ({len(caminho) - 1} passos)"
                else:
                    resultado = "Caminho não encontrado com Procura Sôfrega."

            # Coordenadas para o mapa
            if caminho:
                for cidade in caminho:
                    nome = cidade.title()
                    cidade_lower = cidade.lower()
                    if cidade_lower in COORDENADAS:
                        coordenadas_caminho.append(list(COORDENADAS[cidade_lower]))
                        marcadores_nomes.append(nome)

    return render(request, 'caminho_app/index.html', {
        'form': form,
        'resultado': resultado,
        'coordenadas_caminho': coordenadas_caminho,
        'marcadores_nomes': marcadores_nomes,
        'interacoes': [str(linha) for linha in interacoes],  # Garantir strings
        'imagem_form': EscolherImagemForm(),
        'resultado_matricula': matricula_detectada
    })

def detectar_matricula_view(request):
    resultado = None

    if request.method == "POST":
        form = EscolherImagemForm(request.POST, request.FILES)
        if form.is_valid():
            caminho = form.cleaned_data['imagem']
            detector = Matricula_detector("caminho_app/license_plate_detector.pt", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
            resultado = detector.detetar_matricula(caminho)

            if resultado:
                request.session['matricula_detectada'] = resultado.lower()
                return redirect('processar_algoritmo')
    else:
        form = EscolherImagemForm()
