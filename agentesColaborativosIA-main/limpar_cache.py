"""
Script para Limpar Cache Python e Diagnosticar Problemas

Executa:
1. Remove todos __pycache__ recursivamente
2. Remove todos .pyc files
3. Testa imports básicos
4. Verifica integridade de janela_principal.py
"""

import os
import shutil
from pathlib import Path
import sys


def limpar_cache_python(caminho_raiz: str):
    """Remove todos arquivos de cache Python"""
    print(f"Limpando cache Python em: {caminho_raiz}")
    
    # Remove __pycache__ directories
    cache_dirs = list(Path(caminho_raiz).rglob('__pycache__'))
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"  ✓ Removido: {cache_dir}")
        except Exception as e:
            print(f"  ✗ Erro ao remover {cache_dir}: {e}")
    
    # Remove .pyc files
    pyc_files = list(Path(caminho_raiz).rglob('*.pyc'))
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"  ✓ Removido: {pyc_file}")
        except Exception as e:
            print(f"  ✗ Erro ao remover {pyc_file}: {e}")
    
    print(f"✅ Cache limpo! Removidos {len(cache_dirs)} diretórios e {len(pyc_files)} arquivos.\n")


def testar_imports(caminho_projeto: str):
    """Testa imports básicos"""
    print("Testando imports de módulos críticos...")
    sys.path.insert(0, os.path.join(caminho_projeto, 'fontes'))
    
    modulos = [
        ('agentes.agente_base', 'AgenteBase'),
        ('agentes.memoria_partilhada', 'MemoriaPartilhada'),
        ('ambientes.gerador_de_mapa', 'GeradorMapa'),
        ('simulacao.motor', 'MotorSimulacao'),
        ('simulacao.gerenciador_corridas', 'GerenciadorGrupos'),
        ('simulacao.abordagens', 'AbordagensPadrao'),
        ('simulacao.gestor_logs', 'GestorLogs'),
        ('simulacao.sistema_forca', 'SistemaForca'),
        ('agentes.modelos_ml', 'GestorModelos'),
    ]
    
    for modulo, classe in modulos:
        try:
            mod = __import__(modulo, fromlist=[classe])
            print(f"  ✅ {modulo}.{classe}")
        except Exception as e:
            print(f"  ❌ {modulo}: {e}")


def diagnosticar_janela_principal(caminho_arquivo: str):
    """Verifica integridade de janela_principal.py"""
    print("\nDiagnosticando janela_principal.py...")
    
    if not os.path.exists(caminho_arquivo):
        print(f"  ❌ Arquivo não encontrado: {caminho_arquivo}")
        return
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            linhas = conteudo.split('\n')
            
        print(f"  ✓ Arquivo lido: {len(linhas)} linhas")
        
        # Verifica se referencia janela_principal_multi_grupo
        if 'janela_principal_multi_grupo' in conteudo:
            print(f"  ✓ Contém importação de janela_principal_multi_grupo")
        else:
            print(f"  ⚠️  Não importa janela_principal_multi_grupo")
        
        # Verifica tamanho do arquivo
        if len(linhas) > 50:
            print(f"  ⚠️  Arquivo muito grande ({len(linhas)} linhas) - pode ter código legado")
        else:
            print(f"  ✓ Arquivo parece estar limpo (apenas {len(linhas)} linhas)")
            
    except Exception as e:
        print(f"  ❌ Erro ao ler arquivo: {e}")


def main():
    """Executa limpeza e diagnóstico"""
    
    # Caminho raiz do projeto
    caminho_projeto = r"c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main"
    
    print("="*70)
    print("LIMPEZA E DIAGNÓSTICO DO CACHE PYTHON")
    print("="*70 + "\n")
    
    # 1. Limpar cache
    limpar_cache_python(caminho_projeto)
    
    # 2. Testar imports
    testar_imports(caminho_projeto)
    
    # 3. Diagnosticar janela_principal.py
    janela_principal = os.path.join(caminho_projeto, 'fontes', 'ui', 'janela_principal.py')
    diagnosticar_janela_principal(janela_principal)
    
    print("\n" + "="*70)
    print("✅ DIAGNÓSTICO CONCLUÍDO")
    print("="*70)
    print("""
Se não há erros acima, o cache foi limpo com sucesso.
Você pode agora executar:
    python main.py
    
Se ainda houver erros de cache, tente:
    python -B main.py
    
Ou reinicie a sessão do Python completamente.
    """)


if __name__ == "__main__":
    main()

