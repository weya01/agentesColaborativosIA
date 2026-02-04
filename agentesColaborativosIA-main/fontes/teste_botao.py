#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste focado - abre GUI e mostra se botão funciona
"""
import sys
sys.path.insert(0, '.')

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo

print("Abrindo interface...")
app = QApplication(sys.argv)
janela = JanelaPrincipalMultiGrupo()
janela.show()

# Agenda um clique no botão após 1 segundo
def clicar_botao():
    print(f"\n⏱️  1 segundo depois...")
    print(f"   Status antes: {janela.label_status.text()}")
    print(f"   Clicando botão...")
    janela.btn_iniciar.click()
    print(f"   Status depois: {janela.label_status.text()}")
    print(f"   Grupos criados: {list(janela.gerenciador.grupos.keys())}")
    
    # Fecha após 2 segundos
    QTimer.singleShot(2000, app.quit)

QTimer.singleShot(1000, clicar_botao)

print("Iniciando loop de eventos...")
sys.exit(app.exec())
