from collections import deque
from utils.constantes import ModoJogo

class ValidadorMapa:

    def __init__(self, mapa, modo):
        self.mapa = mapa
        self.modo = modo
        self.tam = mapa.tamanho

    def validar(self):
        if self.modo == ModoJogo.C_BANDEIRA:
            return self._validar_bandeira()
        return self._validar_conectividade()

    def _validar_conectividade(self):
        visitados = self._flood_fill()

        # Todos os tesouros devem ser acessíveis
        for i in range(self.tam):
            for j in range(self.tam):
                if self.mapa.ver((i, j)) == "T" and (i, j) not in visitados:
                    return False
        return True

    def _validar_bandeira(self):
        visitados = self._flood_fill()
        for i in range(self.tam):
            for j in range(self.tam):
                if self.mapa.ver((i, j)) == "F":
                    return (i, j) in visitados
        return False

    def _flood_fill(self):
        fila = deque([(0, 0)])
        visitados = set([(0, 0)])

        while fila:
            x, y = fila.popleft()

            for nx, ny in self.mapa.vizinhos((x, y)):
                if (nx, ny) not in visitados:
                    if self.mapa.ver((nx, ny)) != "B":
                        visitados.add((nx, ny))
                        fila.append((nx, ny))

        return visitados
