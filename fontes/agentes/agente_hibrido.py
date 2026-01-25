from agentes.agente_busca import AgenteBusca
import random

class AgenteHibrido(AgenteBusca):
    def decidir_acao(self):
        if random.random() < 0.7:
            return super().decidir_acao()
        return random.choice(self.mapa.vizinhos(self.posicao))

# BFS + heuristica
# BFS + ML
# A* + Memoria Estatica