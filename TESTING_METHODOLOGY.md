# Metodologia de Testes: AGO com e sem Elitismo

## 1. Objetivo da Análise

Comparar o desempenho de um Algoritmo Genético (AG) com e sem implementação de elitismo para otimização da função Sphere em "n" dimensões, verificando se o elitismo melhora significativamente a convergência e o fitness final.

---

## 2. Hipótese

**H0 (Nula)**: O elitismo não afeta significativamente o desempenho do AG  
**H1 (Alternativa)**: O elitismo melhora a convergência e o fitness final do AG

---

## 3. Configuração dos Experimentos

### 3.1 Grupos de Teste

Apenas **2 variações por teste**:

| Grupo           | Descrição                                      |
| --------------- | ---------------------------------------------- |
| **Controle**    | AG sem elitismo (descarte de não-elite)        |
| **Experimento** | AG com elitismo (preserva melhores indivíduos) |

### 3.2 Testes e Configurações de Parâmetros

Executaremos **3 testes com diferentes números de dimensões**. Cada teste terá **2 variações** (sem elitismo e com elitismo) com **30 execuções cada**.

**Princípio de Controle Experimental**:

- **Variáveis REALMENTE FIXAS**: Taxa crossover, tipo cruzamento, tipo seleção (não mudam em nenhuma circunstância)
- **Variáveis ADAPTADAS SISTEMATICAMENTE**: População, gerações, mutação (ajustadas conforme a dimensionalidade seguindo recomendações da literatura)
- **Variáveis DE COMPARAÇÃO**: Dimensionalidade e elitismo (estas são as variáveis que queremos medir)

#### **TESTE 1: Baixa Dimensionalidade**

| Parâmetro                                | Valor          | Classificação                           |
| ---------------------------------------- | -------------- | --------------------------------------- |
| Número de dimensões (`quantidade_genes`) | **10**         | **VARIÁVEL DE COMPARAÇÃO**              |
| Tamanho da população (`n_pop`)           | 20             | Adaptado sistematicamente (2x dimensão) |
| Número de gerações (`n_geracoes`)        | 50             | Adaptado sistematicamente               |
| Taxa de crossover (`taxa_crossover`)     | 0.80           | **FIXA**                                |
| Taxa de mutação (`taxa_mutacao`)         | 0.05           | **FIXA**                                |
| Número de cortes (`n_cortes`)            | 1              | **FIXA** - Cruzamento 1-ponto           |
| Tipo de seleção (`selecao`)              | 'torneio'      | **FIXA** - Seleção por torneio          |
| Limites da variável                      | -100, 100      | Conforme especificação Sphere           |
| Seed (`random.seed`)                     | Varia por exec | Ver seção 3.4 (Reprodutibilidade)       |
| **Elitismo**                             | Sim/Não        | **VARIÁVEL DE COMPARAÇÃO**              |

**Justificativa de adaptações:**

- **População = 20**: Recomendação clássica é 2-10x o número de variáveis. Para 10D, usamos 2x.
- **Gerações = 50**: Suficiente para convergência em baixa dimensão.
- **Mutação = 0.05 (5%)**: Taxa padrão para manter diversidade em espaços pequenos.

---

#### **TESTE 2: Dimensionalidade Média**

| Parâmetro                                | Valor          | Classificação                            |
| ---------------------------------------- | -------------- | ---------------------------------------- |
| Número de dimensões (`quantidade_genes`) | **30**         | **VARIÁVEL DE COMPARAÇÃO**               |
| Tamanho da população (`n_pop`)           | 30             | Adaptado sistematicamente (≈1x dimensão) |
| Número de gerações (`n_geracoes`)        | 100            | Adaptado sistematicamente                |
| Taxa de crossover (`taxa_crossover`)     | 0.80           | **FIXA**                                 |
| Taxa de mutação (`taxa_mutacao`)         | 0.05           | **FIXA**                                 |
| Número de cortes (`n_cortes`)            | 1              | **FIXA** - Cruzamento 1-ponto            |
| Tipo de seleção (`selecao`)              | 'torneio'      | **FIXA** - Seleção por torneio           |
| Limites da variável                      | -100, 100      | Conforme especificação Sphere            |
| Seed (`random.seed`)                     | Varia por exec | Ver seção 3.4 (Reprodutibilidade)        |
| **Elitismo**                             | Sim/Não        | **VARIÁVEL DE COMPARAÇÃO**               |

**Justificativa de adaptações:**

- **População = 30**: Recomendação é 1-10x o número de variáveis. Para 30D, usamos 1x.
- **Gerações = 100**: Aumentado para permitir melhor exploração do espaço.
- **Mutação = 0.05 (5%)**: Mantém a mesma taxa de diversidade.

---

#### **TESTE 3: Alta Dimensionalidade**

| Parâmetro                                | Valor          | Classificação                               |
| ---------------------------------------- | -------------- | ------------------------------------------- |
| Número de dimensões (`quantidade_genes`) | **50**         | **VARIÁVEL DE COMPARAÇÃO**                  |
| Tamanho da população (`n_pop`)           | 50             | Adaptado sistematicamente (1x dimensão)     |
| Número de gerações (`n_geracoes`)        | 150            | Adaptado sistematicamente                   |
| Taxa de crossover (`taxa_crossover`)     | 0.80           | **FIXA**                                    |
| Taxa de mutação (`taxa_mutacao`)         | 0.10           | Aumentada para manter diversidade em alta D |
| Número de cortes (`n_cortes`)            | 1              | **FIXA** - Cruzamento 1-ponto               |
| Tipo de seleção (`selecao`)              | 'torneio'      | **FIXA** - Seleção por torneio              |
| Limites da variável                      | -100, 100      | Conforme especificação Sphere               |
| Seed (`random.seed`)                     | Varia por exec | Ver seção 3.4 (Reprodutibilidade)           |
| **Elitismo**                             | Sim/Não        | **VARIÁVEL DE COMPARAÇÃO**                  |

**Justificativa de adaptações:**

- **População = 50**: Necessário maior população em espaço grande para exploração.
- **Gerações = 150**: Muito mais tempo para explorar e convergir em 50D.
- **Mutação = 0.10 (10%)**: AUMENTADA para manter diversidade e evitar convergência prematura. Recomendado em AGs para espaços complexos.

### 3.3 Implementação do Elitismo

**Sem elitismo (Controle)**:

- Usa os `n_pop` melhores filhos de `2 * n_pop` gerados
- Não garante preservação dos melhores indivíduos da geração anterior

**Com elitismo (Experimento)**:

- Preserva os `k` melhores indivíduos da geração anterior
- Recomendação: `k = 10% da população`
  - Teste 1: k = 2 (10% de 20)
  - Teste 2: k = 3 (10% de 30)
  - Teste 3: k = 5 (10% de 50)
- Substitui os `k` piores filhos gerados pelos `k` melhores da geração anterior

### 3.4 Reprodutibilidade e Seed

**Estratégia de Seed:**
Para garantir **reprodutibilidade** dos resultados, cada execução usará um seed baseado no seu ID:

```python
execution_id = 1  # a 30
seed_value = 1000 + execution_id
random.seed(seed_value)
np.random.seed(seed_value)
```

**Benefícios:**

- ✓ Cada execução produz sempre os mesmos resultados (reproduzível)
- ✓ Execuções diferentes produzem valores diferentes (variabilidade capturada)
- ✓ Facilita debug e verificação de resultados

**Implementação nos Notebooks:**
No início de cada execução, adicione:

```python
import random
import numpy as np

execution_id = 1  # incrementar para cada execução
random.seed(1000 + execution_id)
np.random.seed(1000 + execution_id)
```

### 3.5 Justificativa das Adaptações Sistemáticas

Os valores adaptados (população, gerações, mutação) não são arbitrários. Seguem recomendações clássicas:

**População:**

- Literatura recomenda: 2-10x o número de variáveis (genes)
- Teste 1 (10D): pop=20 (2x)
- Teste 2 (30D): pop=30 (1x)
- Teste 3 (50D): pop=50 (1x)

**Gerações:**

- Aumentam conforme a dimensionalidade para permitir exploração mais completa do espaço
- Teste 1: 50 gerações
- Teste 2: 100 gerações
- Teste 3: 150 gerações

**Taxa de Mutação:**

- Para alta dimensionalidade, aumenta para manter diversidade genética
- Teste 1-2: 0.05 (5%)
- Teste 3: 0.10 (10%)

**O que NÃO muda NUNCA:**

- Taxa de crossover: 0.80
- Tipo de cruzamento: 1-ponto
- Tipo de seleção: torneio

---

## 4. Plano de Execução

### 4.1 Estrutura de Diretórios

```
comp-inteligente/
├── tests/
│   ├── test_1_10d/
│   │   ├── sem_elitismo.ipynb
│   │   └── com_elitismo.ipynb
│   ├── test_2_30d/
│   │   ├── sem_elitismo.ipynb
│   │   └── com_elitismo.ipynb
│   └── test_3_50d/
│       ├── sem_elitismo.ipynb
│       └── com_elitismo.ipynb
├── experiments/
│   ├── results/
│   │   ├── test_1_10d/
│   │   │   ├── sem_elitismo_results.csv
│   │   │   ├── com_elitismo_results.csv
│   │   │   └── consolidated_results.csv
│   │   ├── test_2_30d/
│   │   │   ├── sem_elitismo_results.csv
│   │   │   ├── com_elitismo_results.csv
│   │   │   └── consolidated_results.csv
│   │   └── test_3_50d/
│   │       ├── sem_elitismo_results.csv
│   │       ├── com_elitismo_results.csv
│   │       └── consolidated_results.csv
│   └── plots/
│       ├── convergence_test_1.png
│       ├── convergence_test_2.png
│       ├── convergence_test_3.png
│       └── comparison_all_tests.png
├── scripts/
│   ├── run_experiments.py
│   ├── generate_report.py
│   └── README.md
├── TESTING_METHODOLOGY.md (este arquivo)
├── ago_fase1.ipynb (original)
└── README.md
```

### 4.2 Resumo de Execuções

| Teste     | Dimensões | Pop | Ger | Mut  | Config 1 (30 exec) | Config 2 (30 exec) | Ger por Config | Total Ger por Teste |
| --------- | --------- | --- | --- | ---- | ------------------ | ------------------ | -------------- | ------------------- |
| 1         | 10        | 20  | 50  | 0.05 | sem_elit           | com_elit           | 1.500          | **3.000**           |
| 2         | 30        | 30  | 100 | 0.05 | sem_elit           | com_elit           | 3.000          | **6.000**           |
| 3         | 50        | 50  | 150 | 0.10 | sem_elit           | com_elit           | 4.500          | **9.000**           |
| **TOTAL** | -         | -   | -   | -    | -                  | -                  | -              | **18.000 gerações** |

**Detalhamento:**

- 30 execuções × 2 configurações × 3 testes = **180 execuções totais**
- Teste 1: 30 (sem) + 30 (com) = 60 exec × 50 ger = 3.000 ger
- Teste 2: 30 (sem) + 30 (com) = 60 exec × 100 ger = 6.000 ger
- Teste 3: 30 (sem) + 30 (com) = 60 exec × 150 ger = 9.000 ger

---

## 5. Passo a Passo para Executar

### Fase 1: Preparação

- [ ] Revisar esta documentação (TESTING_METHODOLOGY.md)
- [ ] Preencher os 6 notebooks com código do AG
  - Baseados em `ago_fase1.ipynb`
  - Adaptar parâmetros conforme tabelas acima
  - Implementar seed (seção 3.4)
  - Implementar elitismo apenas em `com_elitismo.ipynb`
  - Salvar resultados em CSV no final de cada notebook
- [ ] Testar 1 execução de cada notebook manualmente

### Fase 2: Execução

```bash
cd scripts
python run_experiments.py
```

- Tempo estimado: **10-20 horas** (máquina dependente)
- Script executa 180 rodadas do AG em sequência
- Salva CSVs automaticamente

### Fase 3: Análise

```bash
python generate_report.py
```

- Gera 4 gráficos PNG
- Calcula estatísticas
- Cria `ANALYSIS.csv`
- Imprime resumo no console

### Fase 4: Documentação

- [ ] Documentar resultados em README.md
- [ ] Subir código e notebooks no GitHub
- [ ] Escrever seções do artigo (Metodologia + Resultados)

---

## 6. Formato Esperado dos CSVs

### Arquivo Individual: `sem_elitismo_results.csv`

```csv
execution_id,generation,best_fitness,avg_fitness,std_fitness
1,1,1245.32,1502.15,127.43
1,2,1001.28,1312.54,98.32
...
1,50,12.45,34.21,5.12
2,1,1876.23,2102.54,156.23
...
30,50,15.67,42.31,7.54
```

### Arquivo Consolidado: `consolidated_results.csv`

```csv
configuration,execution_id,generation,best_fitness,avg_fitness,std_fitness
sem_elitismo,1,1,1245.32,1502.15,127.43
sem_elitismo,1,2,1001.28,1312.54,98.32
...
com_elitismo,1,1,1200.00,1450.00,120.00
com_elitismo,1,2,900.00,1250.00,95.00
...
```

### Arquivo de Análise: `ANALYSIS.csv`

```csv
test,dimensions,configuration,avg_final_fitness,std_final_fitness,avg_convergence_gen,std_convergence_gen
test_1,10,sem_elitismo,3.21,0.89,22,3.4
test_1,10,com_elitismo,1.89,0.42,12,1.8
test_2,30,sem_elitismo,12.12,3.21,45,5.2
test_2,30,com_elitismo,5.23,1.87,28,3.5
test_3,50,sem_elitismo,67.89,18.76,95,12.3
test_3,50,com_elitismo,28.54,9.23,58,8.7
```

---

## 7. Observações Importantes

- **Tempo**: Cada notebook pode levar alguns minutos. Não interrompa durante execução.
- **Reprodutibilidade**: Com seed definido, resultados são reproduzíveis.
- **Variabilidade**: Mesmo com seed, há variação entre as 30 execuções (é esperado).
- **Outliers**: Algumas execuções podem ser muito piores/melhores (descarte apenas se houver erro).

---

**Versão**: 2.0 (Refatorada - 6 notebooks + 2 scripts)  
**Data**: 2026-04-10  
**Status**: ✅ Documentação, estrutura e scripts completos
