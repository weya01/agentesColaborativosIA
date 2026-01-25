import json
import os
import random
from agentes.agente_base import AgenteBase

class AgenteML(AgenteBase):

    def __init__(self, nome, mapa, memoria, modo, ficheiro="qtable.json"):
        super().__init__(nome, mapa, memoria, modo)

        self.ficheiro = ficheiro
        self.alpha = 0.1      # taxa de aprendizagem
        self.gamma = 0.9      # desconto futuro
        self.epsilon = 0.2    # exploração
        self.grupo = "N-Busca"
        self.q = self._carregar_q()

    # -------------------------
    # Q-TABLE
    # -------------------------
    def _carregar_q(self):
        if os.path.exists(self.ficheiro):
            with open(self.ficheiro, "r") as f:
                return json.load(f)
        return {}

    def _guardar_q(self):
        with open(self.ficheiro, "w") as f:
            json.dump(self.q, f)

    def _estado(self):
        return f"{self.x},{self.y}"

    # -------------------------
    # AÇÃO
    # -------------------------
    def decidir_acao(self):
        estado = self._estado()
        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]

        if random.random() < self.epsilon:
            return random.choice(acoes)

        # melhor ação conhecida
        valores = self.q.get(estado, {})
        if not valores:
            return random.choice(acoes)

        return max(valores, key=valores.get)

    # -------------------------
    # APRENDIZAGEM
    # -------------------------
    def aprender(self, estado_antigo, acao, recompensa, estado_novo):
        if estado_antigo not in self.q:
            self.q[estado_antigo] = {}

        valor_atual = self.q[estado_antigo].get(acao, 0)
        futuro = max(self.q.get(estado_novo, {}).values(), default=0)

        novo_valor = valor_atual + self.alpha * (
            recompensa + self.gamma * futuro - valor_atual
        )

        self.q[estado_antigo][acao] = novo_valor
        self._guardar_q()

    # -------------------------
    # EXECUÇÃO
    # -------------------------
    def executar_acao(self, acao):
        estado_antigo = self._estado()

        super().executar_acao(acao)

        estado_novo = self._estado()
        recompensa = self._calcular_recompensa()

        self.aprender(estado_antigo, acao, recompensa, estado_novo)

    def _calcular_recompensa(self):
        celula = self.mapa.ver((self.x, self.y))

        if celula == "F":
            return 100
        if celula == "T":
            return 10
        if celula == "B":
            return -100
        return -1
