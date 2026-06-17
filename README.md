# Last-Mile Delivery — Otimização de Rotas com Clarke-Wright Savings

## Descrição do Projeto

Este projeto implementa uma solução para otimização de rotas de entrega de última milha (*Last-Mile Delivery*) utilizando o algoritmo **Clarke-Wright Savings**.

O cenário simula uma operação logística semelhante à utilizada por empresas de e-commerce, como o Mercado Livre, durante períodos de alta demanda, como a Black Friday.

O objetivo é reduzir a distância total percorrida pelos entregadores, diminuindo custos operacionais, tempo de entrega e consumo de combustível.

---

## Problema

Durante a distribuição de encomendas, rotas planejadas sem critérios de otimização podem gerar deslocamentos desnecessários.

Para resolver esse problema, modelamos a região de entregas como um **grafo ponderado**, onde:

* O nó 0 representa o depósito.
* Os demais nós representam os clientes.
* As arestas representam a distância entre dois pontos.

A partir dessa representação, aplicamos o algoritmo Clarke-Wright Savings para construir rotas mais eficientes.

---

## Estrutura do Grafo

### Vértices

* Depósito (nó 0)
* Clientes (nós 1 até N)

### Arestas

Cada aresta possui um peso correspondente à distância entre dois pontos.

### Tipo de Grafo

* Ponderado
* Dirigido

---

## Algoritmo Utilizado

### Clarke-Wright Savings

O algoritmo segue os seguintes passos:

1. Inicializa uma rota individual para cada cliente.
2. Calcula a economia (*Savings*) para cada par de clientes.
3. Ordena as economias em ordem decrescente.
4. Realiza fusões de rotas respeitando:

   * Capacidade máxima do entregador;
   * Extremidades das rotas.

### Fórmula da Economia

S(i,j) = d(0,i) + d(0,j) − d(i,j)

Onde:

* d(0,i) = distância do depósito ao cliente i
* d(0,j) = distância do depósito ao cliente j
* d(i,j) = distância entre os clientes i e j

Quanto maior o valor de S(i,j), maior a vantagem de colocar os clientes na mesma rota.

---

## Tecnologias Utilizadas

* Python 3
* Math
* Random
* Matplotlib

---

## Como Executar

### 1. Instalar dependências

```bash
pip install matplotlib
```

### 2. Executar o projeto

```bash
python main.py
```

---

## Parâmetros da Simulação

```python
NUM_ENDERECOS = 24
CAPACIDADE_ENTREGADOR = 6
SEED = 7
```

Esses valores podem ser alterados para testar diferentes cenários.

---

## Métricas Avaliadas

O sistema compara:

* Número de entregadores utilizados;
* Distância total percorrida;
* Percentual de redução obtido após a otimização.

---

## Resultado Esperado

Ao final da execução, o programa apresenta:

* Relatório comparativo entre o cenário inicial e o otimizado;
* Distância total percorrida;
* Percentual de economia;
* Gráfico comparando as rotas antes e depois da aplicação do algoritmo.

---

## Conceitos Aplicados

* Grafos
* Grafos Ponderados
* Vehicle Routing Problem (VRP)
* Algoritmos Gulosos (Greedy)
* Clarke-Wright Savings
* Otimização Logística

---

## Organização dos Commits

### Commit 1

Implementação da modelagem do grafo e matriz de distâncias.

### Commit 2

Implementação do cenário inicial sem otimização.

### Commit 3

Implementação do algoritmo Clarke-Wright Savings.

### Commit 4

Implementação das métricas, visualização e relatório final.
