from collections import deque
from utils.constantes import ModoJogo

class ValidadorMapa:

    def __init__(self, mapa, modo):
        self.mapa = mapa
        self.modo = modo
        self.tam = len(mapa)

    def validar(self):
        if self.modo == ModoJogo.C_BANDEIRA:
            return self._validar_bandeira()
        return self._validar_conectividade()

    def _validar_conectividade(self):
        return self._flood_fill()

    def _validar_bandeira(self):
        return self._flood_fill(bandeira=True)

    def _flood_fill(self, bandeira=False):
        fila = deque([(0, 0)])
        visitados = set([(0, 0)])

        while fila:
            x, y = fila.popleft()

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.tam and 0 <= ny < self.tam:
                    if (nx, ny) not in visitados:
                        if self.mapa[nx][ny] != "B":
                            visitados.add((nx, ny))
                            fila.append((nx, ny))

        if bandeira:
            for i in range(self.tam):
                for j in range(self.tam):
                    if self.mapa[i][j] == "F":
                        return (i, j) in visitados

        return True

    from collections import deque

    def mapa_valido(mapa, inicio=(0,0)):
        visitado = set()
        fila = deque([inicio])

        while fila:
            x, y = fila.popleft()
            if (x,y) in visitado:
                continue

        visitado.add((x,y))

        for nx, ny in mapa.vizinhos((x,y)):
            if mapa.ver((nx,ny)) != "B":
                fila.append((nx,ny))

        # verifica se todos os tesouros são acessíveis
        for i in range(mapa.tamanho):
            for j in range(mapa.tamanho):
                if mapa.ver((i,j)) == "T" and (i,j) not in visitado:
                    return False
        return True