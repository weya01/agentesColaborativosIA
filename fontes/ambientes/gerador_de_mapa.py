from utils.constantes import ModoJogo
import random
from copy import deepcopy

L = "L"
B = "B"
T = "T"
F = "F"

class GeradorDeMapa:

    def __init__(self, tamanho=10, modo=ModoJogo.A_TESOUROS):
        self.tamanho = tamanho
        self.modo = modo

    def gerar(self):
        if self.modo == ModoJogo.A_TESOUROS:
            return self._mapa_tesouros()

        if self.modo == ModoJogo.B_SOBREVIVENCIA:
            return self._mapa_sobrevivencia()

        if self.modo == ModoJogo.C_BANDEIRA:
            return self._mapa_bandeira()

    # ---------- MODOS ----------

    def _mapa_tesouros(self):
        return self._gerar_mapa(
            prob_bomba=0.3,
            prob_tesouro=0.3,
            com_bandeira=False
        )

    def _mapa_sobrevivencia(self):
        return self._gerar_mapa(
            prob_bomba=0.6,
            prob_tesouro=0.1,
            com_bandeira=False
        )

    def _mapa_bandeira(self):
        return self._gerar_mapa(
            prob_bomba=0.4,
            prob_tesouro=0.0,
            com_bandeira=True
        )

    # ---------- FUNÇÃO BASE ----------

    def _gerar_mapa(self, prob_bomba, prob_tesouro, com_bandeira):
        mapa = []

        for i in range(self.tamanho):
            linha = []
            for j in range(self.tamanho):
                r = random.random()
                if r < prob_bomba:
                    linha.append(B)
                elif r < prob_bomba + prob_tesouro:
                    linha.append(T)
                else:
                    linha.append(L)
            mapa.append(linha)

        mapa[0][0] = L

        if com_bandeira:
            self._colocar_bandeira(mapa)

        return mapa

    def _colocar_bandeira(self, mapa):
        while True:
            x = random.randint(0, self.tamanho - 1)
            y = random.randint(0, self.tamanho - 1)
            if mapa[x][y] == L:
                mapa[x][y] = F
                break



class Mapa:
    def __init__(self, tamanho=10):
        self.tamanho = tamanho
        self.matriz = [["L" for _ in range(tamanho)] for _ in range(tamanho)]

    def gerar(self, bombas=20, tesouros=5):
        self._espalhar("B", bombas)
        self._espalhar("T", tesouros)

    def _espalhar(self, tipo, qtd):
        while qtd:
            x = random.randint(0, self.tamanho-1)
            y = random.randint(0, self.tamanho-1)
            if self.matriz[x][y] == "L":
                self.matriz[x][y] = tipo
                qtd -= 1

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
