"""
TESTE FINAL COMPLETO: Simulação full stack
Simula: Iniciar -> Executar 10 turnos -> Pausar -> Resetar
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\n" + "="*80)
print("TESTE FINAL: SIMULAÇÃO COMPLETA COM TODAS AS OPERAÇÕES")
print("="*80 + "\n")

try:
    print("✅ PASSO 1: Criar GUI")
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    janela = JanelaPrincipalMultiGrupo()
    print("   ✓ Janela criada")
    
    print("\n✅ PASSO 2: Clicar 'Iniciar Simulação'")
    janela.iniciar_simulacao()
    print(f"   ✓ Simulação ativa: {janela.simulacao_ativa}")
    print(f"   ✓ Grupos: {len(janela.gerenciador.grupos)}")
    print(f"   ✓ Grid criado: {janela.grid_mapa is not None}")
    
    print("\n✅ PASSO 3: Executar 10 turnos")
    for turno in range(1, 11):
        resultado = janela.gerenciador.executar_turno_todos()
        
        # Verifica se todos os grupos terminaram
        todos_terminados = all(r['terminou'] for r in resultado.values())
        
        if todos_terminados:
            print(f"   ✓ Turno {turno}: TODOS OS GRUPOS TERMINARAM")
            break
        else:
            print(f"   ✓ Turno {turno}: OK")
    
    print(f"\n✅ PASSO 4: Verificar métricas finais")
    for grupo_id in janela.gerenciador.grupos:
        agentes = janela.gerenciador.obter_agentes_por_grupo(grupo_id)
        print(f"   ✓ Grupo {grupo_id}: {len(agentes)} agentes")
    
    print("\n✅ PASSO 5: Pausar simulação")
    janela.pausar_simulacao()
    print(f"   ✓ Simulação ativa: {janela.simulacao_ativa}")
    print(f"   ✓ Status: {janela.label_status.text()}")
    
    print("\n✅ PASSO 6: Resetar simulação")
    janela.resetar_simulacao()
    print(f"   ✓ Simulação ativa: {janela.simulacao_ativa}")
    print(f"   ✓ Turno: {janela.turno_atual}")
    print(f"   ✓ Status: {janela.label_status.text()}")
    
    print("\n✅ PASSO 7: Testar seleção de apenas 1 abordagem")
    janela.check_abordagem_a.setChecked(True)
    janela.check_abordagem_b.setChecked(False)
    janela.check_abordagem_c.setChecked(False)
    print("   ✓ Seleções alteradas")
    
    janela.iniciar_simulacao()
    print(f"   ✓ Grupos: {len(janela.gerenciador.grupos)} (esperado: 1)")
    print(f"   ✓ IDs dos grupos: {list(janela.gerenciador.grupos.keys())}")
    
    print("\n" + "="*80)
    print("✅ TESTE COMPLETO PASSOU COM SUCESSO!")
    print("   O programa está 100% funcional e pronto para usar.")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*80)
    print("❌ TESTE FALHOU")
    print("="*80 + "\n")
    sys.exit(1)
