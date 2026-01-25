import agentes
from simulacao.comparador import Comparador


class MotorSimulacao:
    def __init__(self, mapa, agentes, modo="padrao"):
        self.mapa = mapa
        self.agentes = agentes
        self.modo = modo
        self.turno_atual = 0
        self.max_turnos = 100  # segurança
        self.resultados = []
        self.comparador = Comparador()
        for agente in agentes:
            self.comparador.registrar_agente(agente)

        

    # -----------------------------
    # Execução principal
    # -----------------------------
    def executar(self):
        if not self._fim():
            self._executar_turno()
        else:
            for agente in self.agentes:
                dados = agente.metricas.finalizar()
                self.comparador.registrar_resultado(agente.grupo, dados)
            relatorio = self.comparador.finalizar() 

    # -----------------------------
    # Turno
    # -----------------------------
    def _executar_turno(self):
        for agente in self.agentes:
            if agente.vivo and not agente.terminou:
                acao = agente.decidir_acao()
                self.comparador.registrar_passo(agente)
                if acao:
                    agente.executar_acao(acao)
                    print(f"Turno {self.turno_atual} | Agente {agente.nome} em ({agente.x},{agente.y})")
            elif not agente.vivo:
                print(f"Agente {agente.nome} morreu em ({agente.x},{agente.y}).")
        self.turno_atual += 1
        #print(f"Turno {self.turno_atual} | Agente em ({self.agentes[0].x},{self.agentes[0].y})")
        #self.turno_atual += 1

    def _fim(self):
        todos_mortos = all(not agente.vivo for agente in self.agentes)
        todos_terminaram = all(agente.terminou or not agente.vivo for agente in self.agentes)
        return todos_mortos or todos_terminaram or self.turno_atual >= self.max_turnos    

    def _coletar_resultados(self):
        for a in self.agentes:
            self.resultados.append(a.obter_metricas())
