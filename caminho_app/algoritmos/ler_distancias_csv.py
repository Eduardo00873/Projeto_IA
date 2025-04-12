import csv
import os
from django.conf import settings

def ler_distancias_csv(nome_ficheiro):
    grafo = {}
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'caminho_app', 'algoritmos', nome_ficheiro)

    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        cidades = [cidade.strip().lower() for cidade in reader[0]]

        for i in range(1, len(reader)):
            linha = reader[i]
            origem = linha[0].strip().lower()
            grafo.setdefault(origem, [])

            for j in range(1, len(linha)):
                if linha[j].strip() == '':
                    continue
                try:
                    destino = cidades[j].strip().lower()
                    distancia = float(linha[j])
                    grafo[origem].append((destino, distancia))
                    grafo.setdefault(destino, []).append((origem, distancia))
                except ValueError:
                    print(f"Erro ao processar distância entre {origem} e {cidades[j]}: '{linha[j]}'")
    return grafo

def ler_heuristica_faro(nome_ficheiro):
    heuristica = {}
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'caminho_app', 'algoritmos', nome_ficheiro)

    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # pula cabeçalho
        for linha in reader:
            if len(linha) < 2:
                continue
            cidade = linha[0].strip().lower()
            try:
                heuristica[cidade] = float(linha[1])
            except ValueError:
                print(f"Heurística inválida para {cidade}: '{linha[1]}'")
    return heuristica
