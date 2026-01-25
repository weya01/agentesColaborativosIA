from ambientes.validador import ValidadorMapa
from utils.constantes import ModoJogo
import random

class Mapa:
    def __init__(self, matriz):
        self.matriz = matriz
        self.tamanho = len(matriz)

    def ver(self, pos):
        x, y = pos
        return self.matriz[x][y]

    def vizinhos(self, pos):
        x, y = pos
        direcoes = [(1,0),(-1,0),(0,1),(0,-1)]
        validos = []
        for dx, dy in direcoes:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                validos.append((nx, ny))
        return validos

    def vizinhos_com_direcao(self, x, y):
        direcoes = {
            "CIMA": (-1, 0),
            "BAIXO": (1, 0),
            "ESQUERDA": (0, -1),
            "DIREITA": (0, 1)
        }
        resultado = []
        for nome, (dx, dy) in direcoes.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                resultado.append((nome, (nx, ny)))
        return resultado

class GeradorDeMapa:
    def __init__(self, tamanho, prob_bomba, prob_tesouro, modo):
        self.tamanho = tamanho
        self.prob_bomba = prob_bomba
        self.prob_tesouro = prob_tesouro
        self.modo = modo

    def gerar(self):
        while True:
            matriz = self._gerar_matriz()
            mapa = Mapa(matriz)

            if ValidadorMapa(mapa, self.modo).validar():
                return mapa

    def _gerar_matriz(self):
        matriz = []
        for i in range(self.tamanho):
            linha = []
            for j in range(self.tamanho):
                r = random.random()
                if r < self.prob_bomba:
                    linha.append("B")
                elif r < self.prob_bomba + self.prob_tesouro:
                    linha.append("T")
                else:
                    linha.append("L")
            matriz.append(linha)

        matriz[0][0] = "L"

        if self.modo in ["A", "C"]:
            self._colocar_bandeira(matriz)

        return matriz

    def _colocar_bandeira(self, matriz):
        while True:
            x = random.randint(0, self.tamanho - 1)
            y = random.randint(0, self.tamanho - 1)
            if matriz[x][y] == "L":
                matriz[x][y] = "F"
                break
