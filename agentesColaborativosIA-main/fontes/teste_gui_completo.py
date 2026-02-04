"""
Teste completo: Inicializar GUI, simular cliques, executar turnos
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\n" + "="*80)
print("TESTE COMPLETO: INICIALIZAÇÃO + EXECUÇÃO DE TURNOS")
print("="*80 + "\n")

try:
    print("✅ FASE 1: Importando e criando janela...")
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    janela = JanelaPrincipalMultiGrupo()
    print("   ✓ GUI criada com sucesso")
    
    print("\n✅ FASE 2: Simulando clique em 'Iniciar Simulação'...")
    janela.iniciar_simulacao()
    print("   ✓ Simulação inicializada")
    
    print("\n✅ FASE 3: Verificando grupos...")
    num_grupos = len(janela.gerenciador.grupos)
    print(f"   ✓ {num_grupos} grupos criados")
    
    for grupo_id in janela.gerenciador.grupos:
        agentes = janela.gerenciador.obter_agentes_por_grupo(grupo_id)
        print(f"   ✓ Grupo {grupo_id}: {len(agentes)} agentes")
    
    print("\n✅ FASE 4: Executando 5 turnos manualmente...")
    for turno in range(1, 6):
        print(f"\n   Turno {turno}:")
        
        # Executa turno (sem o timer)
        resultado = janela.gerenciador.executar_turno_todos()
        print(f"      • Resultado: {resultado}")
        
        # Obtém métricas
        for grupo_id in janela.gerenciador.grupos:
            agentes = janela.gerenciador.obter_agentes_por_grupo(grupo_id)
            vivos = sum(1 for a in agentes if hasattr(a, 'estado') and a.estado.value != 'MORTO')
            print(f"      • Grupo {grupo_id}: {vivos}/{len(agentes)} vivos")
    
    print("\n✅ FASE 5: Parando timer...")
    janela.timer.stop()
    print("   ✓ Timer parado")
    
    print("\n" + "="*80)
    print("✅ TESTE COMPLETO EXECUTADO COM SUCESSO!")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*80)
    print("❌ TESTE FALHOU")
    print("="*80 + "\n")
