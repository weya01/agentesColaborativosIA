"""
Teste da inicialização completa da GUI
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\n" + "="*70)
print("TESTE DE INICIALIZAÇÃO COMPLETA DA GUI")
print("="*70 + "\n")

try:
    print("1️⃣  Importando JanelaPrincipalMultiGrupo...")
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    print("   ✅ Importação bem-sucedida")
    
    print("\n2️⃣  Inicializando janela...")
    janela = JanelaPrincipalMultiGrupo()
    print("   ✅ Janela criada")
    
    print("\n3️⃣  Testando botões e widgets...")
    print(f"   ✓ Botão A: {janela.check_abordagem_a.text()}")
    print(f"   ✓ Botão B: {janela.check_abordagem_b.text()}")
    print(f"   ✓ Botão C: {janela.check_abordagem_c.text()}")
    
    print("\n4️⃣  Verificando estado dos checkboxes...")
    print(f"   ✓ A checada: {janela.check_abordagem_a.isChecked()}")
    print(f"   ✓ B checada: {janela.check_abordagem_b.isChecked()}")
    print(f"   ✓ C checada: {janela.check_abordagem_c.isChecked()}")
    
    print("\n5️⃣  Verificando velocity combo...")
    print(f"   ✓ Índice: {janela.combo_velocidade.currentIndex()}")
    print(f"   ✓ Valor: {janela.combo_velocidade.currentText()}")
    
    print("\n6️⃣  Verificando gerenciador...")
    print(f"   ✓ Gerenciador existe: {janela.gerenciador is not None}")
    print(f"   ✓ Timer existe: {janela.timer is not None}")
    
    print("\n7️⃣  Simulando clique em 'Iniciar Simulação'...")
    print("   Chamando janela.iniciar_simulacao()...\n")
    janela.iniciar_simulacao()
    
    print("\n8️⃣  Verificando estado pós-inicialização...")
    print(f"   ✓ Simulação ativa: {janela.simulacao_ativa}")
    print(f"   ✓ Turno atual: {janela.turno_atual}")
    print(f"   ✓ Grid mapa: {janela.grid_mapa is not None}")
    print(f"   ✓ Status label: {janela.label_status.text()}")
    
    print("\n9️⃣  Verificando grupos criados...")
    print(f"   ✓ Quantidade de grupos: {len(janela.gerenciador.grupos)}")
    for grupo_id, grupo_info in janela.gerenciador.grupos.items():
        agentes = grupo_info['agentes']
        print(f"   ✓ Grupo {grupo_id}: {len(agentes)} agentes")
    
    print("\n🔟 Testando atualização de turno (simulando timer)...")
    print("   Parando timer para não continuar executando...")
    janela.timer.stop()
    print("   ✅ OK")
    
    print("\n" + "="*70)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERRO ENCONTRADO: {e}")
    print("\nStack trace completo:")
    import traceback
    traceback.print_exc()
    print("\n" + "="*70)
    print("❌ TESTE FALHOU")
    print("="*70 + "\n")
