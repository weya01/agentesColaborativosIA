from abc import ABC, abstractmethod


class AgenteBase(ABC):
    def __init__(self, nome, mapa, memoria):
        self.nome = nome
        self.mapa = mapa              # objeto Mapa
        self.memoria = memoria

        # Dimensão correta do mapa
        self.tamanho = mapa.tamanho

        # Estado do agente
        self.x = 0
        self.y = 0
        self.vivo = True
        self.terminou = False

        # Métricas
        self.passos = 0
        self.bombas_acionadas = 0
        self.tesouros_coletados = 0
        self.chegou_objetivo = False

    # -----------------------------
    # Método abstrato
    # -----------------------------
    @abstractmethod
    def decidir_acao(self):
        """Retorna a próxima ação do agente"""
        pass

    # -----------------------------
    # Execução da ação
    # -----------------------------
    def executar_acao(self, acao):
        if not self.vivo or self.terminou:
            return

        dx, dy = 0, 0

        if acao == "CIMA":
            dx = -1
        elif acao == "BAIXO":
            dx = 1
        elif acao == "ESQUERDA":
            dy = -1
        elif acao == "DIREITA":
            dy = 1

        novo_x = self.x + dx
        novo_y = self.y + dy

        if self._posicao_valida(novo_x, novo_y):
            self.x = novo_x
            self.y = novo_y
            self.passos += 1
            self._avaliar_celula()

    def posicao(self):
        return (self.x, self.y)

    # -----------------------------
    # Funções auxiliares
    # -----------------------------
    def _posicao_valida(self, x, y):
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho

    def _avaliar_celula(self):
        celula = self.mapa.ver((self.x, self.y))

        if celula == "B":
            self.bombas_acionadas += 1
            self.vivo = False

        elif celula == "T":
            self.tesouros_coletados += 1

        elif celula == "F":
            self.chegou_objetivo = True
            self.terminou = True

        # Atualiza memória partilhada
        self.memoria.atualizar((self.x, self.y), celula)

    # -----------------------------
    # Métricas finais
    # -----------------------------
    def obter_metricas(self):
        return {
            "nome": self.nome,
            "passos": self.passos,
            "bombas": self.bombas_acionadas,
            "tesouros": self.tesouros_coletados,
            "chegou_objetivo": self.chegou_objetivo,
            "vivo": self.vivo
        }
