#!/usr/bin/env python3
"""
Teste simples para verificar se o sistema de múltiplos grupos funciona
"""
import sys
import os

# Adiciona fontes ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fontes'))

from PySide6.QtWidgets import QApplication
from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo

def test_gui_initialization():
    """Testa inicialização da GUI"""
    print("\n" + "="*70)
    print("🧪 TESTE DE INICIALIZAÇÃO DA GUI")
    print("="*70)
    
    try:
        app = QApplication.instance() or QApplication(sys.argv)
        
        print("✅ QApplication criado")
        
        janela = JanelaPrincipalMultiGrupo()
        print("✅ JanelaPrincipalMultiGrupo criado")
        
        # Testa métodos de estratégia
        print("\n📋 Testando método _definir_estrategias_grupo()...")
        
        estrategias_a = janela._definir_estrategias_grupo(0)
        print(f"   Abordagem A: {len(estrategias_a)} estratégias")
        for nome, factory in estrategias_a:
            print(f"     - {nome}")
        
        estrategias_b = janela._definir_estrategias_grupo(1)
        print(f"   Abordagem B: {len(estrategias_b)} estratégias")
        for nome, factory in estrategias_b:
            print(f"     - {nome}")
        
        estrategias_c = janela._definir_estrategias_grupo(2)
        print(f"   Abordagem C: {len(estrategias_c)} estratégias")
        for nome, factory in estrategias_c:
            print(f"     - {nome}")
        
        print("\n✅ TESTE PASSOU!")
        print("="*70)
        
        # Mostra janela
        janela.show()
        
        # Executa por pouco tempo
        import time
        QTimer = __import__('PySide6.QtCore').QTimer
        def close_app():
            janela.close()
        
        timer = QTimer()
        timer.timeout.connect(close_app)
        timer.start(1000)  # Fecha após 1 segundo
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_gui_initialization()
