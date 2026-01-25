import math
import random
from agentes.agente_base import AgenteBase

class AgenteKNN(AgenteBase):

    def __init__(self, nome, mapa, memoria, modo, k=3):
        super().__init__(nome, mapa, memoria, modo)
        self.k = k
        self.memoria_exp = []  # (x,y,acao,recompensa)
        self.grupo = "N-Busca"

    def decidir_acao(self):
        if len(self.memoria_exp) < self.k:
            return random.choice(["CIMA","BAIXO","ESQUERDA","DIREITA"])

        vizinhos = sorted(
            self.memoria_exp,
            key=lambda e: self._distancia((self.x,self.y),(e[0],e[1]))
        )[:self.k]

        votos = {}
        for _,_,acao, recompensa in vizinhos:
            votos[acao] = votos.get(acao,0) + recompensa

        return max(votos, key=votos.get)

    def executar_acao(self, acao):
        x0, y0 = self.x, self.y
        super().executar_acao(acao)
        recompensa = self._avaliar()
        self.memoria_exp.append((x0, y0, acao, recompensa))

    def _avaliar(self):
        c = self.mapa.ver((self.x, self.y))
        if c == "F": return 100
        if c == "T": return 10
        if c == "B": return -100
        return -1

    def _distancia(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
