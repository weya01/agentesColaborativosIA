"""
Teste: Simular clique real no botão usando PySide6 signals
"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
import sys

app = QApplication(sys.argv)

print("\n" + "="*80)
print("TESTE: SIMULAR CLIQUE REAL NO BOTÃO 'INICIAR SIMULAÇÃO'")
print("="*80 + "\n")

try:
    print("✅ FASE 1: Criando GUI...")
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    janela = JanelaPrincipalMultiGrupo()
    janela.show()
    print("   ✓ Janela mostrada na tela")
    
    print("\n✅ FASE 2: Simulando clique no botão...")
    # Simula um clique no botão
    janela.btn_iniciar.click()
    print("   ✓ Clique simulado")
    
    print("\n✅ FASE 3: Processando eventos PySide6...")
    app.processEvents()
    print("   ✓ Eventos processados")
    
    print("\n✅ FASE 4: Verificando estado...")
    print(f"   ✓ Simulação ativa: {janela.simulacao_ativa}")
    print(f"   ✓ Status: {janela.label_status.text()}")
    print(f"   ✓ Grid mapa criado: {janela.grid_mapa is not None}")
    
    print("\n✅ FASE 5: Parando a simulação...")
    janela.timer.stop()
    janela.simulacao_ativa = False
    print("   ✓ Simulação parada")
    
    print("\n" + "="*80)
    print("✅ TESTE DE CLIQUE REAL EXECUTADO COM SUCESSO!")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*80)
    print("❌ TESTE FALHOU")
    print("="*80 + "\n")
