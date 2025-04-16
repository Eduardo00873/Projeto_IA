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


def profundidade_limitada(grafo, atual, destino, limite, caminho, visitados, interacoes):
    interacoes.append(f"Visitando: {atual.upper()}, Caminho: {' -> '.join(caminho)}, Limite restante: {limite}")
    
    if atual == destino:
        interacoes.append(f"Destino {destino.upper()} encontrado!\n")
        return caminho

    if limite <= 0:
        interacoes.append(f"Limite atingido ao chegar em {atual.upper()}.\n")
        return None

    visitados.add(atual)
    for vizinho, _ in grafo.get(atual, []):
        if vizinho not in visitados:
            resultado = profundidade_limitada(
                grafo, vizinho, destino, limite - 1, caminho + [vizinho], visitados.copy(), interacoes
            )
            if resultado:
                return resultado
    return None


def busca_aprofundamento_progressivo(grafo, origem, destino, limite_max=50):
    interacoes = []
    interacoes.append("Início da Busca em Aprofundamento Progressivo:\n")

    for limite in range(1, limite_max + 1):
        interacoes.append(f"Profundidade atual: {limite}")
        resultado = profundidade_limitada(grafo, origem, destino, limite, [origem], set(), interacoes)
        if resultado:
            return resultado, interacoes
        interacoes.append(f"Nenhum caminho encontrado com profundidade {limite}.\n")

    interacoes.append("Caminho não encontrado após atingir o limite máximo.")
    return None, interacoes


def main():
    grafo = ler_distancias_csv('distancesCities.csv')

    origem = input("Cidade de origem: ").strip().lower()
    destino = input("Cidade de destino: ").strip().lower()

    if origem not in grafo or destino not in grafo:
        print("Cidade não encontrada no grafo.")
        return

    limite_max = input("Profundidade máxima (pressiona Enter para usar 50): ").strip()
    limite_max = int(limite_max) if limite_max.isdigit() else 50

    caminho, interacoes = busca_aprofundamento_progressivo(grafo, origem, destino, limite_max)

    print("\nINTERAÇÕES:")
    print("-" * 40)
    for linha in interacoes:
        print(linha)

    print("\nRESULTADO:")
    if caminho:
        print(" -> ".join(caminho))
        print(f"Número de passos: {len(caminho) - 1}")
    else:
        print(f"Não foi possível encontrar um caminho entre '{origem}' e '{destino}' com profundidade até {limite_max}.")


if __name__ == "__main__":
    main()
