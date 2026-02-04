#!/usr/bin/env python3
"""
Teste de integração completa do sistema de múltiplos grupos
Simula o fluxo de uso real da interface
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

class SimuladorMultiGrupos:
    """Simulador que imita o comportamento da JanelaPrincipalMultiGrupo"""
    
    def __init__(self):
        self.gerenciador = GerenciadorGrupos()
        self.gestores_metricas = {}  # {abordagem_id: {grupo_id: GestorMetricas}}
        self.resultados_abordagens = {}  # {abordagem_id: {grupo_id: resultado}}
        self.turno_atual = 0
        self.abordagem_selecionada = 0
        self.tabs_grupos = {}
    
    def definir_estrategias_grupo(self, abordagem_id):
        """Retorna estratégias para uma abordagem (imitando o método da UI)"""
        estrategias = []
        
        if abordagem_id == 0:  # Abordagem A
            estrategias = [
                ("Grupo 1: 3x BFS", GeradorAgentesAbordagem.criar_grupo_bfs),
                ("Grupo 2: 3x KNN", GeradorAgentesAbordagem.criar_grupo_knn),
                ("Grupo 3: 2x BFS + 1x KNN", GeradorAgentesAbordagem.criar_grupo_hibrido),
            ]
        elif abordagem_id == 1:  # Abordagem B
            estrategias = [
                ("Grupo 1: Padrão", GeradorAgentesAbordagem.criar_para_abordagem_b),
                ("Grupo 2: Agressivo", 
                 lambda mapa, mem, num_agentes=None: GeradorAgentesAbordagem.criar_para_abordagem_b(mapa, mem, num_agentes=7)),
            ]
        elif abordagem_id == 2:  # Abordagem C
            estrategias = [
                ("Grupo 1: KNN Focado", GeradorAgentesAbordagem.criar_grupo_knn),
            ]
        
        return estrategias
    
    def iniciar_simulacao(self, abordagens_selecionadas):
        """Inicia simulação com as abordagens selecionadas"""
        print("\n" + "="*70)
        print("🚀 INICIAR SIMULAÇÃO - Múltiplos Grupos")
        print("="*70)
        
        abordagens = {
            0: AbordagensPadrao.obter_abordagem_a(),
            1: AbordagensPadrao.obter_abordagem_b(),
            2: AbordagensPadrao.obter_abordagem_c(),
        }
        
        grupo_contador = 0
        
        for abordagem_id in abordagens_selecionadas:
            abordagem = abordagens[abordagem_id]
            abord_nomes = {0: 'A', 1: 'B', 2: 'C'}
            print(f"\n📌 Abordagem {abord_nomes[abordagem_id]}")
            
            estrategias_grupo = self.definir_estrategias_grupo(abordagem_id)
            
            if abordagem_id not in self.gestores_metricas:
                self.gestores_metricas[abordagem_id] = {}
            if abordagem_id not in self.resultados_abordagens:
                self.resultados_abordagens[abordagem_id] = {}
            
            for estrategia_nome, factory in estrategias_grupo:
                grupo_id = grupo_contador
                grupo_contador += 1
                
                print(f"   ✓ Criando {estrategia_nome}")
                
                # Cria grupo
                self.gerenciador.criar_grupo(
                    grupo_id=grupo_id,
                    abordagem=abordagem.tipo.value,
                    modo=abordagem.modo_jogo,
                    agentes_factory=factory,
                    num_agentes=None
                )
                
                # Cria gestor de métricas
                self.gestores_metricas[abordagem_id][grupo_id] = GestorMetricas()
                
                # Obtém agentes
                agentes = self.gerenciador.obter_agentes_por_grupo(grupo_id)
                
                # Inicializa métricas
                grupo_metricas = self.gestores_metricas[abordagem_id][grupo_id].criar_grupo(
                    grupo_id, abordagem.modo_jogo, 0
                )
                for agente in agentes:
                    tipo_nome = agente.__class__.__name__
                    grupo_metricas.adicionar_agente(agente.id, tipo_nome)
                
                # Armazena resultado
                self.resultados_abordagens[abordagem_id][grupo_id] = {
                    "estrategia": estrategia_nome,
                    "num_agentes": len(agentes),
                    "tipos": [a.__class__.__name__ for a in agentes],
                    "objetivo_alcancado": False,
                    "turno_conclusao": None
                }
    
    def atualizar_tabs_grupos(self):
        """Atualiza abas para abordagem selecionada"""
        abordagem = self.abordagem_selecionada
        
        if abordagem not in self.resultados_abordagens:
            print(f"Nenhum resultado para Abordagem {abordagem}")
            return
        
        resultados = self.resultados_abordagens[abordagem]
        print(f"\n📊 Abas da Abordagem {abordagem}: {len(resultados)} grupos")
        
        for grupo_id in sorted(resultados.keys()):
            estrategia = resultados[grupo_id].get("estrategia", f"Grupo {grupo_id}")
            print(f"   - Grupo {grupo_id}: {estrategia}")
    
    def executar_turno(self):
        """Executa um turno de simulação"""
        self.turno_atual += 1
        resultado_turno = self.gerenciador.executar_turno_todos()
        
        # Atualiza métricas para abordagem selecionada
        if self.abordagem_selecionada in self.gestores_metricas:
            for grupo_id in self.gestores_metricas[self.abordagem_selecionada].keys():
                if grupo_id in self.gerenciador.grupos:
                    grupos_ativos = sum(1 for r in resultado_turno.values() if not r['terminou'])
                    return grupos_ativos > 0
        
        return False
    
    def simular_workflow(self):
        """Simula o fluxo completo de uso"""
        print("\n" + "="*70)
        print("🧪 TESTE DE FLUXO COMPLETO DE USO")
        print("="*70)
        
        try:
            # 1. Utilizador seleciona abordagens (A e B)
            print("\n1️⃣  Utilizador seleciona Abordagens A e B")
            abordagens_selecionadas = [0, 1]
            
            # 2. Inicia simulação
            print("\n2️⃣  Inicia simulação")
            self.iniciar_simulacao(abordagens_selecionadas)
            
            # 3. Visualiza Abordagem A
            print("\n3️⃣  Visualiza Abordagem A (índice 0)")
            self.abordagem_selecionada = 0
            self.atualizar_tabs_grupos()
            
            # 4. Muda para Abordagem B
            print("\n4️⃣  Muda para Abordagem B (índice 1)")
            self.abordagem_selecionada = 1
            self.atualizar_tabs_grupos()
            
            # 5. Executa vários turnos
            print("\n5️⃣  Executa 5 turnos de simulação")
            for i in range(5):
                ativo = self.executar_turno()
                print(f"   Turno {self.turno_atual}: {'✓ Ativo' if ativo else '✗ Completo'}")
                if not ativo:
                    break
            
            # 6. Mostra resumo final
            print("\n6️⃣  Resumo Final")
            print(f"   Total de turnos: {self.turno_atual}")
            print(f"   Abordagens simuladas: {len(self.resultados_abordagens)}")
            print(f"   Total de grupos: {sum(len(g) for g in self.resultados_abordagens.values())}")
            
            abord_nomes = {0: 'A', 1: 'B', 2: 'C'}
            for abord_id, grupos in self.resultados_abordagens.items():
                print(f"\n   Abordagem {abord_nomes[abord_id]}: {len(grupos)} grupos")
                for grupo_id, info in grupos.items():
                    print(f"      - {info['estrategia']}: {info['num_agentes']} agentes")
            
            print("\n✅ TESTE COMPLETO PASSOU!")
            print("="*70)
            return True
            
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    simulador = SimuladorMultiGrupos()
    sucesso = simulador.simular_workflow()
    return 0 if sucesso else 1

if __name__ == "__main__":
    sys.exit(main())
