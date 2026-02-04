"""
Agentes Híbridos que combinam múltiplas estratégias e algoritmos.
Mudam de estratégia dinamicamente baseado em situação.
"""
import random
from ..base.agente_base import AgenteBase
from ..agentes_busca.agente_busca import AgenteBusca
from ..agentes_nao_busca.agente_nao_busca import AgenteAleatorio, AgenteKNN


class AgenteHibrido(AgenteBase):
    """
    Agente híbrido que combina busca formal com aleatoriedade.
    Escolhe entre busca (quando próximo de objetivo) e exploração aleatória.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.limiar_proximidade = 5  # Se dentro de 5 passos, usa busca
        self.prob_busca = 0.7  # Probabilidade de usar busca
        self.modo_busca = AgenteBusca(nome + "_busca", mapa, memoria_grupo, grupo_id,
                                      algoritmos=["bfs", "gulosa"])
        self.modo_aleatorio = AgenteAleatorio(nome + "_aleatorio", mapa, memoria_grupo, grupo_id,
                                              algoritmos=["aleatorio_seguro"])
        self.estrategia_atual = "busca"

    def _decidir_acao_interna(self):
        """Escolhe entre busca e aleatoriedade"""
        tesouros = self.memoria_grupo.obter_tesouros(self.grupo_id)
        
        # Se conhece tesouro próximo, usa busca
        if tesouros:
            tesouro_mais_proximo = min(tesouros, 
                                       key=lambda t: abs(t[0] - self.x) + abs(t[1] - self.y))
            distancia = abs(tesouro_mais_proximo[0] - self.x) + abs(tesouro_mais_proximo[1] - self.y)
            
            if distancia <= self.limiar_proximidade or random.random() < self.prob_busca:
                self.estrategia_atual = "busca"
                self.algoritmo_em_uso = "busca_com_knn"
                return self._acao_busca_direcionada(tesouro_mais_proximo)

        # Senão, explora aleatoriamente
        self.estrategia_atual = "aleatorio"
        self.algoritmo_em_uso = "aleatorio_seguro"
        return self.modo_aleatorio._decidir_acao_interna()

    def _acao_busca_direcionada(self, objetivo):
        """Move uma unidade em direção ao objetivo"""
        x_obj, y_obj = objetivo
        
        # Prefere movimento horizontal antes de vertical
        if x_obj < self.x:
            return "CIMA"
        elif x_obj > self.x:
            return "BAIXO"
        elif y_obj < self.y:
            return "ESQUERDA"
        elif y_obj > self.y:
            return "DIREITA"
        
        return "CIMA"


class AgenteAdaptativo(AgenteBase):
    """
    Agente que se adapta dinamicamente às condições.
    Muda algoritmo baseado em sucesso/falha.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.algoritmos = ["bfs", "aleatorio_seguro", "knn", "explorar"]
        self.indice_atual = 0
        self.sucessos_algoritmo = {alg: 0 for alg in self.algoritmos}
        self.falhas_algoritmo = {alg: 0 for alg in self.algoritmos}
        self.turno_contador = 0

    def _decidir_acao_interna(self):
        """Escolhe algoritmo com maior taxa de sucesso"""
        self.turno_contador += 1
        
        # A cada 20 turnos, reavalia algoritmo
        if self.turno_contador % 20 == 0:
            self._reavalia_algoritmo()

        algoritmo = self.algoritmos[self.indice_atual]
        self.algoritmo_em_uso = algoritmo

        if algoritmo == "bfs":
            return self._busca_bfs()
        elif algoritmo == "aleatorio_seguro":
            return self._aleatorio_seguro()
        elif algoritmo == "knn":
            return self._knn_simples()
        elif algoritmo == "explorar":
            return self._explorar_simples()

        return self._aleatorio_seguro()

    def _reavalia_algoritmo(self):
        """Seleciona algoritmo com melhor taxa de sucesso"""
        melhor_algoritmo = 0
        melhor_score = -1

        for i, alg in enumerate(self.algoritmos):
            total = self.sucessos_algoritmo[alg] + self.falhas_algoritmo[alg]
            if total > 0:
                score = self.sucessos_algoritmo[alg] / total
            else:
                score = 0
            
            if score > melhor_score:
                melhor_score = score
                melhor_algoritmo = i

        self.indice_atual = melhor_algoritmo

    def _registrar_sucesso(self):
        """Registra sucesso do algoritmo atual"""
        alg = self.algoritmos[self.indice_atual]
        self.sucessos_algoritmo[alg] += 1

    def _registrar_falha(self):
        """Registra falha do algoritmo atual"""
        alg = self.algoritmos[self.indice_atual]
        self.falhas_algoritmo[alg] += 1

    def _busca_bfs(self):
        """BFS simples"""
        from collections import deque
        
        fila = deque([(self.x, self.y)])
        pais = {(self.x, self.y): None}
        visitados = {(self.x, self.y)}

        while fila:
            x, y = fila.popleft()
            if self.mapa.ver((x, y)) == "T":
                self._registrar_sucesso()
                return self._mover_para_objetivo((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        visitados.add((nx, ny))
                        pais[(nx, ny)] = (x, y)
                        fila.append((nx, ny))

        self._registrar_falha()
        return self._acao_aleatoria()

    def _aleatorio_seguro(self):
        """Movimento aleatório evitando bombas"""
        acoes_possiveis = []
        direcoes = [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]
        bombas = self.memoria_grupo.obter_bombas(self.grupo_id)

        for acao, dx, dy in direcoes:
            novo_x, novo_y = self.x + dx, self.y + dy
            if self._posicao_valida(novo_x, novo_y) and (novo_x, novo_y) not in bombas:
                acoes_possiveis.append(acao)

        if acoes_possiveis:
            return random.choice(acoes_possiveis)
        return self._acao_aleatoria()

    def _knn_simples(self):
        """KNN para encontrar tesouros"""
        tesouros = self.memoria_grupo.obter_tesouros(self.grupo_id)
        
        if not tesouros:
            self._registrar_falha()
            return self._acao_aleatoria()

        tesouro = min(tesouros, key=lambda t: abs(t[0] - self.x) + abs(t[1] - self.y))
        self._registrar_sucesso()
        return self._mover_para_objetivo(tesouro)

    def _explorar_simples(self):
        """Exploração simples: vai para células não visitadas"""
        for acao, dx, dy in [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]:
            novo_x, novo_y = self.x + dx, self.y + dy
            if self._posicao_valida(novo_x, novo_y):
                if (novo_x, novo_y) not in self.celulas_exploradas:
                    self._registrar_sucesso()
                    return acao

        self._registrar_falha()
        return self._acao_aleatoria()

    def _mover_para_objetivo(self, objetivo):
        """Move uma unidade em direção ao objetivo"""
        x_obj, y_obj = objetivo
        
        if x_obj < self.x:
            return "CIMA"
        elif x_obj > self.x:
            return "BAIXO"
        elif y_obj < self.y:
            return "ESQUERDA"
        elif y_obj > self.y:
            return "DIREITA"
        
        return self._acao_aleatoria()

    def _acao_aleatoria(self):
        """Ação completamente aleatória"""
        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
        return random.choice(acoes)


class AgenteCombinado(AgenteBase):
    """
    Agente que combina BFS + Heurística + KNN simultaneamente.
    Usa votação de 3 estratégias para decidir.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.peso_busca = 0.4
        self.peso_heuristica = 0.3
        self.peso_knn = 0.3

    def _decidir_acao_interna(self):
        """Combina 3 estratégias por votação ponderada"""
        self.algoritmo_em_uso = "bfs+heuristica+knn"

        # Estratégia 1: BFS
        acao_bfs = self._sugerir_bfs()

        # Estratégia 2: Heurística (Manhattan)
        acao_heuristica = self._sugerir_heuristica()

        # Estratégia 3: KNN
        acao_knn = self._sugerir_knn()

        # Votação ponderada
        votos = {}
        for acao, peso in [(acao_bfs, self.peso_busca),
                          (acao_heuristica, self.peso_heuristica),
                          (acao_knn, self.peso_knn)]:
            if acao:
                votos[acao] = votos.get(acao, 0) + peso

        if votos:
            return max(votos, key=votos.get)

        return self._acao_aleatoria()

    def _sugerir_bfs(self):
        """Sugere próxima ação usando BFS até tesouro"""
        from collections import deque
        
        fila = deque([(self.x, self.y)])
        pais = {(self.x, self.y): None}
        visitados = {(self.x, self.y)}

        while fila:
            x, y = fila.popleft()
            if self.mapa.ver((x, y)) == "T":
                return self._calcular_direcao_para((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        visitados.add((nx, ny))
                        fila.append((nx, ny))

        return None

    def _sugerir_heuristica(self):
        """Sugere próxima ação usando heurística Manhattan"""
        melhor_acao = None
        melhor_h = float('inf')

        for acao, dx, dy in [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]:
            novo_x, novo_y = self.x + dx, self.y + dy
            if self._posicao_valida(novo_x, novo_y) and self.mapa.ver((novo_x, novo_y)) != "B":
                # Heurística para encontrar tesouro mais próximo
                h = abs(novo_x - 9) + abs(novo_y - 9)
                if h < melhor_h:
                    melhor_h = h
                    melhor_acao = acao

        return melhor_acao

    def _sugerir_knn(self):
        """Sugere próxima ação usando KNN"""
        tesouros = self.memoria_grupo.obter_tesouros(self.grupo_id)
        
        if not tesouros:
            return None

        tesouro = min(tesouros, key=lambda t: abs(t[0] - self.x) + abs(t[1] - self.y))
        return self._calcular_direcao_para(tesouro)

    def _calcular_direcao_para(self, objetivo):
        """Calcula uma direção para objetivo"""
        x_obj, y_obj = objetivo
        
        if x_obj < self.x:
            return "CIMA"
        elif x_obj > self.x:
            return "BAIXO"
        elif y_obj < self.y:
            return "ESQUERDA"
        elif y_obj > self.y:
            return "DIREITA"
        
        return None

    def _acao_aleatoria(self):
        """Ação aleatória"""
        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
        return random.choice(acoes)
