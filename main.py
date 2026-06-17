"""
==================================================================
LAST-MILE DELIVERY — Otimizacao de Rotas com Clarke-Wright Savings
==================================================================
Cenario : Equipe de Logistica do Mercado Livre
Dor     : No pico da Black Friday, cada entregador visita em media
          80 enderecos/dia. Rotas mal otimizadas custam ~40% mais
          em tempo e combustivel.
Solucao : Modelar o bairro como um grafo ponderado dirigido (ruas
          com tempo/distancia de deslocamento como peso) e aplicar
          o algoritmo de Clarke-Wright Savings para dividir as
          entregas entre varios entregadores, minimizando a
          distancia total percorrida.

GRAFO: ponderado dirigido
  - No 0           = Centro de Distribuicao (deposito)
  - Nos 1..N        = enderecos de entrega
  - Aresta (i, j)   = distancia/tempo de deslocamento entre dois pontos

Variante do problema: VRP (Vehicle Routing Problem), uma
generalizacao do Problema do Caixeiro Viajante (TSP) para
MULTIPLOS entregadores, cada um com capacidade maxima de paradas.
==================================================================
"""

import math
import random
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# PARAMETROS DA SIMULACAO (ajuste estes valores para o demo ao vivo)
# ------------------------------------------------------------------
NUM_ENDERECOS = 24        # quantidade de entregas no bairro
CAPACIDADE_ENTREGADOR = 6  # numero maximo de paradas por rota/entregador
SEED = 7                  # semente aleatoria (reprodutibilidade)


# ------------------------------------------------------------------
# 1. MODELAGEM DO GRAFO
# ------------------------------------------------------------------
def gerar_enderecos(n, seed=SEED):
    """Gera coordenadas (x, y) para o deposito (no 0) e n enderecos."""
    random.seed(seed)
    pontos = [(0.0, 0.0)]  # deposito fica na origem
    for _ in range(n):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        pontos.append((x, y))
    return pontos


def construir_matriz_distancias(pontos):
    """Constroi a matriz de pesos do grafo (distancia euclidiana
    como aproximacao do tempo de deslocamento entre dois pontos)."""
    n = len(pontos)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = pontos[i][0] - pontos[j][0]
                dy = pontos[i][1] - pontos[j][1]
                dist[i][j] = math.hypot(dx, dy)
    return dist


# ------------------------------------------------------------------
# 2. CENARIO "ANTES" — despacho ingenuo (sem otimizacao)
#    Simula o que o dispatcher faz hoje: agrupa enderecos na ordem
#    em que chegaram, sem nenhum criterio de proximidade.
# ------------------------------------------------------------------
def rotas_ingenuas(n, capacidade):
    clientes = list(range(1, n + 1))
    rotas = [clientes[i:i + capacidade] for i in range(0, len(clientes), capacidade)]
    return rotas


# ------------------------------------------------------------------
# 3. ALGORITMO CLARKE-WRIGHT SAVINGS
# ------------------------------------------------------------------
def clarke_wright_savings(n, dist, capacidade):
    """
    Passo 1: cada cliente comeca em sua propria rota
             (deposito -> cliente -> deposito).
    Passo 2: calcula a 'economia' (savings) de unir cada par (i, j):
             s(i, j) = dist(0, i) + dist(0, j) - dist(i, j)
             -> quanto maior, mais vantajoso visitar i e j na
                MESMA rota em vez de rotas separadas.
    Passo 3: ordena as economias da maior para a menor e funde
             rotas greedily, respeitando duas regras:
               a) so se pode fundir nas EXTREMIDADES de cada rota
                  (clientes "interiores" ja estao travados);
               b) a rota resultante nao pode exceder a capacidade
                  do entregador.
    """
    rotas = {i: [i] for i in range(1, n + 1)}
    rota_de = {i: i for i in range(1, n + 1)}

    # calcula as economias para todos os pares de enderecos
    economias = []
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            s = dist[0][i] + dist[0][j] - dist[i][j]
            economias.append((s, i, j))
    economias.sort(key=lambda x: x[0], reverse=True)

    for s, i, j in economias:
        ri, rj = rota_de[i], rota_de[j]
        if ri == rj:
            continue  # ja estao na mesma rota

        rota_i, rota_j = rotas[ri], rotas[rj]
        if len(rota_i) + len(rota_j) > capacidade:
            continue  # excede a capacidade do entregador

        i_inicio, i_fim = rota_i[0] == i, rota_i[-1] == i
        j_inicio, j_fim = rota_j[0] == j, rota_j[-1] == j

        if not (i_inicio or i_fim) or not (j_inicio or j_fim):
            continue  # i ou j esta "preso" no meio de uma rota

        if i_fim and j_inicio:
            nova_rota = rota_i + rota_j
        elif j_fim and i_inicio:
            nova_rota = rota_j + rota_i
        elif i_fim and j_fim:
            nova_rota = rota_i + rota_j[::-1]
        elif i_inicio and j_inicio:
            nova_rota = rota_i[::-1] + rota_j
        else:
            continue

        novo_id = ri
        rotas[novo_id] = nova_rota
        del rotas[rj]
        for cliente in nova_rota:
            rota_de[cliente] = novo_id

    return list(rotas.values())


# ------------------------------------------------------------------
# 4. METRICAS
# ------------------------------------------------------------------
def distancia_rota(rota, dist):
    total = 0.0
    anterior = 0  # comeca no deposito
    for atual in rota:
        total += dist[anterior][atual]
        anterior = atual
    total += dist[anterior][0]  # volta ao deposito
    return total


def distancia_total(rotas, dist):
    return sum(distancia_rota(r, dist) for r in rotas)


# ------------------------------------------------------------------
# 5. VISUALIZACAO
# ------------------------------------------------------------------
def plotar_comparacao(pontos, rotas_antes, rotas_depois, caminho_saida):
    fig, eixos = plt.subplots(1, 2, figsize=(13, 6))
    cores = plt.cm.tab10.colors

    for eixo, rotas, titulo in [
        (eixos[0], rotas_antes, "ANTES — despacho sem otimizacao"),
        (eixos[1], rotas_depois, "DEPOIS — Clarke-Wright Savings"),
    ]:
        # deposito
        eixo.scatter(*pontos[0], c="black", s=200, marker="s", zorder=5)
        eixo.annotate("Deposito", pontos[0], textcoords="offset points",
                      xytext=(8, 8), fontsize=9, fontweight="bold")

        for idx, rota in enumerate(rotas):
            cor = cores[idx % len(cores)]
            caminho = [0] + rota + [0]
            xs = [pontos[p][0] for p in caminho]
            ys = [pontos[p][1] for p in caminho]
            eixo.plot(xs, ys, "-o", color=cor, linewidth=1.8, markersize=6)

        eixo.set_title(f"{titulo}\n{len(rotas)} entregadores | "
                        f"{distancia_total(rotas, dist_global):.1f} km totais")
        eixo.set_xticks([])
        eixo.set_yticks([])
        for spine in eixo.spines.values():
            spine.set_visible(False)

    fig.suptitle("Last-Mile Delivery — Roteamento de Entregas (Mercado Livre)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150)
    print(f"\nGrafico salvo em: {caminho_saida}")


# ------------------------------------------------------------------
# 6. EXECUCAO PRINCIPAL (DEMO AO VIVO)
# ------------------------------------------------------------------
def main():
    global dist_global  # usado apenas para simplificar o plot acima

    pontos = gerar_enderecos(NUM_ENDERECOS)
    dist_global = construir_matriz_distancias(pontos)

    rotas_antes = rotas_ingenuas(NUM_ENDERECOS, CAPACIDADE_ENTREGADOR)
    rotas_depois = clarke_wright_savings(NUM_ENDERECOS, dist_global, CAPACIDADE_ENTREGADOR)

    dist_antes = distancia_total(rotas_antes, dist_global)
    dist_depois = distancia_total(rotas_depois, dist_global)
    reducao = (1 - dist_depois / dist_antes) * 100

    print("=" * 60)
    print("LAST-MILE DELIVERY — RELATORIO DA SIMULACAO")
    print("=" * 60)
    print(f"Enderecos de entrega simulados : {NUM_ENDERECOS}")
    print(f"Capacidade por entregador       : {CAPACIDADE_ENTREGADOR} paradas")
    print("-" * 60)
    print(f"ANTES  (despacho ingenuo)")
    print(f"   Entregadores necessarios     : {len(rotas_antes)}")
    print(f"   Distancia total              : {dist_antes:.2f} km")
    print("-" * 60)
    print(f"DEPOIS (Clarke-Wright Savings)")
    print(f"   Entregadores necessarios     : {len(rotas_depois)}")
    print(f"   Distancia total              : {dist_depois:.2f} km")
    print("-" * 60)
    print(f"REDUCAO DE DISTANCIA PERCORRIDA : {reducao:.1f}%")
    print("=" * 60)

    plotar_comparacao(pontos, rotas_antes, rotas_depois, "comparacao_rotas.png")


if __name__ == "__main__":
    main()