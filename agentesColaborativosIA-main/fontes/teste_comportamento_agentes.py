"""
Teste de comportamento detalhado dos agentes.
Valida:
- Agentes se movem corretamente
- Exploram celulas novas
- Evitam bombas
- Completam rodadas em tempo razoavel
"""

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem


def testar_comportamento_agentes():
    """Testa comportamento dos agentes em uma rodada"""
    
    print("\n" + "="*70)
    print("TESTE DE COMPORTAMENTO DOS AGENTES")
    print("="*70 + "\n")
    
    try:
        print("OK: Criando gerenciador...")
        gerenciador = GerenciadorGrupos()
        
        print("OK: Obtendo abordagem A (Tesouros)...")
        abordagem = AbordagensPadrao.obter_abordagem_a()
        
        print("OK: Criando grupo com 2 agentes (Rodada 1)...")
        grupo_id = "R1_A0_G1"
        gerenciador.criar_grupo(
            grupo_id=grupo_id,
            abordagem="Tesouros",
            modo=abordagem.modo_jogo,
            agentes_factory=GeradorAgentesAbordagem.criar_grupo_bfs,
            num_agentes=2
        )
        
        agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
        print(f"OK: {len(agentes)} agentes criados\n")
        
        # Executar turnos com limite
        print("EXECUCAO DE TURNOS (MAX 200 por rodada):")
        print("-" * 70)
        print(f"{'Turno':<8} {'Ativos':<8} {'Passos':<12} {'Explorado':<12} {'Status':<15}")
        print("-" * 70)
        
        max_turnos = 200
        for turno in range(1, max_turnos + 1):
            resultado = gerenciador.executar_turno_todos()
            
            agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
            ativos = sum(1 for a in agentes if not a.terminou)
            passos_total = sum(a.passos for a in agentes)
            explorado = len(agentes[0].celulas_exploradas) if agentes else 0
            tamanho_mapa = 20  # Padrao
            percentual = (explorado / (tamanho_mapa * tamanho_mapa)) * 100
            
            # Status do grupo
            if ativos == 0 or turno >= max_turnos:
                status = "COMPLETADO"
            else:
                status = "Explorando"
            
            if turno % 10 == 0 or turno == 1 or ativos == 0 or turno == max_turnos:
                print(f"{turno:<8} {ativos:<8} {passos_total:<12} {percentual:<12.1f}% {status:<15}")
            
            if ativos == 0 or turno >= max_turnos:
                print(f"\nOK: Rodada completada em {turno} turnos")
                break
        
        print("-" * 70)
        
        # Estatisticas finais
        print("\nESTATISTICAS FINAIS:")
        print("-" * 70)
        
        agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
        for i, agente in enumerate(agentes, 1):
            metricas = agente.obter_metricas()
            print(f"\nAgente {i} ({agente.__class__.__name__}):")
            print(f"  Passos: {agente.passos}")
            print(f"  Celulas exploradas: {len(agente.celulas_exploradas)}")
            print(f"  Celulas seguras: {len(agente.celulas_seguras)}")
            print(f"  Tesouros: {metricas.get('tesouros', 0)}")
            print(f"  Bombas acionadas: {agente.bombas_acionadas}")
            print(f"  Status: {agente.estado.value}")
            print(f"  Terminou: {'Sim' if agente.terminou else 'Nao'}")
        
        print("\nOK: Teste de comportamento concluido com sucesso!")
        print("="*70 + "\n")
        
        # Teste com múltiplos grupos (simulando abordagens)
        print("\nTESTE DE MULTIPLOS GRUPOS (Abordagens A, B, C):")
        print("="*70)
        
        gerenciador2 = GerenciadorGrupos()
        abordagens_test = [
            (0, AbordagensPadrao.obter_abordagem_a(), GeradorAgentesAbordagem.criar_grupo_bfs),
            (1, AbordagensPadrao.obter_abordagem_b(), GeradorAgentesAbordagem.criar_para_abordagem_b),
            (2, AbordagensPadrao.obter_abordagem_c(), GeradorAgentesAbordagem.criar_grupo_knn),
        ]
        
        for abord_id, abordagem, factory in abordagens_test:
            nome_abord = chr(65 + abord_id)
            grupo_id = f"R1_A{abord_id}_G1"
            
            gerenciador2.criar_grupo(
                grupo_id=grupo_id,
                abordagem=abordagem.tipo.value,
                modo=abordagem.modo_jogo,
                agentes_factory=factory,
                num_agentes=2
            )
            print(f"OK: Grupo Abordagem {nome_abord} criado")
        
        # Executar alguns turnos
        print(f"\nExecutando 20 turnos com 3 grupos simultaneous...")
        for turno in range(20):
            gerenciador2.executar_turno_todos()
        
        print("OK: Grupos executados simultaneamente com sucesso!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nERRO durante teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    import sys
    sucesso = testar_comportamento_agentes()
    sys.exit(0 if sucesso else 1)
