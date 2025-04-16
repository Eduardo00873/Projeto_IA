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
    passo = 1
    interacoes = []

    interacoes.append("Início da busca de custo uniforme:\n")

    while fila:
        interacoes.append(f"--- Passo {passo} ---")
        interacoes.append("Fila de prioridade: " + str([(c, n, ' -> '.join(p)) for c, n, p in fila]))

        custo, atual, caminho = heapq.heappop(fila)
        interacoes.append(f"A explorar: {atual.upper()}, Custo acumulado: {custo}, Caminho até agora: {' -> '.join(caminho)}")

        if atual == destino:
            interacoes.append("Destino alcançado!\n")
            return caminho, custo, interacoes
        
        if atual in visitados:
            interacoes.append(f"{atual.upper()} já foi visitado.\n")
            passo += 1
            continue
        visitados.add(atual)

        for vizinho, distancia in grafo.get(atual, []):
            if vizinho not in visitados:
                novo_custo = custo + distancia
                novo_caminho = caminho + [vizinho]
                interacoes.append(f"  Adicionando vizinho: {vizinho.upper()} (Distância: {distancia}, Novo custo: {novo_custo})")
                heapq.heappush(fila, (novo_custo, vizinho, novo_caminho))

        interacoes.append("")  # linha em branco
        passo += 1

    interacoes.append("Caminho não encontrado.")
    return None, float('inf'), interacoes


# Esta função `main()` é útil para testes locais com terminal
def main():
    grafo = ler_distancias_csv('distancesCities.csv')
    
    origem = input("Cidade de origem: ").strip().lower()
    destino = input("Cidade de destino: ").strip().lower()

    if origem not in grafo or destino not in grafo:
        print("Cidade não encontrada no ficheiro.")
        return

    caminho, custo, interacoes = custo_uniforme(grafo, origem, destino)
    
    for linha in interacoes:
        print(linha)

    if caminho:
        print(f"\nCaminho encontrado: {' -> '.join(caminho)}")
        print(f"Km totais: {custo:.1f} km")
    else:
        print("Não foi possível encontrar um caminho.")


if __name__ == "__main__":
    main()
