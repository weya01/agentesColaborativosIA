import random
from agentes.agente_base import AgenteBase

class AgenteNaiveBayes(AgenteBase):

    def __init__(self, nome, mapa, memoria, modo):
        super().__init__(nome, mapa, memoria, modo)
        self.grupo = "N-Busca"
        self.stats = {}  # acao -> [sucessos, tentativas]

    def decidir_acao(self):
        acoes = ["CIMA","BAIXO","ESQUERDA","DIREITA"]

        if not self.stats:
            return random.choice(acoes)

        return max(acoes, key=lambda a: self._prob(a))

    def executar_acao(self, acao):
        super().executar_acao(acao)

        if acao not in self.stats:
            self.stats[acao] = [0,0]

        self.stats[acao][1] += 1

        if self.mapa.ver((self.x,self.y)) in ["T","F"]:
            self.stats[acao][0] += 1

    def _prob(self, acao):
        if acao not in self.stats:
            return 0.5
        s, t = self.stats[acao]
        return s / t if t > 0 else 0.5
