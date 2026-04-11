#!/usr/bin/env python3
"""
Script para gerar relatórios, gráficos e análise estatística dos resultados.

Uso:
    python generate_report.py

O script vai:
1. Ler os CSVs consolidados de cada teste
2. Calcular estatísticas (média, desvio padrão, convergência)
3. Gerar gráficos de convergência por teste
4. Gerar gráfico comparativo de todos os testes
5. Gerar arquivo ANALYSIS.csv com resumo consolidado
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import pandas as pd

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

WORKSPACE_ROOT = Path(__file__).parent.parent  # comp-inteligente/
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results"
PLOTS_DIR = WORKSPACE_ROOT / "experiments" / "plots"

TESTS = ["test_1_10d", "test_2_30d", "test_3_50d"]
CONFIGS = ["original", "sem_elitismo", "com_elitismo"]


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def log(message, level="INFO"):
    """Imprime mensagem com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def read_consolidated_csv(test_name):
    """Lê arquivo consolidado de um teste"""
    filepath = RESULTS_DIR / test_name / "consolidated_results.csv"
    
    if not filepath.exists():
        log(f"Arquivo não encontrado: {filepath}", "WARNING")
        return None
    
    df = pd.read_csv(filepath)
    return df


def calculate_statistics(test_name, df):
    """
    Calcula estatísticas por configuração para um teste.
    
    Retorna dict com:
    - avg_final_fitness: média do fitness na última geração
    - std_final_fitness: desvio padrão
    - avg_convergence_gen: geração média de convergência (primeira com melhor fitness)
    """
    stats = {}
    
    for config in CONFIGS:
        config_data = df[df['configuration'] == config]
        
        if config_data.empty:
            log(f"Nenhum dado para {test_name}/{config}", "WARNING")
            continue
        
        # Agrupar por execution_id e pegar último generation (fitness final)
        final_fitness = []
        convergence_gens = []
        
        for exec_id in config_data['execution_id'].unique():
            exec_data = config_data[config_data['execution_id'] == exec_id]
            last_row = exec_data.iloc[-1]  # Última geração
            final_fitness.append(last_row['best_fitness'])
            
            # Encontrar geração de convergência (primeira vez que atinge best_fitness)
            best_overall = exec_data['best_fitness'].min()
            conv_gen = exec_data[exec_data['best_fitness'] == best_overall].iloc[0]['generation']
            convergence_gens.append(conv_gen)
        
        stats[config] = {
            'avg_final_fitness': np.mean(final_fitness),
            'std_final_fitness': np.std(final_fitness),
            'avg_convergence_gen': np.mean(convergence_gens),
            'std_convergence_gen': np.std(convergence_gens),
        }
    
    return stats


def plot_test_convergence(test_name, df):
    """
    Gera gráfico de convergência para um teste.
    Mostra as 3 configurações com intervalo de confiança.
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = {
        'original': '#1f77b4',
        'sem_elitismo': '#ff7f0e',
        'com_elitismo': '#2ca02c'
    }
    
    for config in CONFIGS:
        config_data = df[df['configuration'] == config]
        
        if config_data.empty:
            continue
        
        # Agrupar por geração
        gen_groups = config_data.groupby('generation')
        
        gens = []
        means = []
        stds = []
        
        for gen, group in gen_groups:
            gens.append(gen)
            means.append(group['best_fitness'].mean())
            stds.append(group['best_fitness'].std())
        
        gens = np.array(gens)
        means = np.array(means)
        stds = np.array(stds)
        
        # Plot
        ax.plot(gens, means, label=config, color=colors[config], linewidth=2, marker='o', markersize=4)
        ax.fill_between(gens, means - stds, means + stds, alpha=0.2, color=colors[config])
    
    ax.set_xlabel('Geração', fontsize=12)
    ax.set_ylabel('Fitness (Melhor)', fontsize=12)
    ax.set_title(f'Convergência - {test_name.upper()}', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)
    
    # Salvar
    output_file = PLOTS_DIR / f"{test_name}_convergence.png"
    plt.tight_layout()
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    
    log(f"✓ Gráfico salvo: {output_file}")


def plot_comparison_all_tests():
    """
    Gera gráfico comparativo dos 3 testes.
    Subplots lado a lado mostrando o efeito de dimensionalidade.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    colors = {
        'original': '#1f77b4',
        'sem_elitismo': '#ff7f0e',
        'com_elitismo': '#2ca02c'
    }
    
    test_configs = [
        ("test_1_10d", "10 Dimensões"),
        ("test_2_30d", "30 Dimensões"),
        ("test_3_50d", "50 Dimensões"),
    ]
    
    for ax, (test_name, test_label) in zip(axes, test_configs):
        df = read_consolidated_csv(test_name)
        
        if df is None:
            ax.text(0.5, 0.5, f'{test_name}\nNão encontrado', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(test_label, fontsize=12, fontweight='bold')
            continue
        
        for config in CONFIGS:
            config_data = df[df['configuration'] == config]
            
            if config_data.empty:
                continue
            
            gen_groups = config_data.groupby('generation')
            gens = []
            means = []
            stds = []
            
            for gen, group in gen_groups:
                gens.append(gen)
                means.append(group['best_fitness'].mean())
                stds.append(group['best_fitness'].std())
            
            gens = np.array(gens)
            means = np.array(means)
            stds = np.array(stds)
            
            ax.plot(gens, means, label=config, color=colors[config], linewidth=2, marker='o', markersize=4)
            ax.fill_between(gens, means - stds, means + stds, alpha=0.2, color=colors[config])
        
        ax.set_xlabel('Geração', fontsize=11)
        ax.set_ylabel('Fitness (Melhor)', fontsize=11)
        ax.set_title(test_label, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)
    
    axes[0].legend(fontsize=10, loc='best')
    
    plt.suptitle('Comparação de Convergência - Efeito de Dimensionalidade', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    output_file = PLOTS_DIR / "comparison_all_tests.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    
    log(f"✓ Gráfico comparativo salvo: {output_file}")


def generate_analysis_csv():
    """
    Gera arquivo ANALYSIS.csv consolidando estatísticas de todos os testes.
    """
    analysis_data = []
    
    for test_name in TESTS:
        df = read_consolidated_csv(test_name)
        
        if df is None:
            continue
        
        stats = calculate_statistics(test_name, df)
        
        # Extrair número de dimensões do nome do teste
        dims_map = {"test_1_10d": 10, "test_2_30d": 30, "test_3_50d": 50}
        dimensions = dims_map.get(test_name, 0)
        
        for config, config_stats in stats.items():
            analysis_data.append({
                'test': test_name,
                'dimensions': dimensions,
                'configuration': config,
                'avg_final_fitness': round(config_stats['avg_final_fitness'], 4),
                'std_final_fitness': round(config_stats['std_final_fitness'], 4),
                'avg_convergence_gen': round(config_stats['avg_convergence_gen'], 2),
                'std_convergence_gen': round(config_stats['std_convergence_gen'], 2),
            })
    
    # Salvar ANALYSIS.csv
    analysis_file = RESULTS_DIR / "ANALYSIS.csv"
    
    if analysis_data:
        fieldnames = [
            'test', 'dimensions', 'configuration', 
            'avg_final_fitness', 'std_final_fitness',
            'avg_convergence_gen', 'std_convergence_gen'
        ]
        
        with open(analysis_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(analysis_data)
        
        log(f"✓ Arquivo ANALYSIS.csv criado: {analysis_file}")
        return True
    else:
        log("✗ Nenhum dado para gerar ANALYSIS.csv", "ERROR")
        return False


def print_statistics_summary():
    """Imprime resumo das estatísticas no console"""
    log("\n" + "=" * 90)
    log("RESUMO DAS ESTATÍSTICAS", "INFO")
    log("=" * 90 + "\n")
    
    for test_name in TESTS:
        df = read_consolidated_csv(test_name)
        
        if df is None:
            continue
        
        print(f"\n{test_name.upper()}")
        print("-" * 90)
        
        stats = calculate_statistics(test_name, df)
        
        for config, config_stats in sorted(stats.items()):
            print(f"\n  {config.upper()}:")
            print(f"    Fitness Final Médio:        {config_stats['avg_final_fitness']:.4f} ± {config_stats['std_final_fitness']:.4f}")
            print(f"    Geração de Convergência:    {config_stats['avg_convergence_gen']:.0f} ± {config_stats['std_convergence_gen']:.0f}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Função principal"""
    log("=" * 90)
    log("GERADOR DE RELATÓRIOS E GRÁFICOS", "INFO")
    log("=" * 90 + "\n")
    
    # 1. Verificar diretórios
    if not RESULTS_DIR.exists():
        log(f"Diretório de resultados não encontrado: {RESULTS_DIR}", "ERROR")
        return 1
    
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Gerar gráficos por teste
    log("Gerando gráficos de convergência...\n")
    for test_name in TESTS:
        df = read_consolidated_csv(test_name)
        if df is not None:
            plot_test_convergence(test_name, df)
    
    # 3. Gerar gráfico comparativo
    log("\nGerando gráfico comparativo...")
    plot_comparison_all_tests()
    
    # 4. Gerar ANALYSIS.csv
    log("\nGerando análise consolidada...")
    generate_analysis_csv()
    
    # 5. Imprimir resumo
    print_statistics_summary()
    
    log("\n" + "=" * 90)
    log("✓ RELATÓRIOS GERADOS COM SUCESSO!", "INFO")
    log("=" * 90 + "\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
