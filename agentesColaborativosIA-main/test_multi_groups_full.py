#!/usr/bin/env python3
"""
Teste completo do sistema de múltiplos grupos por abordagem
"""
import sys
import os

# Adiciona fontes ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fontes'))

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from metricas import GestorMetricas
from utils.constantes import ModoJogo

def test_multiple_groups_per_approach():
    """Testa criação de múltiplos grupos por abordagem"""
    print("\n" + "="*70)
    print("🧪 TESTE: Múltiplos Grupos por Abordagem")
    print("="*70)
    
    try:
        # Inicializa gerenciador
        gerenciador = GerenciadorGrupos()
        print("\n✅ GerenciadorGrupos criado")
        
        # Define estratégias para cada abordagem
        estrategias = {
            0: [  # Abordagem A
                ("Grupo A1: BFS", GeradorAgentesAbordagem.criar_grupo_bfs),
                ("Grupo A2: KNN", GeradorAgentesAbordagem.criar_grupo_knn),
                ("Grupo A3: Híbrido", GeradorAgentesAbordagem.criar_grupo_hibrido),
            ],
            1: [  # Abordagem B
                ("Grupo B1: Aleatório Padrão", GeradorAgentesAbordagem.criar_para_abordagem_b),
                ("Grupo B2: Aleatório Agressivo", 
                 lambda mapa, mem, num_agentes=None: GeradorAgentesAbordagem.criar_para_abordagem_b(mapa, mem, num_agentes=7)),
            ],
            2: [  # Abordagem C
                ("Grupo C1: Balanceado", GeradorAgentesAbordagem.criar_para_abordagem_c),
                ("Grupo C2: KNN Focado", GeradorAgentesAbordagem.criar_grupo_knn),
            ]
        }
        
        # Obtém abordagens
        abordagens = {
            0: AbordagensPadrao.obter_abordagem_a(),
            1: AbordagensPadrao.obter_abordagem_b(),
            2: AbordagensPadrao.obter_abordagem_c(),
        }
        
        # Cria grupos para cada abordagem
        grupos_criados = {}  # {abordagem_id: [grupo_ids]}
        grupo_contador = 0
        
        for abord_id in [0, 1, 2]:
            abordagem = abordagens[abord_id]
            abord_nome = ['A', 'B', 'C'][abord_id]
            
            print(f"\n📌 Abordagem {abord_nome}:")
            grupos_criados[abord_id] = []
            
            for estrategia_nome, factory in estrategias[abord_id]:
                grupo_id = grupo_contador
                grupo_contador += 1
                
                # Cria grupo
                gerenciador.criar_grupo(
                    grupo_id=grupo_id,
                    abordagem=abordagem.tipo.value,
                    modo=abordagem.modo_jogo,
                    agentes_factory=factory,
                    num_agentes=None
                )
                
                # Verifica criação
                if grupo_id in gerenciador.grupos:
                    agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
                    grupos_criados[abord_id].append(grupo_id)
                    print(f"   ✓ {estrategia_nome}: {len(agentes)} agentes")
                else:
                    print(f"   ✗ ERRO ao criar {estrategia_nome}")
        
        # Verifica estrutura
        print(f"\n📊 Resumo de Grupos Criados:")
        total_grupos = 0
        for abord_id in [0, 1, 2]:
            abord_nome = ['A', 'B', 'C'][abord_id]
            num_grupos = len(grupos_criados[abord_id])
            total_grupos += num_grupos
            print(f"   Abordagem {abord_nome}: {num_grupos} grupos")
            for grupo_id in grupos_criados[abord_id]:
                agentes = gerenciador.obter_agentes_por_grupo(grupo_id)
                print(f"      - Grupo {grupo_id}: {len(agentes)} agentes")
        
        print(f"\n   Total: {total_grupos} grupos em {len(grupos_criados)} abordagens")
        
        # Executa alguns turnos
        print(f"\n⚙️  Executando 3 turnos de simulação...")
        for turno in range(3):
            resultado = gerenciador.executar_turno_todos()
            print(f"   Turno {turno+1}: {sum(1 for r in resultado.values() if not r['terminou'])} grupos ativos")
        
        # Verifica métricas
        print(f"\n📈 Verificando métricas...")
        for abord_id in [0, 1, 2]:
            for grupo_id in grupos_criados[abord_id]:
                grupo_info = gerenciador.grupos[grupo_id]
                agentes = grupo_info['agentes']
                print(f"   Grupo {grupo_id}: {len(agentes)} agentes")
        
        print("\n✅ TESTE PASSOU!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_multiple_groups_per_approach()
    sys.exit(0 if success else 1)
