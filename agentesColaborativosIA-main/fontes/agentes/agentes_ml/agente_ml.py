"""
Agentes que utilizam Modelos de Aprendizagem de Máquina para decisão.
Integra ArvoreDecisao, ModeloKNN e NaiveBayes.
"""
import random
from agentes.base.agente_base import AgenteBase
from agentes.modelos_ml import ArvoreDecisao, ModeloKNN, NaiveBayes, TecnicaML


class AgenteML(AgenteBase):
    """
    Agente que utiliza modelos de ML para tomar decisões.
    Pode usar Árvore de Decisão, KNN ou Naive Bayes.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0, tecnica_ml=TecnicaML.ARVORE_DECISAO):
        """
        Args:
            nome: Identificador do agente
            mapa: Objeto Mapa
            memoria_grupo: Memória partilhada
            grupo_id: ID do grupo
            tecnica_ml: Técnica de ML a usar (TecnicaML enum)
        """
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        
        self.tecnica_ml = tecnica_ml
        
        # Inicializa modelo ML apropriado
        if tecnica_ml == TecnicaML.ARVORE_DECISAO:
            self.modelo = ArvoreDecisao()
        elif tecnica_ml == TecnicaML.KNN:
            self.modelo = ModeloKNN()
        elif tecnica_ml == TecnicaML.NAIVE_BAYES:
            self.modelo = NaiveBayes()
        else:
            self.modelo = ArvoreDecisao()  # Default
        
        self.algoritmo_em_uso = f"ML_{tecnica_ml.value}"
        self.historico_movimentos = []  # Rastreia movimentos bem-sucedidos

    def _decidir_acao_interna(self):
        """
        Usa modelo ML para decidir próxima ação.
        
        Returns:
            str: Uma das ações ("CIMA", "BAIXO", "ESQUERDA", "DIREITA")
        """
        # Prepara perceção para o modelo
        percepcao_ml = {
            'vizinhos': {},  # {(x, y): tipo_celula}
            'posicao_atual': (self.x, self.y),
            'celulas_exploradas': self.celulas_exploradas.copy(),
        }
        
        # Coleta vizinhos e seus tipos
        vizinhos = self.mapa.vizinhos((self.x, self.y))
        for viz_x, viz_y in vizinhos:
            tipo = self.mapa.ver((viz_x, viz_y))
            percepcao_ml['vizinhos'][(viz_x, viz_y)] = tipo
        
        # Prepara histórico
        historico_ml = {
            'exploradas': self.celulas_exploradas.copy(),
            'seguras': self.celulas_seguras.copy(),
            'bombas': self.memoria_grupo.obter_bombas(self.grupo_id).copy(),
            'historico_movimentos': self.historico_movimentos[-10:]  # Últimos 10
        }
        
        # Pede recomendação do modelo ML
        try:
            dx, dy = self.modelo.decidir_movimento(percepcao_ml, historico_ml)
            
            # Converte (dx, dy) para ação
            if dx == -1 and dy == 0:
                acao = "CIMA"
            elif dx == 1 and dy == 0:
                acao = "BAIXO"
            elif dx == 0 and dy == -1:
                acao = "ESQUERDA"
            elif dx == 0 and dy == 1:
                acao = "DIREITA"
            else:
                # Fallback: movimento aleatório seguro
                return self._aleatorio_seguro()
            
            # Registra no histórico
            self.historico_movimentos.append({
                'acao': acao,
                'posicao': (self.x, self.y),
                'turnos': len(self.historico_movimentos)
            })
            
            return acao
        
        except Exception as e:
            # Fallback em caso de erro do modelo
            print(f"ERRO no modelo ML: {e}")
            return self._aleatorio_seguro()

    def _aleatorio_seguro(self):
        """
        Fallback: Movimento aleatório evitando bombas conhecidas.
        PRIORIZA FORTEMENTE posições novas sobre exploradas.
        """
        direcoes = [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]
        bombas_conhecidas = self.memoria_grupo.obter_bombas(self.grupo_id)

        # Coleta posições por categoria de segurança
        posicoes_novas = []          # Nunca vistas
        posicoes_seguras_novo = []   # Seguras não vistas
        posicoes_seguras_vistas = [] # Seguras já vistas
        posicoes_desconhecidas = []  # Exploradas mas desconhecidas
        
        for acao, dx, dy in direcoes:
            novo_x, novo_y = self.x + dx, self.y + dy
            
            if not self._posicao_valida(novo_x, novo_y):
                continue
            
            pos = (novo_x, novo_y)
            
            if pos in bombas_conhecidas:
                continue
            
            explorada = pos in self.celulas_exploradas
            segura = pos in self.celulas_seguras
            
            if not explorada and segura:
                posicoes_seguras_novo.append(acao)
            elif not explorada:
                posicoes_novas.append(acao)
            elif segura:
                posicoes_seguras_vistas.append(acao)
            else:
                posicoes_desconhecidas.append(acao)

        # Retorna por ordem de prioridade
        if posicoes_seguras_novo:
            return random.choice(posicoes_seguras_novo)
        elif posicoes_novas:
            return random.choice(posicoes_novas)
        elif posicoes_seguras_vistas:
            return random.choice(posicoes_seguras_vistas)
        elif posicoes_desconhecidas:
            return random.choice(posicoes_desconhecidas)
        else:
            direcoes_validas = [a for a, dx, dy in direcoes 
                               if self._posicao_valida(self.x + dx, self.y + dy)]
            if direcoes_validas:
                return random.choice(direcoes_validas)
            else:
                return "CIMA"
