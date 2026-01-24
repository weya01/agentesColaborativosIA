class MotorSimulacao:
    def __init__(self, mapa, agentes, modo="padrao"):
        self.mapa = mapa
        self.agentes = agentes
        self.modo = modo
        self.turno_atual = 0
        self.max_turnos = 100  # segurança
        self.resultados = []
        

    # -----------------------------
    # Execução principal
    # -----------------------------
    def executar(self):
        while not self._fim():
            self.turno_atual += 1
            for agente in self.agentes:
                if agente.vivo and not agente.terminou:
                    acao = agente.decidir_acao()
                    if acao:
                        agente.executar_acao(acao)
                        
        self._coletar_resultados()
        return self.resultados

    # -----------------------------
    # Turno
    # -----------------------------
    def _executar_turno(self):
        for agente in self.agentes:
            if agente.vivo and not agente.terminou:
                acao = agente.decidir_acao()
                if acao:
                    agente.executar_acao(acao)


    def _fim(self):
        # terminou se TODOS os agentes acabaram
        todos_terminaram = all(
            ag.terminou or not ag.vivo
            for ag in self.agentes
        )
        # ou se estourar limite de turnos
        return todos_terminaram or self.turno_atual >= self.max_turnos
    
    def _coletar_resultados(self):
        for a in self.agentes:
            self.resultados.append(a.metricas.finalizar())
