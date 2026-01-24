import random
from agentes.agente_base import AgenteBase

class AgenteNaoBusca(AgenteBase):
    def decidir_acao(self):
        vizinhos = self.mapa.vizinhos(self.posicao)
        return random.choice(vizinhos)
