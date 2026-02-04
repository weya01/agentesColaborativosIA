#!/usr/bin/env python3
"""
Script de teste isolado - não importa janela_principal
"""
import sys
import os

# Remove ui.janela_principal do cache
for key in list(sys.modules.keys()):
    if 'ui' in key or 'janela' in key:
        del sys.modules[key]

print("=== TESTE DE IMPORTS ===\n")

try:
    from simulacao.gerenciador_corridas import GerenciadorGrupos, Abordagem
    print("✓ GerenciadorGrupos OK")
except Exception as e:
    print(f"✗ GerenciadorGrupos: {e}")
    sys.exit(1)

try:
    from simulacao.abordagens import AbordagensPadrao
    print("✓ AbordagensPadrao OK")
except Exception as e:
    print(f"✗ AbordagensPadrao: {e}")
    sys.exit(1)

try:
    from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
    print("✓ GeradorAgentesAbordagem OK")
except Exception as e:
    print(f"✗ GeradorAgentesAbordagem: {e}")
    sys.exit(1)

print("\n✅ TODOS OS IMPORTS CRÍTICOS OK!")
print("\nA aplicação pode ser iniciada com: python main.py")
