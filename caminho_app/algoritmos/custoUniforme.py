import csv
import heapq

def ler_distancias_csv(nome_ficheiro):
    grafo = {}
    with open(nome_ficheiro, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        
        # Primeira linha: cabeçalho com os nomes das cidades
        cidades = [cidade.strip().lower() for cidade in reader[0]]
        
        for i in range(1, len(reader)):
            linha = reader[i]
            origem = linha[0].strip().lower()
            grafo.setdefault(origem, [])

            for j in range(1, len(linha)):
                if linha[j].strip() == '':
                    continue  # sem ligação
                try:
                    destino = cidades[j].strip().lower()
                    distancia = float(linha[j])
                    grafo[origem].append((destino, distancia))
                    
                    # Assumimos que o grafo é bidirecional
                    grafo.setdefault(destino, []).append((origem, distancia))
                except ValueError:
                    print(f"Erro ao processar distância entre {origem} e {cidades[j]}: '{linha[j]}'")
    return grafo


def custo_uniforme(grafo, origem, destino):
    fila = [(0, origem, [origem])]  # (custo_acumulado, cidade_atual, caminho)
    visitados = set()

    while fila:
        custo, atual, caminho = heapq.heappop(fila)

        if atual == destino:
            return caminho, custo
        
        if atual in visitados:
            continue
        visitados.add(atual)

        for vizinho, distancia in grafo.get(atual, []):
            if vizinho not in visitados:
                heapq.heappush(fila, (custo + distancia, vizinho, caminho + [vizinho]))

    return None, float('inf')

def main():
    grafo = ler_distancias_csv('distancesCities.csv')
    
    origem = input("Cidade de origem: ").strip().lower()
    destino = input("Cidade de destino: ").strip().lower()

    if origem not in grafo or destino not in grafo:
        print("Cidade não encontrada.")
        return

    caminho, custo = custo_uniforme(grafo, origem, destino)
    
    if caminho:
        print(f"Caminho encontrado: {' -> '.join(caminho)}")
        print(f"Km totais: {custo} km")
    else:
        print("Não foi possível encontrar um caminho.")

if __name__ == "__main__":
    main()
