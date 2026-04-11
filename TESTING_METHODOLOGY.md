# Metodologia de Testes: AG com e sem Elitismo

## 1. Objetivo

Comparar AG com e sem elitismo para otimização da função Sphere em 10D, 30D e 50D, verificando se elitismo melhora significativamente convergência e fitness final.

**H0:** Elitismo não afeta desempenho  
**H1:** Elitismo melhora convergência e fitness final

---

## 2. Status Executivo - ✅ CONCLUÍDO

| Métrica                | Valor  | Status          |
| ---------------------- | ------ | --------------- |
| Notebooks executados   | 6/6    | ✅              |
| Replicatas por config  | 30     | ✅              |
| Seeds utilizados       | 42-71  | ✅ Incrementais |
| Total de rodadas       | 180    | ✅              |
| Total de gerações      | 18.000 | ✅              |
| Gráficos gerados       | 12 PNG | ✅              |
| Aderência metodológica | 100%   | ✅              |

**Dados coletados em cada notebook:**

- `historico_melhor_all`: 30 trajetórias de convergência
- `melhor_fitness_por_exec`: 30 valores finais por config
- Estatísticas automáticas: min, max, média, desvio, mediana

---

## 3. Design Experimental

### 3.1 Variáveis Controladas

**Fixas (todas as configurações):**

- Taxa crossover: 0.80
- Tipo cruzamento: 1-ponto
- Tipo seleção: torneio
- Limites função: [-100, 100]
- Seeds: 42-71 (30 variados, incrementais)

**De Comparação (variam entre configs):**

- Dimensionalidade (10D, 30D, 50D)
- Elitismo (sim/não)

**Adaptadas por dimensionalidade** (conforme literatura: pop = 1-2x dimensões):

| Teste | Dimensões | Pop | Gerações | Mutação | k-elite |
| ----- | --------- | --- | -------- | ------- | ------- |
| 1     | 10D       | 20  | 50       | 0.05    | 2       |
| 2     | 30D       | 30  | 100      | 0.05    | 3       |
| 3     | 50D       | 50  | 150      | 0.10    | 5       |

_Mutação aumenta em 50D para manter diversidade em espaço complexo_

### 3.2 Implementação

**Cada notebook executa:**

```python
for execucao in range(30):
    seed_atual = 42 + execucao  # Seeds: 42, 43, ..., 71
    random.seed(seed_atual)
    np.random.seed(seed_atual)
    # Rodar 50/100/150 gerações
    # Coletar históricos
```

**Comparação pareada:** Sem e com elitismo usam EXATAMENTE os mesmos 30 seeds na mesma ordem → isolamento perfeito do efeito de elitismo.

**Sem elitismo:** Seleciona os `n_pop` melhores de `2*n_pop` filhos  
**Com elitismo:** Preserva `k` (2/3/5) melhores da geração anterior, substitui os piores filhos

---

## 4. Estrutura da Implementação

```
tests/
├── test_1_10d/
│   ├── sem_elitismo.ipynb  ✅ 30 exec × 50 ger = 1.500 ger
│   └── com_elitismo.ipynb  ✅ 30 exec × 50 ger = 1.500 ger
├── test_2_30d/
│   ├── sem_elitismo.ipynb  ✅ 30 exec × 100 ger = 3.000 ger
│   └── com_elitismo.ipynb  ✅ 30 exec × 100 ger = 3.000 ger
└── test_3_50d/
    ├── sem_elitismo.ipynb  ✅ 30 exec × 150 ger = 4.500 ger
    └── com_elitismo.ipynb  ✅ 30 exec × 150 ger = 4.500 ger
```

**Total:** 180 execuções × 18.000 gerações

---

## 5. Dados Coletados

Cada notebook armazena em memória:

```python
historico_melhor_all[30][gerações]      # Melhor por geração
melhor_fitness_por_exec[30]             # Melhor final de cada exec
historico_notas_all[30][gerações][pop]  # Fitness populacional

# Impressos automaticamente:
# min, max, média ± desvio, mediana
```

Uso: `melhor_fitness_por_exec` contém os 30 valores para descrição e comparação pareada.

---

## 6. Visualizações

Cada notebook gera **2 subplots**:

**Subplot 1 - Convergência:**

- Linha azul: Melhor médio das 30 execuções
- Banda azul (±1σ): Variabilidade entre execuções
- Eixos: Geração vs Fitness (menor = melhor)

**Subplot 2 - Boxplot:**

- Distribuição dos 30 fitness finais
- Mediana, quartis, min, max, outliers

**Total:** 12 PNG (6 notebooks × 2 subplots)

---

## 7. Análises Possíveis

### ✅ SIM (Com Alta Confiança)

- **Estatísticas descritivas** (média, desvio, mediana, min, max)
- **Convergência estatística** (trajetória ± banda de desvio)
- **Comparação pareada** (deltas entre configs por execução)
- **Variabilidade** (boxplots, amplitude, coef. variação)
- **Padrões visuais** (convergência vs dimensionalidade)

### ⚠️ COM RESSALVA (N=30 é borderline)

- **T-test pareado:** Possível mas requer validação de normalidade
- **Intervalos de confiança:** Possível mas usar como indicador, não limite rigoroso
- **Testes formais:** Usar como suporte descritivo, não conclusão definitiva

### ❌ Impossível

- **Generalizar para outros seeds:** Dados limitados a 42-71
- **Conclusão científica formal:** Requereria mais rigor estatístico
- **Exportação consolidada:** Dados em memória, não em CSV

---

## 8. Isolamento de Efeitos - Controle Experimental

**Pairing perfeito:**

- Execução N de "com elitismo" com seed=42+N
- Execução N de "sem elitismo" com seed=42+N
- Mesma população inicial, mesma sequência aleatória
- Única diferença: **elitismo**

**Vantagem:** Comparação rigorosa sem confundimento de fatores

**Força estatística vs N=1:**

- 30x mais dados
- Estatísticas confiáveis (média, desvio)
- Análise de robustez possível
- Boxplots mostram dispersão real

---

## 9. Status Final e Recomendações

### ✅ O que foi alcançado

- ✅ 100% de aderência ao plano metodológico
- ✅ 30 replicatas por configuração (robusto)
- ✅ Variabilidade capturada (30 seeds variados)
- ✅ Isolamento completo do efeito de elitismo
- ✅ 18.000 gerações processadas
- ✅ 12 gráficos com bandas de confiança
- ✅ Reprodutibilidade 100% (determinístico)

---

**Versão:** 7.0  
**Data:** 2026-04-11  
**Status:** Documentação refatorada
