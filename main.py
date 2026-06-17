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