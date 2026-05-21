# Metodologia de Testes: ABC (Artificial Bee Colony)

## 1. Objetivo

Avaliar o desempenho do ABC variando sistematicamente a **Pressão Seletiva (Roleta vs. Torneio)**, o **Fator de Abandono (*Limit*)** e a **Distribuição de Tarefas da Colônia** em problemas de $30D$. O foco é mapear as fraquezas do algoritmo em alta dimensionalidade e definir a arquitetura campeã para o teste de estresse de convergência.

---

## 2. Status Executivo

| Métrica | Valor |
| --- | --- | --- |
| Notebooks executados | 0/7 |
| Replicatas por config | 30 | 
| Configuração Vencedora | *A definir* | 

**Melhores Resultados Finais (Baseline - Médias):**

* **Sphere:** *Aguardando dados...*
* **Rastrigin:** *Aguardando dados...*
* **Rosenbrock:** *Aguardando dados...*

---

## 3. Design Experimental

### 3.1 Variáveis Controladas

**Fixas (todas as configurações):**

* **Dimensões:** $30$
* **População Base:** $30$ abelhas
* **Iterações Base:** $500$ (Ajustado devido à taxa de convergência mais lenta do ABC)
* **Seeds:** $42-71$ (Pareamento perfeito para isolamento de variáveis)

**Matriz de Testes:**

| Teste | Seleção | Fator de Abandono (Fórmula) | CS / CICLOS | Objetivo do Teste |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Roleta** | `(CS/2) * DIM` | 30 / 100 | Baseline Clássico (Controle). |
| **2** | **Torneio** | `(CS/2) * DIM` | 30 / 100 | Avaliar Pressão Seletiva. |
| **3** | Roleta | `((CS/2) * DIM) / 2` | 30 / 100 | Sensibilidade: Abandono Moderado. |
| **4** | Roleta | `((CS/2) * DIM) / 4` | 30 / 100 | Sensibilidade: Abandono Rápido. |
| **5** | Roleta | `(CS/2) * DIM` | **100 / 100** | Estresse Espacial (Tamanho). |
| **6** | Roleta | `(CS/2) * DIM` | **30 / 500** | Estresse Temporal (Ciclos). |
| **7** | Roleta | `((CS/2) * DIM) / 4` | **100 / 500** | Performance Máxima (Estresse Final). |


### 3.2 Implementação Técnica

**Cada notebook executará o seguinte protocolo:**

```python
for execucao in range(30):
    seed_atual = 42 + execucao
    random.seed(seed_atual)
    np.random.seed(seed_atual)
    # Execução do enxame com T=500 (ou T=2500 para Max Performance)
    # Coleta de gBest_fitness ao final de cada iteração

```

**Isolamento de Efeito:** O pareamento garante que a execução $N$ do teste 1 comece com as mesmas posições iniciais (fontes de alimento) da execução $N$ dos testes subsequentes.

---

## 4. Justificativa das Variáveis de Teste (Paralelo com PSO/AG)

**1. Seleção (Roleta vs. Torneio) - *Análogo ao Elitismo do AG*:**
O ABC com Roleta clássica sofre em funções complexas (como Rosenbrock) porque a diferença relativa de aptidão perde escala. O Torneio força as abelhas observadoras a explorarem as melhores fontes conhecidas mais rapidamente.

**2. Fator de Abandono (*Limit*) - *Análogo à Inércia do PSO*:**

* **Limit Baixo (Teste 3):** Esgota as fontes rapidamente, forçando o recrutamento constante de abelhas escoteiras (busca global aleatória). Evita ótimos locais na Rastrigin.
* **Limit Alto (Teste 4):** Permite que as abelhas tentem melhorar a mesma solução centenas de vezes antes de desistir. Ideal para o vale profundo da Rosenbrock.

**3. Distribuição da Colônia - *Análogo a $c_1, c_2$ do PSO*:**

* **Maioria Operárias (Teste 5):** Privilegia a busca por múltiplas novas fontes simultâneas (equivalente a alto fator cognitivo $c_1$).
* **Maioria Observadoras (Teste 6):** Privilegia o refinamento das poucas fontes já descobertas (equivalente a alto fator social $c_2$).

---

## 5. Estrutura da Implementação (Pastas)

```text
abc_project/
├── baseline_tests/
│   ├── roleta_default.ipynb       (30 exec x 500 iter)
│   └── torneio_default.ipynb      (30 exec x 500 iter)
├── sensitivity_limit/
│   ├── low_limit.ipynb            (Limit=100)
│   └── high_limit.ipynb           (Limit=1500)
├── sensitivity_population/
│   ├── high_employees.ipynb       (80% Operárias)
│   └── high_onlookers.ipynb       (80% Observadoras)
└── final_stress/
    └── max_performance.ipynb      (Ex: Torneio, 2500 iter, param. vencedores)

```

---

## 6. Comportamento Esperado (Hipóteses)

* **Vulnerabilidade Dimensional:** Espera-se que o ABC (baseline) apresente dificuldades na função Rosenbrock em $30D$, dado que a mutação padrão altera apenas uma dimensão por vez. A mudança para **Torneio** deve mitigar parcialmente isso.
* **Estagnação vs. Divergência:** Na função Rastrigin, espera-se que o teste com *Limit* baixo apresente melhor capacidade de escapar dos ótimos locais do que o *Limit* padrão.

---

## 7. Escopo da Análise Estatística

### SIM (Alta Confiança)

* **Estatísticas Descritivas:** Média, desvio padrão, melhor e pior caso por configuração.
* **Curva de Convergência Média:** Trajetória com escala logarítmica para avaliar a velocidade em que as abelhas encontram o vale principal.
* **Boxplots Comparativos:** Avaliação da dispersão (robustez) entre as variações de parâmetros.

---

## 8. Critérios para o Teste de Estresse (Max Performance)

O Teste 7 (`max_performance`) combinará a melhor estratégia de seleção, o melhor limite de abandono e a melhor divisão da colônia identificados nas fases anteriores. Para compensar a característica de alteração uni-dimensional do ABC, o orçamento será elevado (ex: $2500$ iterações) para observar se o algoritmo alcança a precisão do PSO quando dado tempo computacional suficiente.