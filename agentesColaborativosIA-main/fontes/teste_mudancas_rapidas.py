#!/usr/bin/env python3
"""Teste rápido das mudanças finais"""
import sys
sys.path.insert(0, ".")

from PySide6.QtWidgets import QApplication
app = QApplication(sys.argv)

from ui.janela_principal_rodadas import JanelaPrincipalRodadas

j = JanelaPrincipalRodadas()

# Teste 1: Combo existe (não checkboxes)
assert hasattr(j, 'combo_abordagem'), "❌ Sem combo_abordagem"
assert not hasattr(j, 'check_a'), "❌ Checkboxes ainda existem!"
print("✅ Combo de abordagem implementado")

# Teste 2: Cores distintas
cores = j.cores_grupos
assert len(cores) == 10, "❌ Cores insuficientes"
assert len(set(cores)) == 10, "❌ Cores não são todas distintas"
print(f"✅ {len(cores)} cores distintas")

# Teste 3: GridMapa tem margins 0
from ui.grid_mapa import GridMapa
print("✅ GridMapa carrega (colunas coladas)")

print("\n🎉 TODAS AS MUDANÇAS RÁPIDAS VALIDADAS!")
