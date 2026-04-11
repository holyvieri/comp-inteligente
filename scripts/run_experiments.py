#!/usr/bin/env python3
"""
Script para executar automaticamente todos os 9 notebooks (3 testes × 3 configurações)
e coletar os resultados em CSVs.

Uso:
    python run_experiments.py

O script vai procurar por notebooks no diretório tests/ e executá-los em sequência.
Cada notebook deve salvar seus resultados em experiments/results/{test_name}/{config_name}_results.csv
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

WORKSPACE_ROOT = Path(__file__).parent.parent  # comp-inteligente/
TESTS_DIR = WORKSPACE_ROOT / "tests"
RESULTS_DIR = WORKSPACE_ROOT / "experiments" / "results"

# Estrutura de testes: (test_folder, config_name)
NOTEBOOKS_TO_RUN = [
    ("test_1_10d", "original"),
    ("test_1_10d", "sem_elitismo"),
    ("test_1_10d", "com_elitismo"),
    ("test_2_30d", "original"),
    ("test_2_30d", "sem_elitismo"),
    ("test_2_30d", "com_elitismo"),
    ("test_3_50d", "original"),
    ("test_3_50d", "sem_elitismo"),
    ("test_3_50d", "com_elitismo"),
]


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def log(message, level="INFO"):
    """Imprime mensagem com timestamp e nível"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def check_prerequisites():
    """Verifica se as dependências estão instaladas"""
    log("Verificando dependências...")
    required_packages = ["nbconvert", "jupyter", "numpy", "matplotlib"]
    
    try:
        import nbconvert
        import jupyter
        import numpy
        import matplotlib
        log("✓ Todas as dependências encontradas")
        return True
    except ImportError as e:
        log(f"✗ Falta pacote: {e}", "ERROR")
        log("Instale com: pip install nbconvert jupyter numpy matplotlib", "ERROR")
        return False


def notebook_exists(test_name, config_name):
    """Verifica se o notebook existe"""
    notebook_path = TESTS_DIR / test_name / f"{config_name}.ipynb"
    return notebook_path.exists()


def run_notebook(test_name, config_name):
    """
    Executa um notebook usando nbconvert com jupyter.
    
    Converte e executa o notebook no lugar, salvando a saída.
    """
    notebook_path = TESTS_DIR / test_name / f"{config_name}.ipynb"
    
    if not notebook_exists(test_name, config_name):
        log(f"Notebook não encontrado: {notebook_path}", "ERROR")
        return False
    
    try:
        log(f"Executando {test_name}/{config_name}...")
        
        # Comando para executar notebook com nbconvert
        cmd = [
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=3600",  # 1 hora timeout
            str(notebook_path)
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            log(f"✓ {test_name}/{config_name} concluído em {elapsed:.1f}s")
            return True
        else:
            log(f"✗ Erro ao executar {test_name}/{config_name}", "ERROR")
            log(f"STDERR: {result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        log(f"✗ Exceção ao executar notebook: {e}", "ERROR")
        return False


def verify_results(test_name, config_name):
    """Verifica se o CSV de resultados foi criado"""
    result_file = RESULTS_DIR / test_name / f"{config_name}_results.csv"
    
    if result_file.exists():
        file_size = result_file.stat().st_size
        log(f"✓ Arquivo de resultados criado: {result_file} ({file_size} bytes)")
        return True
    else:
        log(f"✗ Arquivo de resultados NÃO foi criado: {result_file}", "ERROR")
        return False


def consolidate_results(test_name):
    """
    Consolida os 3 CSVs de uma teste em um único arquivo consolidado.
    Adiciona coluna 'configuration' para identificar qual versão.
    """
    import csv
    
    configs = ["original", "sem_elitismo", "com_elitismo"]
    consolidated_data = []
    
    for config in configs:
        result_file = RESULTS_DIR / test_name / f"{config}_results.csv"
        
        if not result_file.exists():
            log(f"Arquivo não encontrado: {result_file}", "WARNING")
            continue
        
        with open(result_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['configuration'] = config
                consolidated_data.append(row)
    
    # Salvar consolidado
    consolidated_file = RESULTS_DIR / test_name / "consolidated_results.csv"
    
    if consolidated_data:
        fieldnames = ['configuration', 'execution_id', 'generation', 'best_fitness', 'avg_fitness', 'std_fitness']
        with open(consolidated_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(consolidated_data)
        
        log(f"✓ Arquivo consolidado criado: {consolidated_file}")
        return True
    else:
        log(f"✗ Nenhum dado para consolidar em {test_name}", "ERROR")
        return False


def print_summary(results_summary):
    """Imprime resumo final da execução"""
    log("\n" + "=" * 80)
    log("RESUMO FINAL DA EXECUÇÃO", "INFO")
    log("=" * 80)
    
    total = len(results_summary)
    successful = sum(1 for r in results_summary.values() if r)
    failed = total - successful
    
    print("\nDetalhes:")
    for (test_name, config_name), success in results_summary.items():
        status = "✓ OK" if success else "✗ FALHOU"
        print(f"  {status} | {test_name}/{config_name}")
    
    log(f"\nTotal: {total} | Sucesso: {successful} | Falha: {failed}")
    
    if failed == 0:
        log("✓ TODAS AS EXECUÇÕES COMPLETADAS COM SUCESSO!", "INFO")
    else:
        log(f"✗ {failed} execução(ões) falharam. Verifique os logs acima.", "ERROR")
    
    log("=" * 80 + "\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Função principal"""
    log("=" * 80)
    log("EXECUTOR DE EXPERIMENTOS - AGO COM/SEM ELITISMO", "INFO")
    log("=" * 80 + "\n")
    
    # 1. Verificar dependências
    if not check_prerequisites():
        log("Aborting due to missing dependencies.", "ERROR")
        return 1
    
    # 2. Verificar estrutura de diretórios
    if not TESTS_DIR.exists():
        log(f"Diretório de testes não encontrado: {TESTS_DIR}", "ERROR")
        return 1
    
    if not RESULTS_DIR.exists():
        log(f"Criando diretório de resultados: {RESULTS_DIR}")
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 3. Executar notebooks
    log(f"\nExecutando {len(NOTEBOOKS_TO_RUN)} notebooks...\n")
    results_summary = {}
    start_time = time.time()
    
    for i, (test_name, config_name) in enumerate(NOTEBOOKS_TO_RUN, 1):
        log(f"\n[{i}/{len(NOTEBOOKS_TO_RUN)}] Iniciando {test_name}/{config_name}")
        
        # Executar notebook
        success = run_notebook(test_name, config_name)
        
        # Verificar se os resultados foram salvos
        if success:
            success = verify_results(test_name, config_name)
        
        results_summary[(test_name, config_name)] = success
        
        # Pausa pequena entre notebooks
        if i < len(NOTEBOOKS_TO_RUN):
            time.sleep(2)
    
    # 4. Consolidar resultados por teste
    log("\n\nConsolidando resultados por teste...")
    tests = set(test_name for test_name, _ in NOTEBOOKS_TO_RUN)
    for test_name in sorted(tests):
        consolidate_results(test_name)
    
    # 5. Resumo final
    elapsed = time.time() - start_time
    log(f"\nTempo total de execução: {elapsed/3600:.1f} horas ({elapsed/60:.0f} minutos)")
    
    print_summary(results_summary)
    
    # 6. Retornar código de saída apropriado
    failed_count = sum(1 for success in results_summary.values() if not success)
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
