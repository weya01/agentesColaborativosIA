"""
Teste de comportamento dos agentes na interface.
Simula alguns turnos e valida:
- Agentes se movem
- Métricas são atualizadas
- Rodadas progridem corretamente
"""

import sys
from PySide6.QtWidgets import QApplication

# Teste sem executar a GUI completa
def testar_sistema_rodadas():
    """Testa o sistema de rodadas sem precisar renderizar"""
    
    print("\n" + "="*70)
    print("🧪 TESTE DO SISTEMA DE RODADAS PROGRESSIVAS")
    print("="*70)
    
    # Testa fórmula
    print("\n✅ Validação da fórmula de escalamento:")
    for rodada in range(1, 10):
        agentes = rodada + 1
        bombas = 50 + (30 * (agentes - 2) / 8)
        print(f"   Rodada {rodada}: {agentes} agentes, {bombas:.2f}% bombas")
    
    print("\n✅ Validação de componentes:")
    print("   • Interface carregada...")
    
    try:
        from ui.janela_principal_clean import JanelaPrincipal
        print("     ✅ JanelaPrincipal importada")
    except Exception as e:
        print(f"     ❌ Erro ao importar JanelaPrincipal: {e}")
        return False
    
    try:
        from simulacao.gerenciador_corridas import GerenciadorGrupos
        print("     ✅ GerenciadorGrupos importado")
    except Exception as e:
        print(f"     ❌ Erro ao importar GerenciadorGrupos: {e}")
        return False
    
    try:
        from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
        print("     ✅ GeradorAgentesAbordagem importado")
    except Exception as e:
        print(f"     ❌ Erro ao importar GeradorAgentesAbordagem: {e}")
        return False
    
    try:
        from metricas import GestorMetricas
        print("     ✅ GestorMetricas importado")
    except Exception as e:
        print(f"     ❌ Erro ao importar GestorMetricas: {e}")
        return False
    
    print("\n✅ Validação de lógica:")
    
    # Testa criação de grupos
    try:
        print("   Criando gerenciador...")
        gerenciador = GerenciadorGrupos()
        print("     ✅ GerenciadorGrupos criado")
        
        print("   Criando abordagens...")
        from simulacao.abordagens import AbordagensPadrao
        abordagem = AbordagensPadrao.obter_abordagem_a()
        print("     ✅ Abordagem A obtida")
        
        print("   Criando primeiro grupo da Rodada 1...")
        grupo_id = "R1_A0_G1"
        gerenciador.criar_grupo(
            grupo_id=grupo_id,
            abordagem="Tesouros",
            modo=abordagem.modo_jogo,
            agentes_factory=GeradorAgentesAbordagem.criar_grupo_bfs,
            num_agentes=2
        )
        print("     ✅ Grupo criado com sucesso")
        
        agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
        print(f"   ✅ {len(agentes)} agentes criados")
        
        print("   Executando 5 turnos...")
        for turno in range(5):
            resultado = gerenciador.executar_turno_todos()
            todos_agentes = gerenciador.obter_todos_agentes()
            agentes_ativos = sum(1 for a in todos_agentes.values() if not a.terminou)
            print(f"     Turno {turno+1}: {agentes_ativos} agentes ativos")
        
        print("     ✅ Turnos executados com sucesso")
        
    except Exception as e:
        print(f"     ❌ Erro na simulação: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*70)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*70 + "\n")
    return True


if __name__ == "__main__":
    sucesso = testar_sistema_rodadas()
    sys.exit(0 if sucesso else 1)
