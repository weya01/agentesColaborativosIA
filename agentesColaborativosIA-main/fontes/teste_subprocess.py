#!/usr/bin/env python3
"""
Teste em subprocess isolado
"""
import subprocess
import sys

result = subprocess.run([
    sys.executable, '-B', '-c',
    """
import sys
sys.path.insert(0, '.')
from simulacao.gerenciador_corridas import GerenciadorGrupos
print('✓ OK - GerenciadorGrupos importado')
"""
], cwd=r"C:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes")

sys.exit(result.returncode)
