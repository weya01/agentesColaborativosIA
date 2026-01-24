import random
from agentes.agente_base import AgenteBase

class AgenteRandomico(AgenteBase):
    def __init__(self, nome, mapa):
        super().__init__(nome, mapa)

    def decidir_acao(self):
        if not self.vivo or self.terminou:
            return None

        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
        return random.choice(acoes)
