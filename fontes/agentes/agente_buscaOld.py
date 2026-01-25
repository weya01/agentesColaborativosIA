from collections import deque
from agentes.agente_base import AgenteBase
import heapq

class AgenteBusca(AgenteBase):
    def decidir_acao(self):
        vizinhos = self.mapa.vizinhos((self.x, self.y))
        for v in vizinhos:
            if not self.memoria.consultar(v):
                return v
        return None


class AgenteBusca(AgenteBase):
    def __init__(self, nome, mapa, tipo_busca="BFS"):
        super().__init__(nome, mapa)
        self.tipo_busca = tipo_busca
        self.caminho = []
        self._planear_caminho()

    # -----------------------------
    # Planeamento
    # -----------------------------
    def _planear_caminho(self):
        if self.tipo_busca == "BFS":
            self.caminho = self._bfs()
        elif self.tipo_busca == "DFS":
            self.caminho = self._dfs()
        elif self.tipo_busca == "GULOSA":
            self.caminho = self._gulosa()
        else:
            raise ValueError("Tipo de busca inválido")

    # -----------------------------
    # Execução
    # -----------------------------
    def decidir_acao(self):
        if not self.caminho:
            self.terminou = True
            return None

        prox = self.caminho.pop(0)
        dx = prox[0] - self.x
        dy = prox[1] - self.y

        if dx == -1: return "CIMA"
        if dx == 1: return "BAIXO"
        if dy == -1: return "ESQUERDA"
        if dy == 1: return "DIREITA"

    # -----------------------------
    # DFS
    # -----------------------------
    def _dfs(self):
        pilha = [(self.x, self.y)]
        pais = {}
        visitados = set()

        while pilha:
            x, y = pilha.pop()
            visitados.add((x, y))

            if self.mapa[x][y] == "F":
                return self._reconstruir_caminho(pais, (x, y))

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    pilha.append((nx, ny))
                    pais[(nx, ny)] = (x, y)

        return []

    # -----------------------------
    # Gulosa (heurística Manhattan)
    # -----------------------------
    def _gulosa(self):
        objetivo = self._encontrar_objetivo()
        fronteira = [(self.x, self.y)]
        pais = {}
        visitados = set()

        while fronteira:
            fronteira.sort(key=lambda p: abs(p[0]-objetivo[0]) + abs(p[1]-objetivo[1]))
            x, y = fronteira.pop(0)

            if (x, y) == objetivo:
                return self._reconstruir_caminho(pais, (x, y))

            visitados.add((x, y))

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if self._posicao_valida(nx, ny) and (nx, ny) not in visitados:
                    fronteira.append((nx, ny))
                    pais[(nx, ny)] = (x, y)

        return []

    # -----------------------------
    # Utilitários
    # -----------------------------
    def _reconstruir_caminho(self, pais, fim):
        caminho = []
        atual = fim
        while atual in pais:
            caminho.append(atual)
            atual = pais[atual]
        caminho.reverse()
        return caminho

    def _encontrar_objetivo(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa)):
                if self.mapa[i][j] == "F":
                    return (i, j)


# -----------------------------
# BFS
# -----------------------------
class AgenteBFS(AgenteBase):

    def decidir_acao(self):
        fila = deque()
        visitados = set()

        fila.append(((self.x, self.y), []))

        while fila:
            (x, y), caminho = fila.popleft()

            if (x, y) in visitados:
                continue

            visitados.add((x, y))

            # Se encontrar algo útil
            if self.mapa[x][y] == "T":
                return caminho[0] if caminho else None

            for direcao, (nx, ny) in self.mapa.vizinhos_com_direcao(x, y):
                if self.memoria.consultar((nx, ny)) != "B":
                    fila.append(((nx, ny), caminho + [direcao]))

        return None



class AgenteDFS(AgenteBase):
    def decidir_acao(self):
        pilha = list(self.mapa.vizinhos((self.x,self.y)))
        while pilha:
            pos = pilha.pop()
            if not self.memoria.consultar(pos):
                return pos
        return None


class AgenteAStar(AgenteBase):
    def decidir_acao(self):
        heap = []
        for v in self.mapa.vizinhos((self.x,self.y)):
            custo = abs(v[0]) + abs(v[1])
            heapq.heappush(heap, (custo, v))

        while heap:
            _, pos = heapq.heappop(heap)
            if not self.memoria.consultar(pos):
                return pos
        return None
