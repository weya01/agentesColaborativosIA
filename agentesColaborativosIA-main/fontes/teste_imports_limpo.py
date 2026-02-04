#!/usr/bin/env python3
"""
Teste de imports num ambiente limpo.
Ignora cache de imports.
"""
import sys
import os

# Limpa o cache de módulos
if 'ui.janela_principal' in sys.modules:
    del sys.modules['ui.janela_principal']

# Define path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Testando imports críticos...")

try:
    from simulacao.gerenciador_corridas import GerenciadorGrupos, Abordagem
    print("✓ GerenciadorGrupos OK")
except Exception as e:
    print(f"✗ Erro em GerenciadorGrupos: {e}")
    sys.exit(1)

try:
    from simulacao.abordagens import AbordagensPadrao
    print("✓ AbordagensPadrao OK")
except Exception as e:
    print(f"✗ Erro em AbordagensPadrao: {e}")
    sys.exit(1)

try:
    from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
    print("✓ GeradorAgentesAbordagem OK")
except Exception as e:
    print(f"✗ Erro em GeradorAgentesAbordagem: {e}")
    sys.exit(1)

try:
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    print("✓ JanelaPrincipalMultiGrupo OK")
except Exception as e:
    print(f"✗ Erro em JanelaPrincipalMultiGrupo: {e}")
    sys.exit(1)

print("\n✅ TODOS OS IMPORTS OK - Pronto para executar!")
print("\nPara iniciar a aplicação, execute:")
print("  python main.py")
