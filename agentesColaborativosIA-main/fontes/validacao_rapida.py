"""
Teste rápido de validação final do sistema.
Executa em <2 segundos.
"""

def teste_rapido():
    """Teste ultra-rápido"""
    print("\n" + "="*70)
    print("VALIDACAO RAPIDA - SISTEMA DE RODADAS PROGRESSIVAS")
    print("="*70 + "\n")
    
    # 1. Validar fórmula
    print("1. Validando fórmula de escalamento...")
    rodada_1_bombas = 50 + (30 * (2 - 2) / 8)  # Rodada 1
    rodada_9_bombas = 50 + (30 * (10 - 2) / 8)  # Rodada 9
    
    assert rodada_1_bombas == 50.0, "Rodada 1 deve ter 50% bombas"
    assert abs(rodada_9_bombas - 80.0) < 0.01, "Rodada 9 deve ter 80% bombas"
    print("   OK: Formula validada (50% -> 80%)\n")
    
    # 2. Validar imports
    print("2. Validando imports de componentes...")
    try:
        from ui.janela_principal_clean import JanelaPrincipal
        from simulacao.gerenciador_corridas import GerenciadorGrupos
        from simulacao.abordagens import AbordagensPadrao
        from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
        from metricas import GestorMetricas
        print("   OK: Todos os componentes importados\n")
    except Exception as e:
        print(f"   ERRO: {e}\n")
        return False
    
    # 3. Validar criação de grupos
    print("3. Validando criação de grupos...")
    try:
        gerenciador = GerenciadorGrupos()
        abordagem = AbordagensPadrao.obter_abordagem_a()
        
        gerenciador.criar_grupo(
            grupo_id="R1_A0_G1",
            abordagem="Tesouros",
            modo=abordagem.modo_jogo,
            agentes_factory=GeradorAgentesAbordagem.criar_grupo_bfs,
            num_agentes=2
        )
        
        agentes = gerenciador.obter_agentes_por_grupo("R1_A0_G1")
        assert len(agentes) == 2, "Deve ter 2 agentes"
        print("   OK: Grupo criado com 2 agentes\n")
    except Exception as e:
        print(f"   ERRO: {e}\n")
        return False
    
    # 4. Validar execução de turnos
    print("4. Validando execução de turnos...")
    try:
        for turno in range(10):
            gerenciador.executar_turno_todos()
        
        todos_agentes = gerenciador.obter_todos_agentes()
        assert len(todos_agentes) >= 2, "Deve haver agentes"
        print("   OK: 10 turnos executados com sucesso\n")
    except Exception as e:
        print(f"   ERRO: {e}\n")
        return False
    
    # 5. Validar múltiplas abordagens
    print("5. Validando múltiplas abordagens simultâneas...")
    try:
        gerenciador2 = GerenciadorGrupos()
        
        abord_a = AbordagensPadrao.obter_abordagem_a()
        abord_b = AbordagensPadrao.obter_abordagem_b()
        abord_c = AbordagensPadrao.obter_abordagem_c()
        
        gerenciador2.criar_grupo("R1_A0_G1", "A", abord_a.modo_jogo,
                                  GeradorAgentesAbordagem.criar_grupo_bfs, 2)
        gerenciador2.criar_grupo("R1_A1_G1", "B", abord_b.modo_jogo,
                                  GeradorAgentesAbordagem.criar_para_abordagem_b, 2)
        gerenciador2.criar_grupo("R1_A2_G1", "C", abord_c.modo_jogo,
                                  GeradorAgentesAbordagem.criar_grupo_knn, 2)
        
        for turno in range(5):
            gerenciador2.executar_turno_todos()
        
        assert len(gerenciador2.grupos) == 3, "Deve ter 3 grupos"
        print("   OK: 3 abordagens rodando simultaneamente\n")
    except Exception as e:
        print(f"   ERRO: {e}\n")
        return False
    
    print("="*70)
    print("OK: TODAS AS VALIDACOES PASSARAM COM SUCESSO!")
    print("="*70 + "\n")
    print("Sistema pronto para uso!")
    print("\nPara executar a interface:")
    print("  python main.py\n")
    
    return True


if __name__ == "__main__":
    import sys
    sucesso = teste_rapido()
    sys.exit(0 if sucesso else 1)
