#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste da simulação com 3 abordagens - executa 5 turnos
"""
import sys
sys.path.insert(0, '.')

print("=" * 70)
print("TESTE DE SIMULAÇÃO - 3 Abordagens Simultâneas")
print("=" * 70)

try:
    from simulacao.abordagens import AbordagensPadrao
    from simulacao.gerenciador_corridas import GerenciadorGrupos
    from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
    from metricas import GestorMetricas
    
    print("\n1️⃣  Criando gerenciador...")
    gerenciador = GerenciadorGrupos()
    gestores_metricas = {}
    
    # Criar 3 grupos
    for grupo_id in range(3):
        abordagem = {0: AbordagensPadrao.obter_abordagem_a(),
                    1: AbordagensPadrao.obter_abordagem_b(),
                    2: AbordagensPadrao.obter_abordagem_c()}[grupo_id]
        
        factory = GeradorAgentesAbordagem.obter_factory_por_abordagem(abordagem.tipo.value)
        
        print(f"\n   📍 Grupo {grupo_id} ({abordagem.tipo.value})...")
        gerenciador.criar_grupo(
            grupo_id=grupo_id,
            abordagem=abordagem.tipo.value,
            modo=abordagem.modo_jogo,
            agentes_factory=factory,
            num_agentes=3
        )
        
        # Métricas
        gestores_metricas[grupo_id] = GestorMetricas()
        grupo_metricas = gestores_metricas[grupo_id].criar_grupo(grupo_id, abordagem.modo_jogo, 10)
        agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
        for agente in agentes:
            grupo_metricas.adicionar_agente(agente.id, agente.__class__.__name__)
        print(f"      ✅ {len(agentes)} agentes criados")
    
    print("\n2️⃣  Executando 5 turnos...")
    for turno in range(5):
        print(f"\n   🔄 Turno {turno + 1}:")
        
        # Executa um turno para cada grupo
        for grupo_id in range(3):
            grupo_info = gerenciador.grupos[grupo_id]
            agentes = grupo_info['agentes']
            motor = grupo_info['motor']
            
            # Executa turno para cada agente
            for agente in agentes:
                agente.executar_turno()
            
            # Verifica objetivo
            objetivo = motor.verificar_objetivo_rapido()
            
            # Atualiza métricas
            metricas = gestores_metricas[grupo_id].obter_grupo(grupo_id)
            metricas.avanca_turno()
            
            n_vivos = sum(1 for a in agentes if a.estado.value == 'vivo')
            print(f"      Grupo {grupo_id}: {n_vivos}/{len(agentes)} agentes vivos - Objetivo: {objetivo}")
    
    print("\n" + "=" * 70)
    print("✅ SIMULAÇÃO COMPLETADA COM SUCESSO")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
