"""
Agentes que usam algoritmos de busca informada e não-informada.
Cada agente implementa múltiplos algoritmos e escolhe dinamicamente.
"""
from collections import deque
import heapq
from ..base.agente_base import AgenteBase


class AgenteBusca(AgenteBase):
    """
    Agente com múltiplos algoritmos de busca.
    Implementa: BFS, DFS, Gulosa (Manhattan) e A*.
    Escolhe dinamicamente qual usar baseado em critérios.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0, algoritmos=None):
        """
        Args:
            nome: Nome do agente
            mapa: Referência ao mapa
            memoria_grupo: Memória partilhada do grupo
            grupo_id: ID do grupo
            algoritmos: Lista de algoritmos a usar ["bfs", "dfs", "gulosa", "a_estrela"]
                       Se None, usa todos
        """
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        
        self.algoritmos_disponiveis = algoritmos or ["bfs", "dfs", "gulosa", "a_estrela"]
        self.indice_algoritmo_atual = 0
        self.caminho = []
        self._recalcular_caminho()

    def _decidir_acao_interna(self):
        """
        Decide próxima ação usando busca.
        Se caminho vazio, tenta recalcular ou muda algoritmo.
        """
        # Se não há caminho, tenta recalcular
        if not self.caminho:
            self._tentar_proximo_algoritmo()

        # Se ainda não há caminho, continua explorando
        if not self.caminho:
            return self._acao_aleatoria_segura()

        # Segue o caminho
        prox_pos = self.caminho.pop(0)
        return self._calcular_direcao(prox_pos)

    def _recalcular_caminho(self):
        """Calcula caminho usando algoritmo atual"""
        algoritmo = self.algoritmos_disponiveis[self.indice_algoritmo_atual]
        self.algoritmo_em_uso = algoritmo

        if algoritmo == "bfs":
            self.caminho = self._bfs()
        elif algoritmo == "dfs":
            self.caminho = self._dfs()
        elif algoritmo == "gulosa":
            self.caminho = self._gulosa()
        elif algoritmo == "a_estrela":
            self.caminho = self._a_estrela()

    def _tentar_proximo_algoritmo(self):
        """Tenta o próximo algoritmo disponível"""
        self.indice_algoritmo_atual = (self.indice_algoritmo_atual + 1) % len(self.algoritmos_disponiveis)
        self._recalcular_caminho()

    def _calcular_direcao(self, prox_pos):
        """Calcula ação (CIMA, BAIXO, etc) para ir até próxima posição"""
        x_prox, y_prox = prox_pos
        x_atual, y_atual = self.x, self.y

        dx = x_prox - x_atual
        dy = y_prox - y_atual

        if dx == -1:
            return "CIMA"
        elif dx == 1:
            return "BAIXO"
        elif dy == -1:
            return "ESQUERDA"
        elif dy == 1:
            return "DIREITA"
        return None

    def _acao_aleatoria_segura(self):
        """
        Toma ação aleatória para células seguras e NON-EXPLORADAS.
        
        NUNCA revisa células já exploradas!
        Se não há posições novas disponíveis, retorna None.
        """
        import random
        
        # Coleta posições vizinhas válidas e não exploradas
        vizinhos = self.mapa.vizinhos((self.x, self.y))
        bombas_conhecidas = self.memoria_grupo.obter_bombas(self.grupo_id)
        
        # Filtra: não é bomba, não é explorada
        vizinhos_novos = [v for v in vizinhos 
                         if v not in bombas_conhecidas and v not in self.celulas_exploradas]
        
        if vizinhos_novos:
            prox = random.choice(vizinhos_novos)
            return self._calcular_direcao(prox)
        
        # Nenhuma posição nova disponível
        return None

    # =====================================================================
    # ALGORITMOS DE BUSCA
    # =====================================================================

    def _bfs(self):
        """
        Busca em Largura (BFS).
        Encontra o caminho mais curto para o objetivo.
        """
        fila = deque([(self.x, self.y)])
        pais = {(self.x, self.y): None}
        visitados = {(self.x, self.y)}

        while fila:
            x, y = fila.popleft()

            # Verifica se encontrou bandeira
            if self.mapa.ver((x, y)) == "F":
                return self._reconstruir_caminho(pais, (x, y))

            # Explora vizinhos
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        visitados.add((nx, ny))
                        pais[(nx, ny)] = (x, y)
                        fila.append((nx, ny))

        return []

    def _dfs(self):
        """
        Busca em Profundidade (DFS).
        Útil para exploração mais profunda do mapa.
        """
        pilha = [(self.x, self.y)]
        pais = {(self.x, self.y): None}
        visitados = {(self.x, self.y)}

        while pilha:
            x, y = pilha.pop()

            if self.mapa.ver((x, y)) == "F":
                return self._reconstruir_caminho(pais, (x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        visitados.add((nx, ny))
                        pais[(nx, ny)] = (x, y)
                        pilha.append((nx, ny))

        return []

    def _gulosa(self):
        """
        Busca Gulosa com heurística Manhattan.
        Expande nós com menor distância até o objetivo.
        """
        heap = [(0, self.x, self.y)]
        pais = {(self.x, self.y): None}
        visitados = set()

        while heap:
            _, x, y = heapq.heappop(heap)

            if (x, y) in visitados:
                continue
            visitados.add((x, y))

            if self.mapa.ver((x, y)) == "F":
                return self._reconstruir_caminho(pais, (x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        if (nx, ny) not in pais:
                            pais[(nx, ny)] = (x, y)
                        
                        # Heurística: distância Manhattan até objetivo provável (9, 9)
                        h = abs(nx - 9) + abs(ny - 9)
                        heapq.heappush(heap, (h, nx, ny))

        return []

    def _a_estrela(self):
        """
        Algoritmo A*.
        Combina custo real (g) com heurística (h).
        Melhor que gulosa em muitos casos.
        """
        heap = [(0, self.x, self.y)]
        g_score = {(self.x, self.y): 0}
        pais = {(self.x, self.y): None}
        visitados = set()

        while heap:
            _, x, y = heapq.heappop(heap)

            if (x, y) in visitados:
                continue
            visitados.add((x, y))

            if self.mapa.ver((x, y)) == "F":
                return self._reconstruir_caminho(pais, (x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        novo_g = g_score[(x, y)] + 1
                        
                        if (nx, ny) not in g_score or novo_g < g_score[(nx, ny)]:
                            g_score[(nx, ny)] = novo_g
                            h = abs(nx - 9) + abs(ny - 9)
                            f = novo_g + h
                            pais[(nx, ny)] = (x, y)
                            heapq.heappush(heap, (f, nx, ny))

        return []

    def _reconstruir_caminho(self, pais, objetivo):
        """Reconstrói caminho do início até objetivo"""
        caminho = []
        atual = objetivo
        
        while pais[atual] is not None:
            caminho.append(atual)
            atual = pais[atual]
        
        return list(reversed(caminho))


class AgenteArvoreBusca(AgenteBase):
    """
    Agente que usa estrutura de árvore para busca.
    Implementa métodos de expansão de nós e exploração hierárquica.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0, profundidade_max=5):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.profundidade_max = profundidade_max
        self.arvore_estados = {}
        self.caminho = []

    def _decidir_acao_interna(self):
        """Decide ação usando busca em árvore"""
        if not self.caminho:
            self._construir_arvore_busca()

        if self.caminho:
            prox_pos = self.caminho.pop(0)
            return self._calcular_direcao(prox_pos)

        return self._acao_aleatoria_segura()

    def _construir_arvore_busca(self):
        """
        Constrói uma árvore de estados até profundidade máxima.
        Usa BFS para expansão nivel a nivel.
        """
        fila = deque([((self.x, self.y), 0, [])])
        visitados = {(self.x, self.y)}

        while fila:
            (x, y), profundidade, caminho = fila.popleft()

            if self.mapa.ver((x, y)) == "F":
                self.caminho = caminho
                return

            if profundidade >= self.profundidade_max:
                continue

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        visitados.add((nx, ny))
                        novo_caminho = caminho + [(nx, ny)]
                        fila.append(((nx, ny), profundidade + 1, novo_caminho))

    def _calcular_direcao(self, prox_pos):
        """Calcula ação para ir até próxima posição"""
        x_prox, y_prox = prox_pos
        dx = x_prox - self.x
        dy = y_prox - self.y

        if dx == -1:
            return "CIMA"
        elif dx == 1:
            return "BAIXO"
        elif dy == -1:
            return "ESQUERDA"
        elif dy == 1:
            return "DIREITA"
        return None

    def _acao_aleatoria_segura(self):
        """Ação aleatória para células seguras"""
        import random
        vizinhos = self.mapa.vizinhos((self.x, self.y))
        vizinhos_seguros = [v for v in vizinhos if self.mapa.ver(v) != "B"]
        
        if vizinhos_seguros:
            prox = random.choice(vizinhos_seguros)
            return self._calcular_direcao(prox)
        return None
