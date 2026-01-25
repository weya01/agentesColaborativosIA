from collections import deque

from numpy import info
from agentes.agente_base import AgenteBase
import heapq

class AgenteBFS(AgenteBase):

    def __init__(self, nome, mapa, memoria, modo):
        super().__init__(nome, mapa, memoria, modo)
        self.grupo = "Busca"

    def decidir_acao(self):
        fila = deque()
        visitados = set()

        fila.append((self.posicao(), []))

        while fila:
            (x, y), caminho = fila.popleft()

            if (x, y) in visitados:
                continue
            visitados.add((x, y))

            celula = self.mapa.ver((x, y))
            objetivo_encontrado = (self.modo == "C" and celula == "F") or (self.modo != "C" and (celula == "T" or celula == "F"))
            if objetivo_encontrado:
                return caminho[0] if caminho else None

            for direcao, (nx, ny) in self.mapa.vizinhos_com_direcao(x, y):
                if not self.memoria.consultar((nx, ny)):
                    fila.append(((nx, ny), caminho + [direcao]))

        return None

class AgenteDFS(AgenteBase):

    def __init__(self, nome, mapa, memoria):
        super().__init__(nome, mapa, memoria)
        self.grupo = "Busca"

    def decidir_acao(self):
        pilha = [ (self.posicao(), []) ]
        visitados = set()

        while pilha:
            (x, y), caminho = pilha.pop()

            if (x, y) in visitados:
                continue
            visitados.add((x, y))

            if self.mapa.ver((x, y)) == "T":
                return caminho[0] if caminho else None

            for direcao, (nx, ny) in self.mapa.vizinhos_com_direcao(x, y):
                if not self.memoria.consultar((nx, ny)):
                    pilha.append(((nx, ny), caminho + [direcao]))

        return None

class AgenteGuloso(AgenteBase):

    def __init__(self, nome, mapa, memoria):
        super().__init__(nome, mapa, memoria)
        self.grupo = "Busca"

    def decidir_acao(self):
        objetivo = self._encontrar_objetivo()
        melhores = []

        for direcao, (nx, ny) in self.mapa.vizinhos_com_direcao(self.x, self.y):
            if self.memoria.consultar((nx, ny)) == "B":
                continue

            h = abs(nx - objetivo[0]) + abs(ny - objetivo[1])
            melhores.append((h, direcao))

        if melhores:
            melhores.sort()
            return melhores[0][1]

        return None

    def _encontrar_objetivo(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.mapa.ver((i, j)) == "F":
                    return (i, j)


class AgenteAStar(AgenteBase):

    def __init__(self, nome, mapa, memoria):
        super().__init__(nome, mapa, memoria)
        self.grupo = "Busca"

    def decidir_acao(self):
        heap = []
        heapq.heappush(heap, (0, self.posicao(), []))
        visitados = set()

        while heap:
            custo, (x, y), caminho = heapq.heappop(heap)

            if (x, y) in visitados:
                continue
            visitados.add((x, y))

            if self.mapa.ver((x, y)) == "F":
                return caminho[0] if caminho else None

            for direcao, (nx, ny) in self.mapa.vizinhos_com_direcao(x, y):
                if not self.memoria.consultar((nx, ny)):
                    h = abs(nx - x) + abs(ny - y)
                    heapq.heappush(heap, (custo + h, (nx, ny), caminho + [direcao]))

        return None
