#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste sem GUI - simula o que a interface faria
"""
import sys
sys.path.insert(0, '.')

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from metricas import GestorMetricas

print("=" * 70)
print("TESTE DE SIMULAÇÃO (simulando interface)")
print("=" * 70)

# Simula o que o método iniciar_simulacao faz
try:
    print("\n1️⃣  Criando gerenciador...")
    gerenciador = GerenciadorGrupos()
    gestores_metricas = {}
    
    # Abordagens selecionadas (simula checkboxes)
    abordagens_selecionadas = [0, 1, 2]  # A, B, C
    
    print(f"\n2️⃣  Criando grupos: {abordagens_selecionadas}")
    
    abordagens = {
        0: AbordagensPadrao.obter_abordagem_a(),
        1: AbordagensPadrao.obter_abordagem_b(),
        2: AbordagensPadrao.obter_abordagem_c(),
    }

    for grupo_id in abordagens_selecionadas:
        abordagem = abordagens[grupo_id]
        print(f"\n   📍 Grupo {grupo_id} ({abordagem.tipo.value})...")
        
        factory = GeradorAgentesAbordagem.obter_factory_por_abordagem(abordagem.tipo.value)
        
        gerenciador.criar_grupo(
            grupo_id=grupo_id,
            abordagem=abordagem.tipo.value,
            modo=abordagem.modo_jogo,
            agentes_factory=factory,
            num_agentes=None
        )
        
        gestores_metricas[grupo_id] = GestorMetricas()
        agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
        
        grupo_metricas = gestores_metricas[grupo_id].criar_grupo(grupo_id, abordagem.modo_jogo, 10)
        for agente in agentes:
            grupo_metricas.adicionar_agente(agente.id, agente.__class__.__name__)
        
        print(f"      ✅ {len(agentes)} agentes criados")
    
    print(f"\n3️⃣  Executando 5 turnos...")
    
    for turno in range(1, 6):
        print(f"\n   🔄 Turno {turno}:")
        
        # Executa um turno para todos os grupos
        resultado = gerenciador.executar_turno_todos()
        
        # Atualiza métricas
        for grupo_id in abordagens_selecionadas:
            grupo_info = gerenciador.grupos[grupo_id]
            agentes = grupo_info['agentes']
            
            gestor = gestores_metricas[grupo_id]
            grupo_metricas = gestor.obter_grupo(grupo_id)
            grupo_metricas.avanca_turno()
            
            # Mostra métricas
            abordagem_nome = ['A', 'B', 'C'][grupo_id]
            n_vivos = sum(1 for a in agentes if a.estado.value == 'vivo')
            cobertura = grupo_metricas.obter_cobertura_mapa()
            tesouros = grupo_metricas.obter_tesouros_coletados()
            
            print(f"      [{abordagem_nome}] {n_vivos}/{len(agentes)} vivos | Cobertura: {cobertura:.0f}% | Tesouros: {tesouros}")
    
    print(f"\n" + "=" * 70)
    print("✅ TESTE COMPLETADO COM SUCESSO")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
