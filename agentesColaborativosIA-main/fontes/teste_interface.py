#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste simples - iniciar simulação e executar 5 turnos
"""
import sys
sys.path.insert(0, '.')

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo

print("=" * 70)
print("TESTE DE INTERFACE GRÁFICA")
print("=" * 70)

app = QApplication(sys.argv)
janela = JanelaPrincipalMultiGrupo()
janela.show()

print(f"\n1️⃣  Interface aberta")
print(f"   Status inicial: {janela.label_status.text()}")

# Simula clique no botão "Iniciar"
print(f"\n2️⃣  Clicando 'Iniciar Simulação'...")
try:
    janela.iniciar_simulacao()
    print(f"   ✅ Método chamado")
    print(f"   Status após click: {janela.label_status.text()}")
    print(f"   Grupos criados: {list(janela.gerenciador.grupos.keys())}")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    import traceback
    traceback.print_exc()

# Executa alguns turnos
print(f"\n3️⃣  Executando 3 turnos...")
for i in range(3):
    try:
        janela.atualizar_turno()
        print(f"   Turno {i+1}: {janela.label_turno.text()}")
    except Exception as e:
        print(f"   ❌ Erro no turno {i+1}: {e}")
        import traceback
        traceback.print_exc()
        break

print(f"\n4️⃣  Status final: {janela.label_status.text()}")
print(f"   Turnos executados: {janela.turno_atual}")

# Fechar após 2 segundos
QTimer.singleShot(2000, app.quit)
sys.exit(app.exec())
