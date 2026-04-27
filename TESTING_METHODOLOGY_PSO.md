# Metodologia de Testes: PSO (Particle Swarm Optimization)

## 1. Objetivo
Avaliar o desempenho do PSO variando sistematicamente **Inércia** e **Topologia** em problemas de $30D$. O foco é definir a arquitetura campeã para realizar os testes de sensibilidade de coeficientes ($c_1, c_2$) e estresse de convergência.

---

## 2. Status Executivo 

| Métrica | Valor | Status |
| :--- | :--- | :--- |
| Notebooks executados | 7/7 | ✅ Concluído |
| Replicatas por config | 30 | ✅ Concluído |
| Configuração Vencedora | `linear_global` | 🏆 (Fase 1) |

**Melhores Resultados Finais (Baseline - Médias):**
* **Sphere:** $5492.45$ (`linear_global`)
* **Rastrigin:** $231.87$ (`constant_global`)
* **Rosenbrock:** $971264.59$ (`linear_global`)

---

## 3. Design Experimental

### 3.1 Variáveis Controladas
**Fixas (todas as configurações):**
* **Dimensões:** $30$
* **População Base:** $30$
* **Iterações Base:** $20$
* **Seeds:** $42-71$ (Pareamento perfeito para isolamento de variáveis)

**Matriz de Testes:**

| Teste | Inércia ($\omega$) | Topologia | $c_1$ | $c_2$ | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Linear** | **Global** | $2.05$ | $2.05$ | ✅ Vencedor |
| **2** | **Linear** | **Local** | $2.05$ | $2.05$ | ✅ Concluído |
| **3** | **Constante** | **Global** | $2.05$ | $2.05$ | ✅ Concluído |
| **4** | **Constante** | **Local** | $2.05$ | $2.05$ | ✅ Concluído |
| **5** | Linear | Global | **$2.80$** | **$1.30$** | ✅ Concluído |
| **6** | Linear | Global | **$1.30$** | **$2.80$** | ✅ Concluído |
| **7** | Linear | Global | $2.05$ | $2.05$ | ✅ Concluído |

### 3.2 Implementação Técnica
**Cada notebook executa o seguinte protocolo:**
```python
for execucao in range(30):
    seed_atual = 42 + execucao
    random.seed(seed_atual)
    np.random.seed(seed_atual)
    # Execução do enxame com T=20 ou T=500
    # Coleta de gBest_fitness ao final de cada iteração
```
**Isolamento de Efeito:** O pareamento garante que a execução $N$ do teste 1 comece com as mesmas posições iniciais da execução $N$ do teste 2, garantindo que a diferença de performance venha apenas da **topologia** ou **inércia**.

---

## 4. Justificativa da Transição de Fase (Testes 5 e 6)

**Critério de Seleção:**
A configuração **Linear Global** foi selecionada como base devido à sua superioridade estatística na fase inicial:
* **Superioridade em Rosenbrock:** Redução de aproximadamente $56\%$ no custo em comparação à inércia constante.
* **Velocidade de Comunicação:** A topologia Global mostrou-se necessária para o orçamento limitado de $20$ iterações.



**Objetivos da Sensibilidade:**
1.  **Teste 5 (Cognitivo):** Verificar se um $c_1 > c_2$ favorece a exploração individual e evita a estagnação precoce.
2.  **Teste 6 (Social):** Verificar se um $c_2 > c_1$ acelera a convergência em direção ao líder, sacrificando a diversidade.

---

## 5. Estrutura da Implementação (Pastas)
```text
pso_project/
├── baseline_tests/
│   ├── linear_global.ipynb    (30 exec x 20 iter)
│   ├── linear_local.ipynb     (30 exec x 20 iter)
│   ├── constant_global.ipynb  (30 exec x 20 iter)
│   └── constant_local.ipynb   (30 exec x 20 iter)
├── sensitivity_analysis/
│   ├── high_cognitive.ipynb   (c1=2.8, c2=1.3)
│   └── high_social.ipynb      (c1=1.3, c2=2.8)
└── final_stress/
    └── max_performance.ipynb  (100 pop, 500 iter)
```

---

## 6. Análise de Comportamento Observada

### 6.1 Efeito da Topologia
Os dados confirmam que a topologia **Global** é superior em cenários de baixo custo computacional ($T=20$). A topologia **Local** gerou custos quase dobrados (ex: Sphere $10.110$ vs $5.492$), pois as partículas levam mais tempo para propagar a melhor solução através da vizinhança.

### 6.2 Efeito da Inércia
O decaimento **Linear** de $\omega$ mostrou-se fundamental para a função *Rosenbrock*. Ao reduzir a velocidade das partículas ao longo do tempo, o algoritmo permitiu um "ajuste fino" dentro do vale estreito da função, superando a inércia constante em desempenho absoluto.

---

## 7. Escopo da Análise Estatística

### SIM (Alta Confiança)
* **Estatísticas Descritivas:** Média, desvio padrão, melhor e pior caso.
* **Convergência:** Trajetória média com bandas de variabilidade ($1\sigma$).
* **Robustez:** Comparação via boxplots da dispersão dos 30 resultados finais.

### COM RESSALVA
* **Conclusões sobre o Ótimo:** Com apenas $20$ iterações nas fases iniciais, os resultados indicam tendência de busca, mas não atingem o mínimo global absoluto.

---

## 8. Observações Técnicas Finais (Resultados Consolidados)

Após a execução de todos os notebooks planejados, as seguintes conclusões foram extraídas:

* **Exploração vs. Convergência ($c_1, c_2$):** O teste **High Cognitive ($c_1=2.8, c_2=1.3$)** apresentou resultados significativamente melhores nas funções Sphere ($2.171$) e Rastrigin ($202$) do que o modelo High Social. Isso demonstra que, em orçamentos de iteração curtos, permitir que as partículas confiem mais em sua própria experiência evita que o enxame colapse prematuramente em um líder sub-ótimo.
* **Aceleração Social na Rosenbrock:** Curiosamente, o teste **High Social** superou o High Cognitive especificamente na função Rosenbrock ($1.08 \times 10^6$ vs $1.20 \times 10^6$), embora o baseline equilibrado ($2.05, 2.05$) tenha permanecido superior ($9.71 \times 10^5$).
* **Impacto da Escala (Max Performance):** A transição para o Teste 7 (100 indivíduos e 500 iterações) validou a eficácia da arquitetura `linear_global`. Houve uma redução drástica nos erros residuais:
    * **Sphere:** Caiu de $5.492$ (Baseline) para **$0.59$**.
    * **Rosenbrock:** Caiu de $971.264$ (Baseline) para **$266.43$**.
    * **Rastrigin:** Caiu de $231$ (Baseline) para **$46.34$**.


**Conclusão Final:** O PSO demonstra uma dependência crítica do equilíbrio entre os coeficientes de aceleração e o orçamento de iterações. Enquanto a configuração **Linear Global** é a arquitetura mais robusta, o ajuste para um viés cognitivo mais alto favorece a exploração inicial em problemas de alta dimensionalidade ($30D$).