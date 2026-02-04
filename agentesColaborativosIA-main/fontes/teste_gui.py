#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste da interface gráfica
"""
import sys
sys.path.insert(0, '.')

from PySide6.QtWidgets import QApplication
from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo

print("Abrindo interface gráfica...")
app = QApplication(sys.argv)
janela = JanelaPrincipalMultiGrupo()
janela.show()

print("✅ Interface aberta com sucesso!")
print("Clique em '▶ Iniciar Simulação' para começar")

sys.exit(app.exec())
