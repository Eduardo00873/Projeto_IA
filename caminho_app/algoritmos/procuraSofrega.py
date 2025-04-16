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

def procura_sofrega(grafo, heuristica, origem, destino="faro"):
    fila = [(heuristica.get(origem, float('inf')), origem, [origem])]
    visitados = set()
    interacoes = []
    passo = 1

    interacoes.append("Início da Procura Sôfrega:\n")

    while fila:
        interacoes.append(f"--- Passo {passo} ---")
        interacoes.append("Fila de prioridade: " + str([
            (round(prio, 1), n, ' -> '.join(p)) for prio, n, p in fila
        ]))

        prioridade, atual, caminho = heapq.heappop(fila)
        interacoes.append(f"A explorar: {atual.upper()} (h: {prioridade})")

        if atual == destino:
            interacoes.append("Destino alcançado!\n")
            return caminho, interacoes

        if atual in visitados:
            interacoes.append(f"{atual.upper()} já foi visitado.\n")
            passo += 1
            continue
        visitados.add(atual)

        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados:
                h = heuristica.get(vizinho, float('inf'))
                interacoes.append(f"  Adicionando vizinho: {vizinho.upper()} (h: {h})")
                heapq.heappush(fila, (h, vizinho, caminho + [vizinho]))

        interacoes.append("")
        passo += 1

    interacoes.append("Caminho não encontrado.")
    return None, interacoes

def main():
    grafo = ler_distancias_csv('distancesCities.csv')
    heuristica = ler_heuristica_faro('distancesFaro.csv')

    origem = input("Cidade de origem: ").strip().lower()
    destino = "faro"

    if origem not in grafo:
        print("Cidade de origem não encontrada.")
        return

    caminho, interacoes = procura_sofrega(grafo, heuristica, origem, destino)

    print("\nINTERAÇÕES:")
    print("-" * 40)
    for linha in interacoes:
        print(linha)

    print("\nRESULTADO:")
    if caminho:
        print(" -> ".join(caminho))
        print(f"Número de passos: {len(caminho) - 1}")
    else:
        print("Não foi possível encontrar um caminho até Faro.")

if __name__ == "__main__":
    main()
