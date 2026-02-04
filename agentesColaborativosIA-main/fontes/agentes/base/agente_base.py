"""
Classe base para todos os agentes.
Implementa o ciclo de IA: percepção → atualização de memória → decisão → ação
"""
from abc import ABC, abstractmethod
from enum import Enum


class EstadoAgente(Enum):
    """Estados possíveis de um agente"""
    ATIVO = "ativo"
    MORTO = "morto"
    COMPLETO = "completo"


class AgenteBase(ABC):
    """
    Classe base para todos os agentes inteligentes.
    
    Implementa o ciclo de IA obrigatório:
    1. Percepção: observa o ambiente
    2. Atualização de memória: armazena informações
    3. Decisão: escolhe ação com base em algoritmos
    4. Ação: executa movimento no ambiente
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0):
        """
        Inicializa o agente.
        
        Args:
            nome: Identificador único do agente
            mapa: Referência ao objeto Mapa
            memoria_grupo: Memória partilhada do grupo
            grupo_id: ID do grupo a que pertence (para separação de grupos)
        """
        self.nome = nome
        self.id = nome  # Alias para compatibilidade
        self.mapa = mapa
        self.memoria_grupo = memoria_grupo
        self.grupo_id = grupo_id
        self.tamanho_mapa = mapa.tamanho

        # Estado do agente
        self.x = 0
        self.y = 0
        self.estado = EstadoAgente.ATIVO
        self.terminou = False

        # Ciclo de IA
        self.percepcao_atual = None
        self.algoritmo_em_uso = None
        self.caminho_planejado = []

        # Métricas
        self.passos = 0
        self.bombas_acionadas = 0
        self.tesouros_coletados = 0
        self.chegou_objetivo = False
        self.celulas_exploradas = set()
        self.celulas_seguras = set()
        
        # Valida que posição inicial é segura (DEPOIS de inicializar)
        self._validar_posicao_inicial()

    # =====================================================================
    # VALIDAÇÃO E SEGURANÇA
    # =====================================================================

    def _validar_posicao_inicial(self):
        """
        Valida que posição inicial (0,0) é segura (não é bomba).
        Se não for, levanta exceção.
        """
        celula_inicial = self.mapa.ver((0, 0))
        if celula_inicial == "B":
            raise ValueError(
                f"ERRO: Posição inicial (0,0) contém bomba! "
                f"Mapa inválido. Gere novo mapa."
            )
        
        # Registra posição inicial como segura
        self.celulas_seguras.add((0, 0))
        self.celulas_exploradas.add((0, 0))

    # =====================================================================
    # CICLO DE IA - Implementação do padrão obrigatório
    # =====================================================================

    def executar_turno(self):
        """
        Executa um turno completo do agente com o ciclo de IA.
        
        Ciclo:
        1. Percepção: observa célula atual
        2. Atualização de Memória: armazena informação
        3. Decisão: escolhe próxima ação
        4. Ação: executa movimento
        """
        if not self._pode_agir():
            return

        # Etapa 1: PERCEPÇÃO
        percepcao = self._percepcao()

        # Etapa 2: ATUALIZAÇÃO DE MEMÓRIA
        self._atualizar_memoria(percepcao)

        # Etapa 3: DECISÃO
        acao = self._decisao()

        # Etapa 4: AÇÃO
        if acao:
            self._executar_acao(acao)

    def _pode_agir(self):
        """Verifica se o agente pode continuar agindo"""
        return self.estado == EstadoAgente.ATIVO and not self.terminou

    # =====================================================================
    # ETAPA 1: PERCEPÇÃO
    # =====================================================================

    def _percepcao(self):
        """
        Percebe o ambiente atual.
        Retorna informação sobre a célula em que o agente está.
        """
        celula = self.mapa.ver((self.x, self.y))
        vizinhos = self.mapa.vizinhos((self.x, self.y))

        percepcao = {
            "posicao": (self.x, self.y),
            "celula_atual": celula,
            "vizinhos": vizinhos,
            "numero_vizinhos": len(vizinhos)
        }

        self.percepcao_atual = percepcao
        return percepcao

    # =====================================================================
    # ETAPA 2: ATUALIZAÇÃO DE MEMÓRIA
    # =====================================================================

    def _atualizar_memoria(self, percepcao):
        """
        Atualiza a memória partilhada do grupo com as informações percebidas.
        Rastreia: bombas, tesouros, células exploradas, células seguras.
        """
        posicao = percepcao["posicao"]
        celula = percepcao["celula_atual"]

        # Registra célula como explorada
        self.celulas_exploradas.add(posicao)
        self.memoria_grupo.registrar_explorada(posicao, celula, self.grupo_id)

        # Atualiza conhecimento sobre a célula
        if celula == "B":
            self.memoria_grupo.registrar_bomba(posicao, self.grupo_id)
        elif celula == "T":
            self.memoria_grupo.registrar_tesouro(posicao, self.grupo_id)
        elif celula == "F":
            self.memoria_grupo.registrar_bandeira(posicao, self.grupo_id)
        elif celula == "L":
            self.celulas_seguras.add(posicao)
            self.memoria_grupo.registrar_segura(posicao, self.grupo_id)

        # Registra vizinhos como percebidos (útil para heurísticas)
        for vizinho in percepcao["vizinhos"]:
            if vizinho not in self.celulas_exploradas:
                self.memoria_grupo.registrar_percebido(vizinho, self.grupo_id)

    # =====================================================================
    # ETAPA 3: DECISÃO
    # =====================================================================

    @abstractmethod
    def _decidir_acao_interna(self):
        """
        Método abstrato que deve ser implementado por subclasses.
        Cada tipo de agente decide sua ação com base em seus algoritmos.
        
        Returns:
            str: Uma ação ("CIMA", "BAIXO", "ESQUERDA", "DIREITA") ou None
        """
        pass

    def _decisao(self):
        """
        Toma decisão sobre próxima ação.
        Chama o método abstrato que cada agente implementa.
        """
        acao = self._decidir_acao_interna()
        return acao

    # =====================================================================
    # ETAPA 4: AÇÃO
    # =====================================================================

    def _executar_acao(self, acao):
        """
        Executa a ação escolhida.
        Atualiza posição e avalia a célula resultante.
        """
        if acao not in ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]:
            return

        dx, dy = 0, 0
        if acao == "CIMA":
            dx = -1
        elif acao == "BAIXO":
            dx = 1
        elif acao == "ESQUERDA":
            dy = -1
        elif acao == "DIREITA":
            dy = 1

        novo_x = self.x + dx
        novo_y = self.y + dy

        if self._posicao_valida(novo_x, novo_y):
            self.x = novo_x
            self.y = novo_y
            self.passos += 1
            self._avaliar_celula()

    def _posicao_valida(self, x, y):
        """Verifica se posição está dentro dos limites do mapa"""
        return 0 <= x < self.tamanho_mapa and 0 <= y < self.tamanho_mapa

    def priorizar_posicoes_novas(self, posicoes: list) -> list:
        """
        Prioriza posições não exploradas sobre exploradas.
        Preferência: Novas > Seguras Conhecidas > Exploradas.
        
        Args:
            posicoes: Lista de posições disponíveis
        
        Returns:
            Lista ordenada por prioridade (novas primeiro)
        """
        novas = [p for p in posicoes if p not in self.celulas_exploradas]
        seguras = [p for p in posicoes if p in self.celulas_seguras and p not in novas]
        exploradas = [p for p in posicoes if p in self.celulas_exploradas 
                     and p not in seguras and p not in novas]
        
        return novas + seguras + exploradas
    
    def deve_evitar_posicao(self, x: int, y: int) -> bool:
        """
        Verifica se deve evitar uma posição.
        Retorna True se: já foi explorada E existem alternativas não exploradas.
        
        Args:
            x, y: Posição a verificar
        
        Returns:
            True se deve evitar, False se pode visitar
        """
        # Sempre visita posições não exploradas
        if (x, y) not in self.celulas_exploradas:
            return False
        
        # Conta quantas posições novas existem
        vizinhos = self.mapa.vizinhos((self.x, self.y))
        novas_disponiveis = sum(1 for v in vizinhos if v not in self.celulas_exploradas)
        
        # Se existem posições novas, evita a explorada
        return novas_disponiveis > 0

    def _avaliar_celula(self):
        """
        Avalia a célula onde o agente chegou.
        Pode morrer em bomba, coletar tesouro ou completar objetivo.
        
        Também registra na memória o que foi encontrado.
        """
        celula = self.mapa.ver((self.x, self.y))
        posicao_atual = (self.x, self.y)

        if celula == "B":
            self.bombas_acionadas += 1
            self.estado = EstadoAgente.MORTO
            self.memoria_grupo.registrar_agente_morto(self.nome, self.grupo_id)
            self.memoria_grupo.registrar_bomba(posicao_atual, self.grupo_id)

        elif celula == "T":
            # Registra na memória que achou tesouro
            self.memoria_grupo.registrar_tesouro(posicao_atual, self.grupo_id)
            
            # Tenta coletar tesouro (se ainda não foi coletado por outro agente)
            if self.memoria_grupo.registrar_tesouro_coletado(self.nome, self.grupo_id, posicao_atual):
                self.tesouros_coletados += 1

        elif celula == "F":
            self.chegou_objetivo = True
            self.terminou = True
            self.estado = EstadoAgente.COMPLETO
            self.memoria_grupo.registrar_bandeira(posicao_atual, self.grupo_id)
        
        elif celula == "L":
            self.celulas_seguras.add(posicao_atual)
            self.memoria_grupo.registrar_segura(posicao_atual, self.grupo_id)

    def posicao(self):
        """Retorna a posição atual do agente como tupla (x, y)"""
        return (self.x, self.y)

    def esta_vivo(self):
        """Verifica se o agente está vivo"""
        return self.estado == EstadoAgente.ATIVO

    def obter_metricas(self):
        """
        Retorna dicionário com as métricas finais do agente.
        """
        return {
            "nome": self.nome,
            "id": self.nome,
            "tipo": self.__class__.__name__,
            "grupo_id": self.grupo_id,
            "passos": self.passos,
            "bombas_acionadas": self.bombas_acionadas,
            "tesouros_coletados": self.tesouros_coletados,
            "tesouros": self.tesouros_coletados,  # Alias para UI
            "celulas_exploradas": len(self.celulas_exploradas),
            "celulas_seguras": len(self.celulas_seguras),
            "chegou_objetivo": self.chegou_objetivo,
            "vivo": self.esta_vivo(),
            "algoritmo_usado": self.algoritmo_em_uso,
            "eficiencia": self._calcular_eficiencia()
        }

    def _calcular_eficiencia(self):
        """
        Calcula índice de eficiência do agente.
        Eficiência = benefício / custo
        """
        if self.passos == 0:
            return 0.0
        
        beneficio = self.tesouros_coletados + (len(self.celulas_exploradas) * 0.1)
        return beneficio / self.passos
