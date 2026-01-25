from abc import ABC, abstractmethod
from simulacao.metricas import Metricas

class AgenteBase(ABC):
    def __init__(self, nome, mapa, memoria, modo):
        self.nome = nome
        self.mapa = mapa              # objeto Mapa
        self.memoria = memoria
        self.modo = modo
        self.grupo = "Default"
        # Dimensão correta do mapa
        self.tamanho = mapa.tamanho

        # Estado do agente
        self.x = 0
        self.y = 0
        self.vivo = True
        self.terminou = False
        self.metricas = Metricas(self.nome)

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
        self.metricas.passos = self.passos

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
            if self.tesouros_coletados > 0:
                self.tesouros_coletados -= 1  # Perde um tesouro ao acionar bomba
                self.metricas.desarmadas += 1
            else:
                self.vivo = False
                self.metricas.vivo = False
                self.metricas.morreu = True
            self.bombas_acionadas += 1
            self.metricas.bombas += 1

        elif celula == "T":
            self.tesouros_coletados += 1
            self.metricas.tesouros += 1
            self.mapa.matriz[self.x][self.y] = "L"  # Remove o tesouro do mapa

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
    
    # MOVIMENTO TEMPORARIO
    def decidir_acao(self):
        return "DIREITA"

