import csv
import heapq

def ler_distancias_csv(nome_ficheiro):
    grafo = {}
    with open(nome_ficheiro, newline='', encoding='utf-8') as csvfile:
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
    with open(nome_ficheiro, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignora cabeçalho
        for linha in reader:
            if len(linha) < 2:
                continue
            cidade = linha[0].strip().lower()
            try:
                heuristica[cidade] = float(linha[1])
            except ValueError:
                print(f"Heurística inválida para {cidade}: '{linha[1]}'")
    return heuristica

def a_estrela(grafo, heuristica, origem, destino="faro"):
    fila = [(heuristica.get(origem, float('inf')), 0, origem, [origem])]
    visitados = set()
    interacoes = []
    passo = 1

    interacoes.append("Início da busca A*:\n")

    while fila:
        interacoes.append(f"--- Passo {passo} ---")
        interacoes.append("Fila de prioridade: " + str([
            (round(f, 1), n, ' -> '.join(p)) for f, g, n, p in fila
        ]))

        f, g, atual, caminho = heapq.heappop(fila)
        interacoes.append(f"A explorar: {atual.upper()}, Custo acumulado: {g}, Heurística: {heuristica.get(atual, '?')}")

        if atual == destino:
            interacoes.append("Destino alcançado!\n")
            return caminho, g, interacoes

        if atual in visitados:
            interacoes.append(f"{atual.upper()} já foi visitado.\n")
            passo += 1
            continue
        visitados.add(atual)

        for vizinho, custo in grafo.get(atual, []):
            if vizinho not in visitados:
                g_novo = g + custo
                h = heuristica.get(vizinho, float('inf'))
                f_novo = g_novo + h
                interacoes.append(f"  Adicionando vizinho: {vizinho.upper()} (g: {g_novo}, h: {h}, f: {f_novo})")
                heapq.heappush(fila, (f_novo, g_novo, vizinho, caminho + [vizinho]))

        interacoes.append("")
        passo += 1

    interacoes.append("Caminho não encontrado.")
    return None, float('inf'), interacoes

def main():
    grafo = ler_distancias_csv('distancesCities.csv')
    heuristica = ler_heuristica_faro('distancesFaro.csv')

    origem = input("Cidade de origem: ").strip().lower()
    destino = "faro"

    if origem not in grafo:
        print("Cidade de origem não encontrada.")
        return

    caminho, custo, interacoes = a_estrela(grafo, heuristica, origem, destino)

    print("\nINTERAÇÕES:")
    print("-" * 40)
    for linha in interacoes:
        print(linha)

    print("\nRESULTADO:")
    if caminho:
        print(" -> ".join(caminho))
        print(f"Km totais: {custo} km")
        print(f"Número de passos: {len(caminho) - 1}")
    else:
        print("Não foi possível encontrar um caminho até Faro.")

if __name__ == "__main__":
    main()
