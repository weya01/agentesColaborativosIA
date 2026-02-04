"""
Gerador de Agentes por Abordagem.

Cria agentes com comportamento adaptado a cada abordagem (A, B, C).
Implementa aleatoriedade controlada:
- Número de agentes: 2-10 aleatoriamente
- Tipos de agentes: escolhidos aleatoriamente
- Algoritmos: dinâmicos por agente
"""
import random
from agentes.agentes_busca.agente_busca import AgenteBusca, AgenteArvoreBusca
from agentes.agentes_nao_busca.agente_nao_busca import (
    AgenteAleatorio, AgenteExploracao, AgenteKNN
)
from agentes.agentes_hibridos.agente_hibrido import (
    AgenteHibrido, AgenteAdaptativo, AgenteCombinado
)
from agentes.agentes_ml.agente_ml import AgenteML
from agentes.modelos_ml import TecnicaML


class GeradorAgentesAbordagem:
    """Gera agentes adaptados para cada abordagem"""
    
    # Mapeamento de tipos de agentes
    TIPOS_AGENTES = {
        "BFS": AgenteBusca,
        "Árvore de Busca": AgenteArvoreBusca,
        "Aleatório": AgenteAleatorio,
        "Exploração": AgenteExploracao,
        "KNN": AgenteKNN,
        "Híbrido": AgenteHibrido,
        "Adaptativo": AgenteAdaptativo,
        "Combinado": AgenteCombinado,
        "ML (Árvore Decisão)": "ML_ARVORE",
        "ML (KNN)": "ML_KNN",
        "ML (Naive Bayes)": "ML_NAIVEBAYES",
    }
    
    @staticmethod
    def criar_para_abordagem_a(mapa, memoria, num_agentes=None):
        """
        Cria agentes otimizados para ABORDAGEM A (Tesouros).
        
        Estratégia: Prioriza algoritmos de busca inteligente
        - BFS/DFS para exploração sistemática
        - KNN para localização de tesouros
        - Híbridos para adaptabilidade
        
        Args:
            mapa: Mapa isolado
            memoria: Memória partilhada
            num_agentes: Quantidade (se None, 2-10 aleatoriamente)
            
        Returns:
            Lista de agentes
        """
        if num_agentes is None:
            num_agentes = random.randint(2, 10)
        
        # Prioriza agentes de busca e híbridos
        tipos_preferenciais = [
            AgenteBusca,          # BFS - exploração sistemática
            AgenteArvoreBusca,    # Árvore - estruturada
            AgenteKNN,            # KNN - localização de tesouros
            AgenteHibrido,        # Adaptável
            AgenteAdaptativo,     # Muito adaptável
        ]
        
        agentes = []
        for i in range(num_agentes):
            tipo = random.choice(tipos_preferenciais)
            agente = tipo(
                nome=f"A{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0  # Será ajustado pelo GerenciadorGrupos
            )
            agentes.append(agente)
        
        return agentes
    
    @staticmethod
    def criar_para_abordagem_b(mapa, memoria, num_agentes=None):
        """
        Cria agentes otimizados para ABORDAGEM B (Sobrevivência).
        
        Estratégia: Prioriza cautela e exploração
        - Exploração sistemática com aleatorio_seguro
        - Evitação de risco
        - Coordenação de grupo
        
        Args:
            mapa: Mapa isolado
            memoria: Memória partilhada
            num_agentes: Quantidade (se None, 2-10 aleatoriamente)
            
        Returns:
            Lista de agentes
        """
        if num_agentes is None:
            num_agentes = random.randint(2, 10)
        
        # MODO B: Usa APENAS AgenteAleatorio com aleatorio_seguro
        # Critério de sobrevivência: >80% exploração + 1 agente vivo
        # AgenteAleatorio com aleatorio_seguro é a escolha mais segura
        
        agentes = []
        for i in range(num_agentes):
            agente = AgenteAleatorio(
                nome=f"B{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0,  # Será ajustado pelo GerenciadorGrupos
                algoritmos=["aleatorio_seguro"]  # FORÇAR uso apenas de aleatorio_seguro
            )
            agentes.append(agente)
        
        return agentes
    
    @staticmethod
    def criar_para_abordagem_c(mapa, memoria, num_agentes=None):
        """
        Cria agentes otimizados para ABORDAGEM C (Bandeira).
        
        Estratégia: Sobrevivência máxima + busca de bandeira
        - Modo C tem 45% de bombas, muito perigoso
        - Precisa de sobrevivência como Modo B
        - Mas também busca agressiva pela bandeira
        
        Args:
            mapa: Mapa isolado
            memoria: Memória partilhada
            num_agentes: Quantidade (se None, 2-10 aleatoriamente)
            
        Returns:
            Lista de agentes
        """
        if num_agentes is None:
            num_agentes = random.randint(2, 10)
        
        # Combina defensiva (como Modo B) com inteligência (como Modo C)
        # Usa AgenteAleatorio com aleatorio_seguro para sobrevivência máxima
        # + alguns agentes KNN/Híbridos para busca da bandeira
        
        tipos_preferenciais = [
            (AgenteAleatorio, 0.6),      # 60% defensivo (sobrevivência)
            (AgenteKNN, 0.3),            # 30% inteligente (busca)
            (AgenteHibrido, 0.1),        # 10% adaptativo (flexibilidade)
        ]
        
        agentes = []
        for i in range(num_agentes):
            # Escolhe tipo por probabilidade
            r = random.random()
            cum_prob = 0
            tipo = AgenteAleatorio  # Default
            
            for tipo_agente, prob in tipos_preferenciais:
                cum_prob += prob
                if r < cum_prob:
                    tipo = tipo_agente
                    break
            
            # Cria agente
            if tipo == AgenteAleatorio:
                agente = tipo(
                    nome=f"C{i+1}",
                    mapa=mapa,
                    memoria_grupo=memoria,
                    grupo_id=0,
                    algoritmos=["aleatorio_seguro"]  # Força defensiva
                )
            else:
                agente = tipo(
                    nome=f"C{i+1}",
                    mapa=mapa,
                    memoria_grupo=memoria,
                    grupo_id=0
                )
            
            agentes.append(agente)
        
        return agentes
    
    @staticmethod
    def criar_agentes_aleatorios(mapa, memoria, num_agentes=None):
        """
        Cria agentes completamente aleatoriamente.
        
        Args:
            mapa: Mapa isolado
            memoria: Memória partilhada
            num_agentes: Quantidade (se None, 2-10 aleatoriamente)
            
        Returns:
            Lista de agentes
        """
        if num_agentes is None:
            num_agentes = random.randint(2, 10)
        
        tipos_disponiveis = list(GeradorAgentesAbordagem.TIPOS_AGENTES.values())
        
        agentes = []
        for i in range(num_agentes):
            tipo = random.choice(tipos_disponiveis)
            agente = tipo(
                nome=f"R{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        
        return agentes
    
    @staticmethod
    def obter_factory_por_abordagem(abordagem):
        """
        Retorna função factory de criação de agentes para uma abordagem.
        
        Args:
            abordagem: 'A', 'B', 'C' ou TipoAbordagem
            
        Returns:
            Função factory(mapa, memoria, num_agentes) -> lista_agentes
        """
        if hasattr(abordagem, 'value'):
            abordagem = abordagem.value
        
        if abordagem == 'A':
            return GeradorAgentesAbordagem.criar_para_abordagem_a
        elif abordagem == 'B':
            return GeradorAgentesAbordagem.criar_para_abordagem_b
        elif abordagem == 'C':
            return GeradorAgentesAbordagem.criar_para_abordagem_c
        else:
            return GeradorAgentesAbordagem.criar_agentes_aleatorios
    
    @staticmethod
    def criar_agentes_com_ml(mapa, memoria, num_agentes=None, tecnica_ml=None):
        """
        Cria agentes que utilizam modelos de ML.
        
        Args:
            mapa: Mapa isolado
            memoria: Memória partilhada
            num_agentes: Quantidade de agentes
            tecnica_ml: TecnicaML (ARVORE_DECISAO, KNN, NAIVE_BAYES ou None para misto)
            
        Returns:
            Lista de agentes ML
        """
        if num_agentes is None:
            num_agentes = random.randint(2, 10)
        
        # Se técnica não especificada, alterna entre todas
        tecnicas = [TecnicaML.ARVORE_DECISAO, TecnicaML.KNN, TecnicaML.NAIVE_BAYES]
        
        agentes = []
        for i in range(num_agentes):
            # Escolhe técnica (alternando ou sorteando)
            if tecnica_ml:
                tecnica = tecnica_ml
            else:
                tecnica = tecnicas[i % len(tecnicas)]
            
            agente = AgenteML(
                nome=f"ML{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0,
                tecnica_ml=tecnica
            )
            agentes.append(agente)
        
        return agentes

    # ============================================
    # MÉTODOS PARA ESTRATÉGIAS DE COMPARAÇÃO
    # ============================================

    @staticmethod
    def criar_grupo_bfs(mapa, memoria, num_agentes=None):
        """Cria grupo com apenas agentes BFS puros"""
        if num_agentes is None:
            num_agentes = 3
        agentes = []
        for i in range(num_agentes):
            agente = AgenteBusca(
                nome=f"BFS{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        return agentes

    @staticmethod
    def criar_grupo_knn(mapa, memoria, num_agentes=None):
        """Cria grupo com apenas agentes KNN puros"""
        if num_agentes is None:
            num_agentes = 3
        agentes = []
        for i in range(num_agentes):
            agente = AgenteKNN(
                nome=f"KNN{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        return agentes

    @staticmethod
    def criar_grupo_hibrido(mapa, memoria, num_agentes=None):
        """Cria grupo com mistura 2x BFS + 1x KNN"""
        if num_agentes is None:
            num_agentes = 3
        agentes = []
        # 2 BFS
        for i in range(2):
            agente = AgenteBusca(
                nome=f"BFS{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        # 1 KNN
        agente = AgenteKNN(
            nome="KNN1",
            mapa=mapa,
            memoria_grupo=memoria,
            grupo_id=0
        )
        agentes.append(agente)
        return agentes

    @staticmethod
    def criar_grupo_hibrido_inverso(mapa, memoria, num_agentes=None):
        """Cria grupo com mistura 1x BFS + 2x KNN"""
        if num_agentes is None:
            num_agentes = 3
        agentes = []
        # 1 BFS
        agente = AgenteBusca(
            nome="BFS1",
            mapa=mapa,
            memoria_grupo=memoria,
            grupo_id=0
        )
        agentes.append(agente)
        # 2 KNN
        for i in range(2):
            agente = AgenteKNN(
                nome=f"KNN{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        return agentes

    @staticmethod
    def criar_hibrido_balanceado(mapa, memoria, num_agentes=None):
        """Cria grupo com 50% Aleatório, 50% KNN"""
        if num_agentes is None:
            num_agentes = 4
        agentes = []
        # Metade Aleatório
        for i in range(num_agentes // 2):
            agente = AgenteAleatorio(
                nome=f"Aleatório{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        # Metade KNN
        for i in range(num_agentes - num_agentes // 2):
            agente = AgenteKNN(
                nome=f"KNN{i+1}",
                mapa=mapa,
                memoria_grupo=memoria,
                grupo_id=0
            )
            agentes.append(agente)
        return agentes

